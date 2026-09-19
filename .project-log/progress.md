# Progress

## Current Snapshot

- Current phase: implementation
- Current task: TASK-030 is blocked on Q-021 after all machine-checkable submission-package checks passed
- Current status: Only author-supplied factual metadata and the replacement equipment photograph remain
- Latest verification: EV-069; RAS-style numbered bibliography with 25/25 first-citation order, no DOI/URL output, a clean nine-page manuscript build, a one-page highlights build, and synchronized main PDFs
- Latest layout check: Figures 2-7 use `figurehere` with `-6pt` caption-top spacing; Figure 1 uses `abovecap=-6pt,belowcap=0pt` on the two-column float
- Latest table check: Tables 1-2 now use the non-floating `tablehere` environment and follow their source positions
- Next steps:
  - Obtain the real author names, full affiliations, corresponding-author email, funding information, and actual generative-AI use status
  - Use the captured notes when the dedicated paper-writing and revision Skill is requested
  - Replace the equipment figure when the new soft-platform photograph is supplied
  - Perform the final page-layout and author-guide pass after those facts and the photograph are supplied

## 2026-09-19 RAS Machine-Checkable Submission-Package Completion

- Status: done for all machine-verifiable items; the overall submission package remains pending author facts.
- Abstract is 217 words, keywords are five, and all four highlights are at most 74 characters.
- All 25 first citations exactly match bibliography order; all seven figure PDFs are present and cited, and the two tables are editable LaTeX.
- `main.pdf` is nine pages, `highlights.pdf` is one page, and strict build-log scans are clean.
- The synchronized manuscript PDFs share SHA256 `105132747514A4F4E689F9CC95DEC51C7FB629873AB9DBB80813D0910920F7E7`; the highlights PDF is `6FAA79FCDC2F705FD2F9CF120FAC1E5D50050B1814F0818B28D8ACCA47294E2B`. Evidence: EV-068.
- Still required from the author: real names and CRediT attribution, full affiliations, corresponding-author email, funding details, applicable generative-AI disclosure, and the replacement equipment photograph.

## 2026-09-19 RAS Numbered Bibliography Style

- Status: done for the reference-presentation alignment.
- Replaced `unsrtnat` with local `ras-num.bst`, derived from the official Elsevier numbered style, to match the RAS reference examples while keeping first-citation numbering.
- Normalized journal abbreviations and suppressed DOI output without changing citation keys or scientific content.
- Verification: 9-page main PDF, 1-page highlights PDF, clean warning scans, 25/25 citation-order match, no DOI/URL output, and identical main PDF hashes across both output paths. Evidence: EV-069.

## 2026-09-19 Competing-Interest and Data-Availability Declarations

- Status: done.
- Added `Declaration of competing interest` and `Data availability` after the CRediT statement and before the bibliography in `main.tex`.
- Used a no-known-competing-interest statement and a conservative corresponding-author data-availability statement.
- Verification: clean 9-page build, empty strict warning scan, rendered page 8 inspection, and synchronized PDF hashes. Evidence: EV-067.

## 2026-09-19 User-Optimized Experimental Sections

- Status: done.
- Reviewed the user's compressed Sections 5.2--5.3 and kept the revised shared experimental structure.
- Added explicit interword spacing after the two `\footnotemark` calls in the quantitative-result paragraphs; the first call previously caused a 9.8655 pt Overfull hbox in the left column.
- Verification: clean 9-page build, empty strict warning scan, rendered pages 6--9 inspected, and synchronized PDF hashes. Evidence: EV-066.

## 2026-09-19 Compact Figure Caption Spacing

- Status: done.
- The first 6 pt adjustment still left visible whitespace, so the non-floating figure environment now uses `-6pt` caption-top spacing and `0pt` caption-bottom spacing.
- Applied the same compact spacing to the full-width Figure 1 float through `abovecap=-6pt,belowcap=0pt`.
- Verification: clean 9-page build, empty strict warning scan, visually inspected pages 3, 6, and 8, and synchronized PDF hashes. Evidence: EV-065.

## 2026-09-19 Symmetric Modeling Setup

