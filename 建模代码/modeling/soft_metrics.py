"""Metrics for fixed-trajectory soft-platform evaluation."""

from __future__ import annotations

import numpy as np


def _validate_xy_arrays(
    prediction: np.ndarray, target: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    prediction = np.asarray(prediction, dtype=np.float64)
    target = np.asarray(target, dtype=np.float64)
    if prediction.shape != target.shape:
        raise ValueError(
            f"Prediction/target shape mismatch: {prediction.shape} vs {target.shape}"
        )
    if not np.isfinite(prediction).all() or not np.isfinite(target).all():
        raise ValueError("Prediction or target contains NaN or Inf")
    return prediction, target


def xy_mse(prediction: np.ndarray, target: np.ndarray) -> float:
    prediction, target = _validate_xy_arrays(prediction, target)
    return float(np.mean((prediction - target) ** 2))


def xy_rmse(prediction: np.ndarray, target: np.ndarray) -> float:
    return float(np.sqrt(xy_mse(prediction, target)))


def xy_mae(prediction: np.ndarray, target: np.ndarray) -> float:
    prediction, target = _validate_xy_arrays(prediction, target)
    return float(np.mean(np.abs(prediction - target)))


def xy_tracking_metrics(prediction: np.ndarray, target: np.ndarray) -> dict[str, float]:
    prediction, target = _validate_xy_arrays(prediction, target)
    squared_error = (prediction - target) ** 2
    mse = float(np.mean(squared_error))
    return {
        "mse": mse,
        "rmse": float(np.sqrt(mse)),
        "mae": float(np.mean(np.abs(prediction - target))),
    }


def summarize_trajectory_metrics(rows: list[dict], method: str) -> dict:
    values = [float(row[f"{method}_rmse"]) for row in rows]
    if not values:
        raise ValueError(f"No trajectory metrics for {method}")
    best_index = int(np.argmin(values))
    return {
        "average_rmse": float(np.mean(values)),
        "best_rmse": float(values[best_index]),
        "best_trajectory_id": int(rows[best_index]["trajectory_id"]),
        "trajectory_count": len(values),
    }
