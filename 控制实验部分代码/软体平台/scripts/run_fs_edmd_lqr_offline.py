"""Offline closed-loop FS-EDMD LQR experiment on soft-platform trajectory 66."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from algorithms.fs_edmd_lqr_controller import FSEDMDLQRController


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="controller-offline-001")
    parser.add_argument("--trajectory-id", type=int, default=66)
    parser.add_argument(
        "--config-path",
        default=str(PROJECT_ROOT / "algorithms/configs/fs_edmd_lqr_controller.json"),
    )
    parser.add_argument(
        "--assets-dir",
        default=str(PROJECT_ROOT / "algorithms/fs_edmd_lqr_controller_assets"),
    )
    parser.add_argument(
        "--output-dir",
        default=(
            r"C:\Users\Windows\Desktop\论文材料\杂项\软体平台探索实验结果"
            r"\controller_offline\controller-offline-001"
        ),
    )
    parser.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Override one controller config value, e.g. --set ff_gain=0.5.",
    )
    return parser.parse_args()


def load_trajectory(data: np.lib.npyio.NpzFile, trajectory_id: int) -> dict:
    mask = data["trajectory_id"] == trajectory_id
    if not np.any(mask):
        raise ValueError(f"Trajectory {trajectory_id} not found in test.npz")
    return {
        "X": np.asarray(data["X"][mask], dtype=np.float64),
        "Y": np.asarray(data["Y"][mask], dtype=np.float64),
        "U": np.asarray(data["U"][mask], dtype=np.float64),
        "step_index": np.asarray(data["step_index"][mask], dtype=np.int64),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_plots(out_dir: Path, ref: np.ndarray, sim: np.ndarray, control: np.ndarray) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    steps = np.arange(sim.shape[0])

    axes[0, 0].plot(steps, ref[1:, 0], label="reference", linewidth=2)
    axes[0, 0].plot(steps, sim[:, 0], label="FS-EDMD LQR", linewidth=2)
    axes[0, 0].set_xlabel("step")
    axes[0, 0].set_ylabel("x")
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    axes[0, 1].plot(steps, ref[1:, 1], label="reference", linewidth=2)
    axes[0, 1].plot(steps, sim[:, 1], label="FS-EDMD LQR", linewidth=2)
    axes[0, 1].set_xlabel("step")
    axes[0, 1].set_ylabel("y")
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    axes[1, 0].plot(ref[:, 0], ref[:, 1], label="reference path", linewidth=2)
    axes[1, 0].plot(
        np.vstack([ref[:1], sim])[:, 0],
        np.vstack([ref[:1], sim])[:, 1],
        label="controlled path",
        linewidth=2,
    )
    axes[1, 0].scatter(ref[0, 0], ref[0, 1], marker="o", color="black", label="start")
    axes[1, 0].scatter(ref[-1, 0], ref[-1, 1], marker="s", color="red", label="end")
    axes[1, 0].set_xlabel("x")
    axes[1, 0].set_ylabel("y")
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    axes[1, 1].plot(control[:, 0], label="u_x", linewidth=2)
    axes[1, 1].plot(control[:, 1], label="u_y", linewidth=2)
    axes[1, 1].set_xlabel("step")
    axes[1, 1].set_ylabel("control")
    axes[1, 1].legend()
    axes[1, 1].grid(True)

    fig.suptitle("Trajectory 66 FS-EDMD LQR offline closed-loop")
    fig.tight_layout()
    figure_dir = out_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(figure_dir / "trajectory66_fs_edmd_lqr.png", dpi=200)
    fig.savefig(figure_dir / "trajectory66_fs_edmd_lqr.pdf")
    fig.savefig(figure_dir / "trajectory66_fs_edmd_lqr.svg")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    controller = FSEDMDLQRController(args.config_path)
    if controller.lifter is None or controller.K is None:
        raise RuntimeError("FS-EDMD LQR controller did not load correctly")

    for item in args.set:
        if "=" not in item:
            raise ValueError(f"Invalid --set value: {item}")
        key, raw = item.split("=", 1)
        lowered = raw.strip().lower()
        if lowered in {"true", "false"}:
            controller.config[key] = lowered == "true"
        else:
            try:
                controller.config[key] = int(raw)
            except ValueError:
                try:
                    controller.config[key] = float(raw)
                except ValueError:
                    controller.config[key] = raw
    controller.design_lqr()

    assets_dir = Path(args.assets_dir)
    test_data = np.load(assets_dir / "test.npz", allow_pickle=True)
    meta = np.load(assets_dir / "meta.npz", allow_pickle=True)
    traj = load_trajectory(test_data, args.trajectory_id)

    lifter = controller.lifter
    x0_phys = lifter.denormalize_state(traj["X"][0])
    target_phys = lifter.denormalize_state(traj["Y"])
    ref_phys = np.vstack([x0_phys.reshape(1, -1), target_phys])
    traj_list = [tuple(row) for row in ref_phys]

    steps = traj["U"].shape[0]
    z = lifter.augmented_state(x0_phys)
    sim_x_norm = np.zeros((steps, lifter.n), dtype=np.float64)
    controls = np.zeros((steps, lifter.m), dtype=np.float64)
    controls_norm = np.zeros((steps, lifter.m), dtype=np.float64)
    clipped = 0

    for step in range(steps):
        current_phys = lifter.denormalize_state(z[:2])
        control = controller.calculate_control(current_phys, step, traj_list)
        u_phys = np.asarray(control, dtype=np.float64).reshape(lifter.m)
        sign_x = float(controller.config.get("output_sign_x", 1.0))
        sign_y = float(controller.config.get("output_sign_y", 1.0))
        u_model_phys = u_phys.copy()
        u_model_phys[0] = u_phys[0] / sign_x if sign_x != 0.0 else u_phys[0]
        u_model_phys[1] = u_phys[1] / sign_y if sign_y != 0.0 else u_phys[1]
        u_norm = lifter.normalize_control(u_model_phys)
        controls[step] = u_phys
        controls_norm[step] = u_norm
        if np.any(np.abs(u_phys) >= float(controller.config.get("u_limit", 50.0))):
            clipped += 1

        z_next = lifter.A @ z + lifter.B @ u_norm
        x_next_norm = z_next[:2]
        sim_x_norm[step] = x_next_norm
        z = np.concatenate(
            [
                x_next_norm,
                lifter.D @ lifter.lift_state_norm(x_next_norm),
            ]
        )

    sim_phys = lifter.denormalize_state(sim_x_norm)
    sim_all = np.vstack([ref_phys[:1], sim_phys])
    error = sim_all - ref_phys
    rmse = float(np.sqrt(np.mean(np.sum(error * error, axis=1))))
    rmse_x = float(np.sqrt(np.mean(error[:, 0] ** 2)))
    rmse_y = float(np.sqrt(np.mean(error[:, 1] ** 2)))
    max_error = float(np.max(np.linalg.norm(error, axis=1)))
    control_rms = float(np.sqrt(np.mean(controls * controls)))

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).isoformat()

    summary = {
        "run_id": args.run_id,
        "created_at": created_at,
        "reference_trajectory_id": args.trajectory_id,
        "plant": "FS-EDMD model in-the-loop",
        "controller": controller.get_name(),
        "model_dimensions": {
            "lift_dimension": int(lifter.D.shape[1]),
            "augmented_dimension": int(lifter.d),
            "N": int(lifter.N),
            "state_dim": int(lifter.n),
            "control_dim": int(lifter.m),
        },
        "controller_config": controller.config,
        "closed_loop_rho": float(controller.closed_loop_rho),
        "steps": int(steps),
        "clipped_control_steps": int(clipped),
        "metrics": {
            "rmse": rmse,
            "rmse_x": rmse_x,
            "rmse_y": rmse_y,
            "max_error": max_error,
            "control_rms": control_rms,
        },
        "output_dir": str(out_dir),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    rows = []
    for step in range(steps):
        rows.append(
            {
                "step": int(step),
                "ref_x": float(ref_phys[step + 1, 0]),
                "ref_y": float(ref_phys[step + 1, 1]),
                "sim_x": float(sim_phys[step, 0]),
                "sim_y": float(sim_phys[step, 1]),
                "err_x": float(error[step + 1, 0]),
                "err_y": float(error[step + 1, 1]),
                "u_x": float(controls[step, 0]),
                "u_y": float(controls[step, 1]),
            }
        )
    write_csv(out_dir / "tracking_metrics.csv", rows)
    np.savez(
        out_dir / "tracking_results.npz",
        reference=ref_phys,
        simulated=sim_all,
        control=controls,
        control_norm=controls_norm,
    )
    write_plots(out_dir, ref_phys, sim_phys, controls)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
