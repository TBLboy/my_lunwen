"""Runtime loading and lifting utilities for the soft-platform FS-EDMD model."""

from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

from algorithms.tk_assets.soft_lift import SoftLift


class FSEDMDKoopmanLifter:
    """Load the exported FS-EDMD pickle plus training normalization metadata."""

    def __init__(self, model_dir: str | Path):
        self.model_dir = Path(model_dir)
        if not self.model_dir.exists():
            raise FileNotFoundError(f"FS-EDMD asset directory not found: {self.model_dir}")

        with (self.model_dir / "fs_edmd.pkl").open("rb") as handle:
            model = pickle.load(handle)

        self.A = np.asarray(model["A_model"], dtype=np.float64)
        self.B = np.asarray(model["B_model"], dtype=np.float64)
        self.C = np.asarray(model["C_model"], dtype=np.float64)
        self.D = np.asarray(model["D_model"], dtype=np.float64)
        self.N = int(model["N"])

        params = model.get("params", {})
        lift_config = params.get("lift_config") or model.get("lift_config")
        if lift_config is None or lift_config.get("kind") != "soft_lift":
            raise ValueError("FS-EDMD model does not contain a SoftLift config")
        self.lifting_fn = SoftLift.from_config(lift_config)

        meta = np.load(self.model_dir / "meta.npz", allow_pickle=True)
        self.x_mean = np.asarray(meta["x_mean"], dtype=np.float64).reshape(-1)
        self.x_scale = np.asarray(meta["x_scale"], dtype=np.float64).reshape(-1)
        self.u_mean = np.asarray(meta["u_mean"], dtype=np.float64).reshape(-1)
        self.u_scale = np.asarray(meta["u_scale"], dtype=np.float64).reshape(-1)

        self.d = int(self.A.shape[0])
        self.m = int(self.B.shape[1])
        self.n = int(self.C.shape[0])
        if self.n != 2:
            raise ValueError(f"FS-EDMD state dimension must be 2, got {self.n}")
        if self.D.shape[1] != self.lifting_fn.dimension:
            raise ValueError(
                f"D feature dimension mismatch: {self.D.shape[1]} vs "
                f"{self.lifting_fn.dimension}"
            )

    def reset(self) -> None:
        return None

    def normalize_state(self, x) -> np.ndarray:
        value = np.asarray(x, dtype=np.float64)
        if value.shape[-1] != self.n:
            raise ValueError(f"State dimension must be {self.n}, got {value.shape}")
        return (value - self.x_mean) / self.x_scale

    def denormalize_state(self, x_norm) -> np.ndarray:
        value = np.asarray(x_norm, dtype=np.float64)
        if value.shape[-1] != self.n:
            raise ValueError(f"State dimension must be {self.n}, got {value.shape}")
        return value * self.x_scale + self.x_mean

    def normalize_control(self, u_phys) -> np.ndarray:
        value = np.asarray(u_phys, dtype=np.float64).reshape(self.m)
        return (value - self.u_mean) / self.u_scale

    def denormalize_control(self, u_norm) -> np.ndarray:
        value = np.asarray(u_norm, dtype=np.float64).reshape(self.m)
        return value * self.u_scale + self.u_mean

    def lift_state_norm(self, x_norm: np.ndarray) -> np.ndarray:
        value = np.asarray(x_norm, dtype=np.float64).reshape(1, self.n)
        return np.asarray(self.lifting_fn.transform(value), dtype=np.float64).reshape(
            self.lifting_fn.dimension
        )

    def _augment_norm(self, x_norm: np.ndarray) -> np.ndarray:
        x_norm = np.asarray(x_norm, dtype=np.float64).reshape(self.n)
        return np.concatenate([x_norm, self.D @ self.lift_state_norm(x_norm)])

    def lift_current(self, current_pos) -> np.ndarray:
        return self._augment_norm(self.normalize_state(current_pos))

    def lift_reference(
        self, trajectory_sequence, current_step: int, shift: int = 0
    ) -> np.ndarray:
        if not trajectory_sequence:
            raise ValueError("trajectory_sequence is empty.")
        idx = min(max(int(current_step) + shift, 0), len(trajectory_sequence) - 1)
        return self._augment_norm(self.normalize_state(trajectory_sequence[idx]))

    def augmented_state(self, current_pos) -> np.ndarray:
        return self._augment_norm(self.normalize_state(current_pos))
