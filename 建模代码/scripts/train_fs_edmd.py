"""CLI entrypoint for FS-EDMD training and model loading."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modeling.data_io import get_model_path, load_train_data
from modeling.lift_function import lift_function
from modeling.trainers.fs_edmd import OursKoopmanTrainer


def parse_args():
    parser = argparse.ArgumentParser(description="Train or load the FS-EDMD model.")
    parser.add_argument(
        "--model-path",
        default=get_model_path("ours_model.pkl"),
        help="Output or input pickle path.",
    )
    parser.add_argument(
        "--meta-path",
        default=get_model_path("meta.npz"),
        help="Output path for normalization metadata.",
    )
    parser.add_argument(
        "--check-load",
        action="store_true",
        help="Load the project model and exit without training.",
    )
    parser.add_argument("--lam", type=float, default=0.001)
    parser.add_argument("--beta", type=float, default=0.001)
    parser.add_argument("--N", type=int, default=40)
    parser.add_argument("--eta-d", type=float, default=1e-2)
    parser.add_argument("--max-iter", type=int, default=2000)
    parser.add_argument("--tol", type=float, default=1e-6)
    return parser.parse_args()


def check_load(args):
    trainer = OursKoopmanTrainer()
    trainer.load(args.model_path)
    print(f"FS-EDMD model loaded from {args.model_path}")
    print(
        f"A={trainer.A_model.shape}, B={trainer.B_model.shape}, "
        f"C={trainer.C_model.shape}, D={trainer.D_model.shape}"
    )


def train(args):
    X_train, Y_train, U_train, meta = load_train_data()
    X_Phi = lift_function(X_train).T
    Y_Phi = lift_function(Y_train).T

    trainer = OursKoopmanTrainer(
        lam=args.lam,
        beta=args.beta,
        N=args.N,
        eta_D=args.eta_d,
        max_iter=args.max_iter,
        tol=args.tol,
        verbose=True,
    )
    trainer.fit(X_train.T, Y_train.T, U_train.T, X_Phi, Y_Phi)

    model_path = Path(args.model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    trainer.save(str(model_path))
    np.savez(
        args.meta_path,
        q_scaler=meta["q_scaler"],
        q_dc=meta["q_dc"],
        u_scaler=meta["u_scaler"],
        u_dc=meta["u_dc"],
    )
    print(f"FS-EDMD metadata saved to {args.meta_path}")


if __name__ == "__main__":
    args = parse_args()
    if args.check_load:
        check_load(args)
    else:
        train(args)
