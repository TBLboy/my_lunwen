"""Trainer package for FS-EDMD, EDMDDL and standard EDMD."""

from modeling.trainers.edmd import EDMDTrainer
from modeling.trainers.edmddl import EDMDDLTrainer
from modeling.trainers.fs_edmd import FSEDMDTrainer, OursKoopmanTrainer

__all__ = [
    "OursKoopmanTrainer",
    "FSEDMDTrainer",
    "EDMDDLTrainer",
    "EDMDTrainer",
]
