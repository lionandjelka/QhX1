
from QhX.data_manager import DataManager
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


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


def generate_tiktok_signal(time_instances, initial_period, damping_factor_amplitude, damping_factor_frequency):
    """
    Generates a 'tik-tok' signal based on the given parameters.

    Parameters:
    -----------
    - time_instances (array): Array of time instances for the signal generation.
    - initial_period (float): Initial period of the signal.
    - damping_factor_amplitude (float): Damping factor for the amplitude.
    - damping_factor_frequency (float): Damping factor for the frequency.

    Returns:
    --------
    array: Generated tik-tok signal values corresponding to the time instances.
    """
    frequency = 1 / (initial_period * np.exp(-damping_factor_frequency * time_instances))
    amplitude = np.exp(-damping_factor_amplitude * time_instances)
    tiktok_signal = amplitude * np.sin(2 * np.pi * frequency * time_instances)
    return tiktok_signal

def inject_tiktok_to_light_curve(real_times, real_light_curve, initial_period, damping_factor_amplitude, damping_factor_frequency, snr=None, inject_signal=False):
    """
    Injects a tik-tok signal into a real light curve.

    Parameters:
    -----------
     - real_times (array): Array of time instances for the light curve.
     - real_light_curve (array): Original light curve data.
     - initial_period (float): Initial period of the tik-tok signal.
     - damping_factor_amplitude (float): Damping factor for the amplitude of the tik-tok signal.
     - damping_factor_frequency (float): Damping factor for the frequency of the tik-tok signal.
     - snr (float, optional): Signal-to-noise ratio for scaling the tik-tok signal.
     - inject_signal (bool): Flag to decide whether to inject the tik-tok signal or not.

    Returns:
    --------
    tuple: Modified light curve with tik-tok signal injected and the interpolated tik-tok signal.
    """
    if not inject_signal:
        return real_light_curve, np.zeros_like(real_light_curve)

    # Generate tik-tok signal on a regular grid of time instances
    t = np.linspace(real_times.min(), real_times.max(), 5 * len(real_times))
    tiktok_signal_regular = generate_tiktok_signal(t - t.min(), initial_period, damping_factor_amplitude, damping_factor_frequency)

    if snr is not None:
        noise_power = np.var(real_light_curve)
        signal_power = noise_power * snr
        scale_factor = np.sqrt(signal_power)
        tiktok_signal_regular *= scale_factor

    # Interpolate the tik-tok signal to the real light curve time instances
    interpolator = interp1d(t, tiktok_signal_regular, kind='linear', fill_value="extrapolate")
    tiktok_signal_interpolated = interpolator(real_times)

    # Add the interpolated tik-tok signal to the real light curve
    combined_light_curve = real_light_curve + tiktok_signal_interpolated

    return combined_light_curve, tiktok_signal_interpolated

def get_lctiktok(data_manager, set1, initial_period, damping_factor_amplitude, damping_factor_frequency, snr=None, inject_signal=False):
    """
    Processes light curve data and optionally injects a tik-tok signal based on specified parameters.

    Parameters:
    -----------
     - set1: Identifier for the dataset to process.
     - initial_period (float): Initial period of the tik-tok signal.
     - damping_factor_amplitude (float): Damping factor affecting the amplitude of the tik-tok signal.
     - damping_factor_frequency (float): Damping factor affecting the frequency of the tik-tok signal.
     - snr (float, optional): Signal-to-noise ratio for the tik-tok signal.
     - inject_signal (bool): Flag to determine whether to inject the tik-tok signal into the light curve.

    Returns:
    --------
    tuple: Processed time and magnitude data for multiple filters, their sampling rates, and tik-tok signals if injected.
    """
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None
       # Retrieve the light curve data for the specified set
    # Retrieve and process the light curve data for the specified set
    demo_lc = data_manager.fs_gp.get_group(set1)
 
    # Process the data for each filter, sort by MJD, drop rows where MJD is 0 or NaN
    d0, d1, d2, d3 = [
        demo_lc[(demo_lc['filter'] == f) & (demo_lc['mjd'] != 0)].sort_values(by=['mjd']).dropna()
        for f in range(1, 5)
    ]
    # Convert the MJD and magnitude data to numpy arrays for each filter
    tt00, yy00 = d0['mjd'].to_numpy(), d0['psMag'].to_numpy()
    tt11, yy11 = d1['mjd'].to_numpy(), d1['psMag'].to_numpy()
    tt22, yy22 = d2['mjd'].to_numpy(), d2['psMag'].to_numpy()
    tt33, yy33 = d3['mjd'].to_numpy(), d3['psMag'].to_numpy()

    # Remove outliers from each dataset
    tt0, yy0 = outliers(tt00, yy00)
    tt1, yy1 = outliers(tt11, yy11)
    tt2, yy2 = outliers(tt22, yy22)
    tt3, yy3 = outliers(tt33, yy33)

    # Calculate the mean sampling rate for each dataset
    sampling0, sampling1, sampling2, sampling3 = [np.mean(np.diff(tt)) for tt in [tt0, tt1, tt2, tt3]]

    # Inject the tik-tok signal into the light curve data if specified
    yy0, tik0 = inject_tiktok_to_light_curve(tt0, yy0, initial_period, damping_factor_amplitude, damping_factor_frequency, snr, inject_signal)
    yy1, tik1 = inject_tiktok_to_light_curve(tt1, yy1, initial_period, damping_factor_amplitude, damping_factor_frequency, snr, inject_signal)
    yy2, tik2 = inject_tiktok_to_light_curve(tt2, yy2, initial_period, damping_factor_amplitude, damping_factor_frequency, snr, inject_signal)
    yy3, tik3 = inject_tiktok_to_light_curve(tt3, yy3, initial_period, damping_factor_amplitude, damping_factor_frequency, snr, inject_signal)

    # Return the processed data
    return tt0, yy0, tt1, yy1, tt2, yy2, tt3, yy3, sampling0, sampling1, sampling2, sampling3, tik0, tik1, tik2, tik3