- Status: done.
- Reworked Section 5.2 so shared method choices are introduced first, followed by separate robotic-arm and soft-platform configurations before any result discussion.
- Added the actual soft-platform configuration: 112-term candidate library, 20-dimensional EDMDDL dictionary with two 256-neuron hidden layers, and a 40-by-112 FS-EDMD selection matrix.
- Matched the evaluation descriptions by stating the robotic-arm 800-step/3.2 s rollout and the soft-platform 299-step rollout on test trajectory 66.
- Verification: clean 9-page build, empty strict warning scan, visually inspected pages 6-7, and synchronized PDF hashes. Evidence: EV-063.

## 2026-09-19 Symmetric Platform Data-Collection Description

- Status: done.
- Rewrote the Section 5.1 data-collection paragraph so the soft-platform description mirrors the robotic-arm description.
- The soft platform now explicitly reports random two-dimensional cable-motion commands, a 0.2 s sampling period, 100 trajectories of 60 s each, and the light-spot position plus applied command contained in every trajectory.
- Preserved the shared trajectory-level split statement and the existing 15:4:1 and 70/20/10 ratios.
- Verification: clean 9-page `latexmk` build, empty strict warning scan, revised page-6 text, and synchronized PDF hashes. Evidence: EV-062.

## 2026-09-19 Compiled PDF Path Synchronization

- Status: done.
- Identified that the stale-image report came from two PDF outputs: the fresh build was in `els-cas-templates/main.pdf`, while `els-cas/main.pdf` was still the old build.
- Synchronized the top-level PDF and verified matching size, timestamp, and SHA256.
- Verification: both PDFs are 3126615 bytes with SHA256 `0CE7267131056BB3388010287872C87A79C7FF728C618DB3DB9CF8DA5BDB672F`. Evidence: EV-061.

## 2026-09-19 Figure 3 Dual-Platform 5.1 Alignment

- Status: done.
- Updated Figure 3 to use a combined experimental-setting caption and matched its label/reference to both platforms.
- Revised Section 5.1 so the rigid arm and soft platform are introduced from the same figure, with the soft-platform hardware and drive electronics described consistently with the labels in the figure.
- Kept the random-input data-collection procedure and trajectory-level splits unchanged.
- Verification: 9-page `latexmk` build, clean strict warning scan, and rendered page 6. Evidence: EV-060.

## 2026-09-19 Section 5.1 Two-Platform Rewrite

- Status: done.
- Reworked Section 5.1, now titled `Experimental Platforms and Data Collection`, to introduce the robotic arm and soft platform separately before summarizing the shared experimental procedure.
- Generalized data collection as randomly generated control inputs for both platforms, with platform-specific sampling and trajectory counts.
- Kept the train/validation/test split description at trajectory level, and removed trajectory 66 from the platform/data-collection subsection.
- Removed the unverified coupled-boundary claim while retaining the fixed-stylus isolation statement.
- Verification: 9-page `latexmk` build, clean strict warning scan, and rendered page 6. Evidence: EV-059.

## 2026-09-19 Non-Floating In-Column Tables

- Status: done.
- Added `tablehere` alongside `figurehere`.
- Replaced both floating `table[htbp]` environments with `tablehere` without changing table data or widths.
- Verification: 9-page `latexmk` build, no table-related overfull/underfull warnings, and rendered pages 7-8.

## 2026-09-19 Non-Floating In-Column Figures

- Status: done.
- Replaced Figure 3's remaining top-only float with the existing `figurehere` environment.
- Figures 2-7 now stay inside a single column at their source positions; Figure 1 remains a two-column `figure*`.
- Moved Figure 2 after the LQR cost discussion so it renders inside the left column of page 5.
- Verification: 9-page `latexmk` build and rendered pages 5-6.

## 2026-09-19 Citation-Order Bibliography

- Status: done.
- Switched from the author-sorted CAS bibliography style to natbib-compatible `unsrtnat`.
- Verified that the first-citation sequence in `main.aux` exactly matches the 25-entry bibliography order in `main.bbl`.
- The Introduction now uses sequential citation groups with repeats only where references are cited again later.
- Verification: 9-page clean build, clean strict warning scan, and rendered pages 1, 8, and 9. Evidence: EV-056.

## 2026-09-19 Layered Abbreviation Audit

