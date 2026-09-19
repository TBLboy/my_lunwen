# Vibe Coding 框架真实使用问题复盘

日期：2026-09-19

范围：本仓库从 2026-09-10 到 2026-09-19 的真实使用记录，包括论文建模、数据审计、绘图、LaTeX 排版、参考文献格式调整和项目日志维护。

目的：总结 Vibe Coding 框架在实际执行中暴露的流程、运行时、工具适配和状态管理问题，为后续优化提供依据。本文不是对框架价值的否定，而是对“当前实现是否按预期工作、代价是否合理”的复盘。

## 1. 结论摘要

当前框架的主要问题不是“没有记录”，而是：

1. 记录和控制层过重，简单修改也容易触发完整生命周期。
2. 多个状态文件需要手工同步，真实状态开始出现不一致。
3. 证据失效按文件路径粗粒度处理，导致大量有效证据被误伤。
4. 运行时对 Windows、PowerShell、中文路径和非 UTF-8 Git diff 的适配不足。
5. 独立验证、复盘和蒸馏在真实使用中没有形成稳定闭环。

一句话判断：当前框架更像一个高审计强度的工程控制系统，但缺少按风险分级、自动生成视图和语义化证据依赖的机制，因此真实使用中的边际收益快速下降。

## 2. 使用数据快照

以下数据来自当前 `.project-log`：

| 对象 | 数量或大小 | 说明 |
|---|---:|---|
| 任务 | 38 | 36 done，1 cancelled，1 blocked |
| 决策 | 17 | 14 active，3 superseded |
| 证据 | 69 | 30 valid，39 stale |
| 工作轨迹 | 15 | 数量远少于任务数 |
| Loop 事件 | 2511 | 2249 次 `work-unit-finished`，37 次 `run-started`，71 次 `handoff-generated`，76 次 `evidence-recorded`，39 次 `evidence-invalidated`，37 次 `loop-decision` |
| 独立复核事件 | 0 | 未发现 `review-completed` 事件 |
| `task-list.yaml` | 98,627 bytes / 2,534 行 | 单体大文件 |
| `decision-log.yaml` | 43,048 bytes / 731 行 | 单体大文件 |
| `evidence-index.yaml` | 96,684 bytes / 1,892 行 | 单体大文件 |
| `events.jsonl` | 588,026 bytes / 2,499 行 | 事件量很大 |
| `current-session.md` | 72,609 bytes / 538 行 | 已接近建议归档阈值 |
| `progress.md` | 40,307 bytes / 503 行 | 与 current-session 存在重复维护 |
| `trace.yaml` | 24,516 bytes / 227 行 | 覆盖密度明显低于事件日志 |

## 3. 高优先级问题

### P0-1：控制层状态与业务目标脱节

当前状态同时出现：

- `GOAL-001` 已标记为 `complete`。
- `workflow.yaml` 显示 `implementation` 和 `verification` 已完成，`current_phase` 为 `verification`。
- `active-run.yaml` 仍显示 `phase: implementation`、`task_id: TASK-030`、`status: active`。
- `TASK-030` 在任务清单中实际为 `blocked`，阻塞于 `Q-021`。
- `active-run.yaml` 的 `next_action` 为 `null`，没有表达“等待用户提供作者信息”。
- Native Goal 为 `unbound`。

影响：

- 恢复会话时，机器状态无法回答“现在到底是在执行、等待用户，还是已经结束”。
- `active` 与 `blocked` 同时存在，容易让后续 Agent 继续执行一个实际上必须等待用户的任务。
- 旧目标已经完成，但新论文工作仍挂在一个未重新绑定的运行中，目标生命周期没有正确切换。

建议：

- 明确定义 Goal、Run、Task 三者的关闭和切换规则。
- 当任务需要用户事实时，`active-run.status` 应切换为 `waiting-user` 或 `blocked`，并写入明确 `next_action`。
- Goal 完成时，必须同步关闭或替换旧 Run；不能留下旧的 `active` Run 继续承接新工作。
- 增加一致性校验：Goal 完成、Task blocked、Run active、Next action null 不能同时通过校验。

### P0-2：证据失效粒度过粗

当前证据绑定方式以文件路径为主。只要某个被覆盖文件发生变化，相关证据就可能全部失效。

观察到：

