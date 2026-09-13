"""Fit and validate the default soft-platform lift library."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.soft_data import EXPERIMENT_ROOT, load_processed_split
from modeling.soft_lift import default_soft_lift


def main() -> None:
    train = load_processed_split("train")
    sample_indices = np_random_sample(train["X"].shape[0], 5000)
    lift = default_soft_lift(train["X"])
    report = lift.report(train["X"][sample_indices])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    report_path = EXPERIMENT_ROOT / "feature_reports" / "default_soft_lift.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"report: {report_path}")


def np_random_sample(length: int, count: int):
    import numpy as np

    if length <= count:
        return np.arange(length)
    return np.random.default_rng(0).choice(length, count, replace=False)


if __name__ == "__main__":
    main()