- Status: done.
- Defined EDMD, EDMDDL, and FS-EDMD in the Abstract and removed their repeated full terms from the Introduction.
- Left common field abbreviations such as LQR, PID, PCA, ReLU, MSE, RMSE, and MAE unchanged, avoiding mechanical expansion.
- Corrected the reusable terminology rule to audit the Abstract and main text as one document-level first-use sequence.
- Verification: 9-page clean build, clean strict warning scan, and rendered pages 1-2. Evidence: EV-055.

## 2026-09-19 Conclusion Evidence-Scope Audit

- Status: done.
- Separated two-platform prediction and tracking claims from the arm-only disturbance-recovery test.
- Limited robustness wording to the disturbance-recovery test and stated the operating-range and bounded-disturbance scope.
- Added the Conclusion consistency rule to the future paper-revision Skill material.
- Verification: 9-page clean build, clean warning scan, and rendered Conclusion page. Evidence: EV-053.

## 2026-09-19 Reusable Paper-Revision Skill Material

- Status: done.
- Created a consolidated notes artifact covering review triage, claim-evidence mapping, experiment planning, figure/page budgets, data audits, writing checks, and the future Skill contract.
- Added four reusable work traces and four distillation candidates tied to the notes and existing evidence.
- Verification: `loopctl validate` passed. Evidence: EV-052.

## 2026-09-19 Abstract and Introduction Content Audit

- Status: done.
- Corrected the Abstract so robustness is attributed only to the robotic-arm disturbance-recovery test rather than to both platforms.
- Added the dual-platform validation to the contribution list and corrected the section roadmap from one platform to experiments on both platforms.
- Tightened the problem-method-theory-validation sequence and replaced several formulaic transitions while preserving all technical claims and metrics.
- Verification: clean-copy `latexmk` exits 0 with 9 pages and a clean strict warning scan; pages 1--2 were rendered and inspected.
- Evidence: EV-051.

## 2026-09-19 LaTeX Warning and Typography Polish

- Status: done.
- Updated `main.tex` to disable hyperlinked footnotes, omit an empty ORCID footnote, handle the CAS keyword-box layout warning locally, use unique hyperref targets, raise the PDF output version to 1.7, and use ragged-right bibliography lines.
- Made minimal wording and line-break adjustments in `manuscript_body.tex`; scientific meaning, metrics, figures, and tables were unchanged.
- Verification: independent clean-copy `latexmk` build is 9 pages with no actionable `Overfull`, `Underfull`, hyperref, pdfTeX, undefined-reference, or fatal warnings; rendered pages 3, 4, and 9 were inspected.
- Evidence: EV-050.

## 2026-09-19 Soft-Platform Modeling Metrics Completion

- Status: done.
- Added MSE, RMSE, and MAE computation to the soft-platform trajectory-66 evaluation script.
- Recovered and persisted soft-platform metrics for FS-EDMD, EDMD, and EDMDDL.
- Updated Table 1 and the modeling-results text with the complete metrics and reductions.
- Verification: the previous RMSE values are unchanged; the table fits on page 7; `main.pdf` remains 9 pages with no fatal errors.
- Evidence: EV-048.

## 2026-09-19 Paper Picture Filename Normalization

- Status: done.
- Renamed the seven active manuscript images to `Figure1.pdf`--`Figure7.pdf` in first-reference order.
- Updated all `\includegraphics` paths in `manuscript_body.tex`.
- Deleted six unreferenced legacy images from `pictures`.
- Verification: the pictures folder contains only the seven active files, all figure labels resolve to Figures 1--7, and `main.pdf` remains 9 pages with no fatal errors.
- Evidence: EV-047.

## 2026-09-19 Soft-Platform Triangle/Lissajous Figure Integration

- Status: done.
- Replaced the manuscript image with `figure7_soft_tracking_singlecol_v4.pdf`.
- Updated the Figure 7 caption, Section 5.3 discussion, and Table 2 soft-platform labels and metrics to triangle/Lissajous results.
- Recorded triangle FS/PID RMSE 0.1749/0.6645 and MAE 0.1703/0.5468; Lissajous FS/PID RMSE 0.1266/1.7883 and MAE 0.1172/1.6710.
- Verification: 9-page `main.pdf`, Figure 7 and Table 2 on page 8, no undefined references or fatal errors, and a rendered page inspection passed.
- Evidence: EV-046.

