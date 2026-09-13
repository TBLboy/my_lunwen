"""Train and evaluate one soft-platform configuration on the fixed test set."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.soft_data import (
    EXPERIMENT_ROOT,
    denormalize_x,
    iter_trajectories,
    load_processed_meta,
    load_processed_split,
)
from modeling.soft_lift import SoftLift
from modeling.soft_metrics import summarize_trajectory_metrics, xy_rmse
from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import OursKoopmanTrainer


METHODS = ("fs_edmd", "edmd", "edmd_dl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--seed", type=int, default=20260911)
    parser.add_argument("--models", default="fs_edmd,edmd,edmd_dl")
    parser.add_argument("--smoke", action="store_true", help="Use short training settings.")
    parser.add_argument("--lift-poly-degree", type=int, default=4)
    parser.add_argument("--lift-rbf-grid", type=int, default=13)
    parser.add_argument("--lift-rbf-sigma-scale", type=float, default=0.8)
    parser.add_argument("--lift-freqs", default="1,2,3,4")
    parser.add_argument("--fs-n", type=int, default=40)
    parser.add_argument("--fs-lam", type=float, default=1e-3)
    parser.add_argument("--fs-beta", type=float, default=1e-3)
    parser.add_argument("--fs-eta-d", type=float, default=1e-2)
    parser.add_argument("--fs-max-iter", type=int, default=2000)
    parser.add_argument("--fs-tol", type=float, default=1e-6)
    parser.add_argument("--fs-grad-clip-norm", type=float, default=10.0)
    parser.add_argument("--fs-lr-decay-factor", type=float, default=0.9)
    parser.add_argument("--edmd-reg", type=float, default=1e-6)
    parser.add_argument("--edmd-dl-n-psi", type=int, default=50)
    parser.add_argument("--edmd-dl-layers", default="512,512,512")
    parser.add_argument("--edmd-dl-lr", type=float, default=1e-4)
    parser.add_argument("--edmd-dl-reg", type=float, default=1e-6)
    parser.add_argument("--edmd-dl-epochs", type=int, default=50)
    parser.add_argument("--edmd-dl-batch-size", type=int, default=2048)
    parser.add_argument("--test-limit", type=int, default=10)
    parser.add_argument("--eval-splits", default="test,validation")
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def configure_logger(run_dir: Path) -> logging.Logger:
    logger = logging.getLogger("soft_experiment")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    log_path = run_dir / "logs" / "train.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def parse_layers(value: str) -> tuple[int, ...]:
    layers = tuple(int(item) for item in value.split(",") if item.strip())
    if not layers:
        raise ValueError("At least one EDMDDL layer size is required")
    return layers


def evaluate_method(
    model,
    method: str,
    split_data: dict,
    meta: dict,
    split_limit: int,
) -> list[dict]:
    rows: list[dict] = []
    trajectories = list(iter_trajectories(split_data))[:split_limit]
    if not trajectories:
        raise ValueError("No trajectories available for evaluation")
    for trajectory in trajectories:
        prediction_norm = model.predict(
            trajectory["X"][0],
            trajectory["U"],
            steps=len(trajectory["U"]),
        )
        prediction = denormalize_x(prediction_norm, meta)
        target = denormalize_x(trajectory["Y"], meta)
        rows.append(
            {
                "trajectory_id": trajectory["trajectory_id"],
                "steps": int(len(trajectory["U"])),
                f"{method}_rmse": xy_rmse(prediction, target),
            }
        )
    return rows


def merge_rows(all_rows: dict[str, list[dict]]) -> list[dict]:
    merged: dict[int, dict] = {}
    for method, rows in all_rows.items():
        for row in rows:
            trajectory_id = row["trajectory_id"]
            merged.setdefault(
                trajectory_id, {"trajectory_id": trajectory_id, "steps": row["steps"]}
            )[f"{method}_rmse"] = row[f"{method}_rmse"]
    return [merged[key] for key in sorted(merged)]


def write_csv(path: Path, rows: list[dict], methods: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["trajectory_id", "steps"] + [f"{method}_rmse" for method in methods]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    selected = [item.strip() for item in args.models.split(",") if item.strip()]
    unknown = sorted(set(selected) - set(METHODS))
    if unknown:
        raise ValueError(f"Unknown methods: {unknown}")
    set_seed(args.seed)

    run_id = args.run_id or datetime.now(timezone.utc).strftime("soft-%Y%m%d-%H%M%S")
    run_dir = EXPERIMENT_ROOT / "runs" / run_id
    if run_dir.exists():
        raise FileExistsError(f"Run directory already exists: {run_dir}")
    (run_dir / "models").mkdir(parents=True)
    (run_dir / "metrics").mkdir(parents=True)
    logger = configure_logger(run_dir)

    start = time.time()
    train = load_processed_split("train")
    validation = load_processed_split("validation")
    test = load_processed_split("test")
    meta = load_processed_meta()

    lift = SoftLift(
        poly_degree=args.lift_poly_degree,
        rbf_grid_size=args.lift_rbf_grid,
        rbf_sigma_scale=args.lift_rbf_sigma_scale,
        trig_frequencies=tuple(
            int(item) for item in args.lift_freqs.split(",") if item.strip()
        ),
    ).fit(train["X"])
    lift_report = lift.report(train["X"])
    logger.info("lift dimension=%s", lift.dimension)

    models: dict[str, object] = {}
    max_iter = 50 if args.smoke else args.fs_max_iter
    if "fs_edmd" in selected:
        logger.info("Training FS-EDMD")
        fs = OursKoopmanTrainer(
            lam=args.fs_lam,
            beta=args.fs_beta,
            N=args.fs_n,
            eta_D=args.fs_eta_d,
            max_iter=max_iter,
            tol=args.fs_tol,
            grad_clip_norm=args.fs_grad_clip_norm,
            lr_decay_factor=args.fs_lr_decay_factor,
            lift_fn=lift,
            lift_config=lift.to_config(),
            device="cpu",
            verbose=False,
        )
        fs.fit(
            train["X"].T,
            train["Y"].T,
            train["U"].T,
            lift(train["X"]).T,
            lift(train["Y"]).T,
        )
        fs.save(run_dir / "models" / "fs_edmd.pkl")
        models["fs_edmd"] = fs

    if "edmd" in selected:
        logger.info("Training EDMD")
        edmd = EDMDTrainer(
            reg=args.edmd_reg,
            lift_fn=lift,
            lift_config=lift.to_config(),
        )
        edmd.fit(train["X"], train["Y"], train["U"])
        edmd.save(run_dir / "models" / "edmd.pkl")
        models["edmd"] = edmd

    if "edmd_dl" in selected:
        logger.info("Training EDMDDL")
        epochs = 2 if args.smoke else args.edmd_dl_epochs
        edmd_dl = EDMDDLTrainer(
            state_dim=2,
            control_dim=2,
            n_psi=args.edmd_dl_n_psi,
            layer_sizes=parse_layers(args.edmd_dl_layers),
            lr=args.edmd_dl_lr,
            reg=args.edmd_dl_reg,
            device="cpu",
        )
        edmd_dl.fit(
            train["X"],
            train["Y"],
            train["U"],
            validation["X"],
            validation["Y"],
            validation["U"],
            epochs=epochs,
            batch_size=args.edmd_dl_batch_size,
        )
        edmd_dl.save(run_dir / "models" / "edmd_dl.pkl")
        models["edmd_dl"] = edmd_dl

    eval_splits = [item.strip() for item in args.eval_splits.split(",") if item.strip()]
    unknown_splits = sorted(set(eval_splits) - {"test", "validation"})
    if unknown_splits:
        raise ValueError(f"Unknown eval splits: {unknown_splits}")

    split_data_map = {
        "test": test,
        "validation": validation,
    }
    logger.info("Evaluating splits: %s", ",".join(eval_splits))
    methods_order = list(models)
    split_metrics = {}
    for split_name in eval_splits:
        all_rows = {
            method: evaluate_method(
                model,
                method,
                split_data_map[split_name],
                meta,
                args.test_limit,
            )
            for method, model in models.items()
        }
        rows = merge_rows(all_rows)
        split_metrics[split_name] = {
            "per_trajectory": rows,
            "methods": {
                method: summarize_trajectory_metrics(rows, method)
                for method in models
            },
        }
        write_csv(
            run_dir / "metrics" / f"{split_name}_trajectory.csv",
            rows,
            methods_order,
        )

    summary = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "smoke": bool(args.smoke),
        "test_limit": int(args.test_limit),
        "eval_splits": eval_splits,
        "lift": lift_report,
        "methods": split_metrics["test"]["methods"],
        "split_metrics": split_metrics,
    }
    (run_dir / "metrics" / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    config = {
        "run_id": run_id,
        "arguments": vars(args),
        "lift": lift.to_config(),
        "methods": list(models),
        "eval_splits": eval_splits,
    }
    (run_dir / "run_config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    logger.info("Run complete in %.2f seconds", time.time() - start)
    logger.info(
        "Summary: %s",
        json.dumps(split_metrics["test"]["methods"], ensure_ascii=False),
    )


if __name__ == "__main__":
    main()
