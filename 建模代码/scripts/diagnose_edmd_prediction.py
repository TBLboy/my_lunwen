"""Diagnose whether EDMD recursive prediction collapses to a fixed point."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from modeling.soft_data import (
    EXPERIMENT_ROOT,
    denormalize_x,
    iter_trajectories,
    load_processed_meta,
    load_processed_split,
)
from modeling.soft_metrics import xy_rmse
from modeling.trainers.edmd import EDMDTrainer


def main() -> None:
    final_root = EXPERIMENT_ROOT / "final"
    processed_dir = final_root / "processed_data"
    split = load_processed_split("test", processed_dir=processed_dir)
    train = load_processed_split("train", processed_dir=processed_dir)
    meta = load_processed_meta(processed_dir=processed_dir)
    model = EDMDTrainer().load(final_root / "models" / "edmd.pkl")
    trajectory = next(
        item
        for item in iter_trajectories(split)
        if item["trajectory_id"] == 66
    )

    target = denormalize_x(trajectory["Y"], meta)
    prediction = denormalize_x(
        model.predict(
            trajectory["X"][0],
            trajectory["U"],
            steps=len(trajectory["U"]),
        ),
        meta,
    )
    print("EDMD trajectory 66 diagnostic")
    print(f"open-loop RMSE 2D: {xy_rmse(prediction, target):.6f}")
    corrected_C = np.zeros_like(model.C)
    corrected_C[1:3, :] = np.eye(2)
    corrected_prediction = denormalize_x(
        open_loop_with_C(model, trajectory, corrected_C),
        meta,
    )
    print(
        "open-loop RMSE 2D with corrected C: "
        f"{xy_rmse(corrected_prediction, target):.6f}"
    )
    print(
        "corrected-C x range: "
        f"{corrected_prediction[:, 0].min():.4f}.."
        f"{corrected_prediction[:, 0].max():.4f}"
    )
    train_rmse = training_one_step_rmse(model, train, meta)
    print(
        "EDMD training one-step RMSE: "
        f"x={train_rmse[0]:.6f}, y={train_rmse[1]:.6f}, 2D={train_rmse[2]:.6f}"
    )
    linear_recursive, linear_one_step = linear_baseline_rmse(train, trajectory, meta)
    print(
        "linear baseline recursive RMSE: "
        f"x={linear_recursive[0]:.6f}, y={linear_recursive[1]:.6f}, "
        f"2D={linear_recursive[2]:.6f}"
    )
    print(
        "linear baseline one-step RMSE: "
        f"x={linear_one_step[0]:.6f}, y={linear_one_step[1]:.6f}, "
        f"2D={linear_one_step[2]:.6f}"
    )
    for index, name in enumerate(("x", "y")):
        print(
            f"{name}: target[min,max,std]="
            f"{target[:, index].min():.4f},"
            f"{target[:, index].max():.4f},"
            f"{target[:, index].std():.4f}"
        )
        print(
            f"{name}: prediction[min,max,std]="
            f"{prediction[:, index].min():.4f},"
            f"{prediction[:, index].max():.4f},"
            f"{prediction[:, index].std():.4f}"
        )
        print(
            f"{name}: prediction[0:5]="
            f"{np.round(prediction[:5, index], 4).tolist()}"
        )
        print(
            f"{name}: diff[min,max,mean,std]="
            f"{np.diff(prediction[:, index]).min():.6f},"
            f"{np.diff(prediction[:, index]).max():.6f},"
            f"{np.diff(prediction[:, index]).mean():.6f},"
            f"{np.diff(prediction[:, index]).std():.6f}"
        )

    one_step = teacher_forced_predictions(model, trajectory)
    print(
        "one-step teacher-forced RMSE: "
        f"x={np.sqrt(np.mean((one_step[:, 0] - target[:, 0]) ** 2)):.6f}, "
        f"y={np.sqrt(np.mean((one_step[:, 1] - target[:, 1]) ** 2)):.6f}, "
        f"2D={xy_rmse(one_step, target):.6f}"
    )

    names = model.lift_fn.feature_names
    for output_index, output_name in enumerate(("x", "y")):
        row = np.abs(model.A[:, output_index])
        top = np.argsort(row)[::-1][:10]
        print(
            f"top A coefficients -> {output_name}: "
            + ", ".join(
                f"{names[i]}={model.A[i, output_index]:.4f}"
                for i in top
            )
        )
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(model.A))))
    print(f"spectral radius of A: {spectral_radius:.6f}")
    print(
        "raw x/y linear coefficients in A: "
        f"{model.A[1, 0]:.4f}, {model.A[2, 1]:.4f}"
    )
    print(
        "raw control coefficients in B: "
        f"u0->x={model.B[0, 0]:.4f}, u1->x={model.B[1, 0]:.4f}, "
        f"u0->y={model.B[0, 1]:.4f}, u1->y={model.B[1, 1]:.4f}"
    )


def training_one_step_rmse(
    model: EDMDTrainer,
    train: dict,
    meta: dict,
) -> tuple[float, float, float]:
    K = np.vstack([model.A, model.B])
    psi = model.lift_fn(train["X"])
    psi_xu = np.hstack([psi, train["U"]])
    prediction = denormalize_x(model._from_lift_state(psi_xu @ K @ model.C), meta)
    target = denormalize_x(train["Y"], meta)
    return (
        float(np.sqrt(np.mean((prediction[:, 0] - target[:, 0]) ** 2))),
        float(np.sqrt(np.mean((prediction[:, 1] - target[:, 1]) ** 2))),
        float(xy_rmse(prediction, target)),
    )


def linear_baseline_rmse(
    train: dict,
    trajectory: dict,
    meta: dict,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    features = np.hstack([train["X"], train["U"]])
    coef, _, _, _ = np.linalg.lstsq(features, train["Y"], rcond=None)
    A_lin = coef[:2, :]
    B_lin = coef[2:, :]

    state = trajectory["X"][0].astype(np.float64)
    recursive = np.zeros((len(trajectory["U"]), 2), dtype=np.float64)
    one_step = np.zeros_like(recursive)
    for index, control in enumerate(trajectory["U"]):
        target_state = trajectory["Y"][index]
        recursive[index] = state @ A_lin + control @ B_lin
        one_step[index] = target_state @ A_lin + control @ B_lin
        if index + 1 < len(trajectory["X"]):
            state = trajectory["X"][index + 1]

    recursive = denormalize_x(recursive, meta)
    one_step = denormalize_x(one_step, meta)
    target = denormalize_x(trajectory["Y"], meta)
    return (
        _rmse_tuple(recursive, target),
        _rmse_tuple(one_step, target),
    )


def _rmse_tuple(prediction: np.ndarray, target: np.ndarray) -> tuple[float, float, float]:
    return (
        float(np.sqrt(np.mean((prediction[:, 0] - target[:, 0]) ** 2))),
        float(np.sqrt(np.mean((prediction[:, 1] - target[:, 1]) ** 2))),
        float(xy_rmse(prediction, target)),
    )


def teacher_forced_predictions(model: EDMDTrainer, trajectory: dict) -> np.ndarray:
    """Apply the learned one-step EDMD map to observed states."""
    K = np.vstack([model.A, model.B])
    state = trajectory["X"][0].astype(np.float64)
    predictions = np.zeros((len(trajectory["U"]), model.C.shape[1]), dtype=np.float64)
    for index, control in enumerate(trajectory["U"]):
        psi = model.lift_fn(state.reshape(1, -1)).flatten().astype(np.float64)
        psi_next = np.hstack([psi, np.asarray(control).flatten()]) @ K
        prediction = model._from_lift_state(psi_next @ model.C)
        predictions[index] = prediction
        if index + 1 < len(trajectory["X"]):
            state = trajectory["X"][index + 1]
    return predictions


def open_loop_with_C(model: EDMDTrainer, trajectory: dict, C: np.ndarray) -> np.ndarray:
    K = np.vstack([model.A, model.B])
    state = trajectory["X"][0].astype(np.float64)
    predictions = np.zeros((len(trajectory["U"]), C.shape[1]), dtype=np.float64)
    for index, control in enumerate(trajectory["U"]):
        psi = model.lift_fn(state.reshape(1, -1)).flatten().astype(np.float64)
        state = model._from_lift_state(
            np.hstack([psi, np.asarray(control).flatten()]) @ K @ C
        )
        predictions[index] = state
    return predictions


if __name__ == "__main__":
    main()
