"""CLI entrypoint for standard EDMD training and model loading."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.data_io import get_model_path, load_train_data
from modeling.trainers.edmd import EDMDTrainer


def parse_args():
    parser = argparse.ArgumentParser(description="Train or load the standard EDMD model.")
    parser.add_argument(
        "--model-path",
        default=get_model_path("edmd_model.pkl"),
        help="Output or input pickle path.",
    )
    parser.add_argument(
        "--check-load",
        action="store_true",
        help="Load the project model and exit without training.",
    )
    parser.add_argument("--reg", type=float, default=1e-6)
    return parser.parse_args()


def check_load(args):
    trainer = EDMDTrainer()
    trainer.load(args.model_path)
    print(f"EDMD model loaded from {args.model_path}")
    print(f"A={trainer.A.shape}, B={trainer.B.shape}, psi_dim={trainer.psi_dim}")


def train(args):
    X_train, Y_train, U_train, _ = load_train_data()
    trainer = EDMDTrainer(reg=args.reg)
    trainer.fit(
        X_train.astype("float64"),
        Y_train.astype("float64"),
        U_train.astype("float64"),
    )

    model_path = Path(args.model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    trainer.save(str(model_path))


if __name__ == "__main__":
    args = parse_args()
    if args.check_load:
        check_load(args)
    else:
        train(args)
