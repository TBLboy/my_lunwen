"""Local file loading helpers for the self-contained modeling project."""

from pathlib import Path

import numpy as np
import scipy.io as sio

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def get_data_path(filename):
    """Return the absolute path of a file under data/."""
    return str(DATA_DIR / filename)


def get_model_path(filename):
    """Return the absolute path of a file under models/."""
    return str(MODEL_DIR / filename)


def get_output_path(subdir, filename):
    """Return the absolute path of a file under outputs/<subdir>/."""
    return str(OUTPUT_DIR / subdir / filename)


def _load_struct(filename):
    path = get_data_path(filename)
    if not Path(path).exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    return sio.loadmat(path)[Path(filename).stem][0, 0]


def _require_fields(data, fields):
    missing = [name for name in fields if name not in data.dtype.names]
    if missing:
        raise ValueError(f"{data.dtype.names} is missing fields: {missing}")


def load_train_data():
    """Load training data and normalization metadata from train_data.mat."""
    data = _load_struct("train_data.mat")
    _require_fields(data, ["x", "y", "u", "q_scaler", "q_dc", "u_scaler", "u_dc"])
    meta = {
        "q_scaler": data["q_scaler"].flatten(),
        "q_dc": data["q_dc"].flatten(),
        "u_scaler": data["u_scaler"].flatten(),
        "u_dc": data["u_dc"].flatten(),
    }
    return data["x"], data["y"], data["u"], meta


def load_val_data():
    """Load validation data from val_data.mat."""
    data = _load_struct("val_data.mat")
    _require_fields(data, ["x_val", "y_val", "u_val"])
    return data["x_val"], data["y_val"], data["u_val"]


def load_test_data():
    """Load test data from test_data.mat."""
    data = _load_struct("test_data.mat")
    _require_fields(data, ["x_test", "u_test"])
    return data["x_test"], data["u_test"]


def load_meta():
    """Load normalization metadata from models/meta.npz."""
    path = get_model_path("meta.npz")
    if not Path(path).exists():
        raise FileNotFoundError(f"Missing model metadata: {path}")
    return np.load(path)


def denormalize(x_norm, q_scaler, q_dc):
    """Reverse the q normalization applied before training."""
    return np.asarray(x_norm, dtype=np.float64) * np.asarray(
        q_scaler, dtype=np.float64
    ) + np.asarray(q_dc, dtype=np.float64)
