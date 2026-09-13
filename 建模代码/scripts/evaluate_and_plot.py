"""Evaluate the three modeling methods and generate comparison figures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.data_io import (
    denormalize,
    get_model_path,
    get_output_path,
    load_meta,
    load_test_data,
)
from modeling.metrics import calculate_metrics
from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import OursKoopmanTrainer

METHOD_DISPLAY = {
    "fsedmd": "FS-EDMD",
    "edmddl": "EDMDDL",
    "edmd": "EDMD",
}

PLOT_CONFIG = {
    "global_font_scale": 1.8,
    "global_linewidth_scale": 1.6,
    "legend_columnspacing": 0.9,
    "legend_vertical_position": 1.06,
    "legend_handlelength": 0.8,
    "ylabel_horizontal_pad": 10,
    "figure_width": 7.0,
    "figure_height": 8.0,
    "dpi": 300,
    "font_family": "Times New Roman",
    "font_size_label": 11,
    "font_size_tick": 10,
    "font_size_legend": 9,
    "font_size_title": 12,
    "linewidth_truth": 1.3,
    "linewidth_prediction": 1.3,
    "color_truth": "#D62728",
    "color_fsedmd": "#000000",
    "color_edmddl": "#FF7F0E",
    "color_edmd": "#2CA02C",
    "linestyle_truth": "-",
    "linestyle_fsedmd": "-",
    "linestyle_edmddl": "--",
    "linestyle_edmd": "-.",
    "grid_alpha": 1,
    "grid_linestyle": "-",
    "grid_linewidth": 0.8,
    "grid_color": "#CCCCCC",
    "legend_ncol": 4,
    "legend_framealpha": 0.95,
    "legend_frameon": False,
    "legend_loc": "upper center",
    "subplot_hspace": 0.15,
    "subplot_top": 0.98,
    "subplot_bottom": 0.08,
    "subplot_left": 0.12,
    "subplot_right": 0.98,
    "ylim_margin_ratio": 0.05,
}


def setup_plot_style():
    scale = PLOT_CONFIG["global_font_scale"]
    linewidth_scale = PLOT_CONFIG["global_linewidth_scale"]
    plt.rcParams.update(
        {
            "font.family": PLOT_CONFIG["font_family"],
            "font.size": PLOT_CONFIG["font_size_tick"] * scale,
            "axes.labelsize": PLOT_CONFIG["font_size_label"] * scale,
            "axes.titlesize": PLOT_CONFIG["font_size_title"] * scale,
            "xtick.labelsize": PLOT_CONFIG["font_size_tick"] * scale,
            "ytick.labelsize": PLOT_CONFIG["font_size_tick"] * scale,
            "legend.fontsize": PLOT_CONFIG["font_size_legend"] * scale,
            "legend.columnspacing": PLOT_CONFIG["legend_columnspacing"],
            "legend.handlelength": PLOT_CONFIG["legend_handlelength"],
            "figure.dpi": 100,
            "savefig.dpi": PLOT_CONFIG["dpi"],
            "axes.linewidth": 1.0,
            "grid.linewidth": PLOT_CONFIG["grid_linewidth"],
            "lines.linewidth": PLOT_CONFIG["linewidth_prediction"]
            * linewidth_scale,
            "axes.grid": True,
            "grid.alpha": PLOT_CONFIG["grid_alpha"],
            "grid.linestyle": PLOT_CONFIG["grid_linestyle"],
            "grid.color": PLOT_CONFIG["grid_color"],
        }
    )


def load_all_models():
    models = {}

    print("Loading FS-EDMD...")
    fsedmd = OursKoopmanTrainer(device="cpu")
    fsedmd.load(get_model_path("ours_model.pkl"))
    models["fsedmd"] = fsedmd

    print("Loading EDMDDL...")
    edmddl = EDMDDLTrainer(device="cpu")
    edmddl.load(get_model_path("edmddl_model.pkl"), device="cpu")
    models["edmddl"] = edmddl

    print("Loading EDMD...")
    edmd = EDMDTrainer()
    edmd.load(get_model_path("edmd_model.pkl"))
    models["edmd"] = edmd

    return models


def run_predictions(models, X_test, U_test, steps):
    predictions = {}
    x0 = X_test[0]
    for name, model in models.items():
        print(f"Predicting {METHOD_DISPLAY[name]} for {steps} steps...")
        predictions[name] = model.predict(x0, U_test, steps=steps)
    return predictions


def plot_comparison(X_true, predictions, q_scaler, q_dc, save_dir, kind):
    setup_plot_style()
    scale = PLOT_CONFIG["global_font_scale"]
    linewidth_scale = PLOT_CONFIG["global_linewidth_scale"]

    X_true_denorm = denormalize(X_true, q_scaler, q_dc)
    preds_denorm = {
        name: denormalize(pred, q_scaler, q_dc)
        for name, pred in predictions.items()
    }

    T = X_true_denorm.shape[0]
    time = np.arange(T) * 0.004

    if kind == "position":
        indices = [0, 2, 4]
        units = "rad"
        filename = "position_comparison"
    else:
        indices = [1, 3, 5]
        units = "rad/s"
        filename = "velocity_comparison"

    colors = {
        "truth": PLOT_CONFIG["color_truth"],
        "fsedmd": PLOT_CONFIG["color_fsedmd"],
        "edmddl": PLOT_CONFIG["color_edmddl"],
        "edmd": PLOT_CONFIG["color_edmd"],
    }
    linestyles = {
        "truth": PLOT_CONFIG["linestyle_truth"],
        "fsedmd": PLOT_CONFIG["linestyle_fsedmd"],
        "edmddl": PLOT_CONFIG["linestyle_edmddl"],
        "edmd": PLOT_CONFIG["linestyle_edmd"],
    }
    linewidths = {
        "truth": PLOT_CONFIG["linewidth_truth"] * linewidth_scale,
        "fsedmd": PLOT_CONFIG["linewidth_prediction"] * linewidth_scale,
        "edmddl": PLOT_CONFIG["linewidth_prediction"] * linewidth_scale,
        "edmd": PLOT_CONFIG["linewidth_prediction"] * linewidth_scale,
    }

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(PLOT_CONFIG["figure_width"], PLOT_CONFIG["figure_height"]),
    )
    for i, idx in enumerate(indices):
        ax = axes[i]
        ax.plot(
            time,
            X_true_denorm[:, idx],
            color=colors["truth"],
            linestyle=linestyles["truth"],
            linewidth=linewidths["truth"],
            label="Ground Truth",
            zorder=5,
        )
        for name in ["fsedmd", "edmddl", "edmd"]:
            ax.plot(
                time,
                preds_denorm[name][:, idx],
                color=colors[name],
                linestyle=linestyles[name],
                linewidth=linewidths[name],
                label=METHOD_DISPLAY[name],
                alpha=0.85,
            )

        ax.set_ylabel(
            f"Joint {i + 1} ({units})",
            fontsize=PLOT_CONFIG["font_size_label"] * scale,
            labelpad=PLOT_CONFIG["ylabel_horizontal_pad"],
        )
        ax.grid(
            True,
            alpha=PLOT_CONFIG["grid_alpha"],
            linestyle=PLOT_CONFIG["grid_linestyle"],
            linewidth=PLOT_CONFIG["grid_linewidth"],
            color=PLOT_CONFIG["grid_color"],
        )
        ax.tick_params(
            labelsize=PLOT_CONFIG["font_size_tick"] * scale,
            direction="in",
            width=1.0,
            pad=5,
        )
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        ymin, ymax = ax.get_ylim()
        margin = (ymax - ymin) * PLOT_CONFIG["ylim_margin_ratio"]
        if i == 0:
            ax.set_ylim(ymin - margin, ymax + margin * 3.0)
        else:
            ax.set_ylim(ymin - margin, ymax + margin)

        if i == 0:
            ax.legend(
                loc=PLOT_CONFIG["legend_loc"],
                bbox_to_anchor=(0.5, PLOT_CONFIG["legend_vertical_position"]),
                ncol=PLOT_CONFIG["legend_ncol"],
                fontsize=PLOT_CONFIG["font_size_legend"] * scale,
                framealpha=PLOT_CONFIG["legend_framealpha"],
                frameon=PLOT_CONFIG["legend_frameon"],
                columnspacing=PLOT_CONFIG["legend_columnspacing"],
                handlelength=PLOT_CONFIG["legend_handlelength"],
            )

        if i == 2:
            ax.set_xlabel("Time (s)", fontsize=PLOT_CONFIG["font_size_label"] * scale)

    plt.subplots_adjust(
        hspace=PLOT_CONFIG["subplot_hspace"],
        top=PLOT_CONFIG["subplot_top"],
        bottom=PLOT_CONFIG["subplot_bottom"],
        left=PLOT_CONFIG["subplot_left"],
        right=PLOT_CONFIG["subplot_right"],
    )

    Path(save_dir).mkdir(parents=True, exist_ok=True)
    for ext in ["png", "pdf", "svg"]:
        plt.savefig(
            str(Path(save_dir) / f"{filename}.{ext}"),
            dpi=PLOT_CONFIG["dpi"],
            bbox_inches="tight",
            pad_inches=0.05,
        )
    plt.close(fig)
    print(f"{filename} saved to {save_dir} (PNG/PDF/SVG)")


def compute_metrics(X_true, predictions, q_scaler, q_dc):
    X_true_denorm = denormalize(X_true, q_scaler, q_dc)
    results = {}
    for name, pred in predictions.items():
        pred_denorm = denormalize(pred, q_scaler, q_dc)
        results[name] = calculate_metrics(X_true_denorm, pred_denorm)
    return results, X_true_denorm


def save_results_table(results, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("=" * 80 + "\n")
        handle.write("Modeling accuracy comparison\n")
        handle.write("=" * 80 + "\n\n")
        handle.write(f"{'Method':<15} {'MSE':<15} {'RMSE':<15} {'MAE':<15}\n")
        handle.write("-" * 80 + "\n")
        for name in ["fsedmd", "edmddl", "edmd"]:
            metric = results[name]
            handle.write(
                f"{METHOD_DISPLAY[name]:<15} {metric['mse']:<15.6f} "
                f"{metric['rmse']:<15.6f} {metric['mae']:<15.6f}\n"
            )
        handle.write("-" * 80 + "\n\n")
        handle.write("Per-dimension RMSE details:\n")
        handle.write("Dimensions: q1, dq1, q2, dq2, q3, dq3\n\n")
        for name in ["fsedmd", "edmddl", "edmd"]:
            rmse_str = ", ".join(
                f"{value:.6f}" for value in results[name]["rmse_per_dim"]
            )
            handle.write(f"{METHOD_DISPLAY[name]}: [{rmse_str}]\n")
    print(f"Metrics table saved to {path}")


def print_results(results):
    print("\n" + "=" * 80)
    print("Modeling accuracy comparison")
    print("=" * 80)
    for name in ["fsedmd", "edmddl", "edmd"]:
        metric = results[name]
        print(f"\n{METHOD_DISPLAY[name]}:")
        print(f"  MSE:  {metric['mse']:.6f}")
        print(f"  RMSE: {metric['rmse']:.6f}")
        print(f"  MAE:  {metric['mae']:.6f}")
        print(f"  Per-dim RMSE: {metric['rmse_per_dim']}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate three methods and generate paper comparison figures."
    )
    parser.add_argument("--steps", type=int, default=800)
    args = parser.parse_args()

    metrics_path = get_output_path("metrics", "metrics_table.txt")
    figures_dir = str(Path(get_output_path("figures", "")).resolve())

    print("[1/5] Loading test data...")
    X_test, U_test = load_test_data()
    print(f"Test shapes: X_test={X_test.shape}, U_test={U_test.shape}")

    print("[2/5] Loading normalization metadata...")
    meta = load_meta()
    q_scaler = meta["q_scaler"]
    q_dc = meta["q_dc"]

    print("[3/5] Loading trained models...")
    models = load_all_models()

    print(f"[4/5] Running {args.steps}-step predictions...")
    predictions = run_predictions(models, X_test, U_test, args.steps)
    if len(X_test) < args.steps:
        raise ValueError(
            f"Test data has {len(X_test)} steps, fewer than requested {args.steps}."
        )
    X_true = X_test[: args.steps]

    print("[5/5] Generating metrics and figures...")
    plot_comparison(X_true, predictions, q_scaler, q_dc, figures_dir, "position")
    plot_comparison(X_true, predictions, q_scaler, q_dc, figures_dir, "velocity")

    results, _ = compute_metrics(X_true, predictions, q_scaler, q_dc)
    print_results(results)
    save_results_table(results, metrics_path)

    print(f"\nMetrics: {metrics_path}")
    print(f"Figures: {figures_dir}")
    print("Experiment complete.")


if __name__ == "__main__":
    main()
