# Engineering Spec - TASK-001

## Objective

Build a self-contained `建模代码/` Python project in the current repository. It must copy mechanical-arm data and trained models from `杂项/`, refactor the three modeling methods into importable package modules, and provide CLI entrypoints that implement the complete closed loop: data loading, training or model loading, 800-step evaluation, metric output, and paper-style position/velocity comparison figures.

The source of truth is the current `杂项/` plotting scripts and data. `论文3/1_建模精度对比` is used only for comparison context and is not a runtime dependency.

## Non-goals

- Do not migrate `train_nn.py`, old `show_*.py`, control experiments, soft-platform data, result backups, or MATLAB/Simulink generation code.
- Do not modify `杂项/`, `数据备份/`, `结果备份/`, `控制实验部分代码/`, or `论文3/`.
- Do not redesign the mathematical training algorithms or change their numerical contracts.
- Do not commit to Git unless the user explicitly asks.
- Do not create a web application, service, or external data source.

## Related Business Logic

- `REQ-001`: self-contained modeling directory copied from current `杂项` resources, complete closed loop, reproducible output.
- `ARCH-001`: `data/`, `models/`, `outputs/`, `modeling/`, and `scripts/` ownership boundaries.
- `BL-MODELING-001`: copy only, never cut or delete source files.
- `BL-MODELING-002`: data loading contract from local MAT files.
- `BL-MODELING-003`: complete closed-loop entrypoint.
- `BL-MODELING-004`, `BL-MODELING-005`, `BL-MODELING-006`: FS-EDMD, EDMDDL, EDMD training flows.
- `BL-MODELING-007`: metric output contract.
- `BL-MODELING-008`: position/velocity figure output contract.

## Current Behavior And Evidence

Current `杂项/` contains the verified baseline:

- `utils.py`: MAT loading, denormalization, metrics, plotting style.
- `lift_function.py`: standalone feature library; same version as `论文3`.
- `train_ours.py`: `OursKoopmanTrainer`, the current FS-EDMD method.
- `train_edmddl.py`: `DicNN` plus `EDMDDLTrainer`.
- `train_edmd.py`: `EDMDTrainer`.
- `compare_all.py`: verified plotting and metric entrypoint.
- `data/train_data.mat`, `data/val_data.mat`, `data/test_data.mat`; `models/*.pkl` and `models/meta.npz`.

Verified evidence:

- Runtime: `C:\Users\Windows\.conda\envs\edmddl2\python.exe`, Python 3.10.
- Dependencies: NumPy, SciPy, Matplotlib, PyTorch, scikit-learn.
- Baseline metrics in `杂项/figures/metrics_table.txt`:
  - FS-EDMD MSE `0.352044`
  - EDMDDL MSE `0.593580`
  - EDMD MSE `0.725641`
- Current `compare_all.py` completes 800-step predictions and produces non-empty PNG/PDF/SVG figures.

## Target Behavior

`建模代码/` must run without referencing `论文3` or `杂项` at runtime. The following behaviors are required:

1. `data/` and `models/` contain byte-identical copies of the current `杂项` source resources.
2. `modeling/data_io.py` loads `train_data.mat`, `val_data.mat`, `test_data.mat`, and `meta.npz` with the same arrays and metadata as `utils.py`.
3. `modeling/metrics.py` computes scalar MSE/RMSE/MAE and per-dimension RMSE exactly as `utils.calculate_metrics`.
4. `modeling/lift_function.py` exposes the same `lift_function` implementation as current `杂项`.
5. `modeling/trainers/fs_edmd.py`, `edmddl.py`, and `edmd.py` preserve the existing class behavior, Float64 contracts, saved pickle layouts, and prediction semantics.
6. `scripts/train_fs_edmd.py`, `scripts/train_edmddl.py`, and `scripts/train_edmd.py` can train, save, and load their models. Each supports a `--check-load` mode that validates loading the project-local copied model.
7. `scripts/evaluate_and_plot.py` performs evaluation and plotting in one run, writes `outputs/metrics/metrics_table.txt`, and writes `outputs/figures/position_comparison.{png,pdf,svg}` and `outputs/figures/velocity_comparison.{png,pdf,svg}`.
8. `README.md` and `requirements.txt` document commands, environment, directory layout, and expected baseline metrics.

## Affected Components

