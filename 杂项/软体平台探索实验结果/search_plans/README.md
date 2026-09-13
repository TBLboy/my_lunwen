# Soft Platform Parameter Search Plan

## Objective

Starting from `soft-base-001`, find a reproducible paper candidate where
FS-EDMD has the lowest best/min per-trajectory RMSE on the fixed 10 test
trajectories, while its average RMSE is as low as possible.

## Evaluation Discipline

- Coarse and fine searches rank candidates on the validation split only.
- The fixed 10 test trajectories are used only for final candidate confirmation.
- Coarse runs may still write test metrics for compatibility, but those values
  must not be used to prune or select candidates.
- The formal leaderboard counts only complete non-smoke three-model runs.

## Stage 1: Lift Library Coarse Search

Run FS-EDMD and EDMD with baseline FS hyperparameters while varying:

- `lift_poly_degree`: 3, 4
- `lift_rbf_grid`: 9, 11, 13, 15
- `lift_rbf_sigma_scale`: 0.6, 0.8, 1.0

Total: 24 runs. Keep the top 1-3 lift candidates by validation FS-EDMD
`average_rmse`, with FS best/min RMSE and condition number used as tie-breakers
and stability checks.

## Stage 2: FS-EDMD Coarse to Fine Search

Using the best lift configuration:

1. Sweep `fs_n`: 20, 40, 80, 120.
2. At the best `fs_n`, sweep a 3x3x3 grid:
   - `fs_lam`: 1e-4, 1e-3, 1e-2
   - `fs_beta`: 1e-4, 1e-3, 1e-2
   - `fs_eta_d`: 5e-3, 1e-2, 3e-2

Total: 31 FS/EDMD runs. Rank by validation FS-EDMD average RMSE while keeping
the FS best/min RMSE advantage intact. Failed or non-finite runs are recorded
and do not block the campaign.

Additional FS optimizer searches:

- `soft-fs-opt-001`: sweep `fs_lr_decay_factor` and `fs_grad_clip_norm`.
- `soft-fs-opt2-001`: local refinement around the winning optimizer setting.
- `soft-lift-optg-001`: re-check 11/13/15 RBF grids under the improved
  optimizer settings, to confirm the lift dimension choice.

## Stage 3: EDMDDL Fine Search

Using the winning lift and FS settings, run EDMDDL-only validation searches:

- `edmd_dl_n_psi`: 20, 50, 100
- `edmd_dl_layers`: 256,256 and 512,512,512
- `edmd_dl_lr`: 3e-4, 1e-4

Total: 12 runs. Keep the best EDMDDL setting for the final three-model runs.

## Stage 4: Final Three-Model Runs

Select at most 3 full three-model candidates, including the best FS candidate,
a second FS candidate if it is materially different, and the baseline fallback.
Run each on the fixed 10 test trajectories and refresh the formal leaderboard.

Final selection:

- FS-EDMD must be strictly better than the best of EDMD/EDMDDL on the
  best/min trajectory RMSE criterion.
- Among such candidates, choose the lowest FS-EDMD average RMSE.
- If no candidate passes, keep `soft-base-001` as fallback and document why.

## Stage 5: Final Package

Copy to `final` under this experiment root:

- selected models
- `run_config.json`
- per-trajectory RMSE CSVs
- summary metrics
- reproducible command documentation

Campaign or summary reports follow the names:

- `search_plans/*.json`
- `search_plans/*.report.json`
- `summaries/leaderboard.json`
- `summaries/leaderboard.csv`
