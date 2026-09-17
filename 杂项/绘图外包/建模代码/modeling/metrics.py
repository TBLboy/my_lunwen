"""Metric helpers compatible with the verified baseline plotting script."""

import numpy as np


def calculate_metrics(true, pred):
    """Compute MSE, RMSE, MAE and per-dimension RMSE."""
    true = np.asarray(true, dtype=np.float64)
    pred = np.asarray(pred, dtype=np.float64)
    mse = np.mean((true - pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(true - pred))
    rmse_per_dim = np.sqrt(np.mean((true - pred) ** 2, axis=0))
    return {
        "mse": mse,
        "rmse": rmse,
        "mae": mae,
        "rmse_per_dim": rmse_per_dim,
    }