- 69 条证据中已有 39 条 stale。
- 39 次失效中，23 次原因是通用的 `PostToolUse:apply_patch`。
- `main.tex`、`manuscript_body.tex`、`references.bib` 等核心文件几乎参与所有论文证据。
- 一次局部排版、参考文献或图注修改，可能让多个不相关的旧证据同时失效。

影响：

- 证据状态频繁变化，降低索引的可读性。
- 为了重新得到“valid”状态，Agent 容易重复执行同一套编译、扫描和哈希检查。
- 文件级绑定无法表达“这条证据只覆盖某一段公式、某个指标、某张图或某个引用范围”。

建议：

- 为证据增加语义范围，例如 `claim`、`section`、`figure`、`table`、`data-run`、`command-signature`。
- 支持按内容切片、结构化字段或生成产物哈希绑定，而不是只按文件路径。
- 将构建产物、日志文件和源文件分成不同证据层，避免一个临时 build 文件变化使全部源证据失效。
- 引入证据依赖图：只有上游输入或验证范围变化时，才使下游证据 stale。

### P0-3：`record-evidence` 在真实 Windows 环境中会因 Git diff 解码失败而中断

实际故障：

- `loopctl.py record-evidence` 使用 `subprocess.run(..., text=True)` 读取 Git diff。
- 当 diff 包含当前系统 locale 无法解码的字节时，命令直接抛出：
  - `'gbk' codec can't decode byte ...`
  - 或 `'utf-8' codec can't decode byte ...`
- 本次只能通过临时绕过 `version_binding`、改用二进制读取 diff 才完成 `EV-069` 登记。

影响：

- 证据登记是核心操作，一旦失败，后续完成状态、handoff 和校验都会被阻断。
- 中文路径、数学 Unicode 字符、二进制构建产物和 Git 输出都可能触发类似问题。

建议：

- `run_git` 改为二进制模式返回 `bytes`，或者显式使用 `errors="surrogateescape"`。
- `diff_hash` 直接对原始 bytes 计算，不要先强制解码为本地文本。
- 所有 CLI 显式设置 UTF-8 输出编码，并避免依赖 Windows 默认代码页。
- 增加包含中文路径、数学符号、二进制 diff 的回归测试。

## 4. 中优先级问题

### P1-1：Windows 与 PowerShell 适配不足

实际观察：

- 全局文档和 Skill 示例默认使用 Bash、`python3`、`py -3` 和 Unix 路径风格。
- 当前 Windows 环境没有可用的 `py`，`python3` 也不稳定可用。
- 正确的解释器实际记录在 `~/.codex/vibe-python`，但多数命令没有自动读取它。
- 多次命令被交给 WSL/Bash，导致 `Get-Content`、`Select-Object`、`rg` 等 PowerShell 命令无法执行。
- 中文路径在 Bash/WSL 路径转换时曾被显示为 `????`，导致 Python `Path.read_text` 报 `Invalid argument`。

影响：

- 简单操作需要反复手动修正 shell 和解释器。
- 失败原因容易被误判为项目或 Skill 错误，实际是运行环境不匹配。
- 命令不可复现，后续 Agent 难以稳定重放。

建议：

- 提供 Windows 原生入口，例如 `vibe.ps1`、`vibe.cmd` 或 `vibe.exe`。
- 所有脚本从 `vibe-python` 读取解释器，而不是硬编码 `python3` 或依赖 PATH。
- 文档区分 Windows PowerShell 和 Unix shell 的命令示例。
- 中文路径、空格路径和非 ASCII 输出必须进入基础 smoke test。
- 禁止在 PowerShell 任务中静默切换到 WSL。

### P1-2：多个“事实源”需要手工同步

同一状态目前分散在：

- `task-list.yaml`
- `decision-log.yaml`
- `workflow.yaml`
- `active-run.yaml`
- `handoff.md`
- `current-session.md`
- `progress.md`
- `evidence-index.yaml`
- 各任务的 `verification` 和 `result`

影响：

- 更新一个任务通常要改 3 到 6 个位置。
- `current-session.md` 和 `progress.md` 内容高度重复。
- 快照、handoff、workflow 和 task-list 已经出现时间与状态不一致。
- Agent 很大一部分时间花在“让日志彼此看起来一致”，而不是解决用户问题。

