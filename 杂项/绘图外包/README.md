# 论文绘图外包材料包

## 1. 目标和给 GPT 的任务

请帮助优化论文中三张实验图的绘图效果，使其更接近高水平期刊排版风格：

- 图面紧凑但信息完整；
- 曲线区分清晰，图例、坐标轴、标题和面板标签可读；
- 适合 CAS 双栏论文排版，缩小后仍可放大查看；
- 不能改变实验数据、评估窗口、RMSE/MAE 指标或论文结论；
- 优先直接修改现有 Python 绘图脚本，并重新生成 `PNG/PDF/SVG`。

当前脚本文件名与论文编号对应关系：

| 脚本/文件前缀 | 论文中对应 | 内容 |
| --- | --- | --- |
| `figure2_modeling_accuracy` | Figure 4 | 机械臂和软体平台建模精度预测 |
| `figure3_control_tracking` | Figure 5 | 机械臂轨迹跟踪控制 |
| `figure4_soft_control_tracking` | Figure 6 | 软体平台轨迹跟踪控制 |

## 2. 材料包结构

本目录按原工程相对路径镜像，外部拿到后可以直接对应运行：

```text
绘图外包/
├── README.md
├── 背景材料/
│   └── manuscript_body.tex          # 论文实验部分和相关正文
├── 建模代码/
│   ├── modeling/                    # Figure 2 依赖的建模 Python 包
│   ├── data/                        # 机械臂 train/val/test 数据
│   ├── models/                      # 机械臂三个已训练模型
│   └── requirements.txt
├── 数据备份/
│   ├── 机械臂数据/轨迹跟踪数据/      # Figure 3 的三个 .mat 文件
│   └── 软体平台/软体机械臂轨迹跟踪数据/ # Figure 6 的 8 字与五角星数据
├── 杂项/
│   ├── 软体平台探索实验结果/final/    # Figure 2 软体平台模型和测试数据
│   └── 正式论文的绘图部分/            # 三份绘图脚本、当前输出和指标 JSON
```

## 3. 论文背景

论文主题是：

- 用 **FS-EDMD**（带可学习特征选择的 Koopman 建模）提升非线性系统建模精度；
- 在设计 **Koopman-LQR 控制器**时使用同一 FS-EDMD 模型；
- 与 **PID** 控制器进行轨迹跟踪对比；
- 在两个不同平台上验证：3-DOF 机械臂和二维光点软体平台。

实验部分需要控制篇幅，目标主稿不超过 9 页 CAS 双栏 PDF。因此三张图必须：

- 占位少；
- 面板合并紧凑；
- 字号在最终 PDF 中不可过小到无法判读，但允许审稿人通过 PDF 放大查看；
- 不能为了压缩而丢失关键曲线或改变指标。

## 4. Figure 2：建模精度

脚本：`杂项/正式论文的绘图部分/plot_figure2_modeling_accuracy.py`

面板结构：

- 左列从上到下：Joint 1、Joint 2、Joint 3 的关节角度预测；
- 右列从上到下：软体平台光点位置的 `x`、`y` 预测轨迹；
- 每条曲线包含：Ground Truth、FS-EDMD、EDMDDL、EDMD；
- 机械臂横轴为时间，软体平台横轴为 step；
- 机械臂展示 800 步 rollout，软体平台展示测试轨迹 66。

约束：

- 不要展示机械臂速度预测图；
- 软体平台展示的是 `x` 和 `y` 各自的一维预测轨迹，不是二维平面轨迹；
- 表格中软体平台只报告 RMSE；
- 已知建模指标：机械臂 FS-EDMD `MSE=0.3520 / RMSE=0.5933 / MAE=0.3202`；软体平台轨迹 66 的 FS-EDMD `RMSE=0.7889`。

## 5. Figure 3：机械臂轨迹跟踪

脚本：`杂项/正式论文的绘图部分/plot_figure3_control_tracking.py`

面板结构：

- 3 行 3 列；
- 行分别为：Sinusoidal、Irregular、Disturbance recovery；
- 列分别为：Joint 1、Joint 2、Joint 3；
- 前两行比较 Reference、FS-EDMD-LQR、PID；
- 第三行只展示 FS-EDMD-LQR 的扰动恢复；
- 统一评估窗口为原始时间 10--40 s，图中显示 0--30 s。

指标口径：

- RMSE/MAE 按三个关节的位置误差联合计算；
- 单位是 rad；
- 当前指标见 `figure3_control_metrics.json`。

