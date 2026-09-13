"""Prepare the fixed train/validation/test split for soft-platform modeling."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.soft_data import (
    DEFAULT_SEED,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    load_processed_meta,
    load_processed_split,
    prepare_soft_dataset,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare fixed 70/20/10 soft-platform training data."
    )
    parser.add_argument("--raw-dir", default=str(RAW_DATA_DIR))
    parser.add_argument("--output-dir", default=str(PROCESSED_DATA_DIR))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate an existing fixed split. Use only after explicit approval.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing processed data without regenerating it.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.check:
        meta = load_processed_meta(args.output_dir)
        for split in ("train", "validation", "test"):
            data = load_processed_split(split, args.output_dir)
            print(
                f"{split}: samples={data['X'].shape[0]}, "
                f"trajectories={len(set(data['trajectory_id'].tolist()))}"
            )
        print(f"test trajectory ids: {meta['test_trajectory_ids'].tolist()}")
        return

    result = prepare_soft_dataset(
        raw_dir=args.raw_dir,
        output_dir=args.output_dir,
        seed=args.seed,
        force=args.force,
    )
    manifest = result["manifest"]
    print(f"status: {result['status']}")
    print(f"output: {result['output_dir']}")
    print(f"seed: {manifest['seed']}")
    print(f"counts: {manifest['counts']}")
    print(f"test ids: {manifest['trajectory_ids']['test']}")


if __name__ == "__main__":
    main()