## 2026-09-19 New Soft-Platform Control Data Audit

- Status: checked.
- Triangle FS/PID contain 500 unique steps each and their references match exactly.
- Lissajous FS/PID contain 1000/500 unique steps; deduplicate terminal repeats, use `FS[0::2]`, and pair by sample index with the time axis ignored.
- All new CSVs contain 30 repeated terminal-step rows. Triangle and Lissajous data are sufficient for the next control-figure redraw.

## 2026-09-19 Revised Soft-Platform Tracking Figure

- Status: done.
- Added a v4 processing and plotting script, generated PNG/PDF/SVG outputs, an aligned processed CSV, and a metrics JSON.
- Lissajous FS is decimated from 1000 to 500 samples; all task/controller combinations have 500 aligned sample rows.
- The revised figure shows triangle and Lissajous trajectories side by side in a single-column layout and uses sample index rather than raw elapsed time.
- Evidence: EV-045.

## 2026-09-19 Figure 5 Layout Rollback

- Status: done.
- User rejected the compressed Figure 5 layout because it was narrower than Figure 4.
- Restored `width=\columnwidth` and the original paragraph-before-figure order.
- Verification: Figure 5 requests the full column width, `main.pdf` remains 9 pages, and no undefined references or fatal errors are present.
- Evidence: EV-044.

## 2026-09-19 Robustness Experiment Merged into Section 5.3

- Status: done.
- Removed the `Robustness Validation Experiments` subsection and its label.
- Moved the robustness paragraph directly after the irregular-tracking result in Section 5.3, so it reads as part of the robotic-arm tracking evaluation.
- The paragraph identifies the sinusoidal reference, same controller parameters, manual link disturbances, and the disturbance-recovery row of Fig.6.
- Verification: 9-page `main.pdf`, no undefined references or fatal errors, and no remaining `subsection.5.4` label.
- Evidence: EV-042.

## 2026-09-19 Soft-Platform Controller Parameters Aligned with Robotic-Arm Experiment

- Status: done.
- The soft-platform paragraph now reports only the same parameter types as the robotic-arm paragraph: PID \(K_p=20.00\), \(K_i=1.00\), \(K_d=10.00\), and FS-EDMD-LQR \(\mathbf{Q}_x=\diag(250,250)\), \(\mathbf{R}=\mathbf{I}_2\).
- Removed feedforward gain, lifted-feature weight, PID dead zone, input limit, model asset path, output sign, and control-rounding details.
- Verification: 9-page `main.pdf`, no undefined references or fatal errors; existing figure/table page assignments remain unchanged.
- Evidence: EV-041.

## 2026-09-19 Split Figure 4 into Robotic-Arm and Soft-Platform Modeling Figures

- Status: done.
- User wanted the tall combined modeling-accuracy figure split to give the 5.1/5.2 layout more flexibility.
- Added `plot_figure4_modeling_accuracy_split_v1.py` and generated `figure4_robotic_modeling.{png,pdf,svg}` and `figure5_soft_modeling.{png,pdf,svg}`.
- `manuscript_body.tex` now has `fig:robotic_modeling` (q1/q2/q3) and `fig:soft_modeling` (x/y), each using `figurehere` and `\columnwidth`; 5.1/5.2 text was adjusted to describe the two platforms separately.
- Modeling RMSE values remain unchanged: robotic arm FS-EDMD/EDMDDL/EDMD `0.59333305/0.77044169/0.85184558`, soft trajectory 66 `0.78889613/1.29270630/0.89651728`.
- Verification: 9-page `main.pdf`, no undefined references or fatal errors; `main.aux` places Fig.4 on page 6, Fig.5/Fig.6 on page 7, and Fig.7 on page 8; `pdftotext` confirms the 5.1 to 5.2 flow.
- Evidence: EV-039.

## 2026-09-18 Figure 6 Trajectory-Only v3

- Followed the user decision to remove Figure 6's error-curve panels and keep only the figure-eight and five-point-star trajectory tracking panels.
- Added `plot_figure4_soft_control_tracking_singlecol_v3.py`, output `figure6_soft_tracking_singlecol_v3`, and copied the v3 PDF into the CAS template.
- Updated the Figure 6 caption so it no longer describes a bottom error row.
- FS-EDMD-LQR versus PID RMSE/MAE remains unchanged: figure-eight `0.1174/0.1135` versus `0.6386/0.4797`; five-point star `0.1339/0.1294` versus `0.8406/0.6391`.
- Rebuilt `main.pdf` successfully at 9 pages, Figure 6 on page 8, no undefined references or fatal errors.

