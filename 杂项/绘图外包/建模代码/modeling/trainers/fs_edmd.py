"""FS-EDMD trainer migrated from the verified train_ours.py baseline."""

from __future__ import annotations

import pickle

import numpy as np
import torch
from sklearn.decomposition import PCA

from modeling.lift_function import lift_function


class OursKoopmanTrainer:
    """Feature-selective EDMD with alternating Koopman/feature optimization."""

    def __init__(
        self,
        lam=0.01,
        beta=0.01,
        N=50,
        eta_D=1e-2,
        grad_clip_norm=10.0,
        max_iter=1000,
        tol=1e-6,
        lr_decay_factor=0.9,
        lift_fn=None,
        lift_config=None,
        device=None,
        verbose=True,
    ):
        self.lam = lam
        self.beta = beta
        self.N = N
        self.eta_D = eta_D
        self.grad_clip_norm = grad_clip_norm
        self.max_iter = max_iter
        self.tol = tol
        self.lr_decay_factor = lr_decay_factor
        self.lift_fn = lift_fn or lift_function
        self.lift_config = lift_config
        self.verbose = verbose

        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        torch.set_default_dtype(torch.float64)
        if self.verbose:
            print(f"FS-EDMD device: {self.device}")

        self.A_model = None
        self.B_model = None
        self.C_model = None
        self.D_model = None
        self.K = None
        self.D = None
        self.obj_history = []

    def _to_torch(self, array):
        return torch.tensor(array, dtype=torch.float64, device=self.device)

    def _to_numpy(self, tensor):
        return tensor.cpu().detach().numpy()

    def fit(self, X_train, Y_train, U_train, X_Phi_train, Y_Phi_train):
        """Train the augmented Koopman model.

        Inputs follow the existing call convention:
        X/Y of shape (state_dim, n_samples) and U of shape (control_dim, n_samples).
        """
        X_train = np.asarray(X_train, dtype=np.float64)
        Y_train = np.asarray(Y_train, dtype=np.float64)
        U_train = np.asarray(U_train, dtype=np.float64)
        X_Phi_train = np.asarray(X_Phi_train, dtype=np.float64)
        Y_Phi_train = np.asarray(Y_Phi_train, dtype=np.float64)

        n, m = X_train.shape
        p, _ = U_train.shape
        P, _ = X_Phi_train.shape

        if self.verbose:
            print(f"Data dims: n={n}, p={p}, m={m}, P={P}, N={self.N}")

        if self.N >= P:
            self.N = P - 1
            if self.verbose:
                print(f"Warning: N adjusted to {self.N}")

        if self.verbose:
            print("Using PCA to initialize D...")
        try:
            pca = PCA(n_components=self.N)
            pca.fit(X_Phi_train.T)
            D_init = pca.components_.astype(np.float64)
        except Exception as exc:
            if self.verbose:
                print(f"PCA initialization failed ({exc}); using random initialization.")
            D_init = np.random.randn(self.N, P).astype(np.float64) * 0.01

        X_train_t = self._to_torch(X_train)
        Y_train_t = self._to_torch(Y_train)
        U_train_t = self._to_torch(U_train)
        X_Phi_train_t = self._to_torch(X_Phi_train)
        Y_Phi_train_t = self._to_torch(Y_Phi_train)
        D_t = self._to_torch(D_init)

        eta_D_current = self.eta_D
        best_obj = float("inf")
        eye_n_N_p = torch.eye(n + self.N + p, dtype=torch.float64, device=self.device)
        n_plus_N = n + self.N

        if self.verbose:
            print("Starting alternating optimization...")

        for it in range(self.max_iter):
            D_old = D_t.clone()

            W = torch.vstack([X_train_t, D_t @ X_Phi_train_t, U_train_t])
            Y_aug = torch.vstack([Y_train_t, D_t @ Y_Phi_train_t])

            G = W @ W.T + self.beta * eye_n_N_p
            K_t = torch.linalg.solve(G.T, W @ Y_aug.T).T

            K_upper = K_t[:n, :]
            K_lower = K_t[n:, :]

            K1_upper, K2_upper, K3_upper = (
                K_upper[:, :n],
                K_upper[:, n:n_plus_N],
                K_upper[:, n_plus_N:],
            )
            K1_lower, K2_lower, K3_lower = (
                K_lower[:, :n],
                K_lower[:, n:n_plus_N],
                K_lower[:, n_plus_N:],
            )

            R1 = Y_train_t - K1_upper @ X_train_t - K3_upper @ U_train_t
            pred_error_upper = K2_upper @ (D_t @ X_Phi_train_t) - R1
            grad_term1 = K2_upper.T @ pred_error_upper @ X_Phi_train_t.T

            R2 = K1_lower @ X_train_t + K3_lower @ U_train_t
            pred_error_lower = D_t @ Y_Phi_train_t - K2_lower @ (
                D_t @ X_Phi_train_t
            ) - R2
            grad_term2 = (
                pred_error_lower @ Y_Phi_train_t.T
                - K2_lower.T @ pred_error_lower @ X_Phi_train_t.T
            )

            grad_D = grad_term1 + grad_term2 + self.lam * D_t
            grad_norm = torch.linalg.norm(grad_D, ord="fro").item()
            if grad_norm > self.grad_clip_norm:
                grad_D = grad_D * (self.grad_clip_norm / grad_norm)

            D_t = D_t - eta_D_current * grad_D
            D_change = torch.linalg.norm(D_t - D_old, ord="fro").item()

            if it % 10 == 0 or it < 20:
                W_curr = torch.vstack(
                    [X_train_t, D_t @ X_Phi_train_t, U_train_t]
                )
                Y_aug_true = torch.vstack([Y_train_t, D_t @ Y_Phi_train_t])
                Y_aug_pred = K_t @ W_curr

                data_term = (
                    0.5
                    * torch.linalg.norm(Y_aug_true - Y_aug_pred, ord="fro").item()
                    ** 2
                )
                reg_D_term = (
                    0.5 * self.lam * torch.linalg.norm(D_t, ord="fro").item() ** 2
                )
                reg_K_term = (
                    0.5 * self.beta * torch.linalg.norm(K_t, ord="fro").item() ** 2
                )
                current_obj = data_term + reg_D_term + reg_K_term
                self.obj_history.append(current_obj)

                if self.verbose:
                    mse_orig = torch.mean(
                        (Y_train_t - Y_aug_pred[:n, :]) ** 2
                    ).item()
                    print(
                        f"Iter {it}: Obj={current_obj:.6f}, "
                        f"D_Change={D_change:.2e}, MSE_Orig={mse_orig:.6f}"
                    )

                if it > 20 and current_obj > best_obj * (1 + 1e-10):
                    eta_D_current *= self.lr_decay_factor
                    D_t = D_old
                    if self.verbose:
                        print(f"  [Rollback] LR reduced to {eta_D_current:.2e}")
                elif current_obj < best_obj:
                    best_obj = current_obj
                    if it > 20 and len(self.obj_history) > 1:
                        eta_D_current = min(eta_D_current * 1.05, self.eta_D * 10)

            if D_change < self.tol:
                if self.verbose:
                    print(f"Converged at iteration {it}.")
                break

            if torch.any(torch.isnan(D_t)):
                message = "Error: D contains NaN; stopping and rolling back."
                print(message)
                D_t = D_old
                break

        self.K = self._to_numpy(K_t)
        self.D = self._to_numpy(D_t)
        self.A_model = self.K[:, :n_plus_N]
        self.B_model = self.K[:, n_plus_N:]
        self.C_model = np.hstack(
            [
                np.eye(n, dtype=np.float64),
                np.zeros((n, self.N), dtype=np.float64),
            ]
        )
        self.D_model = self.D

        if self.verbose:
            print("Training complete.")
        return self

    def predict(self, x0, u_sequence, steps=None):
        """Run recursive model prediction for the given control sequence."""
        x0 = np.asarray(x0, dtype=np.float64)
        u_sequence = [np.asarray(u, dtype=np.float64) for u in u_sequence]

        n = x0.shape[0]
        T = len(u_sequence) if steps is None else min(steps, len(u_sequence))
        x_pred = np.zeros((T, n), dtype=np.float64)

        phi_0 = self.lift_fn(x0.reshape(1, -1)).flatten().astype(np.float64)
        z_t = np.hstack([x0, self.D_model @ phi_0])

        for t in range(T):
            z_next = self.A_model @ z_t + self.B_model @ u_sequence[t]
            x_next = self.C_model @ z_next
            x_pred[t] = x_next

            phi_next = self.lift_fn(x_next.reshape(1, -1)).flatten().astype(
                np.float64
            )
            z_t = np.hstack([x_next, self.D_model @ phi_next])

        return x_pred

    def save(self, path):
        """Save in the existing pickle schema."""
        model_dict = {
            "A_model": self.A_model,
            "B_model": self.B_model,
            "C_model": self.C_model,
            "D_model": self.D_model,
            "N": self.N,
            "obj_history": self.obj_history,
            "params": {
                "lam": self.lam,
                "beta": self.beta,
                "eta_D": self.eta_D,
                "grad_clip_norm": self.grad_clip_norm,
                "lr_decay_factor": self.lr_decay_factor,
                "lift_config": self.lift_config,
            },
        }
        with open(path, "wb") as handle:
            pickle.dump(model_dict, handle)
        if self.verbose:
            print(f"Model saved to {path}")

    def load(self, path):
        """Load a model produced by the existing pickle schema."""
        with open(path, "rb") as handle:
            model_dict = pickle.load(handle)
        self.A_model = np.asarray(model_dict["A_model"], dtype=np.float64)
        self.B_model = np.asarray(model_dict["B_model"], dtype=np.float64)
        self.C_model = np.asarray(model_dict["C_model"], dtype=np.float64)
        self.D_model = np.asarray(model_dict["D_model"], dtype=np.float64)
        self.N = int(model_dict["N"])
        self.obj_history = model_dict.get("obj_history", [])
        self.lift_config = model_dict.get("params", {}).get("lift_config")
        if isinstance(self.lift_config, dict) and self.lift_config.get("kind") == "soft_lift":
            from modeling.soft_lift import SoftLift

            self.lift_fn = SoftLift.from_config(self.lift_config)
        return self


FSEDMDTrainer = OursKoopmanTrainer
