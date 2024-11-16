"""
Initialization module for QhX package.

This module aggregates various functionalities from submodules, providing a unified 
interface for the QhX package. It imports key classes, functions, and utilities 
across data management, light curve analysis, calculations, detections, output 
classifications, plotting, utilities, and dynamical mode processing.

Imports:
    - Data management: All functionalities from `data_manager`.
    - Light curve analysis: All functionalities from `light_curve`.
    - Calculations: Specific functions for full width calculation, period extraction, and significance classification.
    - Detections: All functionalities from `detection`.
    - Output classification: Period classification functions from `output`.
    - Plotting: All plotting utilities from `plots`.
    - Utilities: All utility functions and helpers from `utils`.
    - Interactive plotting: Functions for handling large files interactively.
    - Dynamical mode processing: Key functions for dynamic light curve processing.

"""

from QhX.data_manager import *
from QhX.light_curve import *
from QhX.calculation import get_full_width,periods, signif_johnson
from QhX.detection import *
from QhX.output import classify_periods, classify_period
from QhX.plots import *
from QhX.utils import *
from QhX.interactive_plot_large_files import *
from .dynamical_mode import get_lc_dyn, process1_new_dyn, DataManagerDynamical

