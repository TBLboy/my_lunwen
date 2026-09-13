"""
训练脚本: 我们的方法 (特征选择矩阵的Koopman表示学习)
核心逻辑: 已升级为 KoopmanEnhancedTrainer (GPU/Float64/自适应学习率)
"""
import numpy as np
import pickle
import torch
import sys
import os
from sklearn.decomposition import PCA

# 假设 lift_function 在上级目录或当前路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lift_function import lift_function

class OursKoopmanTrainer:
    """
    我们的方法: 带特征选择矩阵的Koopman模型
    (框架保持原样，内核已替换为增强版逻辑)
    """

    def __init__(self, lam=0.01, beta=0.01, N=50, eta_D=1e-2,
                 grad_clip_norm=10.0, max_iter=1000, tol=1e-6,
                 lr_decay_factor=0.9, device=None, verbose=True):
        
        # --- 参数保存 ---
        self.lam = lam
        self.beta = beta
        self.N = N
        self.eta_D = eta_D
        self.grad_clip_norm = grad_clip_norm
        self.max_iter = max_iter
        self.tol = tol
        self.lr_decay_factor = lr_decay_factor
        self.verbose = verbose

        # --- 设备与精度配置 (新逻辑) ---
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)

        # 强制设置默认精度为 float64
        torch.set_default_dtype(torch.float64)

        if self.verbose:
            print(f"使用设备: {self.device}")
            if self.device.type == 'cuda':
                print(f"  显存状态: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

        # --- 模型参数初始化 ---
        self.A_model = None
        self.B_model = None
        self.C_model = None
        self.D_model = None
        self.K = None
        self.D = None
        self.obj_history = []

    def _to_torch(self, array):
        """将 numpy 数组转换为 torch tensor，强制 float64"""
        return torch.tensor(array, dtype=torch.float64, device=self.device)

    def _to_numpy(self, tensor):
        """将 tensor 转回 numpy"""
        return tensor.cpu().detach().numpy()

    def fit(self, X_train, Y_train, U_train, X_Phi_train, Y_Phi_train):
        """
        训练入口
        保持旧接口定义，但内部使用新代码的增强训练逻辑
        """
        # 1. 强制输入 Numpy 数据为 float64
        X_train = X_train.astype(np.float64)
        Y_train = Y_train.astype(np.float64)
        U_train = U_train.astype(np.float64)
        X_Phi_train = X_Phi_train.astype(np.float64)
        Y_Phi_train = Y_Phi_train.astype(np.float64)

        n, m = X_train.shape
        p, _ = U_train.shape
        P, _ = X_Phi_train.shape

        if self.verbose:
            print(f"数据维度: n={n}, p={p}, m={m}, P={P}, N={self.N}")

        if self.N >= P:
            self.N = P - 1
            if self.verbose:
                print(f"警告: N 已调整为 {self.N}")

        # --- 2. PCA 初始化 D (带容错机制) ---
        if self.verbose:
            print("使用PCA初始化D矩阵...")
        try:
            pca = PCA(n_components=self.N)
            pca.fit(X_Phi_train.T)
            D_init = pca.components_.astype(np.float64)
        except Exception as e:
            if self.verbose:
                print(f"PCA初始化失败 ({e})，切换为随机初始化。")
            D_init = np.random.randn(self.N, P).astype(np.float64) * 0.01

        # --- 3. 数据转移到 GPU ---
        X_train_t = self._to_torch(X_train)
        Y_train_t = self._to_torch(Y_train)
        U_train_t = self._to_torch(U_train)
        X_Phi_train_t = self._to_torch(X_Phi_train)
        Y_Phi_train_t = self._to_torch(Y_Phi_train)
        D_t = self._to_torch(D_init)

        # 变量初始化
        eta_D_current = self.eta_D
        best_obj = float('inf')
        eye_n_N_p = torch.eye(n + self.N + p, dtype=torch.float64, device=self.device)

        if self.verbose:
            print("开始交替优化 (增强版逻辑)...")

        # --- 4. 优化循环 (完全移植自 New Code) ---
        for t in range(self.max_iter):
            D_old = D_t.clone()

            # === K子问题 ===
            # W: (n + N + p) x m
            W = torch.vstack([X_train_t, D_t @ X_Phi_train_t, U_train_t])
            # Y_aug: (n + N) x m
            Y_aug = torch.vstack([Y_train_t, D_t @ Y_Phi_train_t])
            
            # 使用 solve 求解 K (比 inv 更稳健)
            G = W @ W.T + self.beta * eye_n_N_p
            K_t = torch.linalg.solve(G.T, W @ Y_aug.T).T

            # === D子问题梯度 ===
            # 切片 K
            K_upper = K_t[:n, :]
            K_lower = K_t[n:, :]
            
            n_plus_N = n + self.N
            K1_upper, K2_upper, K3_upper = K_upper[:, :n], K_upper[:, n:n_plus_N], K_upper[:, n_plus_N:]
            K1_lower, K2_lower, K3_lower = K_lower[:, :n], K_lower[:, n:n_plus_N], K_lower[:, n_plus_N:]

            # 梯度项 1 (物理状态误差反传)
            R1 = Y_train_t - K1_upper @ X_train_t - K3_upper @ U_train_t
            pred_error_upper = K2_upper @ (D_t @ X_Phi_train_t) - R1
            grad_term1 = K2_upper.T @ pred_error_upper @ X_Phi_train_t.T

            # 梯度项 2 (特征状态误差反传)
            R2 = K1_lower @ X_train_t + K3_lower @ U_train_t
            pred_error_lower = D_t @ Y_Phi_train_t - K2_lower @ (D_t @ X_Phi_train_t) - R2
            grad_term2 = pred_error_lower @ Y_Phi_train_t.T - K2_lower.T @ pred_error_lower @ X_Phi_train_t.T

            # 总梯度
            grad_D = grad_term1 + grad_term2 + self.lam * D_t

            # 梯度裁剪
            grad_norm = torch.linalg.norm(grad_D, ord='fro').item()
            if grad_norm > self.grad_clip_norm:
                grad_D = grad_D * (self.grad_clip_norm / grad_norm)

            # 更新 D
            D_t = D_t - eta_D_current * grad_D
            D_change = torch.linalg.norm(D_t - D_old, ord='fro').item()

            # === 监控与策略调整 (核心升级点) ===
            # 每 10 次检查一次，或者前 20 次每次都检查
            if t % 10 == 0 or t < 20:
                W_curr = torch.vstack([X_train_t, D_t @ X_Phi_train_t, U_train_t])
                Y_aug_true = torch.vstack([Y_train_t, D_t @ Y_Phi_train_t])
                Y_aug_pred = K_t @ W_curr
                
                # 计算全 Loss (包含 K 的正则项)
                data_term = 0.5 * torch.linalg.norm(Y_aug_true - Y_aug_pred, ord='fro').item() ** 2
                reg_D_term = 0.5 * self.lam * torch.linalg.norm(D_t, ord='fro').item()**2
                reg_K_term = 0.5 * self.beta * torch.linalg.norm(K_t, ord='fro').item()**2
                current_obj = data_term + reg_D_term + reg_K_term
                
                self.obj_history.append(current_obj)

                if self.verbose:
                    mse_orig = torch.mean((Y_train_t - Y_aug_pred[:n, :])**2).item()
                    print(f"Iter {t}: Obj={current_obj:.6f}, D_Change={D_change:.2e}, MSE_Orig={mse_orig:.6f}")

                # === 自适应学习率逻辑 (Bold Driver) ===
                if t > 20 and current_obj > best_obj * (1 + 1e-10):
                    # 变差了 -> 降学习率并回滚
                    eta_D_current *= self.lr_decay_factor
                    D_t = D_old # 回滚！
                    if self.verbose: 
                        print(f"  [回滚] Loss上升，LR降为 {eta_D_current:.2e}")
                elif current_obj < best_obj:
                    # 变好了 -> 更新最佳值，并尝试加速
                    best_obj = current_obj
                    # 如果连续下降且下降幅度不大，尝试激进一点
                    if t > 20 and (len(self.obj_history) > 1):
                        eta_D_current = min(eta_D_current * 1.05, self.eta_D * 10)

            # 收敛检查
            if D_change < self.tol:
                if self.verbose: print(f"收敛于第 {t} 次迭代")
                break
            
            # NaN 熔断保护
            if torch.any(torch.isnan(D_t)):
                print("错误: D 包含 NaN，停止训练并回滚到上一步。")
                D_t = D_old
                break

        # --- 5. 保存结果 (转回 CPU Numpy) ---
        self.K = self._to_numpy(K_t)
        self.D = self._to_numpy(D_t)
        
        n_plus_N = n + self.N
        self.A_model = self.K[:, :n_plus_N]
        self.B_model = self.K[:, n_plus_N:]
        self.C_model = np.hstack([np.eye(n, dtype=np.float64), np.zeros((n, self.N), dtype=np.float64)])
        self.D_model = self.D
        
        if self.verbose: print("训练完成!")

    def predict(self, x0, u_sequence, steps=None):
        """
        预测函数
        (使用 CPU 计算，因为它是顺序执行的，且数据量较小，避免 GPU IO 开销)
        """
        # 强制 Float64
        x0 = x0.astype(np.float64)
        u_sequence = [u.astype(np.float64) for u in u_sequence]
        
        n = x0.shape[0]
        T = len(u_sequence) if steps is None else min(steps, len(u_sequence))
        x_pred = np.zeros((T, n), dtype=np.float64)

        # 初始升维
        phi_0 = lift_function(x0.reshape(1, -1)).flatten().astype(np.float64)
        z_t = np.hstack([x0, self.D_model @ phi_0])

        # 逐步预测
        for t in range(T):
            z_next = self.A_model @ z_t + self.B_model @ u_sequence[t]
            x_next = self.C_model @ z_next
            x_pred[t] = x_next
            
            phi_next = lift_function(x_next.reshape(1, -1)).flatten().astype(np.float64)
            z_t = np.hstack([x_next, self.D_model @ phi_next])

        return x_pred

    def save(self, path):
        """保存模型 (保持旧格式，但增加 params 记录)"""
        model_dict = {
            'A_model': self.A_model, 'B_model': self.B_model,
            'C_model': self.C_model, 'D_model': self.D_model,
            'N': self.N, 'obj_history': self.obj_history,
            'params': {
                'lam': self.lam, 'beta': self.beta, 'eta_D': self.eta_D
            }
        }
        with open(path, 'wb') as f:
            pickle.dump(model_dict, f)
        if self.verbose: print(f"模型已保存到 {path}")

    def load(self, path):
        with open(path, 'rb') as f:
            model_dict = pickle.load(f)
        self.A_model = model_dict['A_model'].astype(np.float64)
        self.B_model = model_dict['B_model'].astype(np.float64)
        self.C_model = model_dict['C_model'].astype(np.float64)
        self.D_model = model_dict['D_model'].astype(np.float64)
        self.N = model_dict['N']


if __name__ == "__main__":
    from utils import load_train_data, get_model_path, get_data_path

    print("=" * 60)
    print("训练我们的方法 (升级版内核: GPU + Adaptive LR)")
    print("=" * 60)

    X_train, Y_train, U_train, meta = load_train_data()

    # 生成特征
    X_Phi = lift_function(X_train).T
    Y_Phi = lift_function(Y_train).T

    # 实例化 (API 保持原样)
    trainer = OursKoopmanTrainer(
        lam=0.001, beta=0.001, N=40,
        eta_D=1e-2, max_iter=2000, tol=1e-6,
        verbose=True
    )

    trainer.fit(X_train.T, Y_train.T, U_train.T, X_Phi, Y_Phi)
    trainer.save(get_model_path('ours_model.pkl'))

    # 保存meta信息
    np.savez(get_model_path('meta.npz'),
             q_scaler=meta['q_scaler'], q_dc=meta['q_dc'],
             u_scaler = meta['u_scaler'], u_dc = meta['u_dc'])