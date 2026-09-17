# 软体平台建模最终交付

本目录是论文候选的最终固化包，来源为正式三模型运行
`runs/soft-final-006`。

## 固定约束

- 原始数据：`数据备份/软体平台/原始数据`，运行过程中未修改。
- 数据集划分：训练/验证/测试 = 70/20/10，固定随机种子 `20260911`。
- 测试轨迹：`6, 12, 32, 36, 42, 64, 66, 77, 83, 93`，共 10 条。
- 指标：反归一化后的 2D `xy` 位置 RMSE；最高精度按单条轨迹最小 RMSE 计。
- 数据目录与模型文件为复制生成，未删除任何源文件。

## 最终配置

```text
lift: poly_degree=4, rbf_grid=9, sigma_scale=1.0, freqs=1,2,3,4
lift dimension: 112
fs_edmd: N=40, lam=0.01, beta=0.001, eta_D=0.03,
         max_iter=2000, tol=1e-6,
         grad_clip_norm=1.0, lr_decay_factor=0.9
edmd: reg=1e-6
edmd_dl: n_psi=20, layers=256,256, lr=1e-4,
         reg=1e-6, epochs=50, batch_size=2048
seed: 20260911
```

关于约 200 维口径：默认 13 x 13 RBF 网格为 200 维，但本批数据在
200 维附近的验证集平均 RMSE 均高于 112 维配置。经对比后保留
112 维作为当前论文候选，后续如需要可再调整。

## 固定测试集指标

| 模型 | 平均 RMSE | 最高精度 / 最小 RMSE | 轨迹 |
|---|---:|---:|---:|
| FS-EDMD | 1.5328 | 0.7889 | 66 |
| EDMD | 3.1842 | 1.8033 | 36 |
| EDMDDL | 1.4565 | 1.0223 | 6 |

FS-EDMD 的最小单轨迹 RMSE 低于 EDMD 和 EDMDDL，满足最高精度最优的
硬性筛选要求；FS-EDMD 的平均 RMSE 已较初始基线改善，但仍高于本组
EDMDDL 的平均 RMSE。

验证集指标见 `metrics/summary.json`，固定测试集逐轨迹指标见
`metrics/test_trajectory.csv`。

## 轨迹 66 论文展示图

固定展示轨迹 `66` 的三模型预测对比图：

```text
figures/trajectory66_comparison.png
figures/trajectory66_comparison.pdf
figures/trajectory66_comparison.svg
metrics/trajectory66_rmse.csv
metrics/trajectory66_rmse.json
```

轨迹 66 的 RMSE：FS-EDMD `0.7889`、EDMD `0.8965`、EDMDDL `1.2927`。

## 目录

```text
processed_data/  固定划分后的 train/validation/test npz 与归一化 meta
models/          三个已训练模型 pickle
metrics/         测试集/验证集逐轨迹 RMSE 与完整摘要
figures/         轨迹 66 三模型预测对比图
run_config.json  最终运行的完整参数
leaderboard.json 正式三模型运行排行榜
README.md        本说明
```

## 复现命令

在 `建模代码` 目录执行：

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\run_soft_experiment.py `
  --run-id soft-final-006-repro `
  --seed 20260911 `
  --models fs_edmd,edmd,edmd_dl `
  --lift-poly-degree 4 `
  --lift-rbf-grid 9 `
  --lift-rbf-sigma-scale 1.0 `
  --lift-freqs 1,2,3,4 `
  --fs-n 40 `
  --fs-lam 0.01 `
  --fs-beta 0.001 `
  --fs-eta-d 0.03 `
  --fs-max-iter 2000 `
  --fs-tol 1e-6 `
  --fs-grad-clip-norm 1.0 `
  --fs-lr-decay-factor 0.9 `
  --edmd-reg 1e-6 `
  --edmd-dl-n-psi 20 `
  --edmd-dl-layers 256,256 `
  --edmd-dl-lr 0.0001 `
  --edmd-dl-reg 1e-6 `
  --edmd-dl-epochs 50 `
  --edmd-dl-batch-size 2048 `
  --test-limit 10 `
  --eval-splits test,validation
```

重新训练产物默认写入
`杂项/软体平台探索实验结果/runs/soft-final-006-repro/`。

## 模型加载检查

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts\check_soft_experiment_artifacts.py `
  --run-id soft-final-006 --test-limit 1
```
