"""
训练脚本: EDMDDL (融合优化版)
特点: 
1. 使用 ResNet 风格的字典网络 (来自新代码)
2. 使用 持续状态的优化器 (来自旧代码)
3. 全程 Float64 精度
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import pickle
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 全局 Float64
torch.set_default_dtype(torch.float64)

class DicNN(nn.Module):
    """
    [移植自新代码] 带有残差连接的字典网络
    ResNet 结构能更好地支持深层网络训练
    """
    def __init__(self, input_dim=6, layer_sizes=[512, 512, 512], n_psi_train=50):
        super(DicNN, self).__init__()
        
        self.input_dim = input_dim
        self.layer_sizes = layer_sizes
        self.n_psi_train = n_psi_train
        
        # 输入层
        self.input_layer = nn.Linear(input_dim, layer_sizes[0], bias=False)
        
        # 隐藏层 (注意：为了使用残差连接，输入输出维度必须相同)
        # 这里我们假设所有隐藏层维度一致，这在 EDMDDL 中很常见
        self.hidden_layers = nn.ModuleList([
            nn.Linear(layer_sizes[i], layer_sizes[i+1] if i < len(layer_sizes)-1 else layer_sizes[-1])
            for i in range(len(layer_sizes))
        ])
        
        # 输出层
        self.output_layer = nn.Linear(layer_sizes[-1], n_psi_train)
        self.tanh = nn.Tanh()

        self.double()

    def forward(self, x):
        # 输入层
        h = self.input_layer(x)
        
        # 隐藏层 (ResNet Block: h = h + tanh(Wx))
        for layer in self.hidden_layers:
            # 只有当输入输出维度一致时才能加残差，否则直接变换
            if layer.in_features == layer.out_features:
                h = h + self.tanh(layer(h))
            else:
                h = self.tanh(layer(h))
                
        return self.output_layer(h)


class EDMDDLTrainer:
    """EDMDDL 训练器 (基于旧代码框架优化)"""

    def __init__(self, state_dim=6, control_dim=3, n_psi=50,
                 layer_sizes=[512, 512, 512], lr=1e-4, reg=1e-6, device=None):
        
        self.state_dim = state_dim
        self.control_dim = control_dim
        self.n_psi = n_psi
        self.layer_sizes = layer_sizes
        self.lr = lr
        self.reg = reg

        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)

        print(f"使用设备: {self.device} (Precision: Float64)")

        self._build_network()
        self.A = None
        self.B = None
        self.loss_history = []

    def _build_network(self):
        self.dic_net = DicNN(self.state_dim, self.layer_sizes, self.n_psi).to(self.device)
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

        # 岭回归求解 K
        # K 的形状: (psi_dim + control_dim) x psi_dim
        XtX = psi_xu.T @ psi_xu + self.reg * torch.eye(psi_xu.shape[1], dtype=torch.float64, device=self.device)
        XtY = psi_xu.T @ psi_y
        
        # 使用 solve (比 pinv 更稳定且快)
        K = torch.linalg.solve(XtX, XtY)
        return K, psi_x, psi_y, psi_xu

    def fit(self, X_train, Y_train, U_train, X_val, Y_val, U_val, epochs=50, batch_size=5000):
        # 强制 Float64
        X_t = torch.tensor(X_train, dtype=torch.float64, device=self.device)
        Y_t = torch.tensor(Y_train, dtype=torch.float64, device=self.device)
        U_t = torch.tensor(U_train, dtype=torch.float64, device=self.device)

        X_v = torch.tensor(X_val, dtype=torch.float64, device=self.device)
        Y_v = torch.tensor(Y_val, dtype=torch.float64, device=self.device)
        U_v = torch.tensor(U_val, dtype=torch.float64, device=self.device)

        # 优化器只初始化一次 (保持动量！)
        optimizer = optim.Adam(self.dic_net.parameters(), lr=self.lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.8, patience=5)

        print(f"开始训练 EDMDDL (ResNet架构), epochs={epochs}")

        for epoch in range(epochs):
            # 1. 更新 K (闭式解)
            self.dic_net.eval()
            with torch.no_grad():
                K, _, _, _ = self._compute_K(X_t, Y_t, U_t)

            # 2. 更新网络 (梯度下降)
            self.dic_net.train()
            n_samples = X_t.shape[0]
            indices = torch.randperm(n_samples)

            epoch_loss = 0
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
                
                # 预测 Loss
                psi_y_pred = psi_xu @ K
                loss = torch.mean((psi_y - psi_y_pred) ** 2)

                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            self.loss_history.append(avg_loss)

            # 3. 验证
            self.dic_net.eval()
            with torch.no_grad():
                # 为了验证准确，这里通常使用当前的 K 或重新计算 K
                # 这里我们复用当前的 K 进行验证，这是常见的做法
                psi_xv = self._lift(X_v)
                psi_yv = self._lift(Y_v)
                psi_xuv = torch.cat([psi_xv, U_v], dim=1)
                psi_yv_pred = psi_xuv @ K
                val_loss = torch.mean((psi_yv - psi_yv_pred) ** 2).item()

            scheduler.step(val_loss)
            
            if (epoch+1) % 1 == 0:
                lr_now = optimizer.param_groups[0]['lr']
                print(f"Epoch {epoch+1}/{epochs}: Train Loss={avg_loss:.8f}, Val Loss={val_loss:.8f}, LR={lr_now:.2e}")

        # 训练结束，保存最终矩阵
        self.dic_net.eval()
        with torch.no_grad():
            K_final, _, _, _ = self._compute_K(X_t, Y_t, U_t)
            K_np = K_final.cpu().numpy()

        self.A = K_np[:self.psi_dim, :]
        self.B = K_np[self.psi_dim:, :]
        print("训练完成!")

    def save(self, path):
        model_dict = {
            'dic_net_state': self.dic_net.state_dict(),
            'A': self.A, 'B': self.B,
            'params': {
                'state_dim': self.state_dim, 'control_dim': self.control_dim,
                'n_psi': self.n_psi, 'layer_sizes': self.layer_sizes, 'reg': self.reg
            },
            'loss_history': self.loss_history
        }
        with open(path, 'wb') as f:
            pickle.dump(model_dict, f)
        print(f"模型已保存到 {path}")

    def load(self, path, device='cpu'):
        self.device = torch.device(device)
        with open(path, 'rb') as f:
            model_dict = pickle.load(f)
        params = model_dict['params']
        self.state_dim = params['state_dim']
        self.control_dim = params['control_dim']
        self.n_psi = params['n_psi']
        self.layer_sizes = params['layer_sizes']
        self._build_network()
        self.dic_net.load_state_dict(model_dict['dic_net_state'])
        self.A = model_dict['A'].astype(np.float64)
        self.B = model_dict['B'].astype(np.float64)
        self.loss_history = model_dict['loss_history']
        print(f"模型已从 {path} 加载")

    def predict(self, x0, u_sequence, steps=None):
        self.dic_net.eval()
        T = len(u_sequence) if steps is None else min(steps, len(u_sequence))
        n = self.state_dim
        x_pred = np.zeros((T, n), dtype=np.float64)
        
        x_curr = torch.tensor(x0.reshape(1, -1), dtype=torch.float64, device=self.device)
        A_t = torch.tensor(self.A, dtype=torch.float64, device=self.device)
        B_t = torch.tensor(self.B, dtype=torch.float64, device=self.device)
        C_t = torch.zeros((self.psi_dim, n), dtype=torch.float64, device=self.device)
        C_t[1:n+1, :] = torch.eye(n, dtype=torch.float64, device=self.device)

        with torch.no_grad():
            for t in range(T):
                u_curr = torch.tensor(u_sequence[t].reshape(1, -1), dtype=torch.float64, device=self.device)
                psi_x = self._lift(x_curr)
                psi_next = psi_x @ A_t + u_curr @ B_t
                x_next = psi_next @ C_t
                x_pred[t] = x_next.cpu().numpy().flatten()
                x_curr = x_next
        return x_pred

if __name__ == "__main__":
    from utils import load_train_data, load_val_data, get_model_path

    print("=" * 60)
    print("训练 EDMDDL (融合版: ResNet架构 + 稳定训练流)")
    print("=" * 60)

    X_train, Y_train, U_train, meta = load_train_data()
    X_val, Y_val, U_val = load_val_data()

    # 数据强制 Float64
    X_train = X_train.astype(np.float64)
    Y_train = Y_train.astype(np.float64)
    U_train = U_train.astype(np.float64)

    # 注意：使用了新代码中的网络配置 (更深的网络，6层)
    trainer = EDMDDLTrainer(
        state_dim=6, control_dim=3, n_psi=50,
        layer_sizes=[512, 512, 512, 512, 512, 512], 
        lr=1e-4, reg=1e-6
    )

    trainer.fit(X_train, Y_train, U_train, X_val, Y_val, U_val, epochs=50, batch_size=5000)
    trainer.save(get_model_path('edmddl_model.pkl'))