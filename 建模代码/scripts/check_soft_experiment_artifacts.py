"""Validate one soft-platform experiment directory after training."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.soft_data import EXPERIMENT_ROOT, denormalize_x, iter_trajectories, load_processed_meta, load_processed_split
from modeling.soft_metrics import xy_rmse
from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import OursKoopmanTrainer


MODEL_FILES = {
    "fs_edmd": ("fs_edmd.pkl", OursKoopmanTrainer),
    "edmd": ("edmd.pkl", EDMDTrainer),
    "edmd_dl": ("edmd_dl.pkl", EDMDDLTrainer),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--models", default="fs_edmd,edmd,edmd_dl")
    parser.add_argument("--test-limit", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = EXPERIMENT_ROOT / "runs" / args.run_id
    if not run_dir.exists():
        raise FileNotFoundError(run_dir)

    captured = {
        "run_id": args.run_id,
        "models": [],
    }
    errors: list[str] = []

    metrics_path = run_dir / "metrics" / "summary.json"
    if not metrics_path.exists():
        raise FileNotFoundError(metrics_path)
    summary = json.loads(metrics_path.read_text(encoding="utf-8"))
    for method in ("fs_edmd", "edmd", "edmd_dl"):
        if method not in summary.get("methods", {}):
            errors.append(f"summary missing method: {method}")
    test_csv = run_dir / "metrics" / "test_trajectory.csv"
    legacy_csv = run_dir / "metrics" / "per_trajectory.csv"
    if not test_csv.exists() and not legacy_csv.exists():
        errors.append("missing trajectory metrics CSV")

    config_path = run_dir / "run_config.json"
    if not config_path.exists():
        raise FileNotFoundError(config_path)

    meta = load_processed_meta()
    test = load_processed_split("test")
    trajectories = list(iter_trajectories(test))[: args.test_limit]
    if not trajectories:
        raise ValueError("No test trajectories available")

    selected = [item.strip() for item in args.models.split(",") if item.strip()]
    unknown = sorted(set(selected) - set(MODEL_FILES))
    if unknown:
        raise ValueError(f"Unknown models: {unknown}")

    for method in selected:
        filename, trainer_cls = MODEL_FILES[method]
        model_path = run_dir / "models" / filename
        if not model_path.exists():
            errors.append(f"missing model: {model_path}")
            continue
        model = trainer_cls()
        model.load(model_path)
        trajectory = trajectories[0]
        prediction_norm = model.predict(
            trajectory["X"][0],
            trajectory["U"],
            steps=min(20, len(trajectory["U"])),
        )
        prediction = denormalize_x(prediction_norm, meta)
        target = trajectory["Y"][: prediction.shape[0]]
        if prediction.shape != target.shape:
            errors.append(f"{method}: prediction shape mismatch")
        if not np.isfinite(prediction).all():
            errors.append(f"{method}: prediction is not finite")
        rmse = xy_rmse(prediction, target)
        captured["models"].append(
            {
                "method": method,
                "path": str(model_path),
                "reloaded": True,
                "prediction_shape": list(prediction.shape),
                "finite": bool(np.isfinite(prediction).all()),
                "rmse": float(rmse),
            }
        )
        print(f"{method}: reloaded and predicted shape={prediction.shape} finite={bool(np.isfinite(prediction).all())}")

    if errors:
        raise RuntimeError("; ".join(errors))
    print(json.dumps(captured, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
