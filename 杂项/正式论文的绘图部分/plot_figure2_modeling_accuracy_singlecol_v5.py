"""Generate a single-column, publication-oriented Figure 4 (modeling accuracy)."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from matplotlib.ticker import MaxNLocator
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
MODELING_ROOT = PROJECT_ROOT / "建模代码"
SOFT_FINAL_ROOT = PROJECT_ROOT / "杂项" / "软体平台探索实验结果" / "final"

if str(MODELING_ROOT) not in sys.path:
    sys.path.insert(0, str(MODELING_ROOT))

from modeling.data_io import denormalize, load_meta, load_test_data
from modeling.soft_data import denormalize_x, iter_trajectories, load_processed_meta, load_processed_split
from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import OursKoopmanTrainer


MECHANICAL_STEPS = 800
SOFT_TRAJECTORY_ID = 66
SAMPLE_PERIOD_S = 0.004

COLORS = {
    "Ground truth": "#202020",
    "FS-EDMD": "#D55E00",
    "EDMDDL": "#009E73",
    "EDMD": "#0072B2",
}
LINESTYLES = {
    "Ground truth": "-",
    "FS-EDMD": "-",
    "EDMDDL": "--",
    "EDMD": "-.",
}
LINEWIDTHS = {
    "Ground truth": 0.95,
    "FS-EDMD": 1.12,
    "EDMDDL": 0.88,
    "EDMD": 0.88,
}
LINE_ORDER = ("Ground truth", "FS-EDMD", "EDMDDL", "EDMD")
PANEL_LABELS = ("(a)", "(b)", "(c)", "(d)", "(e)")
PANEL_TITLES = ("Joint 1", "Joint 2", "Joint 3", "Soft x", "Soft y")


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 6.2,
            "axes.labelsize": 6.4,
            "axes.titlesize": 6.4,
            "xtick.labelsize": 5.8,
            "ytick.labelsize": 5.8,
            "legend.fontsize": 5.8,
            "axes.linewidth": 0.52,
            "axes.edgecolor": "#404040",
            "xtick.major.width": 0.45,
            "ytick.major.width": 0.45,
            "xtick.major.size": 2.0,
            "ytick.major.size": 2.0,
            "axes.axisbelow": True,
            "lines.solid_capstyle": "round",
            "lines.dash_capstyle": "round",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "stix",
        }
    )


def load_mechanical_predictions() -> tuple[np.ndarray, dict[str, np.ndarray], np.ndarray]:
    x_test, u_test = load_test_data()
    if len(x_test) < MECHANICAL_STEPS or len(u_test) < MECHANICAL_STEPS:
        raise ValueError(
            "Mechanical test data contains fewer than "
            f"{MECHANICAL_STEPS} required samples."
        )

    meta = load_meta()
    q_scaler = meta["q_scaler"]
    q_dc = meta["q_dc"]
    truth = denormalize(x_test[:MECHANICAL_STEPS], q_scaler, q_dc)

    models = {
        "FS-EDMD": OursKoopmanTrainer(device="cpu", verbose=False).load(
            MODELING_ROOT / "models" / "ours_model.pkl"
        ),
        "EDMDDL": EDMDDLTrainer(device="cpu").load(
            MODELING_ROOT / "models" / "edmddl_model.pkl",
            device="cpu",
        ),
        "EDMD": EDMDTrainer().load(MODELING_ROOT / "models" / "edmd_model.pkl"),
    }

    predictions = {}
    for name, model in models.items():
        prediction = model.predict(x_test[0], u_test, steps=MECHANICAL_STEPS)
        predictions[name] = denormalize(prediction, q_scaler, q_dc)

    time = np.arange(MECHANICAL_STEPS, dtype=np.float64) * SAMPLE_PERIOD_S
    return truth, predictions, time


def load_soft_predictions() -> tuple[np.ndarray, dict[str, np.ndarray], np.ndarray]:
    processed_dir = SOFT_FINAL_ROOT / "processed_data"
    models_dir = SOFT_FINAL_ROOT / "models"

    test_data = load_processed_split("test", processed_dir=processed_dir)
    meta = load_processed_meta(processed_dir=processed_dir)
    trajectory = next(
        item
        for item in iter_trajectories(test_data)
        if item["trajectory_id"] == SOFT_TRAJECTORY_ID
    )
    truth = denormalize_x(trajectory["Y"], meta)

    models = {
        "FS-EDMD": OursKoopmanTrainer(device="cpu", verbose=False).load(models_dir / "fs_edmd.pkl"),
        "EDMDDL": EDMDDLTrainer(device="cpu").load(models_dir / "edmd_dl.pkl", device="cpu"),
        "EDMD": EDMDTrainer().load(models_dir / "edmd.pkl"),
    }

    predictions = {}
    for name, model in models.items():
        prediction = model.predict(trajectory["X"][0], trajectory["U"], steps=len(trajectory["U"]))
        predictions[name] = denormalize_x(prediction, meta)

    step = np.asarray(trajectory["step_index"], dtype=np.float64)
    return truth, predictions, step


def calculate_rmse(prediction: np.ndarray, truth: np.ndarray) -> float:
    return float(np.sqrt(np.mean((prediction - truth) ** 2)))


def calculate_limits(signals: list[np.ndarray], margin_ratio: float = 0.08) -> tuple[float, float]:
    values = np.concatenate([np.asarray(signal, dtype=np.float64).ravel() for signal in signals])
    lower = float(np.min(values))
    upper = float(np.max(values))
    span = upper - lower
    if span <= 1e-12:
        span = max(abs(upper), 1.0)
    margin = margin_ratio * span
    return lower - margin, upper + margin


def configure_axis(axis: plt.Axes) -> None:
    axis.grid(
        True,
        which="major",
        color="#D8D8D8",
        linewidth=0.30,
        linestyle=(0, (1.2, 2.5)),
        alpha=0.72,
    )
    axis.tick_params(
        which="major",
        direction="in",
        colors="#303030",
        pad=1.4,
        length=2.0,
        width=0.45,
    )
    for spine in axis.spines.values():
        spine.set_color("#404040")
        spine.set_linewidth(0.52)


def plot_signals(axis: plt.Axes, x_values: np.ndarray, truth: np.ndarray, predictions: dict[str, np.ndarray], component: int) -> None:
    signals = {
        "Ground truth": truth[:, component],
        **{name: prediction[:, component] for name, prediction in predictions.items()},
    }
    draw_order = ("EDMD", "EDMDDL", "Ground truth", "FS-EDMD")
    for name in draw_order:
        axis.plot(
            x_values,
            signals[name],
            color=COLORS[name],
            linestyle=LINESTYLES[name],
            linewidth=LINEWIDTHS[name],
            label=name,
            alpha=0.96 if name in ("Ground truth", "FS-EDMD") else 0.90,
            zorder=5 if name == "FS-EDMD" else (4 if name == "Ground truth" else 2),
        )


def add_panel_header(axis: plt.Axes, label: str, title: str) -> None:
    axis.text(
        0.012,
        0.945,
        f"{label}  {title}",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=6.5,
        fontweight="semibold",
        color="#202020",
        zorder=30,
        clip_on=False,
        path_effects=[withStroke(linewidth=2.4, foreground="white")],
    )


def plot_figure(
    mechanical_truth: np.ndarray,
    mechanical_predictions: dict[str, np.ndarray],
    mechanical_time: np.ndarray,
    soft_truth: np.ndarray,
    soft_predictions: dict[str, np.ndarray],
    soft_step: np.ndarray,
) -> plt.Figure:
    configure_style()

    fig = plt.figure(figsize=(3.42, 4.55), facecolor="white")
    grid = fig.add_gridspec(
        6,
        1,
        height_ratios=(1.0, 1.0, 1.0, 0.16, 1.0, 1.0),
        left=0.16,
        right=0.985,
        bottom=0.075,
        top=0.925,
        hspace=0.12,
    )
    axes = [
        fig.add_subplot(grid[0, 0]),
        fig.add_subplot(grid[1, 0]),
        fig.add_subplot(grid[2, 0]),
        fig.add_subplot(grid[4, 0]),
        fig.add_subplot(grid[5, 0]),
    ]

    mechanical_components = (0, 2, 4)

    for idx, component in enumerate(mechanical_components):
        axis = axes[idx]
        plot_signals(axis, mechanical_time, mechanical_truth, mechanical_predictions, component)
        configure_axis(axis)
        add_panel_header(axis, PANEL_LABELS[idx], rf"$q_{{{idx + 1}}}$")
        axis.set_xlim(0.0, mechanical_time[-1])
        axis.set_xticks([0.0, 1.0, 2.0, 3.0])
        axis.set_ylim(*calculate_limits([
            mechanical_truth[:, component],
            *[prediction[:, component] for prediction in mechanical_predictions.values()],
        ], margin_ratio=0.07))
        axis.yaxis.set_major_locator(MaxNLocator(nbins=3))
        axis.margins(x=0.0)
        if idx < 2:
            axis.tick_params(labelbottom=False)
        else:
            axis.set_xlabel("Time (s)", labelpad=1.3)

    for soft_idx, component in enumerate((0, 1)):
        panel_idx = 3 + soft_idx
        axis = axes[panel_idx]
        plot_signals(axis, soft_step, soft_truth, soft_predictions, component)
        configure_axis(axis)
        add_panel_header(axis, PANEL_LABELS[panel_idx], r"$x$" if component == 0 else r"$y$")
        axis.set_xlim(float(soft_step[0]), float(soft_step[-1]))
        axis.xaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        axis.set_ylim(*calculate_limits([
            soft_truth[:, component],
            *[prediction[:, component] for prediction in soft_predictions.values()],
        ], margin_ratio=0.07))
        axis.yaxis.set_major_locator(MaxNLocator(nbins=3))
        axis.margins(x=0.0)
        if soft_idx == 0:
            axis.tick_params(labelbottom=False)
        else:
            axis.set_xlabel("Step", labelpad=1.3)

    fig.text(0.035, 0.675, "Joint angle (rad)", rotation=90, ha="center", va="center", fontsize=6.4)
    fig.text(0.035, 0.265, "Position", rotation=90, ha="center", va="center", fontsize=6.4)

    handle_map = {label: handle for handle, label in zip(*axes[0].get_legend_handles_labels())}
    legend_order = ("Ground truth", "FS-EDMD", "EDMDDL", "EDMD")
    fig.legend(
        [handle_map[name] for name in legend_order],
        legend_order,
        loc="upper center",
        bbox_to_anchor=(0.57, 0.987),
        ncol=4,
        frameon=False,
        columnspacing=0.75,
        handlelength=1.55,
        handletextpad=0.32,
        borderaxespad=0.0,
    )
    return fig


def main() -> None:
    mechanical_truth, mechanical_predictions, mechanical_time = load_mechanical_predictions()
    soft_truth, soft_predictions, soft_step = load_soft_predictions()

    figure = plot_figure(
        mechanical_truth,
        mechanical_predictions,
        mechanical_time,
        soft_truth,
        soft_predictions,
        soft_step,
    )

    output_stem = "figure4_modeling_accuracy_singlecol_v5"
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"{output_stem}.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.01,
        )
    plt.close(figure)

    print("Figure 4 single-column v5 generated:")
    print(f"  mechanical RMSE: {calculate_rmse(mechanical_predictions['FS-EDMD'], mechanical_truth):.8f} (FS-EDMD)")
    print(f"  soft trajectory {SOFT_TRAJECTORY_ID} RMSE: {calculate_rmse(soft_predictions['FS-EDMD'], soft_truth):.8f} (FS-EDMD)")
    print(f"  output directory: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
