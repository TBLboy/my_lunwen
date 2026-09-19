"""Generate split modeling figures: robotic arm and soft platform."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from plot_figure2_modeling_accuracy_singlecol_v7 import (
    add_panel_header,
    calculate_limits,
    calculate_rmse,
    configure_axis,
    configure_style,
    load_mechanical_predictions,
    load_soft_predictions,
    plot_signals,
)


LEGEND_ORDER = ("Ground truth", "FS-EDMD", "EDMDDL", "EDMD")


def save_figure(figure: plt.Figure, stem: str) -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"{stem}.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.01,
        )
    plt.close(figure)


def add_shared_legend(figure: plt.Figure, axis: plt.Axes) -> None:
    handle_map = {label: handle for handle, label in zip(*axis.get_legend_handles_labels())}
    figure.legend(
        [handle_map[name] for name in LEGEND_ORDER],
        LEGEND_ORDER,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.985),
        ncol=4,
        frameon=False,
        columnspacing=0.75,
        handlelength=1.55,
        handletextpad=0.32,
        borderaxespad=0.0,
    )


def plot_mechanical_figure(
    mechanical_truth: np.ndarray,
    mechanical_predictions: dict[str, np.ndarray],
    mechanical_time: np.ndarray,
) -> plt.Figure:
    configure_style()
    fig = plt.figure(figsize=(3.42, 2.30), facecolor="white")
    grid = fig.add_gridspec(
        3,
        1,
        left=0.165,
        right=0.985,
        bottom=0.165,
        top=0.93,
        hspace=0.16,
    )
    axes = [fig.add_subplot(grid[idx, 0]) for idx in range(3)]

    for idx, component in enumerate((0, 2, 4)):
        axis = axes[idx]
        plot_signals(
            axis,
            mechanical_time,
            mechanical_truth,
            mechanical_predictions,
            component,
        )
        configure_axis(axis)
        add_panel_header(axis, rf"$q_{{{idx + 1}}}$")
        axis.set_xlim(0.0, mechanical_time[-1])
        axis.set_xticks([0.0, 1.0, 2.0, 3.0])
        axis.set_ylim(
            *calculate_limits(
                [
                    mechanical_truth[:, component],
                    *[
                        prediction[:, component]
                        for prediction in mechanical_predictions.values()
                    ],
                ],
                margin_ratio=0.07,
            )
        )
        axis.yaxis.set_major_locator(MaxNLocator(nbins=3))
        axis.margins(x=0.0)
        if idx < 2:
            axis.tick_params(labelbottom=False)
        else:
            axis.set_xlabel("Time (s)", labelpad=1.3)

    axes[0].set_ylabel("Joint angle (rad)", labelpad=1.2)
    add_shared_legend(fig, axes[0])
    return fig


def plot_soft_figure(
    soft_truth: np.ndarray,
    soft_predictions: dict[str, np.ndarray],
    soft_step: np.ndarray,
) -> plt.Figure:
    configure_style()
    fig = plt.figure(figsize=(3.42, 1.85), facecolor="white")
    grid = fig.add_gridspec(
        2,
        1,
        left=0.165,
        right=0.985,
        bottom=0.215,
        top=0.92,
        hspace=0.16,
    )
    axes = [fig.add_subplot(grid[idx, 0]) for idx in range(2)]

    for soft_idx, component in enumerate((0, 1)):
        axis = axes[soft_idx]
        plot_signals(axis, soft_step, soft_truth, soft_predictions, component)
        configure_axis(axis)
        add_panel_header(axis, r"$x$" if component == 0 else r"$y$")
        axis.set_xlim(float(soft_step[0]), float(soft_step[-1]))
        axis.xaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        axis.set_ylim(
            *calculate_limits(
                [
                    soft_truth[:, component],
                    *[
                        prediction[:, component]
                        for prediction in soft_predictions.values()
                    ],
                ],
                margin_ratio=0.07,
            )
        )
        axis.yaxis.set_major_locator(MaxNLocator(nbins=3))
        axis.margins(x=0.0)
        if soft_idx == 0:
            axis.tick_params(labelbottom=False)
        else:
            axis.set_xlabel("Step", labelpad=1.3)

    axes[0].set_ylabel("Position", labelpad=1.2)
    add_shared_legend(fig, axes[0])
    return fig


def main() -> None:
    mechanical_truth, mechanical_predictions, mechanical_time = load_mechanical_predictions()
    soft_truth, soft_predictions, soft_step = load_soft_predictions()

    mechanical_figure = plot_mechanical_figure(
        mechanical_truth,
        mechanical_predictions,
        mechanical_time,
    )
    save_figure(mechanical_figure, "figure4_robotic_modeling")

    soft_figure = plot_soft_figure(soft_truth, soft_predictions, soft_step)
    save_figure(soft_figure, "figure5_soft_modeling")

    print("Split modeling figures generated.")
    for name, prediction in mechanical_predictions.items():
        print(f"  arm {name}: RMSE={calculate_rmse(prediction, mechanical_truth):.8f}")
    for name, prediction in soft_predictions.items():
        print(f"  soft trajectory 66 {name}: RMSE={calculate_rmse(prediction, soft_truth):.8f}")


if __name__ == "__main__":
    main()
