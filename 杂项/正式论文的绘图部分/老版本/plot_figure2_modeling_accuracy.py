"""Generate the compact two-platform modeling-accuracy figure for the paper."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
MODELING_ROOT = PROJECT_ROOT / "建模代码"
SOFT_FINAL_ROOT = (
    PROJECT_ROOT / "杂项" / "软体平台探索实验结果" / "final"
)

if str(MODELING_ROOT) not in sys.path:
    sys.path.insert(0, str(MODELING_ROOT))

from modeling.data_io import denormalize, load_meta, load_test_data
from modeling.soft_data import (
    denormalize_x,
    iter_trajectories,
    load_processed_meta,
    load_processed_split,
)
from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import OursKoopmanTrainer


MECHANICAL_STEPS = 800
SOFT_TRAJECTORY_ID = 66
SAMPLE_PERIOD_S = 0.004

COLORS = {
    "Ground Truth": "#111111",
    "FS-EDMD": "#D62728",
    "EDMDDL": "#2CA02C",
    "EDMD": "#2471A3",
}
LINESTYLES = {
    "Ground Truth": "-",
    "FS-EDMD": "-",
    "EDMDDL": "--",
    "EDMD": "-.",
}
LINEWIDTHS = {
    "Ground Truth": 1.35,
    "FS-EDMD": 1.05,
    "EDMDDL": 0.95,
    "EDMD": 0.95,
}
LINE_ORDER = ("Ground Truth", "FS-EDMD", "EDMDDL", "EDMD")


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 7.5,
            "axes.labelsize": 7.5,
            "axes.titlesize": 8.0,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.8,
            "legend.fontsize": 7.4,
            "axes.linewidth": 0.65,
            "xtick.major.width": 0.55,
            "ytick.major.width": 0.55,
            "xtick.major.size": 2.2,
            "ytick.major.size": 2.2,
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
        "EDMD": EDMDTrainer().load(
            MODELING_ROOT / "models" / "edmd_model.pkl"
        ),
    }

    predictions = {}
    for name, model in models.items():
        prediction = model.predict(
            x_test[0],
            u_test,
            steps=MECHANICAL_STEPS,
        )
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
        "FS-EDMD": OursKoopmanTrainer(device="cpu", verbose=False).load(
            models_dir / "fs_edmd.pkl"
        ),
        "EDMDDL": EDMDDLTrainer(device="cpu").load(
            models_dir / "edmd_dl.pkl",
            device="cpu",
        ),
        "EDMD": EDMDTrainer().load(models_dir / "edmd.pkl"),
    }

    predictions = {}
    for name, model in models.items():
        prediction = model.predict(
            trajectory["X"][0],
            trajectory["U"],
            steps=len(trajectory["U"]),
        )
        predictions[name] = denormalize_x(prediction, meta)

    step = np.asarray(trajectory["step_index"], dtype=np.float64)
    return truth, predictions, step


def configure_axis(axis: plt.Axes) -> None:
    axis.grid(True, color="#D9D9D9", linewidth=0.42, alpha=0.65)
    axis.tick_params(direction="in", pad=2.0, length=2.2, width=0.55)
    for spine in axis.spines.values():
        spine.set_linewidth(0.65)


def plot_signals(
    axis: plt.Axes,
    x_values: np.ndarray,
    truth: np.ndarray,
    predictions: dict[str, np.ndarray],
    component: int,
) -> None:
    signals = {
        "Ground Truth": truth[:, component],
        **{
            name: prediction[:, component]
            for name, prediction in predictions.items()
        },
    }
    for name in LINE_ORDER:
        axis.plot(
            x_values,
            signals[name],
            color=COLORS[name],
            linestyle=LINESTYLES[name],
            linewidth=LINEWIDTHS[name],
            label=name,
            alpha=0.96 if name == "Ground Truth" else 0.92,
            zorder=5 if name == "Ground Truth" else 3,
        )


def format_component_axis(
    axis: plt.Axes,
    *,
    title: str,
    ylabel: str | None = None,
    show_xlabels: bool,
    xlabel: str | None = None,
) -> None:
    configure_axis(axis)
    axis.set_title(title, loc="left", pad=2.4, fontweight="normal")
    if ylabel:
        axis.set_ylabel(ylabel, labelpad=2.5)
    if xlabel:
        axis.set_xlabel(xlabel, labelpad=2.0)
    if not show_xlabels:
        axis.tick_params(labelbottom=False)


def plot_figure(
    mechanical_truth: np.ndarray,
    mechanical_predictions: dict[str, np.ndarray],
    mechanical_time: np.ndarray,
    soft_truth: np.ndarray,
    soft_predictions: dict[str, np.ndarray],
    soft_step: np.ndarray,
) -> plt.Figure:
    configure_style()
    fig = plt.figure(figsize=(7.16, 3.62), facecolor="white")
    grid = fig.add_gridspec(
        6,
        2,
        left=0.083,
        right=0.988,
        bottom=0.115,
        top=0.885,
        wspace=0.30,
        hspace=0.38,
    )

    mechanical_axes = [
        fig.add_subplot(grid[0:2, 0]),
        fig.add_subplot(grid[2:4, 0]),
        fig.add_subplot(grid[4:6, 0]),
    ]
    soft_axes = [
        fig.add_subplot(grid[0:3, 1]),
        fig.add_subplot(grid[3:6, 1]),
    ]

    panel_labels = ("(a)", "(b)", "(c)", "(d)", "(e)")
    mechanical_titles = ("Joint 1", "Joint 2", "Joint 3")
    for index, axis in enumerate(mechanical_axes):
        plot_signals(
            axis,
            mechanical_time,
            mechanical_truth,
            mechanical_predictions,
            component=2 * index,
        )
        format_component_axis(
            axis,
            title=f"{panel_labels[index]} {mechanical_titles[index]}",
            ylabel="Joint angle (rad)" if index == 0 else None,
            show_xlabels=index == len(mechanical_axes) - 1,
            xlabel="Time (s)" if index == len(mechanical_axes) - 1 else None,
        )
        axis.set_xlim(0.0, mechanical_time[-1])

    soft_titles = ("Soft platform x", "Soft platform y")
    for index, axis in enumerate(soft_axes):
        plot_signals(
            axis,
            soft_step,
            soft_truth,
            soft_predictions,
            component=index,
        )
        format_component_axis(
            axis,
            title=f"{panel_labels[index + 3]} {soft_titles[index]}",
            ylabel="Position" if index == 0 else None,
            show_xlabels=index == len(soft_axes) - 1,
            xlabel="Step" if index == len(soft_axes) - 1 else None,
        )
        axis.set_xlim(soft_step[0], soft_step[-1])

    handles, labels = mechanical_axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.988),
        ncol=4,
        frameon=False,
        columnspacing=1.25,
        handlelength=1.85,
        handletextpad=0.42,
        borderaxespad=0.0,
    )
    return fig


def calculate_rmse(prediction: np.ndarray, truth: np.ndarray) -> float:
    return float(np.sqrt(np.mean((prediction - truth) ** 2)))


def main() -> None:
    mechanical_truth, mechanical_predictions, mechanical_time = (
        load_mechanical_predictions()
    )
    soft_truth, soft_predictions, soft_step = load_soft_predictions()

    figure = plot_figure(
        mechanical_truth,
        mechanical_predictions,
        mechanical_time,
        soft_truth,
        soft_predictions,
        soft_step,
    )

    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"figure2_modeling_accuracy.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.015,
        )
    plt.close(figure)

    print("Figure 2 generated:")
    print(f"  mechanical RMSE: {calculate_rmse(mechanical_predictions['FS-EDMD'], mechanical_truth):.8f} (FS-EDMD)")
    print(f"  soft trajectory {SOFT_TRAJECTORY_ID} RMSE: {calculate_rmse(soft_predictions['FS-EDMD'], soft_truth):.8f} (FS-EDMD)")
    print(f"  output directory: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
