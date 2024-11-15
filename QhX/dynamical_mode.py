
# pylint: disable=R0801

"""
dynamical_mode.py

This module provides classes and functions for dynamically managing and analyzing light curve data,
including loading, grouping, processing, and detecting periods across different bands using wavelet analysis.

Classes:
--------
- DataManagerDynamical: A class to load, group, and preprocess light curve data, with support for optional column 
  and filter mappings.

Functions:
----------
- get_lc_dyn: Processes and returns light curves with options to handle different filters and include errors.
- process1_new_dyn: Analyzes light curve data from a single object to detect common periods across various bands.

Dependencies:
-------------
- QhX.light_curve: Provides light curve processing functions (e.g., outliers_mad, outliers).
- QhX.calculation and QhX.detection: Modules for light curve calculations and period detection.
- QhX.algorithms.wavelets.wwtz: Performs wavelet analysis on time-series data.
"""

import logging
from io import BytesIO
import requests
import pandas as pd
import numpy as np
from QhX.light_curve import outliers_mad, outliers
from QhX.calculation import *
from QhX.detection import *
from QhX.algorithms.wavelets.wwtz import *


class DataManagerDynamical:
    def __init__(self, column_mapping=None, group_by_key='objectId', filter_mapping=None):
        """
        Initializes the DataManager with optional column and filter mappings.

        Parameters:
        -----------
        column_mapping : dict, optional
            A dictionary to map column names in the dataset (e.g., {'mag': 'psMag'}).
        group_by_key : str, optional
            The key by which to group the dataset (e.g., 'source_id' or 'objectId').
        filter_mapping : dict, optional
            A dictionary to map filter values in the dataset (e.g., {'BP': 1, 'G': 2, 'RP': 3}).
        """
        self.column_mapping = column_mapping or {}
        self.group_by_key = group_by_key
        self.filter_mapping = filter_mapping or {}
        self.data_df = None
        self.fs_gp = None

    def load_data(self, path_source: str) -> pd.DataFrame:
        """
        Load data from a file or a URL, apply any necessary column mappings and filter transformations.
        """
        try:
            if path_source.startswith('http'):
                response = requests.get(path_source)
                response.raise_for_status()
                raw_data = BytesIO(response.content)
                df = pd.read_parquet(raw_data)
            else:
                df = pd.read_parquet(path_source)

            if self.column_mapping:
                df.rename(columns=self.column_mapping, inplace=True)

            if 'filter' in df.columns and self.filter_mapping:
                df['filter'] = df['filter'].map(self.filter_mapping)
                
            self.data_df = df
            logging.info("Data loaded and processed successfully.")
            return df
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return None

    def group_data(self):
        """
        Group data by object ID or another specified key.
        """
        if self.data_df is not None:
            self.fs_gp = self.data_df.groupby(self.group_by_key)
            logging.info(f"Data grouped by {self.group_by_key} successfully.")
            return self.fs_gp

        logging.error("Data is not available for grouping.")
        return None


def get_lc_dyn(data_manager, set1, include_errors=False):
    """
    Process and return light curves with an option to include magnitude errors (psMagErr) for a given set ID.
    This function dynamically handles different numbers of filters based on the dataset.
    """
    max_seed_value = 2**32 - 1
    seed_value = abs(hash(int(set1))) % max_seed_value
    np.random.seed(seed_value)

    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    demo_lc = data_manager.fs_gp.get_group(set1)
    available_filters = sorted(demo_lc['filter'].unique())
    tt_with_errors = {}
    ts_with_errors = {}
    sampling_rates = {}

    for filter_value in available_filters:
        d = demo_lc[demo_lc['filter'] == filter_value].sort_values(by=['mjd']).dropna()
        if d.empty:
            print(f"No data for filter {filter_value} in set {set1}.")
            continue
        tt, yy = d['mjd'].to_numpy(), d['psMag'].to_numpy()
        err_mag = d['psMagErr'].to_numpy() if 'psMagErr' in d.columns and include_errors else None

        if include_errors and err_mag is not None:
            tt, yy, err_mag = outliers_mad(tt, yy, err_mag)
        else:
            tt, yy = outliers_mad(tt, yy)

        ts_with_or_without_errors = yy
        if include_errors and err_mag is not None:
            ts_with_or_without_errors += np.random.normal(0, err_mag, len(tt))

        tt_with_errors[filter_value] = tt
        ts_with_errors[filter_value] = ts_with_or_without_errors
        sampling_rates[filter_value] = np.mean(np.diff(tt)) if len(tt) > 1 else 0

    return tt_with_errors, ts_with_errors, sampling_rates


