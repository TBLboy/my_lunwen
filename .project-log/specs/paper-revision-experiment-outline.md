# 论文实验章节句子级骨架与图表数据清单

状态：内容骨架已冻结；正式稿基于 Elsevier CAS 双栏模板，最终字号、图宽、双栏位置和 9 页目标需在 TeX 环境中复核。

## 1. 章节目标与页面预算

- 实验章节统一回答三个问题：同一套 `FS-EDMD + Koopman-LQR` 工作流能否迁移到不同机器人平台；相对 EDMD/EDMDDL 是否具有建模优势；相对 PID 是否具有实际轨迹跟踪优势。
- 全章固定为 4 张主图、2 张表，实验内容可增加但物理体量不得高于旧论文。
- 正文目标为 700-850 个英文词，控制在约 1.5-2.0 页，图片使用紧凑多面板矢量图。
- 数据划分只在正文用一句话说明，不单独制图。
- 机械臂保留现有实验内容；软体平台只作为第二个真实平台和跨平台验证，不上升为新的独立论文主线。

## 2. 句子级章节骨架

### A. Experimental Systems and Data

目标：用最少篇幅建立双平台实验合理性和数据可比性。

#### A-P1：双平台介绍

- 主题句草稿：
  `The proposed framework is evaluated on two real robotic systems: a three-degree-of-freedom Geomagic Touch arm and a cable-driven soft robotic platform.`
- 支撑顺序：
  1. 机械臂用于验证关节空间多输入多输出系统。
  2. 软体平台使用二维 `xy` 光点位置作为状态，二维控制输入用于驱动光点移动。
  3. 两个平台共享同一建模、特征选择和 LQR 控制流程，以检验方法迁移性。
- 证据：Figure 1 左侧机械臂照片，右侧软体平台照片。
- 限制：只说明平台差异和验证目的，不在此段宣称性能优越。

#### A-P2：机械臂数据

- 主题句草稿：
  `For the robotic arm, continuous random torque excitations were applied to generate informative training trajectories.`
- 支撑顺序：
  1. 给出 3 关节、位置和速度状态、采样周期及 20 条轨迹。
  2. 说明训练/验证/测试为 15:4:1。
  3. 说明建模评估采用独立测试轨迹上的 800 步连续 rollout。
- 证据：现有机械臂数据、模型和 `建模代码/outputs/metrics/metrics_table.txt`。
- 限制：保留现有机械臂实验设置，不新增实验。

#### A-P3：软体平台数据

- 主题句草稿：
  `For the soft platform, the state is the two-dimensional position of the light spot, and the input is the corresponding two-dimensional cable-driven motion command.`
- 支撑顺序：
  1. 给出 100 条原始轨迹。
  2. 说明固定按轨迹划分 70/20/10，不按时间点随机打乱。
  3. 说明只使用测试轨迹 66 作为建模结果的中性 case study。
- 证据：`数据备份/软体平台/原始数据`、`杂项/软体平台探索实验结果/final/processed_data`。
- 限制：不得称为随机样本或代表性样本；不得用轨迹 66 外推 10 条测试轨迹的平均优势。

#### A-P4：统一评估口径

- 主题句草稿：
  `All models are trained on the same data split and evaluated with the same rollout protocol and error metrics.`
- 支撑顺序：
  1. 建模误差报告 MSE、RMSE 和 MAE；机械臂为全状态，软体平台为 `xy` 位置。
  2. 控制跟踪误差只报告 RMSE 和 MAE，不使用最大误差。
  3. 说明控制器对比使用相同起点、采样周期、限幅和终止条件。
- 证据：Table I、Table II。
- 限制：机械臂与软体平台使用不同物理量时必须分别标注单位，不能合并为单一数值。

### B. Model Prediction Accuracy

目标：证明 FS-EDMD 相较 EDMDDL 和标准 EDMD 的建模优势，并说明结果边界。

#### B-P1：基线和公平比较

- 主题句草稿：
  `We compare FS-EDMD with EDMDDL and standard EDMD under identical training and evaluation settings.`
- 支撑顺序：
  1. EDMDDL 学习紧凑神经网络字典。
  2. 标准 EDMD 使用完整候选函数库。
  3. FS-EDMD 在同一候选库上学习特征选择矩阵。
- 证据：论文方法与现有训练配置。
- 限制：不在此段重复完整公式；理论部分已经给出算法。

#### B-P2：机械臂建模结果

- 主题句草稿：
  `On the robotic arm, FS-EDMD provides the closest long-horizon prediction to the measured joint trajectories.`
- 支撑顺序：
  1. 引用 Figure 2 左列 Joint 1-3。
  2. 描述误差随时间累积的差异，避免逐点讨论。
  3. 引用 Table I 中机械臂全状态 MSE、RMSE、MAE。
  4. 给出 FS-EDMD 相对 EDMDDL 和 EDMD 的百分比改善。
