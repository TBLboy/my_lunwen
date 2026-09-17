# Current Session

## Current Snapshot

- Current phase: implementation
- Current task: TASK-033 is complete; TASK-030 remains pending
- Current status: the new figure-eight and five-point-star PID runs are integrated into Figure 6 and Table 2 after explicit user confirmation of their controller identity
- Latest verification: full-trajectory Figure 6 and nine-page manuscript rebuild recorded as `EV-038`
- Next steps:
  - Continue TASK-030 metadata and submission-package checks
  - Replace the equipment figure when the new soft-platform photograph is supplied
  - Perform the final page-layout and author-guide pass

## 2026-09-17 绘图外包资料包

- Goal/task: package the current figure-optimization code, source data, models, metrics, and manuscript background for an external GPT to improve the paper figures.
- Deliverable: `杂项/绘图外包/` contains `README.md`, `背景材料/manuscript_body.tex`, mirrored modeling code and trained models, robotic-arm and soft-platform experimental data, current plotting scripts, generated PNG/PDF/SVG, metric JSON files, and `文件清单.csv` (75 files, about 31.86 MB).
- Scope mapping: `figure2_modeling_accuracy` is paper Figure 4, `figure3_control_tracking` is Figure 5, and `figure4_soft_control_tracking` is Figure 6.
- Confirmed constraints in the brief: no retraining or data re-acquisition, no metric changes, flexible-soft-platform upper trajectories must be complete, lower error panels and tables use `step >= 30`, and the manuscript remains CAS double-column within nine pages.
- Verified: all three plotting scripts were rerun in the mirrored package directory and produced the same Figure 2 / Figure 3 / Figure 6 metrics as the source project.
- Next: external GPT can use `杂项/绘图外包/README.md` as the primary handoff; main-agent work continues with TASK-030 RAS submission-package checks.

## 2026-09-17 New Soft-Platform Control Data Integration

- Goal/task: replace the soft-platform control result with the newly acquired figure-eight and five-point-star PID runs.
- Clarification: the user confirmed that both baseline exports were collected with the PID controller and that the embedded Koopman-LQR names are export-label errors; `Q-020` is answered and `DEC-014` supersedes the temporary block in `DEC-013`.
- Data handling: the generator now reads both ZIP and CSV exports, filters valid samples, drops repeated `step` rows, and keeps the common `step >= 30` evaluation window.
- Figure/metrics: Figure 6 reports FS-EDMD-LQR versus PID RMSE/MAE of `0.1174/0.1135` versus `0.6386/0.4797` for the figure-eight and `0.1339/0.1294` versus `0.8406/0.6391` for the five-point star. After user feedback, the trajectory panels now draw complete FS-EDMD-LQR/PID paths and the shared limits include the full actual ranges; only the lower error panels and Table 2 retain the common `step >= 30` metric window.
- Manuscript: Table 2 and the tracking text now use the new trajectories and reductions of `81.6%/76.3%` and `84.1%/79.8%`.
- Verification: forced `latexmk` rebuild completed with a nine-page PDF; rendered pages 7-9 were visually inspected; no undefined references or fatal errors were found.
- Evidence: EV-038.

## 2026-09-17 New Soft-Platform Control Dataset Audit

- Status: superseded by explicit PID confirmation; retained as the provenance record for the discovered metadata conflict.
- Goal/task: determine whether the new 8-shaped and five-point-star runs are sufficient to regenerate the soft-platform control figure and table.
- Data coverage: 8-shaped FS/PID each have 400 unique control steps with identical references; five-point-star FS/PID each have 500 unique control steps with identical references.
- Completeness: all expected position, error, and control fields are present, with no missing numeric values.
- Data shape: each file repeats the final control step for 30 additional monitoring samples; these must not be weighted as ordinary tracking samples.
- Conflict: the 8-shaped PID CSV header says Koopman-LQR Controller, and the new five-point-star PID archive config says Koopman-LQR with Q=30, R=0.1, and feedforward gain=1.3. PID identity is therefore not established.
- Decision: the FS archives are suitable for use; both PID files are blocked pending corrected export or explicit controller confirmation. Q-020 and TASK-033 record the issue.
- Evidence: EV-036.

