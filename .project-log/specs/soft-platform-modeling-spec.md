# Engineering Spec - TASK-010

## Objective

Implement a reproducible soft-platform modeling pipeline in `建模代码/` using the approved `REQ-002` requirements. The pipeline prepares the 100 raw npz trajectories into a fixed 70/20/10 split, constructs `X=x[t]`, `U=u[t]`, `Y=x[t+1]` samples, provides a configurable roughly 200-dimensional lift library for the 2D `xy` state, trains FS-EDMD, EDMD, and EDMDDL, evaluates every configuration on the fixed 10 test trajectories, and writes all intermediate and final experiment artifacts to `杂项/软体平台探索实验结果`.

The existing mechanical-arm modeling work must remain compatible. The soft-platform implementation reuses the existing modeling package and trainer conventions through narrow adapters rather than creating a parallel `soft_platform` package or directory.

## Non-goals

- Do not modify or move the raw files under `数据备份/软体平台/原始数据`.
- Do not re-split, re-stratify, or tune the dataset split after the fixed split is created.
- Do not use the 10 test trajectories for training, early stopping, or configuration selection.
- Do not replace the FS-EDMD or EDMDDL algorithms with a third-party Koopman package.
- Do not create `建模代码/soft_platform/`.
- Do not modify the completed mechanical-arm data, models, or baseline outputs except for backward-compatible optional trainer parameters.
- Do not write the paper text or final LaTeX figures in this task.

## Related Business Logic

- `REQ-002`: fixed soft-platform split, lift library, three-model exploration, RMSE selection, and output location.
- `BL-SOFT-001`: raw sources are read-only inputs.
- `BL-SOFT-002`: fixed 70/20/10 trajectory split.
- `BL-SOFT-003`: one-step `X/U/Y` sample contract.
- `BL-SOFT-004`: roughly 200-dimensional configurable lift library with constant, `x`, and `y`.
- `BL-SOFT-005`: FS-EDMD exploration training.
- `BL-SOFT-006`: EDMD training.
- `BL-SOFT-007`: EDMDDL exploration training.
- `BL-SOFT-008`: fixed 10-trajectory RMSE evaluation.
- `BL-SOFT-009`: configuration ranking and output contract.
- `BL-SOFT-010`: code and experiment output directory boundary.

## Current Behavior And Evidence

- Raw data contains `01.npz` through `100.npz`, each with `t: (300,)`, `x: (300,2)`, and `u: (300,2)` in Float64.
- Read-only dataset statistics: `x` range approximately `[-10.458, 11.103]` by axis, `u` range approximately `[-68.508, 61.600]`; the split contains 20930 training, 5980 validation, and 2990 test one-step samples.
- The existing `modeling/lift_function.py` is specific to a 6D mechanical-arm state and cannot accept the soft-platform 2D state.
- The existing `modeling/data_io.py` reads MAT files and does not load the soft-platform npz format.
- The existing FS-EDMD and EDMD trainers expose `fit/predict/save/load`; EDMDDL exposes a configurable dictionary network.
- A linear read-only approximation `x[t+1] ~= x[t] + k*u[t]` has residual RMSE about `0.118`, so the lift library must include nonlinear terms.

## Target Behavior

1. `scripts/prepare_soft_data.py` reads and validates all 100 raw npz files, creates one deterministic fixed split with 70 training, 20 validation, and 10 test trajectories, and writes processed `X/U/Y` Float64 npz files plus a split manifest and statistics report under `杂项/软体平台探索实验结果/processed_data`.
2. `modeling/soft_data.py` loads the processed arrays and normalization metadata without changing their trajectory membership.
3. `modeling/soft_lift.py` exposes a configurable `SoftLift`/function contract for `(N,2)` states. The default candidate is about 200 dimensions: constant and `x/y`, polynomial terms through degree 4, a normalized 13x13 Gaussian RBF grid, and low-frequency sin/cos terms.
4. Existing FS-EDMD and EDMD trainers accept an optional `lift_fn` while retaining the current mechanical-arm function as the default.
5. EDMDDL uses `state_dim=2` and `control_dim=2` with configurable `n_psi` and layer sizes.
6. `scripts/run_soft_experiment.py` runs one named configuration, trains all three models, evaluates each on all 10 fixed test trajectories, and writes the configuration, models, per-trajectory RMSE, average RMSE, best trajectory, and logs to `杂项/软体平台探索实验结果/runs/<run_id>`.
7. Configuration selection ranks against the fixed test set only after training and uses the user-confirmed rule: FS-EDMD must have the lowest best-trajectory RMSE; its average RMSE should be as low as possible. The EDMDDL/EDMD second-place order is not a hard constraint.

## Affected Components

Under `建模代码/`:

- `modeling/soft_data.py`
- `modeling/soft_lift.py`
- `modeling/trainers/fs_edmd.py`
- `modeling/trainers/edmd.py`
- `scripts/prepare_soft_data.py`
- `scripts/run_soft_experiment.py`
- `scripts/evaluate_soft_experiments.py`
- `README.md`
- `requirements.txt`

