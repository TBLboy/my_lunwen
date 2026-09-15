# 当前需求摘要

- 当前目标：基于最终 FS-EDMD 软体模型，按论文设计实现软体平台 Koopman-LQR 控制器，并完成轨迹 66 离线闭环验证。
- 当前基线：软体平台建模最终包 `杂项/软体平台探索实验结果/final/`
- 范围内：控制器脚本、参数配置文件、独立资源目录、离线闭环脚本、轨迹 66 离线跟踪评估与可视化。
- 范围外：连接真实软体平台硬件、修改原始训练数据、修改最终 FS-EDMD 模型、论文正文。
- 关键约束：控制器格式遵守 `FlexibleArmControl34/algorithms` 现有约定；模型/归一化等资源独立放在控制器资源目录并采用复制而非剪切；离线实验产物输出到 `杂项/软体平台探索实验结果/controller_offline/`。
- 阻塞问题：无
- 原子规则：控制器离线范围已记录于 Q-007；建模原子规则仍为 BL-SOFT-001 至 BL-SOFT-010

下一步：等待用户确认离线闭环结果；确认后可进入硬件接入阶段。

机器可读事实源：`.project-log/requirements/baseline.yaml`、`.project-log/research/solution-research.yaml`、`.project-log/architecture/architecture.yaml` 与 `.project-log/tasks/task-list.yaml`。