建议：

- 选定一个机器可读的规范状态源。
- `current-session.md`、`progress.md`、`handoff.md` 和摘要表格改为自动生成。
- 只允许通过命令修改状态，禁止 Agent 手工拼接多个视图。
- 为所有状态加入统一 `updated_at`、`state_revision` 和 `source_of_truth`。

### P1-3：单体日志文件不可持续扩展

当前文件规模已经不适合频繁读取和局部修改：

- `task-list.yaml` 接近 100 KB。
- `evidence-index.yaml` 接近 100 KB。
- `events.jsonl` 接近 600 KB。
- `current-session.md` 已超过 70 KB。

影响：

- 每次恢复和更新都要读取大段历史。
- 容易触发输出截断，Agent 只能看到部分内容。
- 修改大 YAML 时，定位和冲突风险显著增加。

建议：

- 已完成任务、历史决策和 stale 证据按月份或目标归档。
- 主索引只保留 active、blocked、最近完成和摘要引用。
- 事件日志按 run 或日期分片，并生成小型状态索引。
- 当查询需求增长时，考虑 SQLite 或等价的结构化存储，而不是继续堆 YAML/JSONL。

### P1-4：生命周期对所有任务一刀切

真实使用中，38 个任务主要落在 `implementation`，而简单排版、术语和参考文献调整也容易触发：

- 任务登记
- 决策记录
- 工作轨迹
- 证据绑定
- handoff
- current-session/progress 同步

影响：

- 低风险、可逆、单文件修改的成本远高于收益。
- Agent 倾向先维护流程，再处理正文。
- 用户感知到“每个小任务都很慢”。

建议：

- 引入任务分级：
  - L0：纯文本、注释、格式或可逆小改动，只做目标检查和一次针对性验证。
  - L1：普通实现，要求任务、变更记录和基础验证。
  - L2：影响数据、结论、接口、安全、投稿格式或跨模块行为，才启用完整证据链和独立复核。
- 在任务入口自动判断等级，而不是默认全量流程。
- 为 L0 提供明确禁止升级流程的条件，避免 Agent 自行扩大审计范围。

### P1-5：独立验证在实践中没有真正发生

事件记录中没有 `review-completed`，说明当前大量“验证”仍然由执行修改的同一 Agent 完成。

影响：

- 验证可能存在自证偏差。
- 框架文档要求“实现 Agent 不得自证完成”，但运行时没有强制该边界。
- 只有编译或扫描通过，不能证明需求、数据和论文结论没有被误解。

建议：

- 对 L2 任务强制使用独立 reviewer 或明确标注 `serial-role-fallback`。
- reviewer 必须只读目标产物、需求、证据和差异，不能直接复用实现者的结论。
- 将 reviewer 结论作为任务 done 的必要条件，而不是可选建议。

## 5. 低优先级问题

### P2-1：复盘和蒸馏没有跟上实现节奏

- 已完成大量任务，但 `retrospective.yaml` 长期为空。
- `distillation/candidates.yaml` 有候选，但 retrospective gate 没有稳定触发。
- 工作轨迹只有 15 条，远少于 38 个任务。

建议：

- 每完成一个目标或一个高风险任务批次，自动生成 retrospective 草稿。
- 只对重复出现且有证据的问题生成 distillation candidate。
- 不要求每个小任务都写工作轨迹。

### P2-2：上下文和工具输出偏重

- 全局规则、项目规则、Skill、任务日志和证据索引叠加后，单次恢复读取量很大。
- `events.jsonl` 和多个大 YAML 很容易触发截断。
- 多次重复读取同一个 PDF、图片、日志或 Skill 文件。

建议：

- 为任务生成最小上下文包，只包含相关任务、业务原子、决策和证据。
- 大文件提供摘要索引和按 ID 查询命令。
- 对图片和 PDF 只在需要视觉判断时加载，并记录一次结论，避免重复读取。

### P2-3：临时产物和归档卫生不足

`.project-log` 根目录存在多张 `tmp-*`、`split_fig_check-*` 和中间检查图片。它们有价值时可以作为证据，但不应长期散落在主目录。

建议：

- 统一放入 `artifacts/<run-id>/` 或 `docs/archive/`。
- 为临时产物增加生命周期、清理规则和引用检查。
- 主日志目录只保留长期可复用的文档和索引。

