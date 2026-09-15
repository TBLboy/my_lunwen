# Current Session

> 会话恢复入口。维护规则：
> - **头部快照**：顶部“当前状态”区块是稳定入口，每次更新时覆盖，不追加旧版本。
> - **最新在最上**：最新一次会话写在文件最上面的会话区块，旧会话依次向下。
> - **超限归档**：文件超过约 50-100 KB 或会话区块达到约 10 条时，把旧会话区块移动到 `.project-log/docs/archive/`，主文档只保留最近内容。
> - **单一事实源**：精确当前状态与下一步以 `.project-log/loop/handoff.md`、`.project-log/loop/active-run.yaml` 为准；不要在多份长文档里维护互相矛盾的“下一步”。
> - **机器文件不手工重排**：`loop/events.jsonl`、`loop/active-run.yaml`、`loop/handoff.md`、`verification/evidence.yaml` 由运行时维护，不做手工重排或改写。

## 当前状态
- 当前阶段：implementation
- 当前目标：软体平台控制器离线闭环验证（FS-EDMD LQR）
- 当前任务：controller-offline-final（done）
- 当前状态：FS-EDMD LQR 控制器已实现并跑通轨迹 66 离线闭环；修复 x 方向 output_sign 后等待硬件复测
- 后台任务：无
- 活跃决策：DEC-001 个人仓库；DEC-002 机械臂基线决策；DEC-003 建模包结构；DEC-004 软体平台代码与实验输出目录；DEC-005 软体平台实现策略；当前离线控制器选型 Q_x=2500/R=0.4/ff=0.8/u_limit=70
- 阻塞项：无
- 下一步：
  - 用户使用修复后的 `output_sign_x=-1.0` 重新连接真实设备复测
  - 正式离线产物位于 `杂项/软体平台探索实验结果/controller_offline/final/`

## 2026-09-15 会话（软体平台控制代码备份）

- 目标/任务：把软体平台控制代码复制备份到 `控制实验部分代码/软体平台`，源文件不移动、不删除。
- 备份内容：`fs_edmd_lqr_controller.py`、`configs/fs_edmd_lqr_controller.json`、`fs_edmd_lqr_controller_assets/`、控制器依赖的 `tk_assets` 模块、`core/base_algorithm.py`、`scripts/run_fs_edmd_lqr_offline.py`、`requirements.txt`。
- 已新增 `README.md`，说明备份目录结构、离线运行方式和源工程位置。
- 验证：从备份目录直接创建 `FSEDMDLQRController`，模型加载成功，`A:(42,42)`、`B:(42,2)`、`D:(40,112)`，LQR 闭环谱半径 `0.9992`，与源工程一致。

## 2026-09-15 会话（FS-EDMD 控制器硬件方向修复）

- 问题：真实设备上目标在光点右侧时，FS-EDMD LQR 控制的光点反而向左移动；EDMD-Koopman LQR 正常。
- 根因：两个控制器模型内部对 x 控制量的符号约定一致，但硬件 `MOVE` 的 x 方向需要取反；EDMD 配置 `output_sign_x=-1.0`，FS-EDMD 默认误设为 `+1.0`。
- 对照：同一目标在右侧场景，FS-EDMD 修复前输出 `-70`，修复后输出 `+70`；EDMD-Koopman 输出 `+89`。y 方向两个控制器符号一致，无需修改。
- 修复：`FlexibleArmControl34/algorithms/configs/fs_edmd_lqr_controller.json` 与 `fs_edmd_lqr_controller.py` 的默认 `output_sign_x` 改为 `-1.0`。
- 配套：`run_fs_edmd_lqr_offline.py` 现在按输出符号反变换回模型输入控制量，使离线 model-in-the-loop 在硬件符号映射下仍保持一致。
- 验证：目标右侧输出 x>0、左侧 x<0、上方 y>0；`controller-offline-final` 复跑 RMSE 仍为 `0.0461`。

## 2026-09-15 会话（软体平台 FS-EDMD LQR 离线闭环）