## 2026-09-17 Fixed In-Column Placement for Figures 4 and 5

- Goal/task: make the modeling-accuracy and robotic-arm tracking figures single-column and non-floating at their corresponding manuscript positions.
- Root cause: the CAS class redefines `figure` and consumes `[H]` as a key-value placement option instead of forwarding it to the standard fixed-placement mechanism.
- Change: added `figurehere`, a local fixed-placement environment using `\@float@HH` and `\float@endH`; changed Figures 4 and 5 to column width and replaced their floating environments with `figurehere`.
- Verification: forced `latexmk` rebuild produced a nine-page PDF; Figure 4 resolves to page 6 and Figure 5 to page 7; rendered pages 6-9 were visually inspected; no undefined references, fatal errors, or ignored float placements were found.
- Evidence: EV-035. Decision: DEC-012.

## 2026-09-17 Figure 2/3 Float Placement Repair

- Goal/task: restore the controller-structure and Geomagic Touch equipment figures to their corresponding manuscript sections.
- Root cause: the figures used permissive/default float placement in the CAS double-column layout, allowing them to be deferred away from the referenced text.
- Change: set explicit top placement for both Figure 2 (`fig:controller`) and Figure 3 (`fig:geomagic_touch`) in `manuscript_body.tex`.
- Verification: forced `latexmk` rebuild completed with a nine-page PDF; `main.aux` resolves Figure 2 to page 5 and Figure 3 to page 6; PDF text and rendered-page inspection place them near Sections 4.1 and 5.1 respectively; no undefined references, fatal errors, or missing figure files.
- Evidence: EV-034.

## 2026-09-17 User-Owned Experimental-Volume Assessment

- The user explicitly stated that the agent does not need to calculate the experimental-section physical volume.
- The user will independently judge whether the added soft-platform content keeps the experimental volume acceptable.
- The agent-side acceptance criteria are limited to the nine-page PDF, figure/table integrity, legibility, and a successful build.
- `EV-033` records the forced nine-page rebuild; it does not assert a quantitative physical-volume comparison.
- TASK-029 is complete from the agent side; no user response is required for this task.

## 2026-09-17 RAS Page-Budget Clarification

- Status: clarified and recorded.
- User confirmed RAS has no hard eight-page limit and accepted nine pages or fewer as the internal target.
- The experiment section may gain scientific content, including the soft-platform validation, but its physical footprint must not increase relative to the old manuscript.
- Figure drawing and experiment-section layout may be adjusted repeatedly to converge on the nine-page target.
- Q-019 is answered; DEC-010 records the approved decision; REQ-003 freezes the revision scope and constraints.
- TASK-029 is now in progress with the nine-page and frozen-experiment-volume acceptance criteria.

## 2026-09-17 RAS Author Guide Review

- Status: clarification completed for the user-provided guide; one page-limit question remains open.
- Recorded the official RAS author guide in `.project-log/research/ras-author-guide-2026.md`.
- Confirmed the abstract is 182 words and there are 5 keywords, both within the guide limits.
- Reduced the four Highlights from 127-145 characters to 58-74 characters.
- Added a standalone editable `highlights.tex` with the same four bullets.
- Confirmed the official RAS guide does not state an eight-page limit; the existing eight-page target is an internal formatting choice.
- Added Q-019 to decide whether to keep eight physical pages as an internal target.
- Added TASK-030 for the remaining author-guide compliance items.
- Remaining author inputs: full author and affiliation metadata, CRediT roles, competing interests, funding, data availability, and generative-AI disclosure.

## 2026-09-17 Official CAS Double-Column Migration