## 2026-09-18 Single-Column Paper Figure Integration

- The three finalized plotting versions were copied into the CAS template `pictures` directory:
  - Figure 4 uses `figure4_modeling_accuracy_singlecol_v7.pdf`.
  - Figure 5 uses `figure5_control_tracking_singlecol_v6.pdf`.
  - Figure 6 uses `figure6_soft_tracking_singlecol_v2.pdf`.
- Figure 6 was changed from full-width `figure*` to `figurehere` with `\columnwidth`; Figures 4/5 already used `figurehere`.
- `latexmk -pdf -interaction=nonstopmode main.tex` rebuilds successfully to 9 pages; Figure labels resolve to page 7/7/8 respectively.
- Remaining: soft-platform equipment photo and final RAS submission-package checks are still pending.

## 2026-09-17 New Soft-Platform Control Data Integration

- Status: done.
- The user confirmed that the new baseline runs were collected with PID and that the embedded Koopman-LQR names are export-label errors; `Q-020` is answered and `DEC-014` supersedes `DEC-013`.
- Figure 6 now uses figure-eight and five-point-star data and supports both ZIP and CSV inputs; trajectory panels show complete FS-EDMD-LQR/PID paths, while Table 2 and the lower error panels use the common `step >= 30` window.
- FS-EDMD-LQR versus PID RMSE/MAE: figure-eight `0.1174/0.1135` versus `0.6386/0.4797`; five-point star `0.1339/0.1294` versus `0.8406/0.6391`.
- The forced manuscript rebuild remains nine pages with no undefined references or fatal errors.
- Evidence: EV-038; task: TASK-033; decision: DEC-014.

## 2026-09-17 New Soft-Platform Control Dataset Audit

- Status: superseded by explicit PID confirmation; retained for provenance.
- The 8-shaped and five-point-star FS/PID runs each have aligned references and enough unique control steps.
- All files contain 30 repeated final-step monitoring samples that must be handled separately from ordinary tracking samples.
- The purported PID files carry Koopman-LQR metadata or configuration, so their controller identity must be corrected before use.
- Evidence: EV-036; task: TASK-033; question: Q-020.

## 2026-09-17 Fixed In-Column Placement for Figures 4 and 5

- Status: done.
- Added a CAS-compatible `figurehere` environment and converted Figures 4 and 5 to single-column fixed placement.
- Figure 4 is on page 6 near the modeling-accuracy discussion; Figure 5 is on page 7 near robotic-arm tracking.
- The rebuilt PDF remains nine pages with no undefined references, fatal errors, or ignored float placements.
- Evidence: EV-035; decision: DEC-012.

## 2026-09-17 Figure 2/3 Float Placement Repair

- Status: done.
- Set explicit top placement for the controller-structure figure and the existing Geomagic Touch equipment figure in the CAS manuscript.
- Forced `latexmk` rebuild produced a nine-page PDF; Figure 2 is on page 5 near Section 4.1 and Figure 3 is on page 6 near Section 5.1.
- Verification passed with no undefined references, fatal errors, or missing figure files.
- Evidence: EV-034.

## 2026-09-17 User-Owned Experimental-Volume Assessment

- The user will judge whether the experimental-section physical volume is acceptable.
- The agent will not perform or report a quantitative old-versus-new footprint comparison.
- TASK-029 is complete from the agent side; the user's judgment remains independent and is not an agent-side blocking acceptance gate.

## 2026-09-17 RAS Page-Budget Clarification

- Status: in progress.
- User confirmed RAS has no hard eight-page limit; the internal target is now nine pages or fewer.
- The experiment section may contain additional scientific content, but it must not occupy more physical space than the old manuscript.
- Q-019, DEC-010, REQ-003, and TASK-029 were updated to make this constraint traceable.

## 2026-09-17 RAS Author Guide Alignment

