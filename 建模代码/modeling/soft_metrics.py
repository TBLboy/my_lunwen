"""Metrics for fixed-trajectory soft-platform evaluation."""

from __future__ import annotations

import numpy as np


def xy_rmse(prediction: np.ndarray, target: np.ndarray) -> float:
    prediction = np.asarray(prediction, dtype=np.float64)
    target = np.asarray(target, dtype=np.float64)
    if prediction.shape != target.shape:
        raise ValueError(
            f"Prediction/target shape mismatch: {prediction.shape} vs {target.shape}"
        )
    if not np.isfinite(prediction).all() or not np.isfinite(target).all():
        raise ValueError("Prediction or target contains NaN or Inf")
    return float(np.sqrt(np.mean((prediction - target) ** 2)))


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
