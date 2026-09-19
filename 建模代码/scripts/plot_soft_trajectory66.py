"""Plot final-model predictions on fixed paper test trajectory 66."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from modeling.soft_data import (
    denormalize_x,
    iter_trajectories,
    load_processed_meta,
    load_processed_split,
)
from modeling.soft_metrics import xy_tracking_metrics
from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import OursKoopmanTrainer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--final-root",
        type=Path,
        default=Path(
            r"C:\Users\Windows\Desktop\论文材料\杂项\软体平台探索实验结果\final"
        ),
    )
    parser.add_argument("--trajectory-id", type=int, default=66)
    args = parser.parse_args()
    if not args.final_root.exists():
        candidate = (
            Path(__file__).resolve().parents[2]
            / "\u6742\u9879"
            / "\u8f6f\u4f53\u5e73\u53f0\u63a2\u7d22\u5b9e\u9a8c\u7ed3\u679c"
            / "final"
        )
        if candidate.exists():
            args.final_root = candidate
    return args


def main() -> None:
    args = parse_args()
    final_root = args.final_root
    processed_dir = final_root / "processed_data"
    models_dir = final_root / "models"
    output_dir = final_root / "figures"

    split_data = load_processed_split("test", processed_dir=processed_dir)
    meta = load_processed_meta(processed_dir=processed_dir)
    trajectory = next(
        item
        for item in iter_trajectories(split_data)
        if item["trajectory_id"] == args.trajectory_id
    )

    models = {
        "FS-EDMD": OursKoopmanTrainer(device="cpu").load(models_dir / "fs_edmd.pkl"),
        "EDMD": EDMDTrainer().load(models_dir / "edmd.pkl"),
        "EDMDDL": EDMDDLTrainer(device="cpu").load(
            models_dir / "edmd_dl.pkl", device="cpu"
        ),
    }

    target = denormalize_x(trajectory["Y"], meta)
    t = np.asarray(trajectory["step_index"], dtype=np.float64)
    predictions = {}
    metric_values = {}
    rmse_values = {}
    for name, model in models.items():
        prediction_norm = model.predict(
            trajectory["X"][0],
            trajectory["U"],
            steps=len(trajectory["U"]),
        )
        prediction = denormalize_x(prediction_norm, meta)
        predictions[name] = prediction
        metric_values[name] = xy_tracking_metrics(prediction, target)
        rmse_values[name] = metric_values[name]["rmse"]

    plot_comparison(
        target,
        predictions,
        rmse_values,
        t,
        trajectory_id=args.trajectory_id,
        output_dir=output_dir,
    )
    write_metrics(
        args.trajectory_id,
        metric_values,
        final_root / "metrics",
        steps=len(target),
    )

    print(f"Trajectory {args.trajectory_id}:")
    for name in ("FS-EDMD", "EDMD", "EDMDDL"):
        metrics = metric_values[name]
        print(
            f"  {name} MSE = {metrics['mse']:.8f}, "
            f"RMSE = {metrics['rmse']:.8f}, MAE = {metrics['mae']:.8f}"
        )
    print(f"Figures: {output_dir}")


def plot_comparison(
    target: np.ndarray,
    predictions: dict[str, np.ndarray],
    rmse_values: dict[str, float],
    t: np.ndarray,
    trajectory_id: int,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    colors = {
        "FS-EDMD": "#c0392b",
        "EDMD": "#2471a3",
        "EDMDDL": "#229954",
    }

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(8.2, 10.4),
        gridspec_kw={"height_ratios": [1.0, 1.0, 1.05]},
    )
    fig.suptitle(
        f"Trajectory {trajectory_id}: prediction comparison",
        fontsize=13,
        fontweight="bold",
        y=0.99,
    )

    for axis, dimension, ylabel in (
        (axes[0], 0, "Position x"),
        (axes[1], 1, "Position y"),
    ):
        axis.plot(t, target[:, dimension], color="#111111", lw=2.0, ls="--", label="Ground truth", zorder=5)
        for name, prediction in predictions.items():
            axis.plot(
                t,
                prediction[:, dimension],
                color=colors[name],
                lw=1.3,
                alpha=0.92,
                label=f"{name} (RMSE {rmse_values[name]:.4f})",
            )
        axis.set_ylabel(ylabel, fontsize=10)
        axis.set_xlabel("Step", fontsize=10)
        axis.grid(alpha=0.25)
        axis.legend(loc="best", fontsize=8.5, ncol=2, framealpha=0.9)

    ax_xy = axes[2]
    ax_xy.plot(target[:, 0], target[:, 1], color="#111111", lw=2.0, ls="--", label="Ground truth", zorder=5)
    for name, prediction in predictions.items():
        ax_xy.plot(
            prediction[:, 0],
            prediction[:, 1],
            color=colors[name],
            lw=1.2,
            alpha=0.92,
            label=f"{name} (RMSE {rmse_values[name]:.4f})",
        )
    ax_xy.set_xlabel("Position x", fontsize=10)
    ax_xy.set_ylabel("Position y", fontsize=10)
    ax_xy.set_title("XY trajectory", fontsize=10)
    ax_xy.grid(alpha=0.25)
    ax_xy.legend(loc="best", fontsize=8.5, ncol=1, framealpha=0.9)

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(output_dir / "trajectory66_comparison.png", dpi=300, facecolor="white")
    fig.savefig(output_dir / "trajectory66_comparison.pdf", facecolor="white")
    fig.savefig(output_dir / "trajectory66_comparison.svg", facecolor="white")
    plt.close(fig)


def write_metrics(
    trajectory_id: int,
    metric_values: dict[str, dict[str, float]],
    metrics_dir: Path,
    steps: int,
) -> None:
    metrics_dir.mkdir(parents=True, exist_ok=True)
    rmse_values = {name: values["rmse"] for name, values in metric_values.items()}
    csv_path = metrics_dir / "trajectory66_rmse.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["trajectory_id", "fs_edmd_rmse", "edmd_rmse", "edmd_dl_rmse"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "trajectory_id": trajectory_id,
                "fs_edmd_rmse": f"{rmse_values['FS-EDMD']:.8f}",
                "edmd_rmse": f"{rmse_values['EDMD']:.8f}",
                "edmd_dl_rmse": f"{rmse_values['EDMDDL']:.8f}",
            }
        )
    json_path = metrics_dir / "trajectory66_rmse.json"
    json_path.write_text(
        json.dumps(
            {
                "trajectory_id": trajectory_id,
                "steps": steps,
                "fs_edmd_rmse": rmse_values["FS-EDMD"],
                "edmd_rmse": rmse_values["EDMD"],
                "edmd_dl_rmse": rmse_values["EDMDDL"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    metrics_csv_path = metrics_dir / "trajectory66_metrics.csv"
    with metrics_csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["trajectory_id", "method", "mse", "rmse", "mae"],
        )
        writer.writeheader()
        for method in ("FS-EDMD", "EDMD", "EDMDDL"):
            values = metric_values[method]
            writer.writerow(
                {
                    "trajectory_id": trajectory_id,
                    "method": method,
                    "mse": f"{values['mse']:.8f}",
                    "rmse": f"{values['rmse']:.8f}",
                    "mae": f"{values['mae']:.8f}",
                }
            )

    metrics_json_path = metrics_dir / "trajectory66_metrics.json"
    metrics_json_path.write_text(
        json.dumps(
            {
                "trajectory_id": trajectory_id,
                "steps": steps,
                "methods": {
                    method: metric_values[method]
                    for method in ("FS-EDMD", "EDMD", "EDMDDL")
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