Target files under `C:\Users\Windows\Desktop\论文材料\建模代码\`:

- `data/`
- `models/`
- `outputs/metrics/`
- `outputs/figures/`
- `modeling/__init__.py`
- `modeling/data_io.py`
- `modeling/lift_function.py`
- `modeling/metrics.py`
- `modeling/trainers/__init__.py`
- `modeling/trainers/fs_edmd.py`
- `modeling/trainers/edmddl.py`
- `modeling/trainers/edmd.py`
- `scripts/train_fs_edmd.py`
- `scripts/train_edmddl.py`
- `scripts/train_edmd.py`
- `scripts/evaluate_and_plot.py`
- `README.md`
- `requirements.txt`

Project log files affected:

- `.project-log/specs/modeling-refactor-spec.md`
- `.project-log/tasks/task-list.yaml`
- `.project-log/workflow.yaml`
- `.project-log/current-session.md`
- `.project-log/verification/evidence.yaml`
- `.project-log/loop/` records managed through `loopctl`.

## Interfaces And Schemas

Run from the project root:

```powershell
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts/evaluate_and_plot.py
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts/train_fs_edmd.py --check-load
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts/train_edmddl.py --check-load
& 'C:\Users\Windows\.conda\envs\edmddl2\python.exe' scripts/train_edmd.py --check-load
```

`data_io` interface:

- `get_data_path(filename)` -> local `data/filename`.
- `get_model_path(filename)` -> local `models/filename`.
- `get_output_path(subdir, filename)` -> local `outputs/subdir/filename`.
- `load_train_data()` -> `(X_train, Y_train, U_train, meta)`.
- `load_val_data()` -> `(X_val, Y_val, U_val)`.
- `load_test_data()` -> `(X_test, U_test)`.
- `denormalize(x_norm, q_scaler, q_dc)` -> inverse normalized array.
- `load_meta()` -> meta dict from `models/meta.npz`.

Trainer interface:

- `fit(...)`, `predict(x0, u_sequence, steps=None)`, `save(path)`, `load(path)`.
- FS-EDMD class keeps the `OursKoopmanTrainer` name for compatibility and may add `FSEDMDTrainer` as an alias.
- EDMDDL keeps `DicNN` and `EDMDDLTrainer`.
- EDMD keeps `EDMDTrainer`.

Evaluation script behavior:

- Default prediction horizon `--steps 800`.
- Model keys: `fsedmd`, `edmddl`, `edmd`.
- Output labels: `FS-EDMD`, `EDMDDL`, `EDMD`.
- Position dimensions: columns `[0, 2, 4]`; velocity dimensions: columns `[1, 3, 5]`.
- Time axis: `t = arange(T) * 0.004`.

Metrics table format must remain readable by the user and comparable to baseline:

```text
方法 MSE RMSE MAE
FS-EDMD ...
EDMDDL ...
EDMD ...
```

## State, Concurrency And Lifecycle

- Filesystem is the main state. No server or shared mutable service is introduced.
- One process writes a fixed set of output paths. Training and evaluation are sequential.
- Training scripts overwrite their configured model paths by default.
- Evaluation overwrites `outputs/` files by default but does not overwrite `models/`.
- Resource migration is copy-only and verifies source files continue to exist.

## Failure Handling

- Missing source or target files in migration fail with an explicit list and do not create partial project artifacts.
- Missing MAT fields produce an error naming the file and missing field.
- Failed model loading in evaluation prints the missing model path and exits non-zero.
- NaN during FS-EDMD training stops with the existing rollback behavior.
- Linear solve failures in EDMD/EDMDDL propagate as script errors.
- Plot save failures prevent a partial-success claim; the script exits non-zero without pretending outputs exist.

## Security And Privacy

- No credentials, private keys, network calls, or external services.
- Local filesystem access only.
- Do not log raw dataset contents beyond shapes and metric values.

## Observability

- Each script prints current step, absolute local paths, shapes, and final metric summary.
- `evaluate_and_plot.py` reports output paths and metrics.
- Verification records exit code, output file existence, non-empty size, and metric comparison.

## Compatibility, Migration, Rollout And Rollback

- Migration source: current `杂项/data` and `杂项/models`.
- Migration method: `Copy-Item`, then hash verification; source files remain untouched.
- Runtime compatibility: Python 3.10 with `numpy`, `scipy`, `matplotlib`, `torch`, `sklearn`.
- Rollback: delete only newly created `建模代码/` files if requested by the user; original `杂项` resources remain intact and are the recovery baseline.

## Verification Matrix

1. Copy hash check: every copied `data/` and `models/` file matches the source SHA-256 and source files still exist.
2. Data contract: load shapes and fields match current `utils.py` behavior.
3. Trainers: `--check-load` succeeds for all three project-local models.
4. Closed loop: `scripts/evaluate_and_plot.py` exits 0, all seven output files are non-empty.
5. Metric alignment: reproduced MSE values match baseline within `1e-4` and no model diverges.
6. Project log: `validate_project.py --root .` succeeds after updates.

## Open Questions And Authority

- No blocking open questions remain.
- Authority: implementation details are `A/B` as recorded in tasks; semantic changes or deletions require user approval.