Experiment outputs under `杂项/软体平台探索实验结果/`:

- `processed_data/`
- `runs/<run_id>/`
- `summaries/`

## Interfaces And Schemas

### Processed data

`prepare_soft_data.py` outputs files equivalent to:

```text
train.npz: X (20930,2), U (20930,2), Y (20930,2), trajectory_id (20930,), step_index (20930,)
val.npz:   X (5980,2),  U (5980,2),  Y (5980,2),  trajectory_id, step_index
test.npz:  X (2990,2),  U (2990,2),  Y (2990,2),  trajectory_id, step_index
meta.npz:  x_mean, x_scale, u_mean, u_scale
split_manifest.json: seed, source files, train/val/test trajectory ids, counts, hashes
dataset_stats.json: raw and processed shapes, ranges, means, standard deviations
```

`X`, `U`, and `Y` are always `float64`. The test set contains exactly 10 trajectory ids and is never concatenated into training or validation.

### Lift interface

```python
lift = SoftLift.from_stats(meta, config)
phi = lift(x)          # (N, 2) -> (N, D) float64
report = lift.report() # dimension, groups, normalization, stability diagnostics
```

The default configuration must contain:

- constant, `x`, `y`;
- polynomial terms through degree 4;
- normalized Gaussian RBF centers;
- low-frequency sin/cos terms.

The exact configuration is persisted for each run so it can be reproduced without inspecting process memory.

### Trainer interface

Existing trainer methods remain:

```text
fit(...), predict(x0, u_sequence, steps=None), save(path), load(path)
```

FS-EDMD and EDMD gain an optional `lift_fn` constructor argument. The default remains the mechanical-arm `lift_function`.

### Run contract

Each experiment run writes:

```text
run.yaml
models/fs_edmd.pkl
models/edmd.pkl
models/edmd_dl.pkl
metrics/per_trajectory.csv
metrics/summary.json
logs/train.log
```

The summary must contain per-method `average_rmse`, `best_rmse`, `best_trajectory_id`, and all 10 per-trajectory values.

## State, Concurrency And Lifecycle

- The split manifest and normalization metadata are immutable inputs to a run.
- Runs are identified by a stable `run_id`; each run owns a separate directory.
- Runs may execute sequentially. Parallel runs are allowed only when their output directories are disjoint.
- Re-running a `run_id` replaces that run directory after writing to a temporary sibling and moving it atomically.
- Failed runs receive a `FAILED` marker and never appear as successful in the summary.

## Failure Handling

- Missing files, missing fields, non-2D arrays, NaN/Inf, or an incorrect split count stop data preparation.
- A test-set trajectory appearing in train/validation is a fatal split error.
- A lift dimension mismatch or non-finite feature output stops that training run.
- Training numerical failures mark the run failed with the exception and configuration recorded.
- Evaluation fails if fewer/more than 10 test trajectories or non-finite predictions are present.
- A failure never silently selects a different split, seed, lift configuration, or normalization mode.

## Security And Privacy

- No network access, credentials, or external services.
- Only local project data is read.
- Raw data is never modified and is not deleted during cleanup.

## Observability

- Every command prints source/output paths, shapes, split counts, run id, feature dimension, model configuration, and metric summary.
- Each run persists the full configuration and a machine-readable summary.
- A top-level summary table provides a compact comparison across runs.

## Compatibility, Migration, Rollout And Rollback

- Mechanical-arm commands continue to use the existing default `lift_function` and MAT data path.
- New soft-platform modules are additive; existing model pickle formats remain unchanged where possible.
- Rollback removes only new soft-platform modules/scripts and generated experiment runs; mechanical-arm data and models remain untouched.
- The Python environment remains Python 3.10 with NumPy, SciPy, Torch, scikit-learn, and Matplotlib.

## Verification Matrix

1. Data preparation check: source files remain unchanged; split counts are exactly 70/20/10 and disjoint; processed arrays are Float64 and finite.
2. Lift check: default dimension is about 200; `(N,2)` input yields finite Float64 output; constant/x/y columns are present; configuration report exists.
3. Trainer regression: existing mechanical-arm `--check-load` commands still pass.
4. Soft smoke: all three models can complete a short training run, save, reload, and predict.
5. Evaluation check: each method has exactly 10 per-trajectory RMSE values; average and best values follow the recorded formulas.
6. Exploration check: the top-level summary records every run and can identify the candidate satisfying the FS-EDMD selection rule.
7. Project log check: `validate_project.py --root .` passes after all task updates.

## Open Questions And Authority

- The exact deterministic split seed and candidate feature-library parameters are A/B implementation details and must be recorded in generated manifests.
- If a model or feature variant produces invalid results, it is retained as failed evidence rather than silently discarded.
- Changing the fixed test trajectory set, metric definition, or requirement to keep FS-EDMD best requires user confirmation.