- 目标/任务：按论文 Koopman-LQR 设计，实现软体平台 FS-EDMD 控制器，并先在轨迹 66 上完成离线闭环。
- 已实现：`FlexibleArmControl34/algorithms/fs_edmd_lqr_controller.py`、`configs/fs_edmd_lqr_controller.json`、资源目录 `algorithms/fs_edmd_lqr_controller_assets/`，以及 `scripts/run_fs_edmd_lqr_offline.py`。
- 资源：复制 `fs_edmd.pkl`、`meta.npz`、`test.npz` 到控制器资源目录，SHA256 与 final 源文件一致，源文件未移动。
- 离线闭环：被控对象为 FS-EDMD 模型本身（model-in-the-loop），参考轨迹为轨迹 66，共 299 步。
- 最终配置：`Q_x1=Q_x2=2500`、`alpha=0.01`、`R_control=0.4`、`ff_gain=0.8`、`u_limit=70`。
- 最终指标：xy RMSE=0.0461，x RMSE=0.0310，y RMSE=0.0341，最大误差=0.1125，限幅步骤=24/299，闭环谱半径=0.9992。
- 验证：`AlgorithmManager` 已能注册 `FS-EDMD LQR Controller`；最终图 PNG 非空且尺寸 2400x1600；控制器单步调用正常。
- 产物：`杂项/软体平台探索实验结果/controller_offline/final/summary.json`、`tracking_metrics.csv`、`tracking_results.npz`、`figures/trajectory66_fs_edmd_lqr.png/pdf/svg`。
- 说明：离线使用同一模型作为被控对象，结果偏乐观；接硬件前需要按实际执行器限幅和模型偏差再核对 Q/R/ff/u_limit。

## 2026-09-13 会话（软体平台训练结果备份更新）

- 目标/任务：把软体平台三个最新模型整理到 `结果备份/软体平台训练结果`。
- 已更新：`edmd.pkl` 替换为修正版 `runs/soft-edmd-cfix-001/models/edmd.pkl`；`fs_edmd.pkl`、`edmd_dl.pkl`、`meta.npz` 保持最终版本。
- 验证：4 个文件 SHA256 与各自源文件一致。

## 2026-09-13 会话（轨迹66修正版预测图）

- 目标/任务：用修正后的 EDMD 重新绘制轨迹 66 的三模型预测对比图。
- 已完成：重新运行 `plot_soft_trajectory66.py`，轨迹 66 RMSE 更新为 FS-EDMD `0.7889`、EDMD `0.8965`、EDMDDL `1.2927`。
- 产物：`final/figures/trajectory66_comparison.png/pdf/svg` 和 `final/metrics/trajectory66_rmse.csv/json` 已更新；PNG 非空且尺寸 3120x2460。

## 2026-09-13 会话（EDMD预测直线问题修复）

- 目标/任务：检查软体平台 EDMD 预测中 x 分量几乎为直线的问题，确认是不是建模脚本 bug。
- 根因 1：`SoftLift` 的前三列是 `constant, x, y`，但 EDMD 的 `C` 被初始化为 `C[:2] = I`，实际选择的是 `constant, x`。这导致 x 分量取到常数项，看起来就是一条水平直线。
- 根因 2：`SoftLift` 会对状态再做一次中心化和缩放，但 EDMD 预测直接取了升维后的 x/y，没有还原回归一化状态空间，相当于少了一次反变换。
- 修复：`modeling/trainers/edmd.py` 增加 `_build_output_matrix()`，按 `SoftLift.feature_names` 选择 `x/y`；增加 `_from_lift_state()` 还原 `input_center/input_scale`；加载旧模型时也会重建正确的 `C`。
- 修正后轨迹 66：EDMD RMSE 从 `2.4239` 降到 `0.8965`，x 不再是直线；测试集 10 条轨迹平均 RMSE 为 `1.1523`，最高精度为轨迹 77 `0.7355`。
- 影响：修正后的 EDMD 平均 RMSE 低于当前 FS-EDMD 和 EDMDDL。`final` 包仍保留旧指标，等待用户确认是否按修正版更新论文候选。
- 验证：`train_edmd.py --check-load` 通过；`check_soft_experiment_artifacts.py --run-id soft-final-006` 通过；修正版运行记录为 `runs/soft-edmd-cfix-001`。

## 2026-09-13 会话（软体平台训练结果备份）

- 目标/任务：把软体平台训练结果复制到 `结果备份/软体平台训练结果`。
- 已复制（按用户要求）：`fs_edmd.pkl`、`edmd.pkl`、`edmd_dl.pkl` 和归一化文件 `meta.npz`。
- 修正：初始误复制了完整 final 包，随后已清理为仅保留上述 4 项文件。
- 验证：4 个文件 SHA256 与源文件全部一致；源文件未移动或删除。