- Status: implemented and verified.
- Created `论文部分/els-cas/els-cas-templates/main.tex` from the official `cas-dc-template.tex`.
- Kept the official `cas-dc.cls`, `cas-common.sty`, and `cas-model2-names.bst` files unchanged.
- Moved the manuscript body into `manuscript_body.tex`; the CAS front matter remains in `main.tex`.
- Copied the existing pictures and bibliography into the CAS template directory.
- Fixed a visible 79.96 pt Q-matrix line overflow by converting the controller weights to display math.
- Verified `latexmk -> pdflatex -> bibtex -> pdflatex`; the CAS PDF builds successfully with no fatal errors or undefined references.
- Result: `论文部分/els-cas/els-cas-templates/main.pdf`, 11 physical pages (1 Highlights page plus 10 article/float pages).
- Evidence: EV-031.
- Remaining: the eight-physical-page constraint is still open because full-width figures are deferred to float-only pages; see TASK-029.

## 2026-09-17 Elsevier Two-Column Format

- Status: implemented and verified.
- Switched `elsarticle/main.tex` from `preprint,12pt` to `final,3p,twocolumn,times`.
- Kept the preprint class option as a comment for later single-column submission builds.
- Adjusted the trajectory-tracking table and controller figure widths to remove horizontal overflow.
- Verified `latexmk -> pdflatex -> bibtex -> pdflatex`; generated an 11-page two-column PDF without undefined references or compile errors.
- Evidence: EV-030.
- Remaining: one page contains only full-width figures; the earlier 8-page target is not yet met and needs a separate content/layout reduction step.

## 2026-09-16 LaTeX Toolchain Installation and Build Verification

- Status: installed and verified.
- Installed MiKTeX 26.5 for the current Windows user.
- Installed Strawberry Perl 5.42.3 for `latexmk` support.
- Added `amsthm` to `论文部分/elsarticle/main.tex`; the source uses `proof` environments.
- Verified `pdflatex`, `bibtex`, and `latexmk` with the full manuscript build sequence.
- Result: `论文部分/elsarticle/main.pdf` generated successfully, 22 pages.
- Evidence: EV-029.
- Remaining: the current preprint build is 22 pages; the production-style 8-page layout still needs a separate layout check after author metadata and the remaining equipment photo are supplied.

> 会话恢复入口。维护规则：
> - **头部快照**：顶部“当前状态”区块是稳定入口，每次更新时覆盖，不追加旧版本。
> - **最新在最上**：最新一次会话写在文件最上面的会话区块，旧会话依次向下。
> - **超限归档**：文件超过约 50-100 KB 或会话区块达到约 10 条时，把旧会话区块移动到 `.project-log/docs/archive/`，主文档只保留最近内容。
> - **单一事实源**：精确当前状态与下一步以 `.project-log/loop/handoff.md`、`.project-log/loop/active-run.yaml` 为准；不要在多份长文档里维护互相矛盾的“下一步”。
> - **机器文件不手工重排**：`loop/events.jsonl`、`loop/active-run.yaml`、`loop/handoff.md`、`verification/evidence.yaml` 由运行时维护，不做手工重排或改写。

## 2026-09-16 会话（Figure 3/4 科研绘图质感优化）

- 目标/任务：在不改变数据和结论的前提下，提升机械臂 Figure 3 与软体平台 Figure 4 的期刊风格和可读性。
- 样式：统一 Reference、FS-EDMD-LQR、PID 的配色、线型、Times 系 serif 字体、细边框、轻网格、次刻度和面板标签。
- Figure 3：删除每个面板的重复长标题，改为列标题、左侧行标签和共享图例，保留每行一个实验、每列一个关节的结构。
- Figure 4：保留螺旋/五角星轨迹和逐时刻二维误差曲线，优化上下两排比例、面板标签、面积填充和图例位置。
- 指标：Figure 3 与 Figure 4 的评估窗口及全部 RMSE/MAE 保持不变。
- 论文同步：两张最新 PDF 已复制到 `论文部分/elsarticle/pictures`，源文件与论文副本 SHA256 一致。
- 验证：EV-028 通过；脚本语法和重跑、PNG 尺寸与非空检查、指标检查、PDF 哈希检查均通过。

## 2026-09-16 会话（Figure 4 螺旋替换与误差曲线）

