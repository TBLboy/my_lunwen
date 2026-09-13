"""
三种建模方法预测对比脚本
加载训练好的三个模型,在测试集上进行预测对比
方法包括: FS-EDMD (Feature-Selective EDMD), EDMDDL, EDMD
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pickle
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import (load_test_data, get_model_path, get_figure_path,
                   denormalize, calculate_metrics)
from train_ours import OursKoopmanTrainer
from train_edmddl import EDMDDLTrainer
from train_edmd import EDMDTrainer

# ============================================================================
# 绘图参数配置区域 - 可根据期刊要求调整
# ============================================================================
PLOT_CONFIG = {
    # !!!!! 便捷调整区域 - 常用参数集中在此 !!!!!
    'global_font_scale': 1.8,      # 全局字体缩放因子 (默认1.0, 建议1.3-2.0)
    'global_linewidth_scale': 1.6, # 全局线宽缩放因子 (默认1.0, 建议0.8-1.5)
    'legend_columnspacing': 0.9,   # 图例列间距 (默认2.0, 值越小间距越小)
    'legend_vertical_position': 1.06,  # 图例竖直位置 (默认1.02, >1在图上方, <1在图内)
    'legend_handlelength': 0.8,    # 图例线段长度 (默认2.0, 现在减半为1.0)
    'ylabel_horizontal_pad': 10,   # Y轴标签水平距离 (默认4, 值越大距离越远, 单位:点)
    
    # 图片尺寸设置 (英寸)
    'figure_width': 7.0,           # IEEE双栏标准宽度
    'figure_height': 8.0,          # 三子图总高度
    'dpi': 300,                    # 输出分辨率
    
    # 字体设置 (基础大小,会被global_font_scale缩放)
    'font_family': 'Times New Roman',  # IEEE推荐字体
    'font_size_label': 11,         # 坐标轴标签字体大小
    'font_size_tick': 10,          # 刻度字体大小
    'font_size_legend': 9,         # 图例字体大小
    'font_size_title': 12,         # 标题字体大小
    
    # 线条设置 (基础线宽,会被global_linewidth_scale缩放)
    'linewidth_truth': 1.3,        # 真实值线宽 (稍粗)
    'linewidth_prediction': 1.3,   # 预测值线宽
    
    # 颜色设置 (IEEE标准配色)
    'color_truth': '#D62728',      # 红色 - 真实值
    'color_fsedmd': '#000000',     # 黑色 - FS-EDMD
    'color_edmddl': '#FF7F0E',     # 橙色 - EDMDDL
    'color_edmd': '#2CA02C',       # 绿色 - EDMD
    
    # 线型设置
    'linestyle_truth': '-',        # 实线 - 真实值
    'linestyle_fsedmd': '-',       # 实线 - FS-EDMD
    'linestyle_edmddl': '--',      # 虚线 - EDMDDL
    'linestyle_edmd': '-.',        # 点划线 - EDMD
    
    # 网格设置 - 增强可见度
    'grid_alpha': 1,             # 网格透明度 (从0.3增加到0.6)
    'grid_linestyle': '-',         # 网格线型 (从':'改为'-'实线)
    'grid_linewidth': 0.8,         # 网格线宽 (从0.5增加到0.8)
    'grid_color': '#CCCCCC',       # 网格颜色 (浅灰色)
    
    # 图例设置
    'legend_ncol': 4,              # 图例列数
    'legend_framealpha': 0.95,     # 图例背景透明度
    'legend_frameon': False,       # 是否显示图例边框
    'legend_loc': 'upper center',  # 图例位置
    
    # 布局设置
    'subplot_hspace': 0.15,        # 子图垂直间距
    'subplot_top': 0.98,           # 顶部边距
    'subplot_bottom': 0.08,        # 底部边距
    'subplot_left': 0.12,          # 左侧边距
    'subplot_right': 0.98,         # 右侧边距
    
    # Y轴范围调整
    'ylim_margin_ratio': 0.05,     # Y轴上下边距比例 (减小以紧凑显示)
}

# 预测步数
PRED_STEPS = 800

# ============================================================================
# 设置全局绘图样式
# ============================================================================
def setup_plot_style():
    """配置Matplotlib全局绘图样式"""
    scale = PLOT_CONFIG['global_font_scale']
    linewidth_scale = PLOT_CONFIG['global_linewidth_scale']
    
    plt.rcParams.update({
        'font.family': PLOT_CONFIG['font_family'],
        'font.size': PLOT_CONFIG['font_size_tick'] * scale,
        'axes.labelsize': PLOT_CONFIG['font_size_label'] * scale,
        'axes.titlesize': PLOT_CONFIG['font_size_title'] * scale,
        'xtick.labelsize': PLOT_CONFIG['font_size_tick'] * scale,
        'ytick.labelsize': PLOT_CONFIG['font_size_tick'] * scale,
        'legend.fontsize': PLOT_CONFIG['font_size_legend'] * scale,
        'legend.columnspacing': PLOT_CONFIG['legend_columnspacing'],
        'legend.handlelength': PLOT_CONFIG['legend_handlelength'],
        'figure.dpi': 100,
        'savefig.dpi': PLOT_CONFIG['dpi'],
        'axes.linewidth': 1.0,
        'grid.linewidth': PLOT_CONFIG['grid_linewidth'],
        'lines.linewidth': PLOT_CONFIG['linewidth_prediction'] * linewidth_scale,
        'axes.grid': True,
        'grid.alpha': PLOT_CONFIG['grid_alpha'],
        'grid.linestyle': PLOT_CONFIG['grid_linestyle'],
        'grid.color': PLOT_CONFIG['grid_color'],
    })


# ============================================================================
# 模型加载与预测
# ============================================================================
def load_all_models():
    """加载所有训练好的模型"""
    models = {}

    # 加载FS-EDMD (Feature-Selective EDMD)
    print("加载 FS-EDMD (Feature-Selective EDMD)...")
    fsedmd = OursKoopmanTrainer()
    fsedmd.load(get_model_path('ours_model.pkl'))
    models['fsedmd'] = fsedmd

    # 加载EDMDDL
    print("加载 EDMDDL...")
    edmddl = EDMDDLTrainer()
    edmddl.load(get_model_path('edmddl_model.pkl'))
    models['edmddl'] = edmddl

    # 加载EDMD
    print("加载 EDMD...")
    edmd = EDMDTrainer()
    edmd.load(get_model_path('edmd_model.pkl'))
    models['edmd'] = edmd

    return models


def run_predictions(models, X_test, U_test, steps):
    """运行所有模型的预测"""
    predictions = {}
    x0 = X_test[0]

    for name, model in models.items():
        print(f"预测: {name.upper()}...")
        pred = model.predict(x0, U_test, steps=steps)
        predictions[name] = pred

    return predictions


# ============================================================================
# 绘图函数
# ============================================================================
def plot_comparison(X_true, predictions, q_scaler, q_dc, save_path):
    """绘制对比图"""
    setup_plot_style()
    
    scale = PLOT_CONFIG['global_font_scale']
    linewidth_scale = PLOT_CONFIG['global_linewidth_scale']

    # 反归一化
    X_true_denorm = denormalize(X_true, q_scaler, q_dc)
    preds_denorm = {name: denormalize(pred, q_scaler, q_dc)
                    for name, pred in predictions.items()}

    T = X_true_denorm.shape[0]
    t = np.arange(T) * 0.004  # 采样时间0.02s

    # 标签配置
    labels = {
        'truth': 'Ground Truth',
        'fsedmd': 'FS-EDMD',
        'edmddl': 'EDMDDL',
        'edmd': 'EDMD'
    }

    # 颜色配置
    colors = {
        'truth': PLOT_CONFIG['color_truth'],
        'fsedmd': PLOT_CONFIG['color_fsedmd'],
        'edmddl': PLOT_CONFIG['color_edmddl'],
        'edmd': PLOT_CONFIG['color_edmd']
    }

    # 线型配置
    linestyles = {
        'truth': PLOT_CONFIG['linestyle_truth'],
        'fsedmd': PLOT_CONFIG['linestyle_fsedmd'],
        'edmddl': PLOT_CONFIG['linestyle_edmddl'],
        'edmd': PLOT_CONFIG['linestyle_edmd']
    }

    # 线宽配置 - 应用全局线宽缩放
    linewidths = {
        'truth': PLOT_CONFIG['linewidth_truth'] * linewidth_scale,
        'fsedmd': PLOT_CONFIG['linewidth_prediction'] * linewidth_scale,
        'edmddl': PLOT_CONFIG['linewidth_prediction'] * linewidth_scale,
        'edmd': PLOT_CONFIG['linewidth_prediction'] * linewidth_scale
    }

    # ========== 图1: 关节位置对比 (索引0,2,4) ==========
    fig1, axes1 = plt.subplots(3, 1, figsize=(PLOT_CONFIG['figure_width'], 
                                               PLOT_CONFIG['figure_height']))
    joint_names = ['Joint 1', 'Joint 2', 'Joint 3']
    pos_indices = [0, 2, 4]

    for i, idx in enumerate(pos_indices):
        ax = axes1[i]

        # 绘制真实值
        ax.plot(t, X_true_denorm[:, idx], 
                color=colors['truth'],
                linestyle=linestyles['truth'], 
                linewidth=linewidths['truth'],
                label=labels['truth'],
                zorder=5)

        # 绘制各模型预测
        for name in ['fsedmd', 'edmddl', 'edmd']:
            ax.plot(t, preds_denorm[name][:, idx], 
                    color=colors[name],
                    linestyle=linestyles[name], 
                    linewidth=linewidths[name],
                    label=labels[name],
                    alpha=0.85)

        # 设置标签 - 添加水平距离控制
        ax.set_ylabel(f'{joint_names[i]} (rad)', 
                     fontsize=PLOT_CONFIG['font_size_label'] * scale,
                     fontweight='normal',
                     labelpad=PLOT_CONFIG['ylabel_horizontal_pad'])
        
        # 网格设置 - 增强可见度
        ax.grid(True, 
                alpha=PLOT_CONFIG['grid_alpha'], 
                linestyle=PLOT_CONFIG['grid_linestyle'],
                linewidth=PLOT_CONFIG['grid_linewidth'],
                color=PLOT_CONFIG['grid_color'])
        
        # 刻度设置
        ax.tick_params(labelsize=PLOT_CONFIG['font_size_tick'] * scale, 
                      direction='in', 
                      width=1.0,
                      pad=5)  # 增加刻度标签与轴的距离

        # 调整y轴范围
        ymin, ymax = ax.get_ylim()
        margin = (ymax - ymin) * PLOT_CONFIG['ylim_margin_ratio']
        # 第一个子图因为有图例,顶部需要更多空间
        if i == 0:
            ax.set_ylim(ymin - margin, ymax + margin * 3.0)
        else:
            ax.set_ylim(ymin - margin, ymax + margin)

        # !!!!! 关键修改: 统一Y轴刻度标签格式,确保对齐 !!!!!
        # 使用固定格式显示Y轴刻度,小数点后保留2位
        from matplotlib.ticker import FormatStrFormatter
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # 第一个子图添加图例 - 添加列间距和线段长度控制
        if i == 0:
            ax.legend(loc=PLOT_CONFIG['legend_loc'], 
                     bbox_to_anchor=(0.5, PLOT_CONFIG['legend_vertical_position']),
                     ncol=PLOT_CONFIG['legend_ncol'], 
                     fontsize=PLOT_CONFIG['font_size_legend'] * scale, 
                     framealpha=PLOT_CONFIG['legend_framealpha'],
                     frameon=PLOT_CONFIG['legend_frameon'],
                     columnspacing=PLOT_CONFIG['legend_columnspacing'],
                     handlelength=PLOT_CONFIG['legend_handlelength'])

        # 最后一个子图添加x轴标签
        if i == 2:
            ax.set_xlabel('Time (s)', 
                         fontsize=PLOT_CONFIG['font_size_label'] * scale,
                         fontweight='normal')

    # 调整子图布局
    plt.subplots_adjust(hspace=PLOT_CONFIG['subplot_hspace'],
                       top=PLOT_CONFIG['subplot_top'],
                       bottom=PLOT_CONFIG['subplot_bottom'],
                       left=PLOT_CONFIG['subplot_left'],
                       right=PLOT_CONFIG['subplot_right'])
    
    # 保存图片 (多种格式)
    plt.savefig(os.path.join(save_path, 'position_comparison.png'), 
                dpi=PLOT_CONFIG['dpi'], 
                bbox_inches='tight',
                pad_inches=0.05)
    plt.savefig(os.path.join(save_path, 'position_comparison.pdf'), 
                bbox_inches='tight',
                pad_inches=0.05)
    plt.savefig(os.path.join(save_path, 'position_comparison.svg'), 
                bbox_inches='tight',
                pad_inches=0.05)
    print(f"位置对比图已保存到 {save_path} (PNG/PDF/SVG)")
    plt.close()

    # ========== 图2: 关节速度对比 (索引1,3,5) ==========
    fig2, axes2 = plt.subplots(3, 1, figsize=(PLOT_CONFIG['figure_width'], 
                                               PLOT_CONFIG['figure_height']))
    vel_indices = [1, 3, 5]

    for i, idx in enumerate(vel_indices):
        ax = axes2[i]

        # 绘制真实值
        ax.plot(t, X_true_denorm[:, idx], 
                color=colors['truth'],
                linestyle=linestyles['truth'], 
                linewidth=linewidths['truth'],
                label=labels['truth'],
                zorder=5)

        # 绘制各模型预测
        for name in ['fsedmd', 'edmddl', 'edmd']:
            ax.plot(t, preds_denorm[name][:, idx], 
                    color=colors[name],
                    linestyle=linestyles[name], 
                    linewidth=linewidths[name],
                    label=labels[name],
                    alpha=0.85)

        # 设置标签 - 添加水平距离控制
        ax.set_ylabel(f'{joint_names[i]} (rad/s)', 
                     fontsize=PLOT_CONFIG['font_size_label'] * scale,
                     fontweight='normal',
                     labelpad=PLOT_CONFIG['ylabel_horizontal_pad'])
        
        # 网格设置 - 增强可见度
        ax.grid(True, 
                alpha=PLOT_CONFIG['grid_alpha'], 
                linestyle=PLOT_CONFIG['grid_linestyle'],
                linewidth=PLOT_CONFIG['grid_linewidth'],
                color=PLOT_CONFIG['grid_color'])
        
        # 刻度设置
        ax.tick_params(labelsize=PLOT_CONFIG['font_size_tick'] * scale, 
                      direction='in', 
                      width=1.0,
                      pad=5)  # 增加刻度标签与轴的距离

        # 调整y轴范围
        ymin, ymax = ax.get_ylim()
        margin = (ymax - ymin) * PLOT_CONFIG['ylim_margin_ratio']
        # 第一个子图因为有图例,顶部需要更多空间
        if i == 0:
            ax.set_ylim(ymin - margin, ymax + margin * 3.0)
        else:
            ax.set_ylim(ymin - margin, ymax + margin)

        # !!!!! 关键修改: 统一Y轴刻度标签格式,确保对齐 !!!!!
        # 使用固定格式显示Y轴刻度,小数点后保留2位
        from matplotlib.ticker import FormatStrFormatter
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # 第一个子图添加图例 - 添加列间距和线段长度控制
        if i == 0:
            ax.legend(loc=PLOT_CONFIG['legend_loc'], 
                     bbox_to_anchor=(0.5, PLOT_CONFIG['legend_vertical_position']),
                     ncol=PLOT_CONFIG['legend_ncol'], 
                     fontsize=PLOT_CONFIG['font_size_legend'] * scale, 
                     framealpha=PLOT_CONFIG['legend_framealpha'],
                     frameon=PLOT_CONFIG['legend_frameon'],
                     columnspacing=PLOT_CONFIG['legend_columnspacing'],
                     handlelength=PLOT_CONFIG['legend_handlelength'])

        # 最后一个子图添加x轴标签
        if i == 2:
            ax.set_xlabel('Time (s)', 
                         fontsize=PLOT_CONFIG['font_size_label'] * scale,
                         fontweight='normal')

    # 调整子图布局
    plt.subplots_adjust(hspace=PLOT_CONFIG['subplot_hspace'],
                       top=PLOT_CONFIG['subplot_top'],
                       bottom=PLOT_CONFIG['subplot_bottom'],
                       left=PLOT_CONFIG['subplot_left'],
                       right=PLOT_CONFIG['subplot_right'])
    
    # 保存图片 (多种格式)
    plt.savefig(os.path.join(save_path, 'velocity_comparison.png'), 
                dpi=PLOT_CONFIG['dpi'], 
                bbox_inches='tight',
                pad_inches=0.05)
    plt.savefig(os.path.join(save_path, 'velocity_comparison.pdf'), 
                bbox_inches='tight',
                pad_inches=0.05)
    plt.savefig(os.path.join(save_path, 'velocity_comparison.svg'), 
                bbox_inches='tight',
                pad_inches=0.05)
    print(f"速度对比图已保存到 {save_path} (PNG/PDF/SVG)")
    plt.close()

    return X_true_denorm, preds_denorm


# ============================================================================
# 误差指标计算与输出
# ============================================================================
def compute_and_print_metrics(X_true, predictions, q_scaler, q_dc):
    """计算并打印各模型的误差指标"""
    X_true_denorm = denormalize(X_true, q_scaler, q_dc)

    print("\n" + "=" * 80)
    print(" " * 25 + "建模精度对比结果")
    print("=" * 80)

    results = {}
    method_display = {
        'fsedmd': 'FS-EDMD',
        'edmddl': 'EDMDDL',
        'edmd': 'EDMD'
    }

    for name, pred in predictions.items():
        pred_denorm = denormalize(pred, q_scaler, q_dc)
        metrics = calculate_metrics(X_true_denorm, pred_denorm)
        results[name] = metrics

        print(f"\n{method_display[name]}:")
        print(f"  MSE:  {metrics['mse']:.6f}")
        print(f"  RMSE: {metrics['rmse']:.6f}")
        print(f"  MAE:  {metrics['mae']:.6f}")
        print(f"  各维度RMSE: {metrics['rmse_per_dim']}")

    # 打印对比表格
    print("\n" + "-" * 80)
    print(f"{'方法':<15} {'MSE':<15} {'RMSE':<15} {'MAE':<15}")
    print("-" * 80)
    for name in ['fsedmd', 'edmddl', 'edmd']:
        m = results[name]
        print(f"{method_display[name]:<15} {m['mse']:<15.6f} {m['rmse']:<15.6f} {m['mae']:<15.6f}")
    print("-" * 80)

    return results


def save_results_table(results, save_path):
    """保存结果表格到文件"""
    method_display = {
        'fsedmd': 'FS-EDMD',
        'edmddl': 'EDMDDL',
        'edmd': 'EDMD'
    }

    filepath = os.path.join(save_path, 'metrics_table.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(" " * 25 + "建模精度对比结果\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"{'方法':<15} {'MSE':<15} {'RMSE':<15} {'MAE':<15}\n")
        f.write("-" * 80 + "\n")
        for name in ['fsedmd', 'edmddl', 'edmd']:
            m = results[name]
            f.write(f"{method_display[name]:<15} {m['mse']:<15.6f} {m['rmse']:<15.6f} {m['mae']:<15.6f}\n")
        f.write("-" * 80 + "\n")

        f.write("\n各维度RMSE详细信息:\n")
        f.write("维度: q1, dq1, q2, dq2, q3, dq3\n\n")
        for name in ['fsedmd', 'edmddl', 'edmd']:
            rmse_str = ', '.join([f'{v:.6f}' for v in results[name]['rmse_per_dim']])
            f.write(f"{method_display[name]}: [{rmse_str}]\n")

    print(f"\n结果表格已保存到: {filepath}")


# ============================================================================
# 主程序
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print(" " * 20 + "三种建模方法预测对比实验")
    print(" " * 15 + "FS-EDMD vs EDMDDL vs EDMD")
    print("=" * 80)

    # 加载测试数据
    print("\n[1/5] 加载测试数据...")
    X_test, U_test = load_test_data()
    print(f"      测试数据形状: X_test={X_test.shape}, U_test={U_test.shape}")

    # 加载归一化参数
    print("\n[2/5] 加载归一化参数...")
    meta = np.load(get_model_path('meta.npz'))
    q_scaler = meta['q_scaler']
    q_dc = meta['q_dc']
    print("      归一化参数加载完成")

    # 加载模型
    print("\n[3/5] 加载训练好的模型...")
    models = load_all_models()
    print("      所有模型加载完成")

    # 运行预测
    print(f"\n[4/5] 运行 {PRED_STEPS} 步预测...")
    predictions = run_predictions(models, X_test, U_test, PRED_STEPS)
    print("      预测完成")

    # 获取真实值
    X_true = X_test[:PRED_STEPS]

    # 绘制对比图
    print("\n[5/5] 生成对比图表...")
    save_path = os.path.dirname(get_figure_path(''))
    plot_comparison(X_true, predictions, q_scaler, q_dc, save_path)

    # 计算并打印指标
    results = compute_and_print_metrics(X_true, predictions, q_scaler, q_dc)

    # 保存结果表格
    save_results_table(results, save_path)

    print("\n" + "=" * 80)
    print(" " * 30 + "实验完成!")
    print("=" * 80)
    print(f"\n结果保存位置: {save_path}")
    print(f"  - position_comparison.png/pdf/svg")
    print(f"  - velocity_comparison.png/pdf/svg")
    print(f"  - metrics_table.txt")
    print("\n")