- Status: in progress; one page-limit decision remains open.
- Recorded the official RAS author guide and checked the current CAS manuscript against its machine-verifiable requirements.
- Abstract has 182 words and the manuscript has 5 keywords, both within the guide limits.
- Reduced all four Highlights to 58-74 characters and added a standalone editable `highlights.tex`.
- Confirmed the official guide does not state an eight-page limit; Q-019 asks whether to retain eight pages as an internal goal.
- Added TASK-030 for author metadata, CRediT, declarations, artwork packaging, and final submission-file checks.
- Verified the standalone Highlights source compiles and the CAS manuscript still builds after the Highlights update.

## 2026-09-17 Official CAS Double-Column Migration

- Status: implemented and verified.
- Rebuilt the RAS manuscript from the official `cas-dc-template.tex` instead of `elsarticle`.
- Kept the official CAS class, style, and bibliography files unchanged.
- Copied the picture and bibliography resources into `els-cas-templates`; the existing `elsarticle` version remains intact.
- Fixed the visible Q-matrix line overflow and verified the rendered equation page.
- Full `latexmk`/BibTeX build succeeds and produces `els-cas-templates/main.pdf`.
- Evidence: EV-031.
- Remaining: the 11-page physical PDF still exceeds the eight-page target because full-width figures are placed on deferred float pages; tracked as TASK-029.

## 2026-09-17 Elsevier Two-Column Format

- Status: done for the requested format switch.
- Changed `elsarticle/main.tex` to `\documentclass[final,3p,twocolumn,times]{elsarticle}`.
- Preserved the preprint class line as a comment for the alternative submission format.
- Reduced two small horizontal overflows in the tracking table and controller figure.
- Rebuilt successfully with `latexmk`, `pdflatex`, and `bibtex`; the output is 11 pages with two-column layout.
- Evidence: EV-030.
- Remaining: one float-only page remains, and the 8-page target still requires a separate reduction of text or figure footprint.

## 2026-09-16 LaTeX Toolchain Installation and Build Verification

- Status: done.
- Installed MiKTeX 26.5 and Strawberry Perl 5.42.3 for the current user.
- Verified `pdflatex`, `bibtex`, and `latexmk` against `论文部分/elsarticle/main.tex`.
- Added the missing `amsthm` package required by `proof` environments.
- Generated `论文部分/elsarticle/main.pdf` successfully; current preprint build is 22 pages.
- Evidence: EV-029.
- Remaining: perform the production-style 8-page layout check after author metadata and the remaining equipment photo are supplied.

> 面向人的阶段进度摘要。维护规则：
> - **最新在最上**：按日期倒序排列，最新阶段段落位于文件顶部，旧段落依次向下。
> - **头部快照**：顶部“当前状态”区块是稳定入口，每次更新时覆盖，不追加旧版本。
> - **超限归档**：文件超过约 50-100 KB 时，把旧段落移动到 `.project-log/docs/archive/`，主文档只保留最近内容。
> - **单一事实源**：本文件是快速摘要；精确当前状态与下一步以 `.project-log/loop/handoff.md`、`.project-log/loop/active-run.yaml` 为准。
> - **机器文件不手工重排**：`loop/events.jsonl`、`loop/active-run.yaml`、`loop/handoff.md`、`verification/evidence.yaml` 由运行时维护，不做手工重排或改写。

## 2026-09-16 Figure 3/4 科研绘图质感优化

- 状态：已完成
- 样式：统一 Reference、FS-EDMD-LQR、PID 的配色、线型、字体、网格、次刻度和面板标签。
- Figure 3：改为列标题、行标签和共享图例，减少重复标题并保持每行一个实验。
- Figure 4：保留螺旋/五角星轨迹与逐时刻误差曲线，优化上下两排层级、图例和面积填充。
- 指标：评估窗口和全部 RMSE/MAE 与优化前一致。
- 论文同步：Figure 3/4 最新 PDF 已同步到 `论文部分/elsarticle/pictures`，源文件和论文副本哈希一致。
- 验证：EV-028 通过；脚本重跑、PNG 非空检查、指标检查和 PDF 哈希检查均通过。

## 2026-09-16 Figure 4 螺旋替换与误差曲线

