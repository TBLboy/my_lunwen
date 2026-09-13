"""Run a reproducible soft-platform parameter search campaign."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.soft_data import EXPERIMENT_ROOT


def parse_config_value(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, bool):
        return [str(value).lower()]
    return [str(value)]


# run_soft_experiment.py uses argparse with hyphenated CLI flags, while config
# files keep natural underscore keys for readability.
ALLOWED_OPTION_NAMES = {
    "models": "--models",
    "smoke": "--smoke",
    "lift_poly_degree": "--lift-poly-degree",
    "lift_rbf_grid": "--lift-rbf-grid",
    "lift_rbf_sigma_scale": "--lift-rbf-sigma-scale",
    "lift_freqs": "--lift-freqs",
    "fs_n": "--fs-n",
    "fs_lam": "--fs-lam",
    "fs_beta": "--fs-beta",
    "fs_eta_d": "--fs-eta-d",
    "fs_max_iter": "--fs-max-iter",
    "fs_tol": "--fs-tol",
    "fs_grad_clip_norm": "--fs-grad-clip-norm",
    "fs_lr_decay_factor": "--fs-lr-decay-factor",
    "edmd_reg": "--edmd-reg",
    "edmd_dl_n_psi": "--edmd-dl-n-psi",
    "edmd_dl_layers": "--edmd-dl-layers",
    "edmd_dl_lr": "--edmd-dl-lr",
    "edmd_dl_reg": "--edmd-dl-reg",
    "edmd_dl_epochs": "--edmd-dl-epochs",
    "edmd_dl_batch_size": "--edmd-dl-batch-size",
    "test_limit": "--test-limit",
    "eval_splits": "--eval-splits",
}


def build_command(config: dict) -> list[str]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "run_soft_experiment.py"),
        "--run-id",
        str(config["run_id"]),
        "--seed",
        str(config.get("seed", 20260911)),
    ]
    for key, option in ALLOWED_OPTION_NAMES.items():
        if key not in config:
            continue
        if key == "smoke":
            if config[key]:
                command.append(option)
            continue
        for item in parse_config_value(config[key]):
            command.extend([option, item])
    return command


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", required=True)
    args = parser.parse_args()

    campaign_dir = EXPERIMENT_ROOT / "search_plans"
    campaign_path = campaign_dir / f"{args.campaign}.json"
    if not campaign_path.exists():
        raise FileNotFoundError(campaign_path)
    plan = json.loads(campaign_path.read_text(encoding="utf-8-sig"))
    configs = plan["configs"]

    report = {
        "campaign": args.campaign,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "runs": [],
    }
    failed = []
    for index, config in enumerate(configs, start=1):
        run_id = config["run_id"]
        command = build_command(config)
        print(f"[{index}/{len(configs)}] {run_id}: {' '.join(command)}", flush=True)
        started = datetime.now(timezone.utc)
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        elapsed = (datetime.now(timezone.utc) - started).total_seconds()
        item = {
            "run_id": run_id,
            "returncode": result.returncode,
            "elapsed_seconds": round(elapsed, 2),
            "tail": result.stdout[-1200:] + result.stderr[-1200:],
        }
        report["runs"].append(item)
        if result.returncode != 0:
            failed.append(run_id)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    report["failed"] = failed
    report_path = campaign_dir / f"{args.campaign}.report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"campaign report: {report_path}", flush=True)
    if failed:
        raise SystemExit(f"failed runs: {failed}")


if __name__ == "__main__":
    main()