def get_lc22(data_manager, set1, include_errors=True):
    """
    Process and return light curves with an option to include magnitude errors for a given set ID.

    Parameters:
    -----------
    - set1 (str): The object ID for which light curves are to be processed.
    - include_errors (bool, optional): Flag to include magnitude errors in the time series. Defaults to True.

    Returns:
    --------
    tuple: Contains the processed time series with or without magnitude errors for each
           filter, along with their respective sampling rates. Returns None if the set ID
           is not found or if any filter data is missing.
    """
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    demo_lc = data_manager.fs_gp.get_group(set1)    
    tt_with_errors0 = ts_with_errors0 = tt_with_errors1 = ts_with_errors1 = None
    tt_with_errors2 = ts_with_errors2 = tt_with_errors3 = ts_with_errors3 = None
    sampling0 = sampling1 = sampling2 = sampling3 = None

    for filter_value in range(1, 5):  # Assuming filters range from 1 to 4
        d = demo_lc[demo_lc['filter'] == filter_value].sort_values(by=['mjd']).dropna()
        if d.empty or ('psMagErr' not in d.columns and include_errors):
            print(f"No data or 'err' column not found for filter {filter_value} in set {set1}.")
            return None
        tt, yy = d['mjd'].to_numpy(), d['psMag'].to_numpy()
        err_mag = d['psMagErr'].to_numpy() if 'psMagErr' in d.columns and include_errors else None

        if include_errors and err_mag is not None:
            tt, yy, err_mag = outliers_mad(tt, yy, err_mag)
        else:
            tt, yy = outliers_mad(tt, yy)

        ts_with_or_without_errors = yy
        if include_errors and err_mag is not None:
            ts_with_or_without_errors += np.random.normal(0, err_mag, len(tt))

        if filter_value == 1:
            tt_with_errors0 = tt
            ts_with_errors0 = ts_with_or_without_errors
            sampling0 = np.mean(np.diff(tt)) if len(tt) > 1 else 0
        elif filter_value == 2:
            tt_with_errors1 = tt
            ts_with_errors1 = ts_with_or_without_errors
            sampling1 = np.mean(np.diff(tt)) if len(tt) > 1 else 0
        elif filter_value == 3:
            tt_with_errors2 = tt
            ts_with_errors2 = ts_with_or_without_errors
            sampling2 = np.mean(np.diff(tt)) if len(tt) > 1 else 0
        elif filter_value == 4:
            tt_with_errors3 = tt
            ts_with_errors3 = ts_with_or_without_errors
            sampling3 = np.mean(np.diff(tt)) if len(tt) > 1 else 0

    return tt_with_errors0, ts_with_errors0, tt_with_errors1, ts_with_errors1, \
           tt_with_errors2, ts_with_errors2, tt_with_errors3, ts_with_errors3, \
           sampling0, sampling1, sampling2, sampling3