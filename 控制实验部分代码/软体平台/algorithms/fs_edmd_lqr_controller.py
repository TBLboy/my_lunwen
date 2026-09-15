"""Soft-platform FS-EDMD Koopman LQR controller for trajectory tracking."""

from __future__ import annotations

import numpy as np

from core.base_algorithm import BaseAlgorithm
from algorithms.tk_assets.fs_edmd_koopman_lifter import FSEDMDKoopmanLifter
from algorithms.tk_assets.koopman_lqr_base import (
    design_lqr_gain,
    resolve_asset_path,
)
from algorithms.tk_assets.koopman_lqr_settings_widget import KoopmanLQRSettingsWidget


class FSEDMDLQRController(BaseAlgorithm):
    """LQR controller in the augmented FS-EDMD state space."""

    def __init__(self, config_path: str):
        super().__init__(config_path)
        if not self.config:
            self.config = self.default_config()
            self.save_config()

        self.lifter = None
        self.K = None
        self.B_pinv = None
        self.closed_loop_rho = None
        self.load_model_and_design_lqr()

    @staticmethod
    def default_config() -> dict:
        return {
            "model_dir": "./fs_edmd_lqr_controller_assets",
            "Q_x1": 2500.0,
            "Q_x2": 2500.0,
            "alpha": 0.01,
            "R_control": 0.4,
            "ff_gain": 0.8,
            "u_limit": 70.0,
            "dt": 0.2,
            "device": "cpu",
            "output_sign_x": -1.0,
            "output_sign_y": 1.0,
            "round_control": False,
        }

    def get_name(self) -> str:
        return "FS-EDMD LQR Controller"

    def reset(self) -> None:
        if self.lifter is not None:
            self.lifter.reset()
        print("[FS-EDMD LQR] State reset")

    def load_model_and_design_lqr(self) -> None:
        model_dir = str(self.config.get("model_dir", "")).strip()
        if not model_dir:
            print("[FS-EDMD LQR] model_dir is empty - controller disabled")
            self._clear_runtime()
            return

        model_dir = resolve_asset_path(__file__, model_dir)
        try:
            self.lifter = FSEDMDKoopmanLifter(model_dir)
            self.B_pinv = np.linalg.pinv(self.lifter.B)
            print(
                f"[FS-EDMD LQR] Model loaded A:{self.lifter.A.shape} "
                f"B:{self.lifter.B.shape} D:{self.lifter.D.shape}"
            )
            self.design_lqr()
        except Exception as exc:
            print(f"[FS-EDMD LQR] Model load failed: {exc}")
            self._clear_runtime()

    def _clear_runtime(self) -> None:
        self.lifter = None
        self.K = None
        self.B_pinv = None
        self.closed_loop_rho = None

    def design_lqr(self) -> None:
        if self.lifter is None or self.B_pinv is None:
            self.K = None
            self.closed_loop_rho = None
            return
        try:
            self.K, self.closed_loop_rho = design_lqr_gain(
                self.lifter.A,
                self.lifter.B,
                float(self.config.get("Q_x1", 100.0)),
                float(self.config.get("Q_x2", 100.0)),
                float(self.config.get("alpha", 0.01)),
                self.lifter.n,
                float(self.config.get("R_control", 1.0)),
            )
            print(
                f"[FS-EDMD LQR] LQR designed K:{self.K.shape} "
                f"closed-loop rho={self.closed_loop_rho:.4f}"
            )
        except Exception as exc:
            print(f"[FS-EDMD LQR] LQR design failed: {exc}")
            self.K = np.zeros((self.lifter.m, self.lifter.d), dtype=np.float64)

    def calculate_control(self, current_pos, current_step, trajectory_sequence):
        if self.lifter is None or self.K is None or self.B_pinv is None:
            return (0.0, 0.0)
        try:
            z_curr = self.lifter.lift_current(current_pos)
            z_ref = self.lifter.lift_reference(trajectory_sequence, current_step, 0)
            z_ref_next = self.lifter.lift_reference(trajectory_sequence, current_step, 1)

            e_z = z_curr - z_ref
            u_fb = -self.K @ e_z
            u_ff = self.B_pinv @ (z_ref_next - self.lifter.A @ z_ref)
            u_norm = u_fb + float(self.config.get("ff_gain", 1.0)) * u_ff

            u_out = self.lifter.denormalize_control(u_norm)
            u_out = np.clip(
                u_out,
                -float(self.config.get("u_limit", 50.0)),
                float(self.config.get("u_limit", 50.0)),
            )
            if bool(self.config.get("round_control", False)):
                u_out = np.round(u_out).astype(int)

            sign_x = float(self.config.get("output_sign_x", 1.0))
            sign_y = float(self.config.get("output_sign_y", 1.0))
            return (sign_x * float(u_out[0]), sign_y * float(u_out[1]))
        except Exception as exc:
            print(f"[FS-EDMD LQR] Control computation failed: {exc}")
            return (0.0, 0.0)

    def get_settings_widget(self):
        return KoopmanLQRSettingsWidget(
            self,
            "Soft Platform - FS-EDMD LQR",
            path_key="model_dir",
            path_label="FS-EDMD asset directory:",
        )
