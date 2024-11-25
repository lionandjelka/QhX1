# pylint: disable=R0801
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from QhX.data_manager import DataManager


def outliers(time, flux, err_flux=None):
    """
    Identifies and removes outliers from a light curve based on a Z-score threshold.
    This function applies a Z-score method to identify and remove outliers from light curve data.
    If flux error values are provided, the function considers these for a more nuanced outlier detection.

    Parameters:
    -----------
    - time (array): Array of time values.
    - flux (array): Array of flux values corresponding to the time values.
    - err_flux (array, optional): Array of flux error values. If provided, the function
      considers error-weighted Z-scores for outlier detection.

    Returns:
    --------
    tuple: A tuple consisting of arrays of time and flux values with outliers removed.
    If 'err_flux' is provided, returns a third array of flux error values with
    outliers removed.

    Example:
    --------
    Assuming `time`, `flux`, and `err_flux` are arrays with light curve data:
    >>> clean_time, clean_flux = outliers(time, flux)
    >>> clean_time, clean_flux, clean_err_flux = outliers(time, flux, err_flux)
    """
    # Function implementation remains unchanged...
    if err_flux is not None:
        # Compute the error-weighted Z-Score for each point in the light curve
        z_scores_flux = np.abs((flux - np.mean(flux)) / err_flux)
    else:
        z_scores_flux = np.zeros(len(flux))

    # Compute the Z-Score for each point in the flux values
    z_scores = np.abs((flux - np.mean(flux)) / np.std(flux))

    # Define a threshold for outlier detection
    threshold = 3.0

    # Find the indices of the non-outlier points
    good_indices = np.where((z_scores <= threshold) & (z_scores_flux <= threshold))[0]

    # Create new arrays with only the non-outlier points
    clean_flux = flux[good_indices]
    clean_time = time[good_indices]

    # Conditionally return the error flux
    if err_flux is not None:
        clean_err_flux = err_flux[good_indices]
        return clean_time, clean_flux, clean_err_flux
    else:
        return clean_time, clean_flux



def outliers_mad(time, flux, err_flux=None, threshold_factor=3.0):
    """
    Identifies and removes outliers from a light curve data set using Median Absolute Deviation (MAD).
    This function applies the MAD method to identify and remove outliers in light curve data. It can optionally
    consider errors in flux measurements for a more nuanced outlier detection. The outlier detection threshold
    is determined as a multiple of the MAD, with an optional inclusion of median error for adjustment.

    Parameters:
    -----------
    - time (array): Array of time values corresponding to light curve measurements.
    - flux (array): Array of flux values corresponding to the light curve.
    - err_flux (array, optional): Array of errors associated with flux measurements.
      If provided, these values adjust the outlier detection threshold.
    - threshold_factor (float, optional): A multiplier used with MAD to set the threshold
      for outlier detection. Default is 3.0. Smaller values imply stricter outlier removal.

    Returns:
    --------
    - clean_time (array): Array of time values with outliers removed.
    - clean_flux (array): Array of flux values with outliers removed.
    - clean_err_flux (array, optional): Array of error flux values with outliers removed,
      returned only if `err_flux` is provided.

    Example:
    --------
    Assuming `time`, `flux`, and `err_flux` are arrays with light curve data:

    >>> clean_time, clean_flux = outliers_mad(time, flux)
    >>> clean_time, clean_flux, clean_err_flux = outliers_mad(time, flux, err_flux)
    """
    # Function implementation remains unchanged...
    median_flux = np.median(flux)
    mad = np.median(np.abs(flux - median_flux))
    threshold = threshold_factor * mad

    # Conditionally adjust threshold based on error in flux
    if err_flux is not None:
        threshold += np.median(err_flux)

    # Identify non-outlier indices
    good_indices = np.where(np.abs(flux - median_flux) <= threshold)[0]

    # Create new arrays with only the non-outlier points
    clean_flux = flux[good_indices]
    clean_time = time[good_indices]

    # Conditionally return the error flux
    if err_flux is not None:
        clean_err_flux = err_flux[good_indices]
        return clean_time, clean_flux, clean_err_flux
    else:
        return clean_time, clean_flux

# Example usage:
# clean_time, clean_flux = outliers(tt, yy)
# clean_time, clean_flux, clean_err_flux = outliers(tt, yy, err_flux=yy_err)


def get_lc22(data_manager, set1, include_errors=True):
    """
    Process and return light curves with an option to include magnitude errors for a given set ID.
    This version is for fixed filters ranging from 0 to 3 and preserves MJD precision.

    Parameters:
    -----------
    - set1 (str): The object ID for which light curves are to be processed.
    - include_errors (bool, optional): Flag to include magnitude errors in the time series. Defaults to True.

    Returns:
    --------
    tuple: Contains the processed time series with or without magnitude errors for each filter (0 to 3),
           along with their respective sampling rates.
    """
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    # Fetch data for the given object ID
    demo_lc = data_manager.fs_gp.get_group(set1)

    # Initialize containers for time series data and sampling rates
    tt_with_errors = {0: None, 1: None, 2: None, 3: None}
    ts_with_errors = {0: None, 1: None, 2: None, 3: None}
    sampling_rates = {0: None, 1: None, 2: None, 3: None}

    for filter_value in range(4):  # Fixed filters from 0 to 3
        d = demo_lc[demo_lc['filter'] == filter_value].sort_values(by=['mjd']).dropna()
        if d.empty or ('psMagErr' not in d.columns and include_errors):
            print(f"No data or 'psMagErr' column not found for filter {filter_value} in set {set1}.")
            continue

        # Extract MJD, magnitude, and errors
        tt, yy = d['mjd'].to_numpy(), d['psMag'].to_numpy()
        err_mag = d['psMagErr'].to_numpy() if 'psMagErr' in d.columns and include_errors else None

        # Handle outliers
        if include_errors and err_mag is not None:
            tt, yy, err_mag = outliers_mad(tt, yy, err_mag)
        else:
            tt, yy = outliers_mad(tt, yy)

        # Create the time series with or without errors
        ts_with_or_without_errors = yy
        if include_errors and err_mag is not None:
            ts_with_or_without_errors += np.random.normal(0, err_mag, len(tt))

        # Store time series and sampling rates
        tt_with_errors[filter_value] = tt
        ts_with_errors[filter_value] = ts_with_or_without_errors
        sampling_rates[filter_value] = np.mean(np.diff(tt)) if len(tt) > 1 else 0

    return tt_with_errors[0], ts_with_errors[0], tt_with_errors[1], ts_with_errors[1], \
           tt_with_errors[2], ts_with_errors[2], tt_with_errors[3], ts_with_errors[3], \
           sampling_rates[0], sampling_rates[1], sampling_rates[2], sampling_rates[3]