## 2026-09-13 会话（机械臂训练结果备份）

- 目标/任务：把机械臂已训练的三个模型和归一化文件复制到 `结果备份/机械臂训练结果`。
- 已复制：`ours_model.pkl`、`edmd_model.pkl`、`edmddl_model.pkl`、`meta.npz`，来源为 `建模代码/models`。
- 验证：4 个文件 SHA256 与源目录全部一致；未移动或删除源文件。

## 2026-09-13 会话（处理后的数据同步备份）

- 目标/任务：把软体平台处理后的数据集复制到用户指定的备份目录。
- 已复制：`final/processed_data` 的 `train/validation/test.npz`、`meta.npz`、`split_manifest.json`、`dataset_stats.json` 到 `数据备份/软体平台/处理后的数据`。
- 验证：6 个文件 SHA256 与 final 目录逐一比对一致；未移动或删除原目录文件。

## 2026-09-11 会话（轨迹66论文展示图）

- 目标/任务：按用户确认以轨迹 66 作为论文唯一展示测试轨迹，绘制 FS-EDMD、EDMD、EDMDDL 三个模型在该轨迹上的预测效果对比图。
- 已实现：新增 `建模代码/scripts/plot_soft_trajectory66.py`，直接读取 `final/processed_data` 与 `final/models`，输出 PNG/PDF/SVG 三格式图和轨迹 66 RMSE CSV/JSON。
- 轨迹 66 RMSE：FS-EDMD=0.7889、EDMD=2.4239、EDMDDL=1.2927，与 `final/metrics/test_trajectory.csv` 一致。
- 验证：脚本退出码 0；预测与 final 固定测试集指标一致；PNG 已生成且非空。
- 产物：`杂项/软体平台探索实验结果/final/figures/trajectory66_comparison.png/pdf/svg`；`final/metrics/trajectory66_rmse.csv/json`。

## 2026-09-11 会话（最终候选封装与验证）

- 目标/任务：继续 TASK-017，完成 FS-EDMD 优化器细搜索、最终三模型确认、论文候选封装和闭环验证。
- FS 优化：新增并搜索 `fs_lr_decay_factor`、`fs_grad_clip_norm`；最终验证集最优候选为 `lr_decay=0.9, grad_clip=1.0`，FS 验证集平均 RMSE 降到 1.5772。
- 升维复核：在改进优化器下重新检查 11/13/15 RBF 网格；200 维配置验证集平均 RMSE 更差，因此保留 112 维作为最终配置，已记录在 final README。
- 最终正式运行：`soft-final-006`，FS-EDMD 测试集 avg RMSE=1.5328/best=0.7889（轨迹 66）；EDMD avg=3.1842/best=1.8033；EDMDDL avg=1.4565/best=1.0223。
- 结论：FS-EDMD 保持三者最低单轨迹 RMSE，平均 RMSE 较初始基线明显下降，但仍高于 EDMDDL；该事实已写入 final README。
- 验证：`check_soft_experiment_artifacts.py --run-id soft-final-006`、三模型机械臂 `--check-load`、final 文件哈希比对、`validate_project.py` 和 `loopctl.py validate` 均通过。
- 关键产物：`杂项/软体平台探索实验结果/final/`、`summaries/leaderboard.json`、`search_plans/soft-fs-opt-001*`、`soft-fs-opt2-001*`、`soft-lift-optg-001*`、`soft-final-opt-001*`。

## 2026-09-11 会话（参数搜索执行与升维/FS/EDMDDL 分阶段筛选）

