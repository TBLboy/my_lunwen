# Progress

> 面向人的阶段进度摘要。维护规则：
> - **最新在最上**：按日期倒序排列，最新阶段段落位于文件顶部，旧段落依次向下。
> - **头部快照**：顶部“当前状态”区块是稳定入口，每次更新时覆盖，不追加旧版本。
> - **超限归档**：文件超过约 50-100 KB 时，把旧段落移动到 `.project-log/docs/archive/`，主文档只保留最近内容。
> - **单一事实源**：本文件是快速摘要；精确当前状态与下一步以 `.project-log/loop/handoff.md`、`.project-log/loop/active-run.yaml` 为准。
> - **机器文件不手工重排**：`loop/events.jsonl`、`loop/active-run.yaml`、`loop/handoff.md`、`verification/evidence.yaml` 由运行时维护，不做手工重排或改写。

## 当前状态
- 当前阶段：implementation
- 当前任务：TASK-017 已完成
- 当前状态：EDMD 预测直线问题已修复；`soft-final-006` 的 EDMD 旧指标已失效，修正版指标待确认是否覆盖 final
- 最近验证：EV-017 至 EV-019 已记录；Project Log、Loop、模型重载和 final 哈希校验通过
- 下一步：
  - 轨迹 66 已确定为论文固定展示轨迹，三模型对比图已输出到 `final/figures/`
  - 确认是否用修正版 EDMD 更新 final 指标、模型和论文展示图
  - 使用 final 中的模型、配置和指标继续论文写作
  - 如后续需要提升 FS-EDMD 平均 RMSE，再开启新的探索任务

## 2026-09-13 轨迹66修正版预测图

- 状态：已完成
- 完成内容：用修正版 EDMD 重新生成轨迹 66 三模型对比图
- 轨迹 66 RMSE：FS-EDMD `0.7889`、EDMD `0.8965`、EDMDDL `1.2927`
- 产物：`final/figures/trajectory66_comparison.png/pdf/svg`；`final/metrics/trajectory66_rmse.csv/json` 已同步
- 验证：PNG 非空，尺寸 3120x2460

## 2026-09-13 EDMD预测直线问题修复

- 状态：代码已修复，final 指标待用户确认
- 根因：EDMD `C` 选错升维列，且未还原 `SoftLift` 的内部状态归一化
- 修正后测试集：EDMD avg=1.1523、best=0.7355（轨迹 77）；轨迹 66 RMSE=0.8965
- 验证：机械臂 EDMD 兼容、软体模型重载、修正版运行 `soft-edmd-cfix-001` 均通过
- 限制：修正后的 EDMD 平均 RMSE 低于 FS-EDMD 和 EDMDDL，尚未覆盖 final 包

## 2026-09-13 软体平台训练结果备份

- 状态：已完成
- 完成内容：将软体平台训练好的三个模型与归一化文件复制到 `结果备份/软体平台训练结果`
- 文件：`fs_edmd.pkl`、`edmd.pkl`、`edmd_dl.pkl`、`meta.npz`
- 修正：初始误复制完整 final 包，已清理为仅保留上述 4 项文件
- 验证：4 个文件 SHA256 与源文件一致；原目录未移动、未删除

## 2026-09-13 机械臂训练结果备份

- 状态：已完成
- 完成内容：将 `建模代码/models` 的机械臂三模型与归一化文件复制到 `结果备份/机械臂训练结果`
- 文件：`ours_model.pkl`、`edmd_model.pkl`、`edmddl_model.pkl`、`meta.npz`
- 验证：4 个文件 SHA256 与源目录一致；原目录未移动、未删除

## 2026-09-13 处理后的数据同步备份

- 状态：已完成
- 完成内容：将 `final/processed_data` 的 6 个文件复制到 `数据备份/软体平台/处理后的数据`
- 验证：所有文件 SHA256 与 final 源目录一致；原目录未移动、未删除

## 2026-09-11 轨迹66论文展示图

- 状态：已完成
- 完成内容：新增 `建模代码/scripts/plot_soft_trajectory66.py`，从 final 数据和模型生成轨迹 66 三模型预测对比图
- 轨迹 66 RMSE：FS-EDMD=0.7889、EDMD=2.4239、EDMDDL=1.2927
- 交付：`final/figures/trajectory66_comparison.png/pdf/svg` 与 `final/metrics/trajectory66_rmse.csv/json`
- 验证：脚本运行成功，RMSE 与 final 固定测试集逐轨迹表一致

## 2026-09-11 最终候选封装与验证

- 状态：已完成
- 完成内容：FS 优化器稳定性参数搜索、优化器局部搜索、200 维附近升维复核、3 组正式三模型确认、leaderboard 刷新、final 目录封装
- 最终候选：`soft-final-006`
- 最终指标：FS-EDMD avg=1.5328/best=0.7889（轨迹 66）；EDMD avg=3.1842/best=1.8033；EDMDDL avg=1.4565/best=1.0223
- 结论：FS-EDMD 保持三者最低单轨迹 RMSE；平均 RMSE 较初始基线改善但仍高于 EDMDDL，已在 final README 明确记录
- 交付：`杂项/软体平台探索实验结果/final/`，包含模型、配置、固定划分数据、逐轨迹指标、排行榜和复现命令
- 验证：模型重载有限值预测、三模型机械臂 `--check-load`、哈希比对、`validate_project.py`、`loopctl.py validate` 全部通过

## 2026-09-11 参数搜索执行与最终候选确认

- 状态：阶段1/2a/2b/3 完成，阶段4 进行中
- 完成内容：修复 run_soft_search.py 参数映射与 UTF-8 BOM；24 组升维库、8 组 N 扫描、54 组正则网格、24 组 EDMDDL 全部成功；生成四份验证集排名 CSV
- 最优升维候选：soft-lift-015（poly4/grid9/sigma1.0，FS 验证 avg=1.5908）、soft-lift-013（poly4/grid9/sigma0.6，FS 验证 avg=1.6264）
- FS 候选：soft-fs-grid-024（avg=1.5842/best=0.8418）、soft-fs-grid-022（avg=1.6184/best=0.5666）、soft-fs-grid-041（sigma=0.6 候选）
- EDMDDL 候选：n_psi=20/layers=256,256/lr=1e-4，验证 avg=1.5973/best=0.7046
- 当前后台：PID=19192，soft-final-001，3 组三模型正式候选
- 下一步：刷新 leaderboard，封装论文 final

## 2026-09-11 参数搜索方案细化与任务拆解

- 状态：方案研究已完成，任务已细化到可执行阶段
- 完成内容：新增 RES-003；创建 `杂项/软体平台探索实验结果/search_plans/README.md` 和 `soft-lift-coarse-001.json`；更新 TASK-017 为五个阶段
- 方案要点：升维库粗搜索 -> FS-EDMD N/正则/eta_D -> EDMDDL 细搜索 -> 三模型正式候选 -> final 封装
- 纪律：粗搜只读验证集；固定 10 条测试轨迹只在最终候选确认时使用
- 下一步：运行 TASK-017 阶段1 的升维库 24 组粗搜索，配置文件已就绪

## 2026-09-11 软体平台初步闭环与参数搜索推进

- 状态：当前基线已完成，参数搜索待推进
- 完成内容：数据准备与固定划分、200 维软体升维库、三模型统一实验入口、固定 10 轨迹 RMSE 评估、正式汇总表、模型独立重载校验
- 基线运行：`soft-base-001`
- 指标：FS-EDMD avg=1.6849/best=0.7346；EDMD avg=3.1618/best=1.7267；EDMDDL avg=1.6214/best=0.9860
- 限制：soft-base-001 尚未完成参数搜索，不是论文最终配置
- 下一步：W 从 FS-EDMD 的 N/正则/eta_D 和升维 RBF/多项式开始粗搜索，再细化 EDMDDL 网络与学习率

## 2026-09-11 软体平台方案研究与任务拆解

- 状态：已完成
- 完成内容：完成 RES-001 技术方案、ARCH-002 架构、DEC-005 实现策略，以及 TASK-010 至 TASK-016 任务拆解
- 方案要点：复用现有训练器，新增 soft_data/soft_lift 与统一实验入口；候选 200 维升维函数库先冒烟验证
- 验证与限制：数据统计与现有代码接口已查阅；尚未开始工程说明和建模代码实现
- 下一步：开始 TASK-010 工程说明

## 2026-09-11 软体平台建模澄清

- 状态：已完成
- 完成内容：确认固定 7:2:1 划分；确认状态 x/控制 u 为 2D；确认升维函数库约 200 维且含常数、x、y；确认 FS-EDMD、EDMD、EDMDDL 训练探索；确认 10 条测试轨迹和 xy RMSE 精度口径；确认代码放建模代码根目录、中间结果放杂项/软体平台探索实验结果
- 已写入：BL-SOFT-001 至 BL-SOFT-010、DEC-004、REQ-002、TASK-009
- 限制：尚未开始建模代码；具体确定性划分种子将在实现时冻结并记录
- 下一步：等待用户确认后进入方案研究和任务分解

## 2026-09-10 建模代码实施

- 状态：已完成
- 完成内容：资源复制、modeling 包重构、FS-EDMD/EDMDDL/EDMD 训练器、scripts/evaluate_and_plot.py、README 与依赖清单
- 验证：三个 --check-load 通过；三个短训练冒烟生成可加载临时模型；800 步评估输出指标与杂项/figures/metrics_table.txt 一致
- 限制：未运行完整 EDMDDL 生产训练，未覆盖复制来的基线模型
- 下一步：等待用户确认或继续论文后续工作

## 2026-09-10 建模代码规划

- 状态：已完成
- 完成内容：完成业务澄清、需求基线、架构和任务分解；确定以当前杂项为基线、完整闭环、自包含复制资源
- 验证与限制：Project Log 校验通过；尚未实施代码迁移，也未复制数据/模型
- 下一步：开始 TASK-001 工程说明，然后依次实施资源复制、共享模块、三训练器、统一闭环和验证

## 2026-09-10 杂项绘图脚本验证

- 状态：已完成
- 完成内容：使用 `edmddl2` Python 3.10 环境运行 `compare_all.py`，加载 `杂项/data` 与 `杂项/models`，生成 `杂项/figures` 图表和指标表
- 验证与限制：退出码 0；Numpy/Scipy/Matplotlib/Torch/Sklearn 依赖齐全；控制台中文显示乱码但不影响文件内容；未修改数据和模型
- 下一步：等待用户确认验证结果或继续定义论文目标

## 2026-09-10 工程初始化

- 状态：已完成
- 完成内容：创建 `.project-log`、根目录 `AGENTS.md`，记录个人仓库规则
- 验证与限制：`validate_project.py` 通过；README 仅有标题，项目级规则待补充
- 下一步：等待用户说明论文或工程目标

<!--
旧段落按日期倒序向下追加；超过约 50-100 KB 时归档到
`.project-log/docs/archive/`，归档文件按日期可检索。
-->