- 目标/任务：将软体平台 Figure 4 的圆形替换为螺旋，并增加每个评估时刻的实际跟踪误差曲线。
- 数据：`螺旋-FS.zip`、`螺旋-PID.zip`、`FS-五角星.zip`、`五角星-PID.zip`；统一按 `step` 去重并使用 `step >= 30` 的评估窗口。
- 图形布局：上排左为螺旋轨迹、上排右为五角星轨迹；下排对应绘制 `e(t)=||p_k-p_k^ref||_2` 的 FS/PID 时间序列。
- 指标：螺旋 FS-EDMD-LQR `RMSE=0.2405, MAE=0.1983`，PID `RMSE=1.1407, MAE=0.9668`；五角星指标保持不变。
- 论文同步：Table II 已改为 `Soft: spiral`，图题和正文已更新为螺旋及逐时刻误差表述。
- 验证：EV-027 通过；脚本重跑、图片视觉检查、指标 JSON、LaTeX 引用/图片路径和 PDF 哈希均通过。

## 2026-09-16 会话（软体平台 Figure 4 与 Table II）

- 目标/任务：使用圆形和五角星的实际控制数据比较 FS-EDMD-LQR 与 PID，并接入 RAS 论文。
- 数据来源：`数据备份/软体平台/软体机械臂轨迹跟踪数据` 下的圆形和五角星 FS/PID 压缩包；螺旋数据不进入正文。
- 数据审计：每条 CSV 含 `time, step, ref_x, ref_y, act_x, act_y, err_x, err_y, err_dist, u_x, u_y`；圆形 1000 个控制步，五角星 500 个控制步；尾部重复监控采样按唯一 `step` 去除。
- 评估口径：参考轨迹完整显示；FS-EDMD-LQR 与 PID 统一从 `step >= 30` 后计算和展示，以排除从静止位置到轨迹起点的初始接近段。
- Figure 4：左侧圆形、右侧五角星，包含 Reference、FS-EDMD-LQR 和 PID，使用统一 `xy` 坐标比例。
- 指标：圆形 FS-EDMD-LQR RMSE/MAE `0.0542/0.0528`，PID `0.3160/0.3038`；五角星 FS-EDMD-LQR `0.1321/0.1278`，PID `0.6313/0.6202`。
- 论文同步：Figure 4 和正文段落已加入实验章节，Table II 增加软体圆形和五角星两组结果，并补充软体平台 `xy` 指标定义。
- 产物：`杂项/正式论文的绘图部分/figure4_soft_control_tracking.png/pdf/svg`、`figure4_soft_control_metrics.json`、生成脚本和论文 `pictures` 中的 PDF 副本。
- 验证：EV-026 通过；图像视觉检查、脚本语法、指标 JSON、论文引用、图表路径和 PDF 哈希一致；当前无 LaTeX 编译器，未执行整篇 PDF 编译。

## 2026-09-16 会话（RAS Elsevier elsarticle 模板迁移）

- 目标/任务：将正式论文从 RA-L 的 `ieeeconf` 前置结构迁移到 Robotics and Autonomous Systems 使用的 Elsevier 官方模板。
- 模板基线：`论文部分/elsarticle/elsarticle-template-num.tex`，版本对应 Elsevier elsarticle 3.4（2024/04/04）。
- 文档配置：`\documentclass[preprint,12pt]{elsarticle}`、`\journal{Robotics and Autonomous Systems}`、`\bibliographystyle{elsarticle-num}`。
- 前置结构：加入 `frontmatter`、占位作者/单位、摘要和 `keyword`，删除 `ieeeconf`、`IEEEoverridecommandlockouts`、`pdfinfo`、`cite` 包和 IEEEtran 引用样式。
- 内容保持：正文、公式、算法、定理、图表、实验指标、图片路径和参考文献键未改写；原 `old` 稿件保持不动。
- 验证：EV-025 静态检查通过；25 个引用键均存在，交叉引用无缺失或重复，旧/新内容差异仅限模板前置和参考文献配置。
- 限制：当前机器没有 `pdflatex`、`xelatex`、`lualatex`、`latexmk` 或 `bibtex`，未执行整篇 PDF 编译。

## 2026-09-16 会话（Figure 3 实验行方向重排）