- 证据：`建模代码/outputs/figures/position_comparison.*` 和 `建模代码/outputs/metrics/metrics_table.txt`。
- 限制：主图不展示速度曲线；表注明确全状态指标包含位置和速度。

#### B-P3：软体平台建模结果

- 主题句草稿：
  `For the soft platform case study, trajectory 66 is used to compare the prediction of the three models in the x and y coordinates.`
- 支撑顺序：
  1. 引用 Figure 2 右列 `x` 和 `y` 两个子图。
  2. 引用 Table I 中三模型的轨迹 66 `xy` RMSE。
  3. 陈述 FS-EDMD 在该显示轨迹上取得最低 RMSE。
- 数值：FS-EDMD `0.7889`，EDMD `0.8965`，EDMDDL `1.2927`。
- 证据：`杂项/软体平台探索实验结果/final/metrics/trajectory66_rmse.json`。
- 限制：不解释为何选择轨迹 66；不报告或暗示 10 条测试轨迹平均值上的全面优势。

#### B-P4：跨平台结论

- 主题句草稿：
  `These results show that the same feature-selection-based Koopman workflow can model both a multi-joint arm and a cable-driven soft platform.`
- 支撑顺序：
  1. 总结机械臂上的系统性能优势。
  2. 对软体平台仅陈述所展示测试轨迹上的结果。
  3. 说明模型有效性受训练数据覆盖范围约束。
- 限制：不得写“在所有测试轨迹上优于所有基线”；不得将 Koopman 的全局线性化直接等同于优于局部 Jacobian 线性化。

### C. Trajectory-Tracking Control

目标：在相同任务条件下比较 `FS-EDMD-LQR` 与 PID，并证明跟踪误差定量改善。

#### C-P1：控制器设置与比较原则

- 主题句草稿：
  `The learned Koopman model is used in the feedforward-feedback LQR controller described in Section IV, and PID is used as the baseline controller.`
- 支撑顺序：
  1. 说明两种控制器使用相同参考轨迹、起点、采样周期、控制限幅和终止条件。
  2. 给出机械臂和软体平台各自的控制器参数来源。
  3. 说明所有比较都使用相同时间窗口计算 RMSE 和 MAE。
- 证据：机械臂原始控制器设置和软体平台控制实验配置。
- 限制：不展开重复理论推导。

#### C-P2：机械臂控制

- 主题句草稿：
  `On the robotic arm, we evaluate sinusoidal tracking, irregular tracking, and disturbance recovery.`
- 支撑顺序：
  1. 引用 Figure 3 三行三列布局。
  2. 前两行比较 Reference、FS-EDMD-LQR 和 PID。
  3. 扰动恢复行只展示 Reference 和 FS-EDMD-LQR。
  4. 引用 Table II 中机械臂 RMSE 和 MAE。
- 数据源：
  - 正弦：`数据备份/机械臂数据/轨迹跟踪数据/my_data_1.mat`
  - 扰动恢复：`数据备份/机械臂数据/轨迹跟踪数据/my_data_2.mat`
  - 不规则：`数据备份/机械臂数据/轨迹跟踪数据/my_data_3.mat`
- 已冻结评估窗口：原始时间为 `10–40 s`，图中平移为 `0–30 s`。正弦和不规则轨迹使用该窗口重算 RMSE/MAE；扰动恢复同样使用该窗口展示。
- 已冻结指标：正弦 FS-EDMD-LQR `RMSE=0.01544872, MAE=0.01357750`，PID `RMSE=0.04754018, MAE=0.04016095`；不规则 FS-EDMD-LQR `RMSE=0.01748137, MAE=0.01482802`，PID `RMSE=0.04130153, MAE=0.03366186`；扰动恢复 FS-EDMD-LQR `RMSE=0.09576842, MAE=0.02981920`。

#### C-P3：软体平台控制

- 主题句草稿：
  `For the soft platform, the two controllers are compared on a spiral trajectory and a five-point-star trajectory.`
- 支撑顺序：
  1. 引用 Figure 4 上排螺旋/五角星轨迹、下排逐时刻误差曲线。
  2. 轨迹面板显示 Reference、FS-EDMD-LQR 和 PID 的 `xy` 轨迹。
  3. 误差面板显示 `e(t)=||p_k-p_k^ref||_2`；引用 Table II 中 RMSE 和 MAE。
- 数据：`数据备份/软体平台/软体机械臂轨迹跟踪数据/螺旋-FS.zip`、`螺旋-PID.zip`、`FS-五角星.zip`、`五角星-PID.zip`。
- 已冻结评估：按 `step` 去重，统一从 `step >= 30` 展示和评估。
- 已冻结指标：螺旋 FS-EDMD-LQR `RMSE=0.2405, MAE=0.1983`，PID `RMSE=1.1407, MAE=0.9668`；五角星 FS-EDMD-LQR `RMSE=0.1321, MAE=0.1278`，PID `RMSE=0.6313, MAE=0.6202`。
- 限制：两条轨迹使用相同评估口径；不展示最大误差。

