"""
公共工具模块
"""
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import sys

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ==================== 绘图配置 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

# 科技论文绘图参数
COLORS = {
    'truth': '#000000',      # 黑色 - 真实值
    'ours': '#E41A1C',       # 红色 - 我们的方法
    'edmddl': '#377EB8',     # 蓝色 - EDMDDL
    'edmd': '#4DAF4A',       # 绿色 - EDMD
    'nn': '#984EA3',         # 紫色 - NN
}

LINE_STYLES = {
    'truth': '-',
    'ours': '--',
    'edmddl': '-.',
    'edmd': ':',
    'nn': '--',
}

LINEWIDTHS = {
    'truth': 2.0,
    'ours': 1.8,
    'edmddl': 1.8,
    'edmd': 1.8,
    'nn': 1.8,
}

def get_data_path(filename):
    """获取数据文件路径"""
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    return os.path.join(base_dir, filename)

def get_model_path(filename):
    """获取模型保存路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', filename)

def get_figure_path(filename):
    """获取图片保存路径"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures', filename)

def load_train_data():
    """加载训练数据"""
    train_data = sio.loadmat(get_data_path('train_data.mat'))['train_data']

    X_train = train_data[0, 0]['x']
    Y_train = train_data[0, 0]['y']
    U_train = train_data[0, 0]['u']

    meta = {
        'q_scaler': train_data[0, 0]['q_scaler'].flatten(),
        'q_dc': train_data[0, 0]['q_dc'].flatten(),
        'u_scaler': train_data[0, 0]['u_scaler'].flatten(),
        'u_dc': train_data[0, 0]['u_dc'].flatten()
    }

    return X_train, Y_train, U_train, meta

def load_val_data():
    """加载验证数据"""
    val_data = sio.loadmat(get_data_path('val_data.mat'))['val_data']

    X_val = val_data[0, 0]['x_val']
    Y_val = val_data[0, 0]['y_val']
    U_val = val_data[0, 0]['u_val']

    return X_val, Y_val, U_val

def load_test_data():
    """加载测试数据"""
    test_data = sio.loadmat(get_data_path('test_data.mat'))['test_data']

    X_test = test_data[0, 0]['x_test']
    U_test = test_data[0, 0]['u_test']

    return X_test, U_test

def denormalize(x_norm, q_scaler, q_dc):
    """反归一化"""
    return x_norm * q_scaler + q_dc

def calculate_metrics(true, pred):
    """计算评估指标"""
    mse = np.mean((true - pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(true - pred))

    # 各维度RMSE
    rmse_per_dim = np.sqrt(np.mean((true - pred) ** 2, axis=0))

    return {
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'rmse_per_dim': rmse_per_dim
    }

def setup_figure_style():
    """设置科技论文绘图风格"""
    mpl.rc('xtick', labelsize=10, direction='in')
    mpl.rc('ytick', labelsize=10, direction='in')
    mpl.rc('axes', labelsize=11, linewidth=1.0)
    mpl.rc('legend', fontsize=9)
    mpl.rc('lines', linewidth=1.5)
    mpl.rc('grid', alpha=0.3, linestyle='--')