## 6. 根因分析

### 根因 A：审计强度没有按风险分级

框架把“可追溯”和“完整审计”绑定得太紧，导致低风险修改也承担高风险任务的控制成本。

### 根因 B：缺少单一规范状态模型

同一事实在多个 Markdown、YAML 和 JSONL 中重复表达，却没有自动生成或双向一致性约束。

### 根因 C：证据依赖仍是文件级，而不是语义级

文件路径是最容易实现的绑定方式，但对论文、代码和实验这类共享核心文件的项目，粒度明显过粗。

### 根因 D：运行时假设了 Unix 风格环境

Skill 和脚本的示例、解释器调用、路径处理、文本解码没有把 Windows 作为一等环境。

### 根因 E：Goal、Run、Task 的职责边界不稳定

项目目标完成后，运行和任务没有可靠切换；等待用户、阻塞和活跃状态也没有被严格区分。

### 根因 F：执行与复核没有形成制度性分离

文档要求独立复核，但运行时没有真正记录或强制 review 事件。

## 7. 建议的优化路线

### 第一阶段：先修正确性和可运行性

1. 修复 `run_git`/`version_binding` 的二进制解码问题。
2. 增加 Windows 原生入口和 `vibe-python` 自动解析。
3. 修正 Goal、Run、Task 的状态机，增加 `waiting-user` 和一致性校验。
4. 自动归档已完成任务和 stale 证据，缩小主索引。

### 第二阶段：降低日常成本

1. 引入 L0/L1/L2 任务分级和对应验证策略。
2. 将 current-session、progress、handoff 改为自动生成视图。
3. 把任务、证据和事件按日期或目标分片。
4. 增加按任务生成的最小上下文包。

### 第三阶段：提高质量保证

1. 实现语义化证据范围。
2. 建立证据依赖图和精确失效规则。
3. 对 L2 任务强制独立 reviewer。
4. 建立 retrospective 和 distillation 的自动触发条件。

## 8. 优化后的验收标准

框架优化完成后，至少应满足：

- 一个 L0 单文件修改不需要更新完整生命周期。
- Windows PowerShell 下不需要手工切换解释器或 shell。
- `record-evidence` 在中文路径、数学 Unicode 和二进制 diff 下稳定运行。
- Goal、Run、Task、handoff 的状态完全一致，不存在完成 Goal 下仍 active 的旧 Run。
- 局部文件修改只使相关证据失效，不使无关证据批量 stale。
- `current-session.md` 和 `progress.md` 不再手工重复维护。
- L2 任务存在真实独立 review 事件。
- 单次会话恢复只读取任务相关的上下文包，而不是全部历史文件。

## 9. 建议优先级

| 优先级 | 事项 | 预期收益 |
|---|---|---|
| P0 | 修复证据登记的解码和二进制 diff 问题 | 避免核心流程直接失败 |
| P0 | 统一 Goal/Run/Task 状态机 | 恢复状态可信，减少错误续跑 |
| P0 | 证据从文件级改为语义级 | 显著减少 stale 和重复验证 |
| P1 | Windows/PowerShell 原生适配 | 消除大量环境性返工 |
| P1 | 自动生成摘要视图 | 减少手工同步和日志冲突 |
| P1 | L0/L1/L2 分级 | 降低简单任务成本 |
| P1 | 独立 reviewer 强制化 | 提高高风险任务可信度 |
| P2 | 归档、分片和上下文包 | 控制长期上下文成本 |

## 10. 证据与置信度

高置信度：

- 日志体量、事件数量、证据 stale 比例和任务状态来自当前结构化文件。
- Windows 解释器、WSL 切换、中文路径和 Git diff 解码问题在本轮真实操作中重复出现。
- Goal、Run、Task 的状态不一致可从当前 YAML 直接复核。

中等置信度：

- “简单任务耗时大部分不在任务本身”来自本轮实际操作体验和日志规模，缺少精确的逐命令耗时统计。
- 独立验证缺失由 `review-completed` 事件为零推断；如果外部流程有未记录的人工复核，该结论需要修正。

低置信度：

- 各问题对总耗时的具体百分比无法从现有日志精确计算。
- 归档阈值、任务分级边界和证据语义范围需要通过一轮真实试用再定稿。

