# Task List

Active goal: REQ-002

## 当前任务状态

- TASK-010 软体平台建模工程说明：done
- TASK-011 软体平台数据准备与固定划分：done
- TASK-012 软体平台升维函数库：done
- TASK-013 三训练器软体平台适配与冒烟：done
- TASK-014 固定 10 条测试轨迹 RMSE 评估与探索输出：done
- TASK-015 初始探索批次与最优配置汇总：in-progress
- TASK-016 软体平台全链路验证与文档：pending
- TASK-017 粗到细参数搜索与论文候选最终化：ready（已拆为 5 个执行阶段）

## 下一步

执行 TASK-017：
1. 按 search_plans/README.md 生成并运行 24 组升维库粗搜索。
2. 基于验证集筛 FS-EDMD N/lam/beta/eta_D。
3. 基于验证集细化 EDMDDL n_psi/layers/lr。
4. 只对最终三模型候选确认固定 10 条测试轨迹并刷新正式 leaderboard。
5. 封装论文候选到 final/。
