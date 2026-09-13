"""EDMDDL trainer migrated from the verified train_edmddl.py baseline."""

from __future__ import annotations

import pickle

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class DicNN(nn.Module):
    """ResNet-style dictionary network used by EDMDDL."""

    def __init__(self, input_dim=6, layer_sizes=(512, 512, 512), n_psi_train=50):
        super().__init__()
        self.input_dim = input_dim
        self.layer_sizes = list(layer_sizes)
        self.n_psi_train = n_psi_train

        self.input_layer = nn.Linear(input_dim, self.layer_sizes[0], bias=False)
        self.hidden_layers = nn.ModuleList(
            [
                nn.Linear(
                    self.layer_sizes[i],
                    self.layer_sizes[i + 1]
                    if i < len(self.layer_sizes) - 1
                    else self.layer_sizes[-1],
                )
                for i in range(len(self.layer_sizes))
            ]
        )
        self.output_layer = nn.Linear(self.layer_sizes[-1], n_psi_train)
        self.tanh = nn.Tanh()
        self.double()

    def forward(self, x):
        h = self.input_layer(x)
        for layer in self.hidden_layers:
            if layer.in_features == layer.out_features:
                h = h + self.tanh(layer(h))
            else:
                h = self.tanh(layer(h))
        return self.output_layer(h)