- 目标/任务：将 Figure 3 从“每行一个关节”转置为“每行一个实验、每列一个关节”，让正弦、不规则和扰动恢复曲线分别完整地横向展示。
- 完成内容：`sinusoidal` 位于第一行，`irregular` 位于第二行，`disturbance recovery` 位于第三行；列对应 Joint 1--3。
- 轴设置：每个关节列共享 y 轴范围，时间轴统一为 `0--30 s`，面板按行优先重新编号 `(a)--(i)`。
- 正文同步：图题改为 rows 为实验、columns 为关节；正文引用改为 sinusoidal row、irregular row 和 disturbance-recovery row。
- 验证：EV-024 通过；RMSE/MAE 与冻结指标完全一致，三种图像格式和论文 PDF 已更新，视觉检查确认同实验位于同一行。
- 限制：当前环境无 LaTeX 编译器，未执行整篇 PDF 编译和 8 页检查。

## 2026-09-15 会话（当前 main.tex 图表整合）

- 目标/任务：将已生成的 Figure 2/3 正式图接入当前 `论文部分/main.tex`，并删除旧的分散控制图和低信息量表格。
- 完成内容：复制两张矢量 PDF 到 `论文部分/pictures`；用新的双平台建模图替换旧机械臂位置预测图；用新的 `3×3` 机械臂控制图替换正弦、不规则和扰动恢复三张旧图；删除不规则参考参数表。
- 建模叙述：主文引用软体平台轨迹 66 的 FS-EDMD/EDMD/EDMDDL RMSE `0.7889/0.8965/1.2927`，并明确软体指标仅覆盖 `xy` 位置。
- 布局结果：实验段当前包含设备图、Figure 2、Figure 3 和两张表；Figure 1 双平台设备图与 Figure 4 软体控制图仍待素材。
- 验证：EV-023 通过；实验段表格数为 2，标签唯一且所有 `\ref` 可解析，所有 `\includegraphics` 路径存在，复制 PDF 与源文件 SHA256 一致。
- 限制：当前环境无 LaTeX 编译器，尚未执行整篇 PDF 编译和 8 页检查。

## 2026-09-15 会话（Figure 3 机械臂控制轨迹跟踪图，初始布局）

- 目标/任务：在 `杂项/正式论文的绘图部分` 生成机械臂控制轨迹跟踪的紧凑 `3×3` 主图。
- 布局：初始版本行为 Joint 1-3、列为实验类型；后由 TASK-023 转置为实验行方向布局。
- 评估窗口：冻结原始时间 `10–40 s`，图中平移为 `0–30 s`；该窗口包含 30 秒轨迹任务及扰动数据中的主要恢复事件。
- 数据源：`数据备份/机械臂数据/轨迹跟踪数据/my_data_1.mat`、`my_data_2.mat`、`my_data_3.mat`。
- 指标：正弦 FS-EDMD-LQR `RMSE=0.01544872, MAE=0.01357750`，PID `RMSE=0.04754018, MAE=0.04016095`；不规则 FS-EDMD-LQR `RMSE=0.01748137, MAE=0.01482802`，PID `RMSE=0.04130153, MAE=0.03366186`；扰动恢复 FS-EDMD-LQR `RMSE=0.09576842, MAE=0.02981920`。
- 产物：`figure3_control_tracking.png/pdf/svg`、`figure3_control_metrics.json`、生成脚本 `plot_figure3_control_tracking.py`。
- Table II：已用统一窗口指标替换旧值，并同步更新正弦/不规则改善百分比；增加扰动恢复的 FS-EDMD-LQR RMSE/MAE。
- 验证：脚本退出码 0；语法检查通过；PNG 已完成版式与曲线检查；PNG/PDF/SVG 均非空；Main TeX 中旧指标已清除。

## 2026-09-15 会话（Figure 2 双平台建模精度图）