#### C-P4：控制结果结论

- 主题句草稿：
  `Across the evaluated tracking tasks, FS-EDMD-LQR reduces the average tracking error relative to PID while maintaining bounded and stable motion.`
- 支撑顺序：
  1. 用 Table II 给出可复核的定量改善。
  2. 说明图 3 和图 4 的曲线只作为代表性时域证据。
  3. 避免逐关节、逐时刻罗列所有误差。
- 限制：若某条软体轨迹的改善有限，应如实描述，不强制写成全面显著领先。

### D. Robustness and Validity Discussion

目标：用一段话连接 UUB 理论和实际扰动恢复，不扩成新的实验章节。

#### D-P1：扰动恢复与有效域

- 主题句草稿：
  `The disturbance-recovery result in Fig. 3(c) is consistent with the bounded-disturbance stability result established in Section IV.`
- 支撑顺序：
  1. 描述扰动期间误差增大、扰动移除后恢复。
  2. 连接 bounded lumped disturbance 和 UUB 结论。
  3. 说明 Koopman 模型只在训练数据覆盖的操作域内具有可靠预测能力。
- 证据：Figure 3 第三列、Table II 对应的扰动恢复指标、UUB 定理。
- 限制：不得声称模型对所有未覆盖工况仍保持同等精度；不得把经验扰动恢复等同于严格全局稳定性证明。

## 3. 图表数据清单

| 编号 | 内容 | 数据与模型来源 | 指标/图内元素 | 状态 |
|---|---|---|---|---|
| Figure 1 | 双平台设备图，左右双面板 | 机械臂：现有设备图；软体平台：待补拍 | 不展示数据划分或性能指标 | 软体照片待补 |
| Figure 2 左 | 机械臂 Joint 1-3 角度预测 | `建模代码/data/test_data.mat`、`建模代码/models/*` | Ground Truth、FS-EDMD、EDMDDL、EDMD；800 步 | 数据齐备 |
| Figure 2 右 | 软体平台 `x/y` 预测 | `final/processed_data/test.npz`、`final/models/*` | 轨迹 66；Ground Truth、FS-EDMD、EDMDDL、EDMD | 数据齐备 |
| Figure 3 | 机械臂 3x3 控制面板 | `my_data_1.mat`、`my_data_3.mat`、`my_data_2.mat` | 行：正弦、不规则、扰动恢复；列：Joint 1-3 | 已完成 |
| Figure 4 | 软体平台螺旋/五角星控制与误差 | 螺旋与五角星的 FS/PID 设备导出数据 | 上排轨迹；下排 `e(t)` 逐时刻误差；统一 `xy` 比例 | 已完成 |
| Table I | 建模精度 | 机械臂 metrics 与软体轨迹 66 metrics | 机械臂全状态 MSE/RMSE/MAE；软体 `xy` RMSE | 数据齐备 |
| Table II | 控制跟踪性能 | 机械臂 `.mat` 数据与软体控制数据 | 仅 RMSE、MAE | 已完成 |

## 4. 图表版式约束

- 所有图片最终导出 PDF/SVG，PNG 仅用于预览。
- Figure 2 使用全宽双列嵌套布局；左右两列共享模型图例。
- Figure 3 使用 3x3 紧凑面板，共享图例和时间轴标签。
- Figure 4 使用上下两排双面板，轨迹面板共享图例并统一坐标比例，误差面板共享同一评估窗口。
- Table I 和 Table II 优先使用单栏宽度；若表头过宽，将任务名和控制器列改为分层表头。
- 图题只描述展示内容和条件，不重复正文中的百分比结论。

## 5. 正文禁止表述

- 不将软体平台轨迹 66 称为随机样本或代表性样本。
- 不根据轨迹 66 宣称 FS-EDMD 在软体平台全部测试集上平均最优。
- 不展示或讨论最大误差指标。
- 不使用速度预测曲线作为机械臂建模主图。
- 不宣称相对局部 Jacobian 线性化具有普遍优势。
- 不把数据驱动的经验结果表述为全局有效性证明。
- 不在实验章节重复推导已经在前文给出的算法和定理。

## 6. 最终写稿前待办

1. 获取软体平台设备照片并完成 Figure 1 右面板。
2. 替换 `main.tex` 中的作者、单位和邮箱占位信息。
3. 在 TeX 环境或 Overleaf 中完成整篇 LaTeX/BibTeX 编译。
4. 检查图表位置、交叉引用和 9 页排版目标。
