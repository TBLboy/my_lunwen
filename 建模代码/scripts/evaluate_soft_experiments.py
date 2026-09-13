"""Aggregate soft-platform experiment runs into a paper-selection leaderboard."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.soft_data import EXPERIMENT_ROOT


def main() -> None:
    runs_dir = EXPERIMENT_ROOT / "runs"
    if not runs_dir.exists():
        raise FileNotFoundError(f"Missing runs directory: {runs_dir}")

    def make_row(summary: dict, summary_path: Path) -> dict:
        methods = summary.get("methods", {})
        if not all(name in methods for name in ("fs_edmd", "edmd", "edmd_dl")):
            return None
        validation_methods = (
            summary.get("split_metrics", {}).get("validation", {}).get("methods", {})
        )
        baseline_best = min(
            methods["edmd"]["best_rmse"],
            methods["edmd_dl"]["best_rmse"],
        )
        fs_best = methods["fs_edmd"]["best_rmse"]
        run_dir = summary_path.parents[1]
        config = {}
        config_path = run_dir / "run_config.json"
        if config_path.exists():
            raw_config = json.loads(config_path.read_text(encoding="utf-8"))
            raw_args = raw_config.get("arguments", {})
            config = {
                "lift_poly_degree": raw_args.get("lift_poly_degree"),
                "lift_rbf_grid": raw_args.get("lift_rbf_grid"),
                "lift_rbf_sigma_scale": raw_args.get("lift_rbf_sigma_scale"),
                "fs_n": raw_args.get("fs_n"),
                "fs_lam": raw_args.get("fs_lam"),
                "fs_beta": raw_args.get("fs_beta"),
                "fs_eta_d": raw_args.get("fs_eta_d"),
                "fs_max_iter": raw_args.get("fs_max_iter"),
                "fs_tol": raw_args.get("fs_tol"),
                "fs_grad_clip_norm": raw_args.get("fs_grad_clip_norm"),
                "fs_lr_decay_factor": raw_args.get("fs_lr_decay_factor"),
                "edmd_reg": raw_args.get("edmd_reg"),
                "edmd_dl_n_psi": raw_args.get("edmd_dl_n_psi"),
                "edmd_dl_layers": raw_args.get("edmd_dl_layers"),
                "edmd_dl_lr": raw_args.get("edmd_dl_lr"),
                "edmd_dl_epochs": raw_args.get("edmd_dl_epochs"),
            }
        return {
            "run_id": summary["run_id"],
            "smoke": bool(summary.get("smoke", False)),
            "fs_average_rmse": methods["fs_edmd"]["average_rmse"],
            "fs_best_rmse": fs_best,
            "fs_best_trajectory_id": methods["fs_edmd"]["best_trajectory_id"],
            "edmd_average_rmse": methods["edmd"]["average_rmse"],
            "edmd_best_rmse": methods["edmd"]["best_rmse"],
            "edmd_dl_average_rmse": methods["edmd_dl"]["average_rmse"],
            "edmd_dl_best_rmse": methods["edmd_dl"]["best_rmse"],
            "fs_has_best_best_rmse": fs_best < baseline_best,
            "best_margin": baseline_best - fs_best,
            "run_dir": str(run_dir),
            "config": config,
            "validation": {
                method: validation_methods.get(method)
                for method in ("fs_edmd", "edmd", "edmd_dl")
            },
        }

    all_rows: list[dict] = []
    for summary_path in sorted(runs_dir.glob("*/metrics/summary.json")):
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        row = make_row(summary, summary_path)
        if row is not None:
            all_rows.append(row)

    def sort_key(row: dict):
        return (
            not row["fs_has_best_best_rmse"],
            row["fs_average_rmse"],
            row["fs_best_rmse"],
        )

    all_rows.sort(key=sort_key)
    rows = [row for row in all_rows if not row["smoke"]]
    smoke_rows = [row for row in all_rows if row["smoke"]]
    if not rows:
        raise ValueError("No complete formal three-method runs found")

    output_dir = EXPERIMENT_ROOT / "summaries"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "leaderboard.json"
    csv_path = output_dir / "leaderboard.csv"
    all_csv_path = output_dir / "leaderboard_all.csv"
    json_path.write_text(
        json.dumps(
            {
                "rows": rows,
                "best": rows[0],
                "smoke_rows": smoke_rows,
                "count": len(rows),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with all_csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)
    print(json.dumps(rows[0], ensure_ascii=False, indent=2))
    print(f"leaderboard: {json_path}")


if __name__ == "__main__":
    main()
