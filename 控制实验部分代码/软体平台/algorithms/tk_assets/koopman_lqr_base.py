from __future__ import annotations

import os
from typing import Callable

import numpy as np

try:
    import control as ct
except Exception:  # pragma: no cover
    ct = None

from numpy.linalg import solve as np_solve


def resolve_asset_path(controller_file: str, configured_path: str) -> str:
    if not configured_path:
        return ""
    if os.path.isabs(configured_path):
        return configured_path
    base_dir = os.path.dirname(os.path.abspath(controller_file))
    return os.path.normpath(os.path.join(base_dir, configured_path))


def default_controller_config(model_path: str = "") -> dict:
    return {
        "model_path": model_path,
        "Q_x1": 10.0,
        "Q_x2": 10.0,
        "alpha": 0.01,
        "R_control": 0.4,
        "ff_gain": 0.5,
        "u_limit": 100.0,
        "device": "cpu",
        "output_sign_x": -1.0,
        "output_sign_y": 1.0,
    }


def design_lqr_gain(A, B, q_x1: float, q_x2: float, alpha: float, n: int, r_control: float):
    d = A.shape[0]
    m = B.shape[1]

    q_diag = np.zeros(d, dtype=np.float64)
    q_diag[0] = float(q_x1)
    if d > 1:
        q_diag[1] = float(q_x2)
    if d > n:
        q_diag[n:] = float(alpha)

    Q = np.diag(q_diag)
    R = float(r_control) * np.eye(m)

    A64 = np.asarray(A, dtype=np.float64)
    B64 = np.asarray(B, dtype=np.float64)

    if ct is not None:
        K, _, _ = ct.dlqr(A64, B64, Q, R)
        K = np.asarray(K, dtype=np.float32)
    else:
        P = Q.copy()
        for _ in range(2000):
            P_next = (
                A64.T @ P @ A64
                - A64.T @ P @ B64 @ np_solve(R + B64.T @ P @ B64, B64.T @ P @ A64)
                + Q
            )
            if np.max(np.abs(P_next - P)) < 1e-9:
                P = P_next
                break
            P = P_next
        K = np_solve(R + B64.T @ P @ B64, B64.T @ P @ A64).astype(np.float32)

    eig_radius = float(max(abs(np.linalg.eigvals(A64 - B64 @ K))))
    return K, eig_radius


def compute_control_output(
    lifter,
    A,
    B_pinv,
    K,
    current_pos,
    current_step,
    trajectory_sequence,
    ff_gain: float,
    u_limit: float,
    output_sign_x: float,
    output_sign_y: float,
):
    z_curr = lifter.lift_current(current_pos)
    z_ref = lifter.lift_reference(trajectory_sequence, current_step, shift=0)
    z_ref_next = lifter.lift_reference(trajectory_sequence, current_step, shift=1)

    e_z = z_curr - z_ref
    u_fb = -K @ e_z
    u_ff = B_pinv @ (z_ref_next - A @ z_ref)
    u_norm = u_fb + float(ff_gain) * u_ff

    u_out = lifter.denormalize_control(u_norm)
    u_out = np.clip(u_out, -float(u_limit), float(u_limit))
    u_out = np.round(u_out).astype(int)
    return (
        int(float(output_sign_x) * u_out[0]),
        int(float(output_sign_y) * u_out[1]),
    )


def load_lifter_from_config(
    controller_file: str,
    config: dict,
    lifter_factory: Callable[[str, str], object],
    path_key: str = "model_path",
):
    asset_path = resolve_asset_path(controller_file, str(config.get(path_key, "")).strip())
    if not asset_path:
        raise ValueError(f"{path_key} is empty")
    device = str(config.get("device", "cpu"))
    lifter = lifter_factory(asset_path, device)
    A = lifter.A
    B = lifter.B
    B_pinv = np.linalg.pinv(B)
    return lifter, A, B, B_pinv
