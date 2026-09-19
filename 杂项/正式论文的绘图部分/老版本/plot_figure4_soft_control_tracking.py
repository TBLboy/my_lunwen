"""Generate the compact soft-platform control comparison figure."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = (
    PROJECT_ROOT
    / "数据备份"
    / "软体平台"
    / "软体机械臂轨迹跟踪数据"
)

EVALUATION_START_STEP = 30

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
    "Reference": 1.35,
    "FS-EDMD-LQR": 0.95,
    "PID": 1.0,
}

TASKS = (
    ("figure_eight", "8字-FS.zip", "8字-PID.csv", "Figure-eight trajectory"),
    ("five_point_star", "五角星-FS.zip", "五角星-PID.zip", "Five-point-star trajectory"),
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


def read_tracking_archive(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing soft-platform tracking data: {path}")

    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            with archive.open("tracking_data.csv") as stream:
                data = pd.read_csv(stream)
    else:
        data = pd.read_csv(path, comment="#")

    required = {
        "time",
        "step",
        "valid",
        "ref_x",
        "ref_y",
        "act_x",
        "act_y",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")

    data = data[data["valid"].astype(int) == 1].copy()
    return data.drop_duplicates("step", keep="first").reset_index(drop=True)


def evaluation_window(data: pd.DataFrame) -> pd.DataFrame:
    result = data[data["step"] >= EVALUATION_START_STEP].reset_index(drop=True)
    if result.empty:
        raise ValueError(f"No valid samples after step {EVALUATION_START_STEP}")
    return result


def calculate_metrics(
    actual_x: np.ndarray,
    actual_y: np.ndarray,
    reference_x: np.ndarray,
    reference_y: np.ndarray,
) -> dict[str, float]:
    error_x = np.asarray(actual_x, dtype=np.float64) - np.asarray(
        reference_x, dtype=np.float64
    )
    error_y = np.asarray(actual_y, dtype=np.float64) - np.asarray(
        reference_y, dtype=np.float64
    )
    distance = np.sqrt(error_x**2 + error_y**2)
    return {
        "rmse": float(np.sqrt(np.mean(distance**2))),
        "mae": float(np.mean(distance)),
        "x_rmse": float(np.sqrt(np.mean(error_x**2))),
        "y_rmse": float(np.sqrt(np.mean(error_y**2))),
    }


def calculate_tracking_error(data: pd.DataFrame) -> np.ndarray:
    return np.sqrt(
        (data["act_x"].to_numpy(dtype=np.float64) - data["ref_x"].to_numpy(dtype=np.float64))
        ** 2
        + (
            data["act_y"].to_numpy(dtype=np.float64)
            - data["ref_y"].to_numpy(dtype=np.float64)
        )
        ** 2
    )


def load_task_data() -> dict[str, dict[str, dict[str, pd.DataFrame]]]:
    task_data: dict[str, dict[str, dict[str, pd.DataFrame]]] = {}
    for task_name, fs_name, pid_name, _title in TASKS:
        task_data[task_name] = {
            "FS-EDMD-LQR": {
                "full": read_tracking_archive(DATA_DIR / fs_name),
            },
            "PID": {
                "full": read_tracking_archive(DATA_DIR / pid_name),
            },
        }
        for controller_data in task_data[task_name].values():
            controller_data["evaluation"] = evaluation_window(
                controller_data["full"]
            )
    return task_data


def calculate_shared_limits(
    task_data: dict[str, dict[str, dict[str, pd.DataFrame]]],
) -> tuple[tuple[float, float], tuple[float, float]]:
    x_values = []
    y_values = []
    for controllers in task_data.values():
        for controller_data in controllers.values():
            full = controller_data["full"]
            x_values.extend(full["ref_x"].to_numpy(dtype=np.float64))
            x_values.extend(full["act_x"].to_numpy(dtype=np.float64))
            y_values.extend(full["ref_y"].to_numpy(dtype=np.float64))
            y_values.extend(full["act_y"].to_numpy(dtype=np.float64))

    x_min, x_max = float(np.min(x_values)), float(np.max(x_values))
    y_min, y_max = float(np.min(y_values)), float(np.max(y_values))
    x_span = x_max - x_min
    y_span = y_max - y_min
    margin = 0.07 * max(x_span, y_span)

    x_center = 0.5 * (x_min + x_max)
    y_center = 0.5 * (y_min + y_max)
    half_span = 0.5 * max(x_span, y_span) + margin
    return (
        (x_center - half_span, x_center + half_span),
        (y_center - half_span, y_center + half_span),
    )


def configure_axis(
    axis: plt.Axes,
    x_limits: tuple[float, float],
    y_limits: tuple[float, float],
) -> None:
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlim(*x_limits)
    axis.set_ylim(*y_limits)
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
    axis.xaxis.set_major_formatter(FormatStrFormatter("%.0f"))
    axis.yaxis.set_major_formatter(FormatStrFormatter("%.0f"))
    for spine in axis.spines.values():
        spine.set_color("#333333")
        spine.set_linewidth(0.65)


def plot_controller_trajectory(
    axis: plt.Axes,
    data: pd.DataFrame,
    name: str,
    show_label: bool,
) -> None:
    axis.plot(
        data["act_x"],
        data["act_y"],
        color=COLORS[name],
        linestyle=LINESTYLES[name],
        linewidth=LINEWIDTHS[name],
        label=name if show_label else "_nolegend_",
        alpha=0.95,
        zorder=5 if name == "FS-EDMD-LQR" else 4,
    )


def plot_tracking_error(
    axis: plt.Axes,
    data: pd.DataFrame,
    name: str,
) -> None:
    elapsed_time = data["time"].to_numpy(dtype=np.float64) - float(data["time"].iloc[0])
    error = calculate_tracking_error(data)
    axis.fill_between(
        elapsed_time,
        error,
        color=COLORS[name],
        alpha=0.10 if name == "FS-EDMD-LQR" else 0.07,
        linewidth=0.0,
        zorder=1,
    )
    axis.plot(
        elapsed_time,
        error,
        color=COLORS[name],
        linestyle=LINESTYLES[name],
        linewidth=LINEWIDTHS[name],
        label="_nolegend_",
        alpha=0.95,
    )


def plot_figure(
    task_data: dict[str, dict[str, dict[str, pd.DataFrame]]],
) -> plt.Figure:
    configure_style()
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(7.16, 4.55),
        facecolor="white",
        gridspec_kw={"height_ratios": (1.28, 0.92)},
    )
    x_limits, y_limits = calculate_shared_limits(task_data)
    trajectory_axes = axes[0]
    error_axes = axes[1]

    for index, (task_name, _fs_name, _pid_name, title) in enumerate(TASKS):
        axis = trajectory_axes[index]
        reference = task_data[task_name]["FS-EDMD-LQR"]["full"]
        axis.plot(
            reference["ref_x"],
            reference["ref_y"],
            color=COLORS["Reference"],
            linestyle=LINESTYLES["Reference"],
            linewidth=LINEWIDTHS["Reference"],
            label="Reference",
            zorder=3,
        )
        plot_controller_trajectory(
            axis,
            task_data[task_name]["FS-EDMD-LQR"]["full"],
            "FS-EDMD-LQR",
            show_label=True,
        )
        plot_controller_trajectory(
            axis,
            task_data[task_name]["PID"]["full"],
            "PID",
            show_label=True,
        )

        configure_axis(axis, x_limits, y_limits)
        axis.text(
            0.018,
            0.94,
            f"({chr(ord('a') + index)})",
            transform=axis.transAxes,
            ha="left",
            va="top",
            fontsize=7.4,
            fontweight="semibold",
            color="#222222",
            zorder=10,
        )
        axis.set_xlabel("$x$ position", labelpad=2.0)
        if index == 0:
            axis.set_ylabel("$y$ position", labelpad=2.0)

        error_axis = error_axes[index]
        plot_tracking_error(
            error_axis,
            task_data[task_name]["FS-EDMD-LQR"]["evaluation"],
            "FS-EDMD-LQR",
        )
        plot_tracking_error(
            error_axis,
            task_data[task_name]["PID"]["evaluation"],
            "PID",
        )
        error_axis.text(
            0.018,
            0.94,
            f"({chr(ord('c') + index)})",
            transform=error_axis.transAxes,
            ha="left",
            va="top",
            fontsize=7.4,
            fontweight="semibold",
            color="#222222",
            zorder=10,
        )
        error_axis.set_xlabel("Time (s)", labelpad=2.0)
        error_axis.set_ylabel("$e(t)$" if index == 0 else "", labelpad=2.0)
        error_axis.grid(
            True,
            color="#D7D7D7",
            linewidth=0.36,
            linestyle=(0, (1.0, 2.6)),
            alpha=0.70,
        )
        error_axis.minorticks_on()
        error_axis.tick_params(
            which="major",
            direction="in",
            colors="#333333",
            pad=1.8,
            length=2.3,
            width=0.55,
        )
        error_axis.tick_params(
            which="minor",
            direction="in",
            colors="#666666",
            length=1.2,
            width=0.42,
        )
        for spine in error_axis.spines.values():
            spine.set_color("#333333")
            spine.set_linewidth(0.65)

        error_axis.set_xlim(
            0.0,
            float(
                task_data[task_name]["FS-EDMD-LQR"]["evaluation"]["time"].iloc[-1]
                - task_data[task_name]["FS-EDMD-LQR"]["evaluation"]["time"].iloc[0]
            ),
        )
        error_axis.margins(x=0.0, y=0.08)

    for column, title in enumerate([task[3] for task in TASKS]):
        trajectory_axes[column].set_title(title, loc="center", pad=4.5)

    handles, labels = trajectory_axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.997),
        ncol=3,
        frameon=False,
        columnspacing=1.5,
        handlelength=1.9,
        handletextpad=0.45,
        borderaxespad=0.0,
    )
    figure.subplots_adjust(
        left=0.082,
        right=0.992,
        bottom=0.085,
        top=0.875,
        wspace=0.18,
        hspace=0.38,
    )

    for row, row_label in enumerate(("Trajectory", "Tracking error")):
        position = axes[row, 0].get_position()
        figure.text(
            0.012,
            0.5 * (position.y0 + position.y1),
            row_label,
            rotation=90,
            ha="center",
            va="center",
            fontsize=7.4,
            fontweight="semibold",
            color="#222222",
        )
    return figure


def build_metrics(
    task_data: dict[str, dict[str, dict[str, pd.DataFrame]]],
) -> dict[str, object]:
    metrics: dict[str, object] = {
        "evaluation_start_step": EVALUATION_START_STEP,
        "error_definition": "sqrt((act_x-ref_x)^2 + (act_y-ref_y)^2)",
        "tasks": {},
    }
    for task_name, controllers in task_data.items():
        reference = controllers["FS-EDMD-LQR"]["evaluation"]
        task_metrics: dict[str, object] = {
            "samples": int(len(reference)),
            "start_time_s": float(reference["time"].iloc[0]),
            "end_time_s": float(reference["time"].iloc[-1]),
            "controllers": {},
        }
        for controller_name, controller_data in controllers.items():
            data = controller_data["evaluation"]
            task_metrics["controllers"][controller_name] = calculate_metrics(
                data["act_x"],
                data["act_y"],
                data["ref_x"],
                data["ref_y"],
            )

        fs_metrics = task_metrics["controllers"]["FS-EDMD-LQR"]
        pid_metrics = task_metrics["controllers"]["PID"]
        task_metrics["fs_over_pid"] = {
            "rmse_reduction_percent": float(
                100.0 * (pid_metrics["rmse"] - fs_metrics["rmse"]) / pid_metrics["rmse"]
            ),
            "mae_reduction_percent": float(
                100.0 * (pid_metrics["mae"] - fs_metrics["mae"]) / pid_metrics["mae"]
            ),
        }
        metrics["tasks"][task_name] = task_metrics
    return metrics


def main() -> None:
    task_data = load_task_data()
    metrics = build_metrics(task_data)
    figure = plot_figure(task_data)

    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"figure4_soft_control_tracking.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.015,
        )
    plt.close(figure)

    metrics_path = SCRIPT_DIR / "figure4_soft_control_metrics.json"
    metrics_path.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Figure 4 generated.")
    for task_name, values in metrics["tasks"].items():
        print(task_name)
        for controller, controller_metrics in values["controllers"].items():
            print(
                f"  {controller}: RMSE={controller_metrics['rmse']:.8f}, "
                f"MAE={controller_metrics['mae']:.8f}"
            )
        print(
            "  FS over PID: "
            f"RMSE={values['fs_over_pid']['rmse_reduction_percent']:.2f}%, "
            f"MAE={values['fs_over_pid']['mae_reduction_percent']:.2f}%"
        )
    print(f"Metrics: {metrics_path}")
    print(f"Output directory: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
