"""
训练脚本: 标准EDMD方法 (使用完整基函数库)
"""
import numpy as np
import pickle
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lift_function import lift_function


class EDMDTrainer:
    """标准EDMD: 使用完整基函数库"""

    def __init__(self, reg=1e-6):
        self.reg = reg
        self.A = None
        self.B = None
        self.C = None
        self.psi_dim = None

    def fit(self, X_train, Y_train, U_train):
        """训练EDMD模型"""
        print("计算升维特征...")
        psi_x = lift_function(X_train)  # (m, P)
        psi_y = lift_function(Y_train)  # (m, P)

        self.psi_dim = psi_x.shape[1]
        print(f"升维维度: {self.psi_dim}")

        # 扩展: [psi_x, u]
        psi_xu = np.hstack([psi_x, U_train])  # (m, P+p)

        print("求解Koopman矩阵...")
        # K = (X'X + reg*I)^{-1} X'Y
        XtX = psi_xu.T @ psi_xu + self.reg * np.eye(psi_xu.shape[1])
        XtY = psi_xu.T @ psi_y
        K = np.linalg.solve(XtX, XtY)  # (P+p, P)

        self.A = K[:self.psi_dim, :]  # (P, P)
        self.B = K[self.psi_dim:, :]  # (p, P)

        # C矩阵: 从psi提取x (假设psi的前几维包含原始状态)
        # lift_function输出: [q1, dq1, q2, dq2, q3, dq3, 1, ...]
        n = X_train.shape[1]
        self.C = np.zeros((self.psi_dim, n))
        self.C[:n, :] = np.eye(n)

        # 计算训练误差
        psi_y_pred = psi_xu @ K
        train_mse = np.mean((psi_y - psi_y_pred) ** 2)
        print(f"训练MSE: {train_mse:.6f}")

        print("训练完成!")

    def predict(self, x0, u_sequence, steps=None):
        """多步预测"""
        T = len(u_sequence) if steps is None else min(steps, len(u_sequence))
        n = x0.shape[0]

        x_pred = np.zeros((T, n))
        psi_curr = lift_function(x0.reshape(1, -1)).flatten()

        K = np.vstack([self.A, self.B])

        for t in range(T):
            u_curr = u_sequence[t]
            psi_xu = np.hstack([psi_curr, u_curr])
            psi_next = psi_xu @ K
            x_next = psi_next @ self.C

            x_pred[t] = x_next
            psi_curr = psi_next

        return x_pred

    def save(self, path):
        model_dict = {
            'A': self.A, 'B': self.B, 'C': self.C,
            'psi_dim': self.psi_dim, 'reg': self.reg
        }
        with open(path, 'wb') as f:
            pickle.dump(model_dict, f)
        print(f"模型已保存到 {path}")

    def load(self, path):
        with open(path, 'rb') as f:
            model_dict = pickle.load(f)
        self.A = model_dict['A']
        self.B = model_dict['B']
        self.C = model_dict['C']
        self.psi_dim = model_dict['psi_dim']


if __name__ == "__main__":
    from utils import load_train_data, get_model_path

    print("=" * 60)
    print("训练标准EDMD (完整基函数库)")
    print("=" * 60)

    X_train, Y_train, U_train, meta = load_train_data()

    trainer = EDMDTrainer(reg=1e-6)
    trainer.fit(X_train, Y_train, U_train)
    trainer.save(get_model_path('edmd_model.pkl'))

    print("训练完成!")