- 目标/任务：绘制机械臂与软体平台并列的建模精度主图，输出到 `杂项/正式论文的绘图部分`。
- 版式：Figure 2 左侧为 Joint 1-3，右侧为软体平台轨迹 66 的 `x/y`；每个面板比较 Ground Truth、FS-EDMD、EDMDDL、EDMD。
- 数据口径：机械臂使用现有测试数据前 800 步 rollout；软体平台固定使用测试轨迹 66 的 299 步。
- 产物：`figure2_modeling_accuracy.png/pdf/svg`；生成脚本 `plot_figure2_modeling_accuracy.py`。
- 关键 RMSE：机械臂 FS-EDMD `0.59333305`；软体平台轨迹 66 FS-EDMD `0.78889613`，与既有指标一致。
- 复现命令：使用 `C:\Users\Windows\.conda\envs\edmddl2\python.exe -X utf8 杂项/正式论文的绘图部分/plot_figure2_modeling_accuracy.py`。
- 验证：脚本退出码 0；`py_compile` 通过；PNG 已完成视觉检查；PNG/PDF/SVG 均非空。

## 2026-09-15 会话（论文改稿业务逻辑澄清启动）

- 目标/任务：结合三次投稿编辑意见，判断哪些意见值得采纳，并规划论文正文与实验部分的修改。
- 主贡献定位：用户同意保留 FS-EDMD + 鲁棒 Koopman-LQR 为第一贡献，软体平台作为第二真实平台和跨平台验证。
- 软体平台指标口径：用户确认只展示轨迹 66，不报告 10 条平均，也不在正文解释选择原因；后续文案使用中性 case study 表述，不做全面平均优势外推。
- Jacobian 对照：用户决定不新增局部线性化 LQR 基线；控制实验维持 FS-EDMD-LQR 与 PID 对比，正文避免宣称相对局部线性化具有普遍优势。
- 软体平台控制实验：固定圆形和五角星两条轨迹，论文合并为左右双子图，比较 FS-EDMD-LQR 与 PID。
- 机械臂建模展示：去掉速度预测图，主图只展示三个关节位置预测；速度信息如保留，只进入定量表。
- 机械臂建模指标：主图只画位置；表格保留全状态 MSE/RMSE/MAE，并明确包含位置和速度。
- 控制跟踪指标：机械臂和软体平台均只在表格与正文中使用 RMSE、MAE，不使用最大误差。
- 实验章节句子级骨架与图表数据清单：`.project-log/specs/paper-revision-experiment-outline.md`。
- 实验章节骨架已完成：4 图 2 表、句子级主题句、数据来源、版式预算和禁止表述均已冻结。
- 实验图表骨架：4 张实验主图 + 2 张表；平台图双面板、建模图双面板、机械臂控制 3x3、软体控制双面板。
- 绘图方案已写入：`.project-log/specs/paper-revision-experiment-plan.md`
- Figure 2 确认采用嵌套子图：左列三关节，右列软体 x/y；每个小面板保留三个模型对比曲线。
- 待补素材：软体平台设备照片，用户后续拍摄后提供。
- 已读取：`论文部分/main.tex`、`论文部分/不同期刊编辑意见汇总.md`、机械臂建模与轨迹跟踪材料、软体平台最终建模结果。
- 论文事实：当前贡献为 FS-EDMD 特征选择、BCD 联合优化和带 UUB 分析的 feedforward-feedback Koopman-LQR；实验仅覆盖 Geomagic Touch 3-DOF 机械臂。
- 审稿意见初步分类：期刊 scope 类意见不回写正文；创新性/必要性、特征选择理论、数据依赖与有效域、Jacobian 对照、实验复杂性需要部分或全部采纳。
- 软体平台证据：轨迹 66 上 FS-EDMD 最小 RMSE 为 `0.7889`，优于修正版 EDMD `0.8965` 和 EDMDDL `1.2927`；但最终包中 FS-EDMD 平均 RMSE `1.5328` 高于 EDMDDL `1.4565`，且修正版 EDMD 平均指标尚未同步进 final。
- 图表事实：现有实验图片多数为约 `2100x2400` 像素、原始画布 `7x8` 英寸；新增实验前必须统一重绘为紧凑多面板图。
- 阅读记录：`.project-log/research/papers/feature-selection-koopman-q3-revision/reading-note.md`

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
