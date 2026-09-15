# Soft-platform FS-EDMD LQR controller backup

This folder is a copy-only backup of the soft-platform FS-EDMD LQR controller
from `C:\Users\Windows\Desktop\FlexibleArmControl34`.

## Contents

- `algorithms/fs_edmd_lqr_controller.py`: FS-EDMD LQR controller
- `algorithms/configs/fs_edmd_lqr_controller.json`: controller configuration
- `algorithms/fs_edmd_lqr_controller_assets/`: model and normalization assets
- `algorithms/tk_assets/`: runtime lifters and LQR helper modules used by the controller
- `core/base_algorithm.py`: base algorithm interface required by the controller
- `scripts/run_fs_edmd_lqr_offline.py`: offline model-in-the-loop experiment
- `requirements.txt`: Python dependencies copied from the source project

## Offline run

From this folder:

```powershell
python scripts\run_fs_edmd_lqr_offline.py --output-dir controller_offline\backup-check
```

The original files in `FlexibleArmControl34` were not moved or deleted.
