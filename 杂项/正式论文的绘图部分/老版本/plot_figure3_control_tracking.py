"""Generate the compact robotic-arm tracking comparison figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import scipy.io as sio


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "数据备份" / "机械臂数据" / "轨迹跟踪数据"

EVALUATION_START_S = 10.0
EVALUATION_END_S = 40.0
POSITION_INDICES = (0, 2, 4)

COLORS = {
    "Reference": "#202020",
    "FS-EDMD-LQR": "#C23B4A",
    "PID": "#2F6F8F",
}
LINESTYLES = {
    "Reference": "-",
    "FS-EDMD-LQR": "-",
    "PID": "--",
}
LINEWIDTHS = {
    "Reference": 1.25,
    "FS-EDMD-LQR": 0.98,
    "PID": 0.95,
}

TASKS = (
    ("sinusoidal", "my_data_1", "Sinusoidal", True),
    ("irregular", "my_data_3", "Irregular", True),
    ("disturbance", "my_data_2", "Disturbance recovery", False),
)


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 7.4,
            "axes.labelsize": 7.3,
            "axes.titlesize": 7.4,
            "axes.titleweight": "semibold",
            "axes.edgecolor": "#333333",
            "axes.axisbelow": True,
            "xtick.labelsize": 6.7,
            "ytick.labelsize": 6.7,
            "legend.fontsize": 7.4,
            "axes.linewidth": 0.65,
            "xtick.major.width": 0.55,
            "ytick.major.width": 0.55,
            "xtick.minor.width": 0.42,
            "ytick.minor.width": 0.42,
            "xtick.major.size": 2.3,
            "ytick.major.size": 2.3,
            "xtick.minor.size": 1.2,
            "ytick.minor.size": 1.2,
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
    pid = (
        np.asarray(raw["q_pid"], dtype=np.float64)
        if "q_pid" in raw.dtype.names
        else None
    )

    mask = (time >= EVALUATION_START_S) & (time <= EVALUATION_END_S)
    if not np.any(mask):
        raise ValueError(
            f"No samples in [{EVALUATION_START_S}, {EVALUATION_END_S}] "
            f"for {path.name}"
        )

    position_indices = (
        POSITION_INDICES if reference.shape[1] == 6 else (0, 1, 2)
    )
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
    error = np.asarray(tracking, dtype=np.float64) - np.asarray(
        reference, dtype=np.float64
    )
    return {
        "rmse": float(np.sqrt(np.mean(error**2))),
        "mae": float(np.mean(np.abs(error))),
    }


def build_metrics(
    task_data: dict[str, dict[str, np.ndarray]],
) -> dict[str, object]:
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
                task_metrics[controller] = calculate_metrics(
                    data[controller],
                    data["Reference"],
                )
        metrics["tasks"][task_name] = task_metrics
    return metrics


def configure_axis(axis: plt.Axes) -> None:
    axis.grid(
        True,
        color="#D7D7D7",
        linewidth=0.36,
        linestyle=(0, (1.0, 2.6)),
        alpha=0.70,
    )
    axis.minorticks_on()
    axis.tick_params(
        which="major",
        direction="in",
        colors="#333333",
        pad=1.8,
        length=2.3,
        width=0.55,
    )
    axis.tick_params(
        which="minor",
        direction="in",
        colors="#666666",
        length=1.2,
        width=0.42,
    )
    axis.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    for spine in axis.spines.values():
        spine.set_color("#333333")
        spine.set_linewidth(0.65)


def plot_signal(
    axis: plt.Axes,
    data: dict[str, np.ndarray],
    component: int,
    show_pid: bool,
) -> None:
    names = ["Reference", "FS-EDMD-LQR"]
    if show_pid and "PID" in data:
        names.append("PID")

    values = {name: data[name][:, component] for name in names}
    order = ["Reference", "FS-EDMD-LQR"] + (["PID"] if show_pid else [])
    for name in order:
        axis.plot(
            data["time"],
            values[name],
            color=COLORS[name],
            linestyle=LINESTYLES[name],
            linewidth=LINEWIDTHS[name],
            label=name,
            alpha=1.0 if name == "Reference" else 0.92,
            zorder=4 if name == "Reference" else 3,
        )


def determine_ylimits(
    task_data: dict[str, dict[str, np.ndarray]],
    component: int,
) -> tuple[float, float]:
    values = []
    for data in task_data.values():
        for name in ("Reference", "FS-EDMD-LQR", "PID"):
            if name in data:
                values.append(data[name][:, component])
    flattened = np.concatenate(values)
    lower = float(np.min(flattened))
    upper = float(np.max(flattened))
    span = upper - lower
    if span <= 1e-12:
        span = max(abs(upper), 1.0)
    margin = 0.06 * span
    return lower - margin, upper + margin


def plot_figure(
    task_data: dict[str, dict[str, np.ndarray]],
) -> plt.Figure:
    configure_style()
    figure, axes = plt.subplots(
        3,
        3,
        figsize=(7.16, 4.62),
        sharex="col",
        sharey="col",
        facecolor="white",
    )

    panel_letters = (
        ("(a)", "(b)", "(c)"),
        ("(d)", "(e)", "(f)"),
        ("(g)", "(h)", "(i)"),
    )
    joint_labels = ("Joint 1 (rad)", "Joint 2 (rad)", "Joint 3 (rad)")
    column_limits = [
        determine_ylimits(task_data, component=column) for column in range(3)
    ]

    for row, (task_name, _stem, _task_title, show_pid) in enumerate(TASKS):
        data = task_data[task_name]
        for column in range(3):
            axis = axes[row, column]
            plot_signal(axis, data, component=column, show_pid=show_pid)
            configure_axis(axis)
            axis.set_xlim(0.0, EVALUATION_END_S - EVALUATION_START_S)
            axis.set_xticks(np.arange(0.0, 31.0, 5.0))
            axis.set_ylim(*column_limits[column])

            axis.text(
                0.018,
                0.94,
                panel_letters[row][column],
                transform=axis.transAxes,
                ha="left",
                va="top",
                fontsize=7.4,
                fontweight="semibold",
                color="#222222",
                zorder=10,
            )

            if column == 0:
                axis.set_ylabel(joint_labels[column], labelpad=2.0)
            if row == len(TASKS) - 1:
                axis.set_xlabel("Time (s)", labelpad=2.0)

    for column in range(3):
        axes[0, column].set_title(
            f"Joint {column + 1}",
            loc="center",
            pad=4.5,
        )

    handles, labels = axes[0, 0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.995),
        ncol=3,
        frameon=False,
        columnspacing=1.4,
        handlelength=1.9,
        handletextpad=0.45,
        borderaxespad=0.0,
    )
    figure.subplots_adjust(
        left=0.075,
        right=0.992,
        bottom=0.095,
        top=0.885,
        wspace=0.18,
        hspace=0.27,
    )

    for row, (_task_name, _stem, task_title, _show_pid) in enumerate(TASKS):
        position = axes[row, 0].get_position()
        figure.text(
            0.012,
            0.5 * (position.y0 + position.y1),
            task_title,
            rotation=90,
            ha="center",
            va="center",
            fontsize=7.4,
            fontweight="semibold",
            color="#222222",
        )
    return figure


def main() -> None:
    task_data = {
        task_name: load_tracking_data(stem)
        for task_name, stem, _title, _show_pid in TASKS
    }
    metrics = build_metrics(task_data)
    figure = plot_figure(task_data)

    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"figure3_control_tracking.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.015,
        )
    plt.close(figure)

    metrics_path = SCRIPT_DIR / "figure3_control_metrics.json"
    metrics_path.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Figure 3 generated.")
    for task_name, values in metrics["tasks"].items():
        print(task_name)
        for controller, controller_metrics in values.items():
            print(
                f"  {controller}: RMSE={controller_metrics['rmse']:.8f}, "
                f"MAE={controller_metrics['mae']:.8f}"
            )
    print(f"Metrics: {metrics_path}")
    print(f"Output directory: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
