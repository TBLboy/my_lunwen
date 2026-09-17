# 建模代码

本目录是从当前论文材料工程中整理出的自包含建模工程，包含机械臂建模代码、数据、已训练模型和可复现的评估绘图闭环。

## 内容

- `data/`：从 `杂项/data` 复制得到的 `train/val/test_data.mat`
- `models/`：从 `杂项/models` 复制得到的三个模型和 `meta.npz`
- `modeling/`：重构后的 Python 包，包含数据加载、特征库、指标和三个训练器
- `scripts/`：训练入口和统一评估绘图入口
- `outputs/`：评估指标表和位置/速度对比图

运行时只读取本目录下的资源，不依赖 `杂项` 或 `论文3`。

## Python 环境

已验证环境：

```text
C:\Users\Windows\.conda\envs\edmddl2\python.exe
Python 3.10
```

依赖见 `requirements.txt`。

## 运行评估闭环

在 `建模代码` 根目录执行：

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\evaluate_and_plot.py
```

默认完成 800 步预测，输出：

```text
outputs\metrics\metrics_table.txt
outputs\figures\position_comparison.png/pdf/svg
outputs\figures\velocity_comparison.png/pdf/svg
```

## 训练与模型加载检查

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\train_fs_edmd.py
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\train_edmddl.py
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\train_edmd.py
```

只验证项目内模型能否被新代码加载：

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\train_fs_edmd.py --check-load
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\train_edmddl.py --check-load
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\train_edmd.py --check-load
```

## 基线指标

使用项目内复制模型评估得到的结果与 `杂项/figures/metrics_table.txt` 一致：

```text
FS-EDMD  MSE 0.352044  RMSE 0.593333  MAE 0.320238
EDMDDL   MSE 0.593580  RMSE 0.770442  MAE 0.454959
EDMD     MSE 0.725641  RMSE 0.851846  MAE 0.502179
```

## 来源说明

- 基线脚本为当前 `杂项` 中已跑通的绘图脚本和机械臂数据。
- 数据和模型是复制迁移，原 `杂项` 文件未删除、未移动。
- 原 `论文3` 中会发散的旧绘图结果不在本工程中使用。