## 6. Figure 6：软体平台轨迹跟踪

脚本：`杂项/正式论文的绘图部分/plot_figure4_soft_control_tracking.py`

面板结构：

- 2 行 2 列；
- 上排为轨迹：左边 figure-eight，右边 five-point star；
- 上排必须展示 **完整 Reference、FS-EDMD-LQR、PID 实测轨迹**，不能从中间截断；
- 下排为逐时刻二维欧氏误差：`e(t)=||p_act-p_ref||_2`；
- 下排误差曲线和表格指标统一从 `step >= 30` 开始；
- FS-EDMD-LQR 与 PID 使用相同参考、初始条件、采样周期和输入限幅。

数据处理：

- ZIP 中的文件名为 `tracking_data.csv`；`8字-PID.csv` 是直接 CSV；
- 每份文件末尾会重复最后一步的多余监控行，绘图前按唯一 `step` 去重；
- `8字-PID.csv` 头部写成了 Koopman-LQR，但用户已确认这实际是 PID 数据，指标仍按 PID 使用；
- 不要使用最大误差指标，表格只保留 RMSE 和 MAE。

当前指标见 `figure4_soft_control_metrics.json`：

| 任务 | 控制器 | RMSE | MAE |
| --- | --- | --- | --- |
| Figure-eight | FS-EDMD-LQR | 0.1174 | 0.1135 |
| Figure-eight | PID | 0.6386 | 0.4797 |
| Five-point star | FS-EDMD-LQR | 0.1339 | 0.1294 |
| Five-point star | PID | 0.8406 | 0.6391 |

## 7. 运行方法

已验证本机 Python 环境：

```text
C:\Users\Windows\.conda\envs\edmddl2\python.exe
Python 3.10
```

依赖见 `建模代码/requirements.txt`：

```text
numpy>=1.26
scipy>=1.11
matplotlib>=3.7
torch>=2.0
scikit-learn>=1.3
```

在 `杂项/绘图外包` 根目录运行：

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' -X utf8 '杂项\正式论文的绘图部分\plot_figure2_modeling_accuracy.py'
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' -X utf8 '杂项\正式论文的绘图部分\plot_figure3_control_tracking.py'
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' -X utf8 '杂项\正式论文的绘图部分\plot_figure4_soft_control_tracking.py'
```

每次修改后应同时生成：

- 高分辨率 PNG；
- 矢量 PDF；
- SVG（如需）；
- 对应指标 JSON（Figure 3 和 Figure 6）。

本材料包已在本机用上述命令完整重跑三份脚本，输出指标与源工程一致：

- Figure 2 机械臂 FS-EDMD `RMSE=0.5933`，软体轨迹 66 `RMSE=0.7889`；
- Figure 3 三组机械臂控制 RMSE/MAE 与 `figure3_control_metrics.json` 一致；
- Figure 6 两组软体控制 RMSE/MAE 与 `figure4_soft_control_metrics.json` 一致。

## 8. 当前已完成的工作

- 已统一使用 Times/serif 字体、细边框、轻网格和向内刻度；
- Figure 3 已改为“每行一个实验、每列一个关节”；
- Figure 6 已加入逐时刻误差曲线，并且轨迹面板已改为完整路径、不截断；
- 论文已接入三张图并编译为 9 页 CAS 双栏 PDF。

## 9. 希望 GPT 重点帮助

- 指出当前三张图在科研期刊视觉上最主要的不足；
- 给出一份对绘图脚本的可执行修改建议，不要只讲原则；
- 重点处理：曲线拥挤、线型/颜色区分、图例占位、面板标题层级、坐标轴留白、误差曲线可读性、最终缩小后的字号；
- 如果某个结构需要调整（例如把 Figure 6 改成更紧凑的布局），请给出修改后的完整脚本或清晰 diff；
- 不要重训练模型，不要重采实验数据，不要改动论文中的 RMSE/MAE 数值。

## 10. 状态标注

- 已确认：三张图的用途、面板结构、数据文件、评估窗口、表格指标和 9 页目标。
- 已确认：软体平台 `8字-PID.csv` 和 `五角星-PID.zip` 数据实际来自 PID，尽管导出元数据写成 Koopman-LQR。
- 已确认：在本机 `edmddl2` 环境下，脚本在本目录镜像结构下已完整重跑成功。
- 假设：外部环境安装上述依赖后，脚本同样可运行。
- 需要帮助：如何在“更小图幅”和“最终缩小后仍清晰”之间取得更好的平衡。
