"""Generate the revised soft-platform tracking figure for triangle and Lissajous paths."""

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

EVALUATION_START_SAMPLE = 30
OUTPUT_STEM = "figure7_soft_tracking_singlecol_v4"

COLORS = {
    "Reference": "#111111",
    "FS-EDMD-LQR": "#C44E52",
    "PID": "#4C78A8",
}
LINESTYLES = {
    "Reference": "-",
    "FS-EDMD-LQR": "-",
    "PID": "--",
}
LINEWIDTHS = {
    "Reference": 0.72,
    "FS-EDMD-LQR": 0.78,
    "PID": 0.78,
}

TASKS = (
    ("triangle", "三三角-FS.zip", "三三角-PID.zip"),
    ("lissajous", "莉萨如-FS.zip", "莉萨如-pid.zip"),
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
    data = data.sort_values("step")
    data = data.drop_duplicates("step", keep="first").reset_index(drop=True)
    if data.empty:
        raise ValueError(f"No valid tracking samples in {path.name}")
    return data


def align_tracking_pair(fs_data: pd.DataFrame, pid_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """Align FS and PID by sample index, ignoring elapsed time."""
    fs_aligned = fs_data.reset_index(drop=True).copy()
    pid_aligned = pid_data.reset_index(drop=True).copy()

    if len(fs_aligned) > len(pid_aligned):
        if len(fs_aligned) % len(pid_aligned) != 0:
            raise ValueError(
                f"Cannot integer-decimate FS samples {len(fs_aligned)} to PID samples {len(pid_aligned)}"
            )
        decimation = len(fs_aligned) // len(pid_aligned)
        fs_aligned = fs_aligned.iloc[::decimation].reset_index(drop=True)
    elif len(fs_aligned) < len(pid_aligned):
        raise ValueError(
            f"FS samples {len(fs_aligned)} are fewer than PID samples {len(pid_aligned)}"
        )
    else:
        decimation = 1

    if len(fs_aligned) != len(pid_aligned):
        raise ValueError("FS/PID sample counts remain mismatched after alignment")

    fs_aligned["sample"] = np.arange(len(fs_aligned), dtype=int)
    pid_aligned["sample"] = np.arange(len(pid_aligned), dtype=int)
    return fs_aligned, pid_aligned, decimation


def calculate_metrics(actual_x, actual_y, reference_x, reference_y) -> dict[str, float]:
    error_x = np.asarray(actual_x, dtype=np.float64) - np.asarray(reference_x, dtype=np.float64)
    error_y = np.asarray(actual_y, dtype=np.float64) - np.asarray(reference_y, dtype=np.float64)
    distance = np.sqrt(error_x**2 + error_y**2)
    return {
        "rmse": float(np.sqrt(np.mean(distance**2))),
        "mae": float(np.mean(distance)),
        "x_rmse": float(np.sqrt(np.mean(error_x**2))),
        "y_rmse": float(np.sqrt(np.mean(error_y**2))),
    }


def reference_disagreement(fs_data: pd.DataFrame, pid_data: pd.DataFrame) -> dict[str, float]:
    error_x = fs_data["ref_x"].to_numpy(dtype=np.float64) - pid_data["ref_x"].to_numpy(dtype=np.float64)
    error_y = fs_data["ref_y"].to_numpy(dtype=np.float64) - pid_data["ref_y"].to_numpy(dtype=np.float64)
    distance = np.hypot(error_x, error_y)
    return {
        "rmse": float(np.sqrt(np.mean(distance**2))),
        "max": float(np.max(distance)),
        "x_max": float(np.max(np.abs(error_x))),
        "y_max": float(np.max(np.abs(error_y))),
    }


def load_task_data() -> tuple[dict[str, dict[str, object]], pd.DataFrame]:
    task_data: dict[str, dict[str, object]] = {}
    processed_frames: list[pd.DataFrame] = []

    for task_name, fs_name, pid_name in TASKS:
        fs_raw = read_tracking_archive(DATA_DIR / fs_name)
        pid_raw = read_tracking_archive(DATA_DIR / pid_name)
        fs_aligned, pid_aligned, decimation = align_tracking_pair(fs_raw, pid_raw)

        fs_eval = fs_aligned[fs_aligned["sample"] >= EVALUATION_START_SAMPLE].reset_index(drop=True)
        pid_eval = pid_aligned[pid_aligned["sample"] >= EVALUATION_START_SAMPLE].reset_index(drop=True)
        if fs_eval.empty or pid_eval.empty:
            raise ValueError(f"No evaluation samples after sample {EVALUATION_START_SAMPLE}")

        task_data[task_name] = {
            "fs_raw_samples": int(len(fs_raw)),
            "pid_raw_samples": int(len(pid_raw)),
            "decimation": int(decimation),
            "reference_disagreement": reference_disagreement(fs_aligned, pid_aligned),
            "controllers": {
                "FS-EDMD-LQR": {"full": fs_aligned, "evaluation": fs_eval},
                "PID": {"full": pid_aligned, "evaluation": pid_eval},
            },
        }

        reference = pid_aligned[["sample", "ref_x", "ref_y"]].rename(
            columns={"ref_x": "reference_x", "ref_y": "reference_y"}
        )
        for controller_name in ("FS-EDMD-LQR", "PID"):
            frame = task_data[task_name]["controllers"][controller_name]["full"].merge(
                reference, on="sample", how="left", validate="one_to_one"
            )
            frame["error_x"] = frame["act_x"] - frame["reference_x"]
            frame["error_y"] = frame["act_y"] - frame["reference_y"]
            frame["error_distance"] = np.hypot(frame["error_x"], frame["error_y"])
            frame.insert(0, "controller", controller_name)
            frame.insert(0, "task", task_name)
            processed_frames.append(
                frame[
                    [
                        "task",
                        "controller",
                        "sample",
                        "step",
                        "time",
                        "ref_x",
                        "ref_y",
                        "act_x",
                        "act_y",
                        "reference_x",
                        "reference_y",
                        "error_x",
                        "error_y",
                        "error_distance",
                    ]
                ]
            )

    processed = pd.concat(processed_frames, ignore_index=True)
    return task_data, processed


def square_limits(
    x_values: np.ndarray,
    y_values: np.ndarray,
    margin_ratio: float = 0.06,
) -> tuple[tuple[float, float], tuple[float, float]]:
    x_min, x_max = float(np.min(x_values)), float(np.max(x_values))
    y_min, y_max = float(np.min(y_values)), float(np.max(y_values))
    span = max(x_max - x_min, y_max - y_min)
    margin = margin_ratio * span
    x_center = 0.5 * (x_min + x_max)
    y_center = 0.5 * (y_min + y_max)
    half_span = 0.5 * span + margin
    return (x_center - half_span, x_center + half_span), (y_center - half_span, y_center + half_span)


def task_trajectory_limits(controllers: dict[str, dict[str, pd.DataFrame]]) -> tuple[tuple[float, float], tuple[float, float]]:
    xs: list[float] = []
    ys: list[float] = []
    for controller_data in controllers.values():
        full = controller_data["full"]
        xs.extend(full["ref_x"].to_numpy(dtype=np.float64))
        xs.extend(full["act_x"].to_numpy(dtype=np.float64))
        ys.extend(full["ref_y"].to_numpy(dtype=np.float64))
        ys.extend(full["act_y"].to_numpy(dtype=np.float64))
    return square_limits(np.asarray(xs), np.asarray(ys))


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
        alpha=0.95 if name != "PID" else 0.88,
        zorder=4 if name == "FS-EDMD-LQR" else 2,
    )


def build_metrics(task_data: dict[str, dict[str, object]]) -> dict[str, object]:
    metrics: dict[str, object] = {
        "evaluation_start_sample": EVALUATION_START_SAMPLE,
        "time_axis_used": False,
        "error_definition": "sqrt((act_x-reference_x)^2 + (act_y-reference_y)^2)",
        "tasks": {},
    }

    for task_name, task_values in task_data.items():
        controllers = task_values["controllers"]
        task_metrics: dict[str, object] = {
            "fs_raw_samples": task_values["fs_raw_samples"],
            "pid_raw_samples": task_values["pid_raw_samples"],
            "decimation": task_values["decimation"],
            "reference_disagreement": task_values["reference_disagreement"],
            "evaluation_samples": int(len(controllers["PID"]["evaluation"])),
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


def plot_figure(task_data: dict[str, dict[str, object]]) -> plt.Figure:
    configure_style()
    figure, axes = plt.subplots(1, 2, figsize=(3.42, 1.90), facecolor="white")
    figure.subplots_adjust(left=0.10, right=0.985, bottom=0.175, top=0.92, wspace=0.20)

    for column, (task_name, _fs_name, _pid_name) in enumerate(TASKS):
        axis = axes[column]
        controllers = task_data[task_name]["controllers"]
        reference = controllers["PID"]["full"]

        axis.plot(
            reference["ref_x"],
            reference["ref_y"],
            color=COLORS["Reference"],
            linestyle=LINESTYLES["Reference"],
            linewidth=LINEWIDTHS["Reference"],
            label="Reference",
            zorder=3,
        )
        plot_controller_trajectory(axis, controllers["PID"]["full"], "PID", show_label=True)
        plot_controller_trajectory(axis, controllers["FS-EDMD-LQR"]["full"], "FS-EDMD-LQR", show_label=True)

        x_limits, y_limits = task_trajectory_limits(controllers)
        axis.set_aspect("equal", adjustable="box")
        axis.set_xlim(*x_limits)
        axis.set_ylim(*y_limits)
        configure_axis(axis)
        axis.xaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        axis.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        axis.set_xlabel(r"$x$", labelpad=1.0)
        if column == 0:
            axis.set_ylabel(r"$y$", labelpad=1.0)

    handle_map = {label: handle for handle, label in zip(*axes[0].get_legend_handles_labels())}
    legend_order = ("Reference", "FS-EDMD-LQR", "PID")
    figure.legend(
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
    return figure


def main() -> None:
    task_data, processed = load_task_data()
    metrics = build_metrics(task_data)
    figure = plot_figure(task_data)

    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        figure.savefig(
            SCRIPT_DIR / f"{OUTPUT_STEM}.{extension}",
            dpi=600,
            facecolor="white",
            bbox_inches="tight",
            pad_inches=0.008,
        )
    plt.close(figure)

    processed_path = SCRIPT_DIR / f"{OUTPUT_STEM}_processed.csv"
    metrics_path = SCRIPT_DIR / f"{OUTPUT_STEM}_metrics.json"
    processed.to_csv(processed_path, index=False, float_format="%.8f")
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated {OUTPUT_STEM}.png/pdf/svg")
    print(f"Processed data: {processed_path}")
    print(f"Metrics: {metrics_path}")
    for task_name, task_values in metrics["tasks"].items():
        print(f"{task_name}: decimation={task_values['decimation']}")
        for controller_name, controller_metrics in task_values["controllers"].items():
            print(
                f"  {controller_name}: "
                f"RMSE={controller_metrics['rmse']:.8f}, "
                f"MAE={controller_metrics['mae']:.8f}"
            )


if __name__ == "__main__":
    main()
