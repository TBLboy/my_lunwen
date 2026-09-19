"""Generate an improved single-column Figure 6 for soft-platform tracking."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "数据备份" / "软体平台" / "软体机械臂轨迹跟踪数据"

EVALUATION_START_STEP = 30

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
    "Reference": 0.80,
    "FS-EDMD-LQR": 0.80,
    "PID": 0.80,
}

TASKS = (
    ("figure_eight", "8字-FS.zip", "8字-PID.csv", "Figure-eight"),
    ("five_point_star", "五角星-FS.zip", "五角星-PID.zip", "Five-point star"),
)


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 6.3,
            "axes.labelsize": 6.4,
            "axes.titlesize": 6.4,
            "xtick.labelsize": 5.8,
            "ytick.labelsize": 5.8,
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


def read_tracking_archive(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing soft-platform tracking data: {path}")

    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            with archive.open("tracking_data.csv") as stream:
                data = pd.read_csv(stream)
    else:
        data = pd.read_csv(path, comment="#")

    required = {"time", "step", "valid", "ref_x", "ref_y", "act_x", "act_y"}
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


def calculate_metrics(actual_x, actual_y, reference_x, reference_y) -> dict[str, float]:
    error_x = np.asarray(actual_x, dtype=np.float64) - np.asarray(reference_x, dtype=np.float64)
    error_y = np.asarray(actual_y, dtype=np.float64) - np.asarray(reference_y, dtype=np.float64)
    distance = np.sqrt(error_x ** 2 + error_y ** 2)
    return {
        "rmse": float(np.sqrt(np.mean(distance ** 2))),
        "mae": float(np.mean(distance)),
        "x_rmse": float(np.sqrt(np.mean(error_x ** 2))),
        "y_rmse": float(np.sqrt(np.mean(error_y ** 2))),
    }


def calculate_tracking_error(data: pd.DataFrame) -> np.ndarray:
    return np.sqrt(
        (data["act_x"].to_numpy(dtype=np.float64) - data["ref_x"].to_numpy(dtype=np.float64)) ** 2
        + (data["act_y"].to_numpy(dtype=np.float64) - data["ref_y"].to_numpy(dtype=np.float64)) ** 2
    )


def load_task_data() -> dict[str, dict[str, dict[str, pd.DataFrame]]]:
    task_data: dict[str, dict[str, dict[str, pd.DataFrame]]] = {}
    for task_name, fs_name, pid_name, _title in TASKS:
        task_data[task_name] = {
            "FS-EDMD-LQR": {"full": read_tracking_archive(DATA_DIR / fs_name)},
            "PID": {"full": read_tracking_archive(DATA_DIR / pid_name)},
        }
        for controller_data in task_data[task_name].values():
            controller_data["evaluation"] = evaluation_window(controller_data["full"])
    return task_data


def square_limits(x_values: np.ndarray, y_values: np.ndarray, margin_ratio: float = 0.07) -> tuple[tuple[float, float], tuple[float, float]]:
    x_min, x_max = float(np.min(x_values)), float(np.max(x_values))
    y_min, y_max = float(np.min(y_values)), float(np.max(y_values))
    x_span = x_max - x_min
    y_span = y_max - y_min
    span = max(x_span, y_span)
    margin = margin_ratio * span
    x_center = 0.5 * (x_min + x_max)
    y_center = 0.5 * (y_min + y_max)
    half_span = 0.5 * span + margin
    return (x_center - half_span, x_center + half_span), (y_center - half_span, y_center + half_span)


def task_trajectory_limits(controllers: dict[str, dict[str, pd.DataFrame]]) -> tuple[tuple[float, float], tuple[float, float]]:
    xs, ys = [], []
    for controller_data in controllers.values():
        full = controller_data["full"]
        xs.extend(full["ref_x"].to_numpy(dtype=np.float64))
        xs.extend(full["act_x"].to_numpy(dtype=np.float64))
        ys.extend(full["ref_y"].to_numpy(dtype=np.float64))
        ys.extend(full["act_y"].to_numpy(dtype=np.float64))
    return square_limits(np.asarray(xs), np.asarray(ys), margin_ratio=0.06)


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


def plot_controller_trajectory(axis: plt.Axes, data: pd.DataFrame, name: str, show_label: bool) -> None:
    axis.plot(
        data["act_x"],
        data["act_y"],
        color=COLORS[name],
        linestyle=LINESTYLES[name],
        linewidth=LINEWIDTHS[name],
        label=name if show_label else "_nolegend_",
        alpha=0.95 if name != "PID" else 0.88,
        zorder=4 if name == "FS-EDMD-LQR" else 2,
    )


def plot_tracking_error(axis: plt.Axes, data: pd.DataFrame, name: str) -> None:
    elapsed_time = data["time"].to_numpy(dtype=np.float64) - float(data["time"].iloc[0])
    error = calculate_tracking_error(data)
    axis.plot(
        elapsed_time,
        error,
        color=COLORS[name],
        linestyle=LINESTYLES[name],
        linewidth=LINEWIDTHS[name],
        label=name,
        alpha=0.95 if name != "PID" else 0.88,
        zorder=4 if name == "FS-EDMD-LQR" else 2,
    )


def build_metrics(task_data: dict[str, dict[str, dict[str, pd.DataFrame]]]) -> dict[str, object]:
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
                data["act_x"], data["act_y"], data["ref_x"], data["ref_y"]
            )
        fs_metrics = task_metrics["controllers"]["FS-EDMD-LQR"]
        pid_metrics = task_metrics["controllers"]["PID"]
        task_metrics["fs_over_pid"] = {
            "rmse_reduction_percent": float(100.0 * (pid_metrics["rmse"] - fs_metrics["rmse"]) / pid_metrics["rmse"]),
            "mae_reduction_percent": float(100.0 * (pid_metrics["mae"] - fs_metrics["mae"]) / pid_metrics["mae"]),
        }
        metrics["tasks"][task_name] = task_metrics
    return metrics


def plot_figure(task_data: dict[str, dict[str, dict[str, pd.DataFrame]]]) -> plt.Figure:
    configure_style()
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(3.42, 4.00),
        facecolor="white",
        gridspec_kw={"height_ratios": (0.72, 1.0)},
    )
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.085, top=0.94, wspace=0.18, hspace=0.16)

    for col, (task_name, _fs_name, _pid_name, _title) in enumerate(TASKS):
        traj_ax = axes[0, col]
        err_ax = axes[1, col]
        controllers = task_data[task_name]
        ref = controllers["FS-EDMD-LQR"]["full"]

        # trajectory panel
        traj_ax.plot(
            ref["ref_x"],
            ref["ref_y"],
            color=COLORS["Reference"],
            linestyle=LINESTYLES["Reference"],
            linewidth=LINEWIDTHS["Reference"],
            label="Reference",
            zorder=3,
        )
        plot_controller_trajectory(traj_ax, controllers["PID"]["full"], "PID", show_label=True)
        plot_controller_trajectory(traj_ax, controllers["FS-EDMD-LQR"]["full"], "FS-EDMD-LQR", show_label=True)

        x_limits, y_limits = task_trajectory_limits(controllers)
        traj_ax.set_aspect("equal", adjustable="box")
        traj_ax.set_xlim(*x_limits)
        traj_ax.set_ylim(*y_limits)
        configure_axis(traj_ax)
        traj_ax.xaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        traj_ax.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        traj_ax.set_xlabel(r"$x$", labelpad=1.0)
        if col == 0:
            traj_ax.set_ylabel(r"$y$", labelpad=1.0)

        # error panel
        plot_tracking_error(err_ax, controllers["PID"]["evaluation"], "PID")
        plot_tracking_error(err_ax, controllers["FS-EDMD-LQR"]["evaluation"], "FS-EDMD-LQR")
        configure_axis(err_ax)
        err_ax.set_xlim(0.0, float(controllers["FS-EDMD-LQR"]["evaluation"]["time"].iloc[-1] - controllers["FS-EDMD-LQR"]["evaluation"]["time"].iloc[0]))
        err_ax.set_xticks([0, 20, 40, 60] if col == 0 else [0, 20, 40, 60, 80])
        err_ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
        err_ax.margins(x=0.0, y=0.08)
        err_ax.set_xlabel("Time (s)", labelpad=1.0)
        if col == 0:
            err_ax.set_ylabel(r"$e(t)$", labelpad=1.0)
    handle_map = {label: handle for handle, label in zip(*axes[0, 0].get_legend_handles_labels())}
    legend_order = ("Reference", "FS-EDMD-LQR", "PID")
    fig.legend(
        [handle_map[name] for name in legend_order],
        legend_order,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.99),
        ncol=3,
        frameon=False,
        columnspacing=0.95,
        handlelength=1.6,
        handletextpad=0.35,
        borderaxespad=0.0,
    )
    return fig


def main() -> None:
    task_data = load_task_data()
    metrics = build_metrics(task_data)
    figure = plot_figure(task_data)

    output_stem = "figure6_soft_tracking_singlecol_v2"
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

    metrics_path = SCRIPT_DIR / "figure6_soft_tracking_metrics_singlecol_v2.json"
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Figure 6 single-column v2 generated.")
    for task_name, values in metrics["tasks"].items():
        print(task_name)
        for controller, controller_metrics in values["controllers"].items():
            print(f"  {controller}: RMSE={controller_metrics['rmse']:.8f}, MAE={controller_metrics['mae']:.8f}")
    print(f"Metrics: {metrics_path}")
    print(f"Output directory: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
