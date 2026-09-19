"""Generate an improved single-column Figure 5 for robotic-arm tracking."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from matplotlib.ticker import MaxNLocator
import numpy as np
import scipy.io as sio

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "数据备份" / "机械臂数据" / "轨迹跟踪数据"

EVALUATION_START_S = 10.0
EVALUATION_END_S = 40.0
POSITION_INDICES = (0, 2, 4)

COLORS = {
    "Reference": "#1F1F1F",
    "FS-EDMD-LQR": "#C44E52",
    "PID": "#4C78A8",
}
LINESTYLES = {
    "Reference": "-",
    "FS-EDMD-LQR": "-",
    "PID": "--",
}
LINEWIDTHS = {
    "Reference": 0.95,
    "FS-EDMD-LQR": 1.12,
    "PID": 0.88,
}

TASKS = (
    ("sinusoidal", "my_data_1", "Sinusoidal", True),
    ("irregular", "my_data_3", "Irregular", True),
    ("disturbance", "my_data_2", "Disturbance", False),
)


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 6.4,
            "axes.labelsize": 6.5,
            "axes.titlesize": 6.6,
            "xtick.labelsize": 5.9,
            "ytick.labelsize": 5.9,
            "legend.fontsize": 6.0,
            "axes.linewidth": 0.50,
            "axes.edgecolor": "#4A4A4A",
            "xtick.major.width": 0.45,
            "ytick.major.width": 0.45,
            "xtick.major.size": 1.9,
            "ytick.major.size": 1.9,
            "axes.axisbelow": True,
            "lines.solid_capstyle": "round",
            "lines.dash_capstyle": "round",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "stix",
        }
    )


def load_tracking_data(stem: str) -> dict[str, np.ndarray]:
    path = DATA_DIR / f"{stem}.mat"
    if not path.exists():
        raise FileNotFoundError(f"Missing mechanical tracking data: {path}")

    raw = sio.loadmat(path)[stem][0, 0]
    time = np.asarray(raw["t"], dtype=np.float64).reshape(-1)
    reference = np.asarray(raw["q_ref"], dtype=np.float64)
    tracking = np.asarray(raw["q"], dtype=np.float64)
    pid = np.asarray(raw["q_pid"], dtype=np.float64) if "q_pid" in raw.dtype.names else None

    mask = (time >= EVALUATION_START_S) & (time <= EVALUATION_END_S)
    if not np.any(mask):
        raise ValueError(f"No samples in [{EVALUATION_START_S}, {EVALUATION_END_S}] for {path.name}")

    position_indices = POSITION_INDICES if reference.shape[1] == 6 else (0, 1, 2)
    reference = reference[mask][:, position_indices]
    tracking = tracking[mask][:, position_indices]
    relative_time = time[mask] - time[mask][0]

    result = {
        "time": relative_time,
        "Reference": reference,
        "FS-EDMD-LQR": tracking,
    }
    if pid is not None:
        result["PID"] = pid[mask][:, position_indices]
    return result


def calculate_metrics(tracking: np.ndarray, reference: np.ndarray) -> dict[str, float]:
    error = np.asarray(tracking, dtype=np.float64) - np.asarray(reference, dtype=np.float64)
    return {
        "rmse": float(np.sqrt(np.mean(error**2))),
        "mae": float(np.mean(np.abs(error))),
    }


def build_metrics(task_data: dict[str, dict[str, np.ndarray]]) -> dict[str, object]:
    metrics: dict[str, object] = {
        "evaluation_window_raw_s": [EVALUATION_START_S, EVALUATION_END_S],
        "plot_window_s": [0.0, EVALUATION_END_S - EVALUATION_START_S],
        "joints": [1, 2, 3],
        "tasks": {},
    }
    for task_name, data in task_data.items():
        task_metrics: dict[str, dict[str, float]] = {}
        for controller in ("FS-EDMD-LQR", "PID"):
            if controller in data:
                task_metrics[controller] = calculate_metrics(data[controller], data["Reference"])
        metrics["tasks"][task_name] = task_metrics
    return metrics


def determine_ylimits(task_data: dict[str, dict[str, np.ndarray]], component: int) -> tuple[float, float]:
    values = []
    for data in task_data.values():
        for name in ("Reference", "FS-EDMD-LQR", "PID"):
            if name in data:
                values.append(data[name][:, component])
    flattened = np.concatenate(values)
    lower, upper = float(np.min(flattened)), float(np.max(flattened))
    span = upper - lower
    if span <= 1e-12:
        span = max(abs(upper), 1.0)
    margin = 0.04 * span
    return lower - margin, upper + margin


def configure_axis(axis: plt.Axes) -> None:
    axis.grid(
        True,
        which="major",
        color="#DEDEDE",
        linewidth=0.24,
        linestyle=(0, (1.0, 2.6)),
        alpha=0.85,
    )
    axis.tick_params(
        which="major",
        direction="in",
        colors="#303030",
        pad=1.0,
        length=1.7,
        width=0.40,
    )
    for spine in axis.spines.values():
        spine.set_color("#4A4A4A")
        spine.set_linewidth(0.42)


def plot_signal(axis: plt.Axes, data: dict[str, np.ndarray], component: int, show_pid: bool) -> None:
    order = ["PID", "Reference", "FS-EDMD-LQR"] if show_pid and "PID" in data else ["Reference", "FS-EDMD-LQR"]
    for name in order:
        axis.plot(
            data["time"],
            data[name][:, component],
            color=COLORS[name],
            linestyle=LINESTYLES[name],
            linewidth=LINEWIDTHS[name],
            label=name,
            alpha=0.95 if name != "PID" else 0.88,
            zorder=4 if name == "FS-EDMD-LQR" else (3 if name == "Reference" else 2),
        )


def plot_figure(task_data: dict[str, dict[str, np.ndarray]]) -> plt.Figure:
    configure_style()
    fig, axes = plt.subplots(
        3,
        3,
        figsize=(3.42, 3.60),
        sharex="col",
        sharey="col",
        facecolor="white",
    )

    fig.subplots_adjust(
        left=0.105,
        right=0.988,
        bottom=0.090,
        top=0.94,
        wspace=0.14,
        hspace=0.15,
    )

    column_limits = [determine_ylimits(task_data, component=c) for c in range(3)]

    for row, (task_name, _stem, _task_title, show_pid) in enumerate(TASKS):
        data = task_data[task_name]
        for col in range(3):
            ax = axes[row, col]
            plot_signal(ax, data, component=col, show_pid=show_pid)
            configure_axis(ax)
            ax.set_xlim(0.0, EVALUATION_END_S - EVALUATION_START_S)
            ax.set_xticks([0, 10, 20, 30])
            ax.set_ylim(*column_limits[col])
            ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
            if row < 2:
                ax.tick_params(labelbottom=False)

    for col in range(3):
        axes[0, col].set_title(rf"$q_{col + 1}$", pad=2.5, fontweight="normal")

    # compact row labels
    row_labels = ("Sinusoidal", "Irregular", "Disturbance recovery")
    for row, task_title in enumerate(row_labels):
        pos = axes[row, 0].get_position()
        fig.text(
            0.048,
            0.5 * (pos.y0 + pos.y1),
            task_title,
            rotation=90,
            ha="center",
            va="center",
            fontsize=6.0,
            color="#222222",
        )

    # shared labels
    fig.text(0.012, 0.50, "Joint angle (rad)", rotation=90, ha="center", va="center", fontsize=6.5)
    fig.text(0.5, 0.040, "Time (s)", ha="center", va="center", fontsize=6.5)

    handle_map = {label: handle for handle, label in zip(*axes[0, 0].get_legend_handles_labels())}
    legend_order = ("Reference", "FS-EDMD-LQR", "PID")
    fig.legend(
        [handle_map[name] for name in legend_order],
        legend_order,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=3,
        frameon=False,
        columnspacing=0.95,
        handlelength=1.6,
        handletextpad=0.38,
        borderaxespad=0.0,
    )
    return fig


def main() -> None:
    task_data = {task_name: load_tracking_data(stem) for task_name, stem, _title, _show_pid in TASKS}
    metrics = build_metrics(task_data)
    figure = plot_figure(task_data)

    output_stem = "figure5_control_tracking_singlecol_v5"
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"{output_stem}.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.008,
        )
    plt.close(figure)

    metrics_path = SCRIPT_DIR / "figure5_control_metrics_singlecol_v5.json"
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Figure 5 single-column v5 generated.")
    for task_name, values in metrics["tasks"].items():
        print(task_name)
        for controller, controller_metrics in values.items():
            print(f"  {controller}: RMSE={controller_metrics['rmse']:.8f}, MAE={controller_metrics['mae']:.8f}")
    print(f"Metrics: {metrics_path}")
    print(f"Output directory: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