- 状态：已完成
- 数据：螺旋和五角星的 FS/PID 轨迹跟踪压缩包；统一从 `step >= 30` 展示和评估。
- 绘制：上排为螺旋/五角星轨迹，下排为对应的 `e(t)=||p_k-p_k^ref||_2` 逐时刻误差曲线。
- 指标：螺旋 FS-EDMD-LQR RMSE/MAE `0.2405/0.1983`，PID `1.1407/0.9668`；五角星 RMSE/MAE `0.1321/0.1278` 对 `0.6313/0.6202`。
- 论文同步：Table II 的 `Soft: circular` 已替换为 `Soft: spiral`，图题和正文已更新。
- 验证：EV-027 通过；脚本重跑、图片视觉检查、指标 JSON、LaTeX 引用和 PDF 哈希均通过。

## 2026-09-16 软体平台 Figure 4 与 Table II

- 状态：已完成
- 数据：圆形和五角星的 FS/PID 轨迹跟踪压缩包；按 `step` 去重，螺旋数据不进入正文。
- Figure 4：左侧圆形、右侧五角星，展示完整 Reference 与从 `step >= 30` 开始的 FS-EDMD-LQR/PID 实际轨迹。
- 指标：圆形 RMSE `0.0542` 对 `0.3160`，MAE `0.0528` 对 `0.3038`；五角星 RMSE `0.1321` 对 `0.6313`，MAE `0.1278` 对 `0.6202`。
- 论文同步：`main.tex` 已加入 Figure 4、软体控制段落及 Table II 两行结果。
- 产物：`杂项/正式论文的绘图部分/figure4_soft_control_tracking.png/pdf/svg`、指标 JSON、生成脚本和论文 `pictures` PDF 副本。
- 验证：EV-026 通过；图像视觉检查、脚本语法、指标 JSON、论文引用、图片路径和 PDF 哈希一致；当前无 LaTeX 编译器，未执行整篇 PDF 编译。

## 2026-09-16 RAS Elsevier elsarticle 模板迁移

- 状态：已实现，待编译验证
- 模板：Elsevier 官方 `elsarticle` 3.4 包中的 `elsarticle-template-num.tex`
- 文档配置：`preprint,12pt`，期刊名设置为 `Robotics and Autonomous Systems`，引用样式为 `elsarticle-num`
- 前置结构：加入 `frontmatter`、摘要和 `keyword`；作者、单位和邮箱暂用占位信息
- 清理内容：移除 `ieeeconf`、IEEE 专用宏、`pdfinfo`、`cite` 包和 IEEEtran 引用样式
- 保持不变：正文、公式、算法、定理、图表、指标、图片路径和参考文献键均未改写；原 `old` 稿件未修改
- 验证：EV-025 通过静态结构和引用完整性检查；当前环境无 LaTeX 编译器，尚未执行整篇 PDF 编译

## 2026-09-16 Figure 3 实验行方向重排

- 状态：已完成
- 完成内容：将 Figure 3 转置为正弦、不规则、扰动恢复各占一行，Joint 1--3 各占一列
- 面板编号：按行优先顺序更新为 `(a)--(i)`，每个关节列共享 y 轴范围
- 正文同步：图题和正文引用从 column-based 更新为 row-based
- 验证：EV-024 通过；RMSE/MAE 保持不变，PNG/PDF/SVG 非空，论文 PDF 与源 PDF 哈希一致
- 限制：无 LaTeX 编译器，尚未进行整篇 PDF 编译和 8 页检查

## 2026-09-15 当前 main.tex 图表整合

- 状态：已完成
- 完成内容：将 Figure 2/3 矢量 PDF 接入主文件，删除旧位置预测图、三张旧控制图和不规则参考参数表
- 建模表：保留机械臂全状态 MSE/RMSE/MAE，并加入软体轨迹 66 的 FS-EDMD/EDMD/EDMDDL RMSE `0.7889/0.8965/1.2927`
- 控制图：初始使用 `3×3` 紧凑控制图，后由 TASK-023 改为正弦、不规则和扰动恢复各占一行
- 验证：EV-023 通过；实验段表格数为 2、标签唯一且引用完整、图片路径存在、PDF 哈希一致
- 限制：无 LaTeX 编译器，尚未进行整篇 PDF 编译和 8 页检查

## 2026-09-15 Figure 3 机械臂控制轨迹跟踪图

