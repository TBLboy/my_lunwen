"""Standard EDMD trainer migrated from the verified train_edmd.py baseline."""

from __future__ import annotations

import pickle

import numpy as np

from modeling.lift_function import lift_function


class EDMDTrainer:
    """Standard EDMD using the complete feature library."""

    def __init__(self, reg=1e-6, lift_fn=None, lift_config=None):
        self.reg = reg
        self.lift_fn = lift_fn or lift_function
        self.lift_config = lift_config
        self.A = None
        self.B = None
        self.C = None
        self.psi_dim = None

    def _build_output_matrix(self, state_dim: int) -> None:
        output = np.zeros((self.psi_dim, state_dim), dtype=np.float64)
        feature_names = getattr(self.lift_fn, "feature_names", None)
        if feature_names and {"x", "y"}.issubset(feature_names):
            indices = [feature_names.index("x"), feature_names.index("y")]
        else:
            indices = list(range(state_dim))
        for column, feature_index in enumerate(indices):
            output[feature_index, column] = 1.0
        self.C = output

    def _from_lift_state(self, value: np.ndarray) -> np.ndarray:
        result = np.asarray(value, dtype=np.float64)
        center = getattr(self.lift_fn, "input_center", None)
        scale = getattr(self.lift_fn, "input_scale", None)
        if center is not None and scale is not None:
            result = result * np.asarray(scale, dtype=np.float64)
            result = result + np.asarray(center, dtype=np.float64)
        return result

    def fit(self, X_train, Y_train, U_train):
        print("Computing lifted features...")
        X_train = np.asarray(X_train, dtype=np.float64)
        Y_train = np.asarray(Y_train, dtype=np.float64)
        U_train = np.asarray(U_train, dtype=np.float64)

        psi_x = self.lift_fn(X_train)
        psi_y = self.lift_fn(Y_train)
        self.psi_dim = psi_x.shape[1]
        print(f"Lifted dimension: {self.psi_dim}")

        psi_xu = np.hstack([psi_x, U_train])
        XtX = psi_xu.T @ psi_xu + self.reg * np.eye(psi_xu.shape[1])
        XtY = psi_xu.T @ psi_y
        K = np.linalg.solve(XtX, XtY)

        self.A = np.asarray(K[: self.psi_dim, :], dtype=np.float64)
        self.B = np.asarray(K[self.psi_dim :, :], dtype=np.float64)

        n = X_train.shape[1]
        self._build_output_matrix(n)

        psi_y_pred = psi_xu @ K
        train_mse = np.mean((psi_y - psi_y_pred) ** 2)
        print(f"Training MSE: {train_mse:.6f}")
        print("Training complete.")
        return self

    def predict(self, x0, u_sequence, steps=None):
        T = len(u_sequence) if steps is None else min(steps, len(u_sequence))
        n = x0.shape[0]
        x_pred = np.zeros((T, n), dtype=np.float64)

        x0 = np.asarray(x0, dtype=np.float64)
        psi_curr = self.lift_fn(x0.reshape(1, -1)).flatten().astype(np.float64)
        K = np.vstack([self.A, self.B])

        for t in range(T):
            u_curr = np.asarray(u_sequence[t], dtype=np.float64).flatten()
            psi_xu = np.hstack([psi_curr, u_curr])
            psi_next = psi_xu @ K
            x_next = self._from_lift_state(psi_next @ self.C)
            x_pred[t] = x_next
            psi_curr = psi_next

        return x_pred

    def save(self, path):
        model_dict = {
            "A": self.A,
            "B": self.B,
            "C": self.C,
            "psi_dim": self.psi_dim,
            "reg": self.reg,
            "lift_config": self.lift_config,
        }
        with open(path, "wb") as handle:
            pickle.dump(model_dict, handle)
        print(f"Model saved to {path}")

    def load(self, path):
        with open(path, "rb") as handle:
            model_dict = pickle.load(handle)
        self.A = np.asarray(model_dict["A"], dtype=np.float64)
        self.B = np.asarray(model_dict["B"], dtype=np.float64)
        self.C = np.asarray(model_dict["C"], dtype=np.float64)
        self.psi_dim = int(model_dict["psi_dim"])
        self.reg = float(model_dict.get("reg", self.reg))
        self.lift_config = model_dict.get("lift_config")
        if isinstance(self.lift_config, dict) and self.lift_config.get("kind") == "soft_lift":
            from modeling.soft_lift import SoftLift

            self.lift_fn = SoftLift.from_config(self.lift_config)
            self._build_output_matrix(self.C.shape[1])
        return self