- 目标/任务：按 TASK-017 阶段1 执行 24 组升维库粗搜索，并进入 FS-EDMD N 扫描。
- 已完成：修复 run_soft_search.py 的下划线/连字符参数映射；阶段1 的 24 组运行全部成功，验证集排名已保存到 `search_plans/soft-lift-coarse-001.validation_ranking.csv`。
- 阶段1 结论：验证集 FS-EDMD 平均 RMSE 最优为 soft-lift-015（poly4/grid9/sigma1.0，avg=1.5908），次优为 soft-lift-013（poly4/grid9/sigma0.6，avg=1.6264）。
- 阶段2a 结论：N=40 在两个候选升维上均为验证集平均 RMSE 最优档；排名写入 `search_plans/soft-fs-coarse-001.validation_ranking.csv`。
- 阶段2b 结论：54 组正则网格全部成功；验证集平均最优为 soft-fs-grid-024（sigma=1.0，lam=0.01，beta=0.001，eta_D=0.03，avg=1.5842），最低单轨候选为 soft-fs-grid-022（best=0.5666，avg=1.6184）。
- 修复记录：run_soft_search.py 改为 utf-8-sig 读取 campaign，兼容 PowerShell UTF-8 BOM。
- 阶段3 结论：24 组 EDMDDL-only 全部成功；验证集平均最优为 n_psi=20/layers=256,256/lr=1e-4，avg=1.5973/best=0.7046。
- 阶段4 结论：soft-final-001 在测试集上 FS best=0.7364 仍为最高精度，但 FS avg=1.6315 高于 EDMDDL avg=1.4565；需要继续压低 FS 平均误差。
- 阶段2c/2d 结论：更细 N、更多迭代和升维库单变量细扫均未超过当前验证 avg=1.5842；继续做最后 27 组正则细网格。
- 当前执行：阶段2e 围绕 lam=0.01/beta=0.001/eta_D=0.03 的稍细范围扫描。
- 下一步：若未明显改进，则确认 soft-final-001 为论文候选并进入 final 封装。

## 2026-09-11 会话（参数搜索方案细化与任务拆解）

- 目标/任务：把 soft-base-001 之后的方案研究和任务拆解推进到可执行粒度。
- 已完成：新增 RES-003 粗到细搜索方案；把参数范围、验证/测试纪律和最终筛选规则写入 `杂项/软体平台探索实验结果/search_plans/README.md`；更新 TASK-017 的分阶段执行计划。
- 方案结论：先筛升维库，再筛 FS-EDMD，再筛 EDMDDL；验证集只用于排序，固定 10 条测试轨迹只用于最终候选确认。
- 候选范围：升维 poly/rbf_grid/sigma；FS-EDMD 的 N/lam/beta/eta_D；EDMDDL 的 n_psi/layers/lr。
- 下一步：运行 `search_plans/soft-lift-coarse-001.json` 的第一轮升维库粗搜索；配置文件已生成，训练尚未启动。

## 2026-09-11 会话（软体平台初步闭环与参数搜索推进）

- 目标/任务：推进软体平台建模方案、任务拆解与首轮可复现基线。
- 已完成：软体数据管线、约 200 维升维库、三类模型训练与固定 10 轨迹 RMSE 评估闭环；`soft-base-001` 正式基线已完成；模型可从磁盘重新加载并预测。
- 当前证据：EV-010 固定划分、EV-011 升维检查、EV-012 机械臂兼容、EV-013 base-001 指标、EV-014 模型重载、EV-015 正式 leaderboard。
- 基线指标：FS-EDMD avg=1.6849/best=0.7346；EDMD avg=3.1618/best=1.7267；EDMDDL avg=1.6214/best=0.9860。
- 下一步：进入 TASK-017 粗到细参数搜索，目标是降低 FS-EDMD 平均 RMSE 同时保持最高精度最优。

## 2026-09-11 会话（软体平台方案研究与任务拆解）

- 目标/任务：完成软体平台数据管线、约 200 维升维函数库、三模型训练、10 条测试轨迹评估和探索输出的技术方案与任务拆解。
- 已写入：RES-001 方案研究、ARCH-002 架构、DEC-005 实现策略、TASK-010 至 TASK-016 依赖任务。
- 方案结论：复用现有 modeling 包和 scripts，新增 soft_data/soft_lift 适配，统一使用 run_soft_experiment 入口；实验产物输出到杂项/软体平台探索实验结果。
- 候选特征库：常数/x/y + 多项式到 4 次 + 13x13 RBF + 低频三角，默认约 200 维，先冒烟验证再扩展探索。
- 下一步：开始 TASK-010 工程说明。

## 2026-09-11 会话（软体平台业务澄清与需求固化）