- 状态：已完成
- 完成内容：生成 3 行 3 列控制轨迹跟踪图，覆盖正弦、不规则和扰动恢复任务
- 评估窗口：原始 `10–40 s`，图中统一平移为 `0–30 s`
- 指标：正弦 FS-EDMD-LQR/PID RMSE 为 `0.01545/0.04754`；不规则为 `0.01748/0.04130`；扰动恢复 FS-EDMD-LQR RMSE 为 `0.09577`
- 产物：`杂项/正式论文的绘图部分/figure3_control_tracking.png/pdf/svg`、`figure3_control_metrics.json` 和生成脚本
- Table II：已更新为正弦 `0.0154/0.0136` 对 `0.0475/0.0402`，不规则 `0.0175/0.0148` 对 `0.0413/0.0337`，并加入扰动恢复 FS-EDMD-LQR `0.0958/0.0298`
- 验证：脚本成功执行、语法检查通过、PNG 视觉检查通过、三种格式文件均非空

## 2026-09-15 Figure 2 双平台建模精度图

- 状态：已完成
- 完成内容：生成左侧三关节、右侧软体平台 `x/y` 的合并建模精度对比图
- 产物：`杂项/正式论文的绘图部分/figure2_modeling_accuracy.png/pdf/svg` 和生成脚本
- 指标：机械臂 FS-EDMD RMSE `0.59333305`；软体轨迹 66 FS-EDMD RMSE `0.78889613`
- 验证：脚本成功执行、语法检查通过、PNG 视觉检查通过、三种格式文件均非空

## 2026-09-15 论文改稿业务逻辑澄清启动

- 状态：进行中
- 完成内容：结构化阅读论文正文；提取当前方法贡献、实验设计、指标和图片规模；将三次投稿意见映射为“丢弃/部分采纳/必须采纳”
- 初步结论：期刊 scope 意见不回写正文；方法必要性、有效域、Jacobian 对照和跨平台实验是改稿重点
- 关键风险：软体平台单轨迹最优但平均 RMSE 暂未全面优于 EDMDDL，论文表述不能无条件宣称全面最优
- 已确认：保留 FS-EDMD + 鲁棒 Koopman-LQR 为主线，软体平台作为跨平台验证
- 已确认：软体平台建模只展示轨迹 66；正文不解释择优过程，且不将其描述为随机或代表性样本
- 已确认：不新增 Jacobian/局部线性化 LQR 对照，控制部分只比较 FS-EDMD-LQR 与 PID
- 已确认：软体平台控制只采集圆形和五角星，论文合并为一张左右双子图
- 已确认：机械臂建模精度不展示速度预测图，只保留关节位置预测图
- 已确认：机械臂建模表保留全状态 MSE/RMSE/MAE，并说明包含位置和速度
- 已确认：机械臂和软体平台的控制性能均只使用 RMSE、MAE，不展示最大误差
- 已完成：实验章节句子级骨架、四图两表数据来源、版式约束和禁止表述清单，见 `.project-log/specs/paper-revision-experiment-outline.md`
- 已确认：实验部分采用 4 图 2 表结构，数据划分写在正文，软体建模展示 x/y 各自预测轨迹
- 已确认：Figure 2 采用左列三关节、右列软体 x/y 的嵌套子图布局，每个小面板保留三个模型对比曲线
- 绘图方案：`.project-log/specs/paper-revision-experiment-plan.md`

## 2026-09-15 软体平台控制代码备份

- 状态：已完成
- 完成内容：把 `FlexibleArmControl34` 的软体平台 FS-EDMD LQR 控制器及其依赖复制到 `控制实验部分代码/软体平台`
- 文件：控制器脚本、配置、模型与归一化资源、`tk_assets` 依赖模块、`core/base_algorithm.py`、离线实验脚本、`requirements.txt`、备份说明 `README.md`
- 验证：从备份目录直接加载控制器成功，模型维度与闭环谱半径和源工程一致

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
- 完成内容：将软体平台最新三个模型与归一化文件复制到 `结果备份/软体平台训练结果`
- 文件：`fs_edmd.pkl`、`edmd.pkl`、`edmd_dl.pkl`、`meta.npz`
- 修正：初始误复制完整 final 包，已清理为仅保留上述 4 项文件
- 更新：`edmd.pkl` 已替换为修正版，轨迹 66 RMSE 为 `0.8965`
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
