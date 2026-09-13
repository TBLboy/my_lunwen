# 当前需求摘要

- 当前目标：基于新设备软体平台的 100 条原始轨迹，完成固定划分、升维函数库、三类模型训练与配置筛选。
- 当前基线：REQ-002（approved，revision 1）
- 范围内：固定 7:2:1 轨迹划分（70/20/10）、X=x[t]/U=u[t]/Y=x[t+1] 样本处理、约 200 维可配置升维函数库、FS-EDMD/EDMD/EDMDDL 探索训练、固定 10 条测试轨迹的 xy RMSE 评估、探索产物输出到 `杂项/软体平台探索实验结果`
- 范围外：修改原始数据、探索数据划分、修改机械臂建模代码与基线、论文正文、控制实验代码
- 关键约束：数据划分固定且测试集不参与调参；升维函数库必须含常数项和 x/y 分量；代码放建模代码根目录且不创建软体平台子文件夹；中间结果输出到杂项/软体平台探索实验结果；我们的模型最高精度最优，平均 RMSE 尽量低
- 阻塞问题：无
- 原子规则：已固化 BL-SOFT-001 至 BL-SOFT-010，见 `.project-log/business-logic/atoms.yaml`；目录决策见 `DEC-004`

下一步：方案研究与任务拆解已完成，开始 TASK-010 软体平台建模工程说明。

机器可读事实源：`.project-log/requirements/baseline.yaml`、`.project-log/research/solution-research.yaml`、`.project-log/architecture/architecture.yaml` 与 `.project-log/tasks/task-list.yaml`。