- 目标/任务：澄清新设备软体平台数据建模的范围、数据形态、精度标准和配置筛选规则，并固化 REQ-002。
- 已确认内容：原始数据 100 条 npz、每条 300 步；状态 x 为 2D xy，控制 u 为 2D；数据集划分固定 7:2:1（70/20/10），测试集 10 条；升维函数库约 200 维并包含常数、x、y；训练 FS-EDMD、EDMD、EDMDDL；探索可调整训练参数和升维函数库，不调整数据划分；精度指标为反归一化 xy 位置预测 RMSE。
- 已确认目录约束：软体平台代码放在 `建模代码` 根目录，不创建 `soft_platform` 等子文件夹；训练/评估中间结果输出到 `杂项\软体平台探索实验结果`。
- 已检查技术事实：`处理后的数据` 目录当前为空；线性近似残差 RMSE 约 0.118，需要非线性升维项。
- 已完成记录：Q-005 已确认，BL-SOFT-001 至 BL-SOFT-010、DEC-004、REQ-002 已固化，TASK-009 已完成。
- 下一步：等待用户确认后进入软体平台方案研究和任务分解。

## 2026-09-10 会话（建模代码实施）

- 目标/任务：完成工程规格并实施资源复制、共享模块、三个训练器、统一评估绘图闭环和验证。
- 已完成内容：写入 modeling-refactor-spec.md；复制 杂项/data 与 杂项/models 并做哈希校验；重构 modeling 包与三类训练器；运行短训练冒烟、--check-load、800 步评估和六类图表输出。
- 重要决策：保持原算法和模型 pickle 兼容；训练冒烟写临时路径，不覆盖复制来的基线模型。
- 验证与限制：FS-EDMD MSE 0.352044、EDMDDL MSE 0.593580、EDMD MSE 0.725641，与基线一致；未运行完整 EDMDDL 生产训练，仅验证脚本可生成可加载模型。
- 下一步：任务清单、工作流和证据索引已更新，可按用户需要继续。

## 2026-09-10 会话（建模代码规划）

- 目标/任务：完成建模代码迁移的业务澄清、需求基线、架构决策和任务分解
- 已完成内容：确认迁移范围和基线；冻结 REQ-001；写入 ARCH-001；生成 8 个依赖任务
- 重要决策：当前杂项为基线；交付完整闭环；自包含资源复制不剪切；采用 modeling 包加 scripts 入口
- 验证与限制：Project Log 校验通过；下一步为 TASK-001
- 下一步：开始工程说明，然后依次实施资源复制、共享模块、三训练器、统一闭环和验证

## 2026-09-10 会话（建模代码迁移澄清）

- 目标/任务：澄清并规划将原工程建模代码迁移到当前干净的建模代码目录
- 已完成内容：确认迁移主体包括我们的模型训练代码、EDMD、EDMDDL；检查原工程和当前副本差异
- 重要决策：以当前杂项已跑通版本和机械臂数据为基线；重构交付为完整闭环
- 验证与限制：原工程三类训练脚本与杂项中的三类训练脚本一致；compare_all.py、utils.py、test_data.mat 存在差异
- 下一步：完成需求基线和任务分解

## 2026-09-10 会话（杂项绘图脚本验证）

- 目标/任务：快速验证 `杂项` 内绘图脚本能否使用该目录资源跑通
- 已完成内容：使用 `edmddl2` Python 3.10 环境运行 `compare_all.py`，加载测试数据和三个模型，完成 800 步预测并生成图表
- 重要决策：验证环境采用 `C:\Users\Windows\.conda\envs\edmddl2\python.exe`；已记录验证证据 EV-001
- 验证与限制：退出码 0；FS-EDMD/EDMDDL/EDMD 的 MSE 分别为 0.352044、0.593580、0.725641；控制台中文曾因编码显示为乱码，但文件内容正常
- 下一步：等待用户确认验证结果，或继续定义论文/工程目标

## 2026-09-10 会话（工程初始化）

- 目标/任务：初始化工程
- 已完成内容：创建 `.project-log` 模板，创建根目录 `AGENTS.md`，写入个人仓库规则
- 重要决策：仓库类型：个人仓库
- 验证与限制：Project Log 校验通过；README 仅含项目标题，暂无 `docs`，项目级规则留待补充
- 下一步：等待用户提供论文/工程目标

<!--
会话区块按日期倒序向下追加；超过约 50-100 KB 或约 10 条时归档到
`.project-log/docs/archive/`，归档文件按日期可检索。
-->