class EDMDDLTrainer:
    """EDMDDL trainer producing a lifted dictionary plus Koopman matrices."""

    def __init__(
        self,
        state_dim=6,
        control_dim=3,
        n_psi=50,
        layer_sizes=(512, 512, 512),
        lr=1e-4,
        reg=1e-6,
        device=None,
    ):
        self.state_dim = state_dim
        self.control_dim = control_dim
        self.n_psi = n_psi
        self.layer_sizes = list(layer_sizes)
        self.lr = lr
        self.reg = reg

        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        torch.set_default_dtype(torch.float64)
        print(f"EDMDDL device: {self.device} (Precision: Float64)")

        self._build_network()
        self.A = None
        self.B = None
        self.loss_history = []

    def _build_network(self):
        self.dic_net = DicNN(self.state_dim, self.layer_sizes, self.n_psi).to(
            self.device
        )
        self.dic_net.double()
        self.psi_dim = 1 + self.state_dim + self.n_psi

    def _lift(self, x):
        batch_size = x.shape[0]
        ones = torch.ones(batch_size, 1, dtype=torch.float64, device=self.device)
        psi = self.dic_net(x)
        return torch.cat([ones, x, psi], dim=1)

    def _compute_K(self, X, Y, U):
        psi_x = self._lift(X)
        psi_y = self._lift(Y)
        psi_xu = torch.cat([psi_x, U], dim=1)

        XtX = psi_xu.T @ psi_xu + self.reg * torch.eye(
            psi_xu.shape[1], dtype=torch.float64, device=self.device
        )
        XtY = psi_xu.T @ psi_y
        K = torch.linalg.solve(XtX, XtY)
        return K, psi_x, psi_y, psi_xu

    def fit(
        self,
        X_train,
        Y_train,
        U_train,
        X_val,
        Y_val,
        U_val,
        epochs=50,
        batch_size=5000,
    ):
        X_t = torch.tensor(X_train, dtype=torch.float64, device=self.device)
        Y_t = torch.tensor(Y_train, dtype=torch.float64, device=self.device)
        U_t = torch.tensor(U_train, dtype=torch.float64, device=self.device)

        X_v = torch.tensor(X_val, dtype=torch.float64, device=self.device)
        Y_v = torch.tensor(Y_val, dtype=torch.float64, device=self.device)
        U_v = torch.tensor(U_val, dtype=torch.float64, device=self.device)

        optimizer = optim.Adam(self.dic_net.parameters(), lr=self.lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, factor=0.8, patience=5
        )

        print(f"Training EDMDDL, epochs={epochs}")
        for epoch in range(epochs):
            self.dic_net.eval()
            with torch.no_grad():
                K, _, _, _ = self._compute_K(X_t, Y_t, U_t)

            self.dic_net.train()
            n_samples = X_t.shape[0]
            indices = torch.randperm(n_samples)
            epoch_loss = 0.0
            n_batches = 0

            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)
                idx = indices[start:end]

                X_batch = X_t[idx]
                Y_batch = Y_t[idx]
                U_batch = U_t[idx]

                optimizer.zero_grad()
                psi_x = self._lift(X_batch)
                psi_y = self._lift(Y_batch)
                psi_xu = torch.cat([psi_x, U_batch], dim=1)
                psi_y_pred = psi_xu @ K
                loss = torch.mean((psi_y - psi_y_pred) ** 2)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            self.loss_history.append(avg_loss)

            self.dic_net.eval()
            with torch.no_grad():
                psi_xv = self._lift(X_v)
                psi_yv = self._lift(Y_v)
                psi_xuv = torch.cat([psi_xv, U_v], dim=1)
                psi_yv_pred = psi_xuv @ K
                val_loss = torch.mean((psi_yv - psi_yv_pred) ** 2).item()

            scheduler.step(val_loss)
            lr_now = optimizer.param_groups[0]["lr"]
            print(
                f"Epoch {epoch + 1}/{epochs}: Train Loss={avg_loss:.8f}, "
                f"Val Loss={val_loss:.8f}, LR={lr_now:.2e}"
            )

        self.dic_net.eval()
        with torch.no_grad():
            K_final, _, _, _ = self._compute_K(X_t, Y_t, U_t)
            K_np = K_final.cpu().numpy()

        self.A = K_np[: self.psi_dim, :]
        self.B = K_np[self.psi_dim :, :]
        print("Training complete.")
        return self

    def save(self, path):
        model_dict = {
            "dic_net_state": self.dic_net.state_dict(),
            "A": self.A,
            "B": self.B,
            "params": {
                "state_dim": self.state_dim,
                "control_dim": self.control_dim,
                "n_psi": self.n_psi,
                "layer_sizes": self.layer_sizes,
                "reg": self.reg,
            },
            "loss_history": self.loss_history,
        }
        with open(path, "wb") as handle:
            pickle.dump(model_dict, handle)
        print(f"Model saved to {path}")

    def load(self, path, device="cpu"):
        self.device = torch.device(device)
        with open(path, "rb") as handle:
            model_dict = pickle.load(handle)
        params = model_dict["params"]
        self.state_dim = params["state_dim"]
        self.control_dim = params["control_dim"]
        self.n_psi = params["n_psi"]
        self.layer_sizes = list(params["layer_sizes"])
        self.reg = float(params.get("reg", self.reg if hasattr(self, "reg") else 1e-6))
        self._build_network()
        self.dic_net.load_state_dict(model_dict["dic_net_state"])
        self.A = np.asarray(model_dict["A"], dtype=np.float64)
        self.B = np.asarray(model_dict["B"], dtype=np.float64)
        self.loss_history = model_dict["loss_history"]
        print(f"Model loaded from {path}")
        return self

    def predict(self, x0, u_sequence, steps=None):
        self.dic_net.eval()
        T = len(u_sequence) if steps is None else min(steps, len(u_sequence))
        n = self.state_dim
        x_pred = np.zeros((T, n), dtype=np.float64)

        x_curr = torch.tensor(
            np.asarray(x0, dtype=np.float64).reshape(1, -1),
            dtype=torch.float64,
            device=self.device,
        )
        A_t = torch.tensor(self.A, dtype=torch.float64, device=self.device)
        B_t = torch.tensor(self.B, dtype=torch.float64, device=self.device)
        C_t = torch.zeros(
            (self.psi_dim, n), dtype=torch.float64, device=self.device
        )
        C_t[1 : n + 1, :] = torch.eye(n, dtype=torch.float64, device=self.device)

        with torch.no_grad():
            for t in range(T):
                u_curr = torch.tensor(
                    np.asarray(u_sequence[t], dtype=np.float64).reshape(1, -1),
                    dtype=torch.float64,
                    device=self.device,
                )
                psi_x = self._lift(x_curr)
                psi_next = psi_x @ A_t + u_curr @ B_t
                x_next = psi_next @ C_t
                x_pred[t] = x_next.cpu().numpy().flatten()
                x_curr = x_next
        return x_pred
