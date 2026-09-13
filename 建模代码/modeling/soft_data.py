"""Data preparation and loading for the soft-platform modeling dataset."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "数据备份" / "软体平台" / "原始数据"
EXPERIMENT_ROOT = PROJECT_ROOT / "杂项" / "软体平台探索实验结果"
PROCESSED_DATA_DIR = EXPERIMENT_ROOT / "processed_data"

EXPECTED_TRAJECTORIES = 100
TRAIN_COUNT = 70
VAL_COUNT = 20
TEST_COUNT = 10
DEFAULT_SEED = 20260911


def _require_2d_float64(name: str, value: np.ndarray, path: Path) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError(f"{path}: {name} must have shape (N, 2), got {array.shape}")
    if not np.isfinite(array).all():
        raise ValueError(f"{path}: {name} contains NaN or Inf")
    return array


def _read_raw_trajectory(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        missing = [name for name in ("t", "x", "u") if name not in data]
        if missing:
            raise ValueError(f"{path} is missing fields: {missing}")
        t = np.asarray(data["t"], dtype=np.float64).reshape(-1)
        x = _require_2d_float64("x", data["x"], path)
        u = _require_2d_float64("u", data["u"], path)

    if t.shape[0] != x.shape[0] or x.shape != u.shape:
        raise ValueError(
            f"{path}: inconsistent lengths t={t.shape}, x={x.shape}, u={u.shape}"
        )
    if x.shape[0] < 2:
        raise ValueError(f"{path}: at least two samples are required")
    if not np.isfinite(t).all():
        raise ValueError(f"{path}: t contains NaN or Inf")
    return {"t": t, "x": x, "u": u}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _raw_files(raw_dir: Path) -> list[Path]:
    files = sorted(raw_dir.glob("*.npz"), key=lambda item: item.name)
    if len(files) != EXPECTED_TRAJECTORIES:
        raise ValueError(
            f"Expected {EXPECTED_TRAJECTORIES} npz files in {raw_dir}, found {len(files)}"
        )
    return files


def _build_split_manifest(raw_dir: Path, seed: int) -> dict:
    files = _raw_files(raw_dir)
    trajectory_ids = [int(path.stem) for path in files]
    shuffled = np.random.default_rng(seed).permutation(trajectory_ids)
    train_ids = sorted(int(value) for value in shuffled[:TRAIN_COUNT])
    val_ids = sorted(int(value) for value in shuffled[TRAIN_COUNT : TRAIN_COUNT + VAL_COUNT])
    test_ids = sorted(int(value) for value in shuffled[TRAIN_COUNT + VAL_COUNT :])
    return {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "seed": int(seed),
        "raw_dir": str(raw_dir.resolve()),
        "source_files": [
            {"name": path.name, "sha256": _sha256(path)} for path in files
        ],
        "trajectory_ids": {
            "train": train_ids,
            "validation": val_ids,
            "test": test_ids,
        },
        "counts": {
            "train": len(train_ids),
            "validation": len(val_ids),
            "test": len(test_ids),
        },
    }


def _validate_split_manifest(manifest: dict) -> None:
    ids = manifest["trajectory_ids"]
    counts = manifest["counts"]
    if counts != {
        "train": TRAIN_COUNT,
        "validation": VAL_COUNT,
        "test": TEST_COUNT,
    }:
        raise ValueError(f"Unexpected split counts: {counts}")
    expected = set(range(1, EXPECTED_TRAJECTORIES + 1))
    train = set(ids["train"])
    val = set(ids["validation"])
    test = set(ids["test"])
    if train & val or train & test or val & test:
        raise ValueError("Train/validation/test trajectory sets overlap")
    if train | val | test != expected:
        missing = sorted(expected - (train | val | test))
        extra = sorted((train | val | test) - expected)
        raise ValueError(f"Split does not cover expected ids; missing={missing}, extra={extra}")


def _trajectory_samples(
    path: Path, raw: dict[str, np.ndarray]
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    trajectory_id = int(path.stem)
    t = raw["t"]
    x = raw["x"]
    u = raw["u"]
    samples = x.shape[0] - 1
    return (
        x[:-1],
        u[:-1],
        x[1:],
        np.full(samples, trajectory_id, dtype=np.int64),
        np.arange(samples, dtype=np.int64),
        t[:-1],
    )


def _stack_split(
    files_by_id: dict[int, Path], ids: list[int]
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    parts: list[tuple[np.ndarray, ...]] = []
    for trajectory_id in ids:
        path = files_by_id[trajectory_id]
        parts.append(_trajectory_samples(path, _read_raw_trajectory(path)))
    if not parts:
        raise ValueError("Cannot build an empty split")
    return tuple(np.concatenate([part[index] for part in parts], axis=0) for index in range(6))


def _normalize(value: np.ndarray, mean: np.ndarray, scale: np.ndarray) -> np.ndarray:
    return (value - mean) / scale


def _save_split(
    output_dir: Path,
    split_name: str,
    x: np.ndarray,
    u: np.ndarray,
    y: np.ndarray,
    trajectory_id: np.ndarray,
    step_index: np.ndarray,
    time: np.ndarray,
    x_mean: np.ndarray,
    x_scale: np.ndarray,
    u_mean: np.ndarray,
    u_scale: np.ndarray,
) -> None:
    np.savez_compressed(
        output_dir / f"{split_name}.npz",
        X=_normalize(x, x_mean, x_scale),
        U=_normalize(u, u_mean, u_scale),
        Y=_normalize(y, x_mean, x_scale),
        trajectory_id=trajectory_id,
        step_index=step_index,
        time=time,
    )


def _stats_report(
    raw_x: np.ndarray,
    raw_u: np.ndarray,
    split_arrays: dict[str, tuple[np.ndarray, ...]],
    x_mean: np.ndarray,
    x_scale: np.ndarray,
    u_mean: np.ndarray,
    u_scale: np.ndarray,
) -> dict:
    report: dict[str, object] = {
        "raw": {
            "x_shape": list(raw_x.shape),
            "u_shape": list(raw_u.shape),
            "x_min": raw_x.min(axis=0).tolist(),
            "x_max": raw_x.max(axis=0).tolist(),
            "u_min": raw_u.min(axis=0).tolist(),
            "u_max": raw_u.max(axis=0).tolist(),
        },
        "normalization": {
            "x_mean": x_mean.tolist(),
            "x_scale": x_scale.tolist(),
            "u_mean": u_mean.tolist(),
            "u_scale": u_scale.tolist(),
        },
    }
    for name, arrays in split_arrays.items():
        x, u, y, trajectory_id, _, _ = arrays
        report[name] = {
            "samples": int(x.shape[0]),
            "trajectory_count": int(np.unique(trajectory_id).size),
            "x_shape": list(x.shape),
            "u_shape": list(u.shape),
            "y_shape": list(y.shape),
        }
    return report


def prepare_soft_dataset(
    raw_dir: str | Path = RAW_DATA_DIR,
    output_dir: str | Path = PROCESSED_DATA_DIR,
    seed: int = DEFAULT_SEED,
    force: bool = False,
) -> dict:
    """Create the fixed soft-platform split and normalized one-step arrays."""
    raw_dir = Path(raw_dir)
    output_dir = Path(output_dir)
    manifest_path = output_dir / "split_manifest.json"
    required = [
        output_dir / "train.npz",
        output_dir / "validation.npz",
        output_dir / "test.npz",
        output_dir / "meta.npz",
        manifest_path,
        output_dir / "dataset_stats.json",
    ]
    if not force and all(path.exists() for path in required):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        _validate_split_manifest(manifest)
        return {"status": "existing", "manifest": manifest, "output_dir": str(output_dir)}
    if manifest_path.exists() and not force:
        raise FileExistsError(
            f"{manifest_path} exists but the processed dataset is incomplete; "
            "use --force only if the fixed split must be regenerated."
        )

    manifest = _build_split_manifest(raw_dir, seed)
    _validate_split_manifest(manifest)
    files_by_id = {int(path.stem): path for path in _raw_files(raw_dir)}
    split_ids = manifest["trajectory_ids"]
    split_arrays = {
        "train": _stack_split(files_by_id, split_ids["train"]),
        "validation": _stack_split(files_by_id, split_ids["validation"]),
        "test": _stack_split(files_by_id, split_ids["test"]),
    }

    train_x = split_arrays["train"][0]
    train_u = split_arrays["train"][1]
    x_mean = train_x.mean(axis=0, dtype=np.float64)
    x_scale = train_x.std(axis=0, dtype=np.float64)
    u_mean = train_u.mean(axis=0, dtype=np.float64)
    u_scale = train_u.std(axis=0, dtype=np.float64)
    x_scale = np.where(x_scale < 1e-12, 1.0, x_scale)
    u_scale = np.where(u_scale < 1e-12, 1.0, u_scale)

    output_dir.mkdir(parents=True, exist_ok=True)
    for split_name, arrays in split_arrays.items():
        x, u, y, trajectory_id, step_index, time = arrays
        _save_split(
            output_dir,
            split_name,
            x,
            u,
            y,
            trajectory_id,
            step_index,
            time,
            x_mean,
            x_scale,
            u_mean,
            u_scale,
        )
    np.savez_compressed(
        output_dir / "meta.npz",
        x_mean=x_mean,
        x_scale=x_scale,
        u_mean=u_mean,
        u_scale=u_scale,
        train_trajectory_ids=np.asarray(split_ids["train"], dtype=np.int64),
        validation_trajectory_ids=np.asarray(split_ids["validation"], dtype=np.int64),
        test_trajectory_ids=np.asarray(split_ids["test"], dtype=np.int64),
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    raw_x = np.vstack([_read_raw_trajectory(path)["x"] for path in files_by_id.values()])
    raw_u = np.vstack([_read_raw_trajectory(path)["u"] for path in files_by_id.values()])
    stats = _stats_report(raw_x, raw_u, split_arrays, x_mean, x_scale, u_mean, u_scale)
    (output_dir / "dataset_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": "created", "manifest": manifest, "output_dir": str(output_dir)}


def load_processed_split(split: str, processed_dir: str | Path = PROCESSED_DATA_DIR) -> dict[str, np.ndarray]:
    """Load one normalized split by name."""
    aliases = {"val": "validation", "validation": "validation", "train": "train", "test": "test"}
    if split not in aliases:
        raise ValueError(f"Unknown split: {split}")
    path = Path(processed_dir) / f"{aliases[split]}.npz"
    if not path.exists():
        raise FileNotFoundError(f"Missing processed split: {path}. Run prepare_soft_data.py first.")
    with np.load(path, allow_pickle=False) as data:
        result = {name: data[name] for name in data.files}
    for name in ("X", "U", "Y"):
        if result[name].dtype != np.float64:
            raise ValueError(f"{path}: {name} must be float64")
        if not np.isfinite(result[name]).all():
            raise ValueError(f"{path}: {name} contains NaN or Inf")
    return result


def load_processed_meta(processed_dir: str | Path = PROCESSED_DATA_DIR) -> dict[str, np.ndarray]:
    path = Path(processed_dir) / "meta.npz"
    if not path.exists():
        raise FileNotFoundError(f"Missing processed metadata: {path}")
    with np.load(path, allow_pickle=False) as data:
        return {name: data[name] for name in data.files}


def denormalize_x(
    value: np.ndarray,
    meta: dict[str, np.ndarray],
) -> np.ndarray:
    return np.asarray(value, dtype=np.float64) * meta["x_scale"] + meta["x_mean"]


def denormalize_u(
    value: np.ndarray,
    meta: dict[str, np.ndarray],
) -> np.ndarray:
    return np.asarray(value, dtype=np.float64) * meta["u_scale"] + meta["u_mean"]


def iter_trajectories(split_data: dict[str, np.ndarray]):
    """Yield contiguous trajectory slices in stored order."""
    for trajectory_id in np.unique(split_data["trajectory_id"]):
        mask = split_data["trajectory_id"] == trajectory_id
        indices = np.flatnonzero(mask)
        if indices.size == 0 or not np.array_equal(indices, np.arange(indices[0], indices[-1] + 1)):
            raise ValueError(f"Trajectory {trajectory_id} samples are not contiguous")
        yield {
            "trajectory_id": int(trajectory_id),
            "X": split_data["X"][mask],
            "U": split_data["U"][mask],
            "Y": split_data["Y"][mask],
            "step_index": split_data["step_index"][mask],
        }
