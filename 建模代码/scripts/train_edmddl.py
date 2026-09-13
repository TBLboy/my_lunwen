"""CLI entrypoint for EDMDDL training and model loading."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.data_io import get_model_path, load_train_data, load_val_data
from modeling.trainers.edmddl import EDMDDLTrainer


def parse_args():
    parser = argparse.ArgumentParser(description="Train or load the EDMDDL model.")
    parser.add_argument(
        "--model-path",
        default=get_model_path("edmddl_model.pkl"),
        help="Output or input pickle path.",
    )
    parser.add_argument(
        "--check-load",
        action="store_true",
        help="Load the project model and exit without training.",
    )
    parser.add_argument("--state-dim", type=int, default=6)
    parser.add_argument("--control-dim", type=int, default=3)
    parser.add_argument("--n-psi", type=int, default=50)
    parser.add_argument(
        "--layer-sizes",
        default="512,512,512,512,512,512",
        help="Comma-separated hidden layer sizes.",
    )
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--reg", type=float, default=1e-6)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=5000)
    return parser.parse_args()


def check_load(args):
    trainer = EDMDDLTrainer()
    trainer.load(args.model_path, device="cpu")
    print(f"EDMDDL model loaded from {args.model_path}")
    print(f"A={trainer.A.shape}, B={trainer.B.shape}, psi_dim={trainer.psi_dim}")


def train(args):
    X_train, Y_train, U_train, _ = load_train_data()
    X_val, Y_val, U_val = load_val_data()

    layer_sizes = [int(item) for item in args.layer_sizes.split(",") if item.strip()]
    trainer = EDMDDLTrainer(
        state_dim=args.state_dim,
        control_dim=args.control_dim,
        n_psi=args.n_psi,
        layer_sizes=layer_sizes,
        lr=args.lr,
        reg=args.reg,
    )
    trainer.fit(
        X_train.astype("float64"),
        Y_train.astype("float64"),
        U_train.astype("float64"),
        X_val.astype("float64"),
        Y_val.astype("float64"),
        U_val.astype("float64"),
        epochs=args.epochs,
        batch_size=args.batch_size,
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