def process1_new_dyn(data_manager, set1, ntau=None, ngrid=None, provided_minfq=None, provided_maxfq=None, include_errors=False, parallel=False):
    """
    Processes and analyzes light curve data from a single object to detect common periods across different bands.
    Supports datasets with different numbers of filters (e.g., 3 for Gaia, 5 for AGN DC).
    """
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    light_curves_data = get_lc_dyn(data_manager, set1, include_errors)
    if light_curves_data is None:
        print(f"Insufficient data for set ID {set1}.")
        return None

    tt_with_errors, ts_with_errors, sampling_rates = light_curves_data
    available_filters = list(tt_with_errors.keys())
    results = []

    for filter_value in available_filters:
        tt = tt_with_errors.get(filter_value)
        yy = ts_with_errors.get(filter_value)
        if tt is None or yy is None:
            continue
        wwz_matrix, corr, extent = hybrid2d(tt, yy, ntau=ntau, ngrid=ngrid, minfq=provided_minfq, maxfq=provided_maxfq, parallel=parallel)
        peaks, hh, r_periods, up, low = periods(set1, corr, ngrid=ngrid, plot=False, minfq=provided_minfq, maxfq=provided_maxfq)
        results.append((r_periods, up, low, peaks, hh))

    if not results:
        return None

    light_curve_labels = [str(f) for f in available_filters]
    det_periods = []
    compared_pairs = set()

    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            pair_key = frozenset([available_filters[i], available_filters[j]])
            if pair_key in compared_pairs:
                continue
            compared_pairs.add(pair_key)

            r_periods_i, up_i, low_i, peaks_i, hh_i = results[i]
            r_periods_j, up_j, low_j, peaks_j, hh_j = results[j]
            filter_i = available_filters[i]
            filter_j = available_filters[j]

            r_periods_common, u_common, low_common, sig_common = same_periods(
                r_periods_i, r_periods_j, up_i, low_i, up_j, low_j, peaks_i, hh_i,
                tt_with_errors[filter_i], ts_with_errors[filter_i],
                peaks_j, hh_j, tt_with_errors[filter_j], ts_with_errors[filter_j],
                ntau=ntau, ngrid=ngrid, minfq=provided_minfq, maxfq=provided_maxfq
            )

            if len(r_periods_common) == 0:
                det_periods.append({
                    "objectid": set1,
                    "sampling_i": sampling_rates[filter_i],
                    "sampling_j": sampling_rates[filter_j],
                    "period": np.nan,
                    "upper_error": np.nan,
                    "lower_error": np.nan,
                    "significance": np.nan,
                    "label": f"{filter_i}-{filter_j}"
                })
            else:
                for k in range(len(r_periods_common)):
                    det_periods.append({
                        "objectid": set1,
                        "sampling_i": sampling_rates[filter_i],
                        "sampling_j": sampling_rates[filter_j],
                        "period": r_periods_common[k],
                        "upper_error": u_common[k],
                        "lower_error": low_common[k],
                        "significance": round(sig_common[k], 2),
                        "label": f"{light_curve_labels[i]}-{light_curve_labels[j]}"
                    })

    return det_periods
