"""Runtime copy of the soft-platform SoftLift dictionary used by FS-EDMD."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np


def _validate_state(x: np.ndarray) -> np.ndarray:
    value = np.asarray(x, dtype=np.float64)
    if value.ndim != 2 or value.shape[1] != 2:
        raise ValueError(f"SoftLift expects state shape (N, 2), got {value.shape}")
    if not np.isfinite(value).all():
        raise ValueError("SoftLift state contains NaN or Inf")
    return value


def _monomial_terms(x: np.ndarray, degree: int) -> tuple[list[np.ndarray], list[str]]:
    terms: list[np.ndarray] = []
    names: list[str] = []
    for total_degree in range(2, degree + 1):
        for x_power in range(total_degree, -1, -1):
            y_power = total_degree - x_power
            terms.append((x[:, 0] ** x_power) * (x[:, 1] ** y_power))
            names.append(f"x^{x_power}*y^{y_power}")
    return terms, names


@dataclass
class SoftLift:
    """Fixed-dimension nonlinear dictionary for normalized 2D xy states."""

    poly_degree: int = 4
    rbf_grid_size: int = 9
    rbf_sigma_scale: float = 1.0
    trig_frequencies: tuple[int, ...] = (1, 2, 3, 4)
    input_center: np.ndarray | None = None
    input_scale: np.ndarray | None = None
    rbf_centers: np.ndarray | None = None
    rbf_sigma: np.ndarray | None = None
    feature_names: list[str] = field(default_factory=list)
    fitted: bool = False

    def fit(self, x: np.ndarray) -> "SoftLift":
        value = _validate_state(x)
        if value.shape[0] < 2:
            raise ValueError("SoftLift.fit requires at least two samples")

        lower = np.quantile(value, 0.005, axis=0)
        upper = np.quantile(value, 0.995, axis=0)
        span = np.maximum(upper - lower, 1e-6)
        center = 0.5 * (lower + upper)
        scale = 0.5 * span

        self.input_center = center.astype(np.float64)
        self.input_scale = scale.astype(np.float64)
        grid = np.linspace(-1.0, 1.0, self.rbf_grid_size, dtype=np.float64)
        center_x, center_y = np.meshgrid(grid, grid)
        self.rbf_centers = np.column_stack([center_x.ravel(), center_y.ravel()])
        spacing = 2.0 / max(self.rbf_grid_size - 1, 1)
        self.rbf_sigma = np.full(
            2, max(spacing * self.rbf_sigma_scale, 1e-6), dtype=np.float64
        )
        self.feature_names = self._make_feature_names()
        self.fitted = True
        return self

    def _make_feature_names(self) -> list[str]:
        names = ["constant", "x", "y"]
        for total_degree in range(2, self.poly_degree + 1):
            for x_power in range(total_degree, -1, -1):
                y_power = total_degree - x_power
                names.append(f"x^{x_power}*y^{y_power}")
        names.extend(
            f"rbf_{index:03d}" for index in range(self.rbf_centers.shape[0])
        )
        for frequency in self.trig_frequencies:
            names.extend(
                [
                    f"sin_x_{frequency}",
                    f"cos_x_{frequency}",
                    f"sin_y_{frequency}",
                    f"cos_y_{frequency}",
                ]
            )
        return names

    def transform(self, x: np.ndarray) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("SoftLift must be fitted before transform")
        value = _validate_state(x)
        normalized = (value - self.input_center) / self.input_scale

        groups: list[np.ndarray] = [
            np.ones((value.shape[0], 1), dtype=np.float64),
            normalized[:, [0]],
            normalized[:, [1]],
        ]
        polynomial, _ = _monomial_terms(normalized, self.poly_degree)
        groups.extend(term[:, None] for term in polynomial)

        dr = (normalized[:, None, :] - self.rbf_centers[None, :, :]) / self.rbf_sigma
        rbf = np.exp(-0.5 * np.sum(dr * dr, axis=2))
        groups.append(rbf)

        trig_columns: list[np.ndarray] = []
        for frequency in self.trig_frequencies:
            angle_x = np.pi * frequency * normalized[:, 0]
            angle_y = np.pi * frequency * normalized[:, 1]
            trig_columns.extend(
                [
                    np.sin(angle_x)[:, None],
                    np.cos(angle_x)[:, None],
                    np.sin(angle_y)[:, None],
                    np.cos(angle_y)[:, None],
                ]
            )
        if trig_columns:
            groups.append(np.hstack(trig_columns))

        result = np.hstack(groups).astype(np.float64)
        if result.shape[1] != len(self.feature_names):
            raise RuntimeError(
                f"SoftLift dimension mismatch: {result.shape[1]} vs "
                f"{len(self.feature_names)}"
            )
        if not np.isfinite(result).all():
            raise ValueError("SoftLift produced NaN or Inf features")
        return result

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.transform(x)

    @property
    def dimension(self) -> int:
        return len(self.feature_names)

    def to_config(self) -> dict:
        if not self.fitted:
            raise RuntimeError("Cannot serialize an unfitted SoftLift")
        return {
            "kind": "soft_lift",
            "poly_degree": self.poly_degree,
            "rbf_grid_size": self.rbf_grid_size,
            "rbf_sigma_scale": self.rbf_sigma_scale,
            "trig_frequencies": list(self.trig_frequencies),
            "input_center": self.input_center.tolist(),
            "input_scale": self.input_scale.tolist(),
        }

    @classmethod
    def from_config(cls, config: dict) -> "SoftLift":
        lift = cls(
            poly_degree=int(config["poly_degree"]),
            rbf_grid_size=int(config["rbf_grid_size"]),
            rbf_sigma_scale=float(config["rbf_sigma_scale"]),
            trig_frequencies=tuple(int(value) for value in config["trig_frequencies"]),
        )
        lift.input_center = np.asarray(config["input_center"], dtype=np.float64)
        lift.input_scale = np.asarray(config["input_scale"], dtype=np.float64)
        grid = np.linspace(-1.0, 1.0, lift.rbf_grid_size, dtype=np.float64)
        center_x, center_y = np.meshgrid(grid, grid)
        lift.rbf_centers = np.column_stack([center_x.ravel(), center_y.ravel()])
        spacing = 2.0 / max(lift.rbf_grid_size - 1, 1)
        lift.rbf_sigma = np.full(
            2, max(spacing * lift.rbf_sigma_scale, 1e-6), dtype=np.float64
        )
        lift.feature_names = lift._make_feature_names()
        lift.fitted = True
        return lift


def default_soft_lift(x_train: np.ndarray) -> SoftLift:
    """Fit the default 112-dimensional soft-platform lift."""
    return SoftLift().fit(x_train)
