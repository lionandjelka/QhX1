# detection.py

import numpy as np
from QhX.light_curve import get_lctiktok, get_lc22
# Ensure to import or define other necessary functions like hybrid2d, periods, same_periods, etc.
from QhX.algorithms.wavelets.wwtz import *
from QhX.calculation import *

# Example ntau parameter
DEFAULT_NTAU = 80
# Example ngrid parameter
DEFAULT_NGRID = 800
# Example provided_minfq parameter
DEFAULT_PROVIDED_MINFQ = 2000
# Example provided maxfq parameter
DEFAULT_PROVIDED_MAXFQ = 10

#from QhX.algorithms.wavelets.wwt import estimate_wavelet_periods

def process1tiktok(data_manager,set1, initial_period, damping_factor_amplitude, damping_factor_frequency, snr=None, inject_signal=False, ntau=None, ngrid=None, minfq=None, maxfq=None, parallel = False):
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    det_periods = []
    tt0, yy0, tt1, yy1, tt2, yy2, tt3, yy3, sampling0, sampling1, sampling2, sampling3, tik0, tik1, tik2, tik3 = get_lctiktok(data_manager,set1, initial_period, damping_factor_amplitude, damping_factor_frequency, snr, inject_signal)
    wwz_matrx0, corr0, extent0 = hybrid2d(tt0, yy0, 120, 3200, minfq=1500., maxfq=10., parallel=parallel)
    peaks0, hh0, r_periods0, up0, low0 = periods(int(set1), corr0, 3200, plot=False)
    wwzmatrx1, corr1, extent1 = hybrid2d(tt1, yy1, 120, 3200, minfq=1500., maxfq=10., parallel=parallel)
    peaks1, hh1, r_periods1, up1, low1 = periods(int(set1), corr1, 3200, plot=False)
    wwz_matrx2, corr2, extent2 = hybrid2d(tt2, yy2, 120, 3200, minfq=1500., maxfq=10., parallel=parallel)
    peaks2, hh2, r_periods2, up2, low2 = periods(int(set1), corr2, 3200, plot=False)
    wwzmatrx3, corr3, extent3 = hybrid2d(tt3, yy3, 120, 3200, minfq=1500., maxfq=10., parallel=parallel)
    peaks3, hh3, r_periods3, up3, low3 = periods(int(set1), corr3, 3200, plot=False)
    r_periods01, u01, low01, sig01 = same_periods(r_periods0, r_periods1, up0, low0, up1, low1, peaks0, hh0, tt0, yy0, peaks1, hh1, tt1, yy1, ntau=ntau, ngrid=ngrid, minfq=minfq, maxfq=maxfq)
    print(set1)
    if r_periods01.size > 0 and u01.size > 0 and low01.size > 0 and sig01.size > 0: 
        for j in range(len(r_periods01.ravel())):
            det_periods.append([int(set1), sampling0, sampling1, r_periods01[j], u01[j], low01[j], sig01[j], 12])
    elif r_periods01.size == 0:
        det_periods.append([int(set1), 0, 0, 0, 0, 0, 0, 12])
   
    r_periods02, u02, low02, sig02 = same_periods(r_periods0, r_periods2, up0, low0, up2, low2, peaks0, hh0, tt0, yy0, peaks2, hh2, tt2, yy2, ntau=ntau, ngrid=ngrid, minfq=minfq, maxfq=maxfq)
    if r_periods02.size > 0 and u02.size > 0 and low02.size > 0 and sig02.size > 0:
        for j in range(len(r_periods02.ravel())):
            det_periods.append([int(set1), sampling0, sampling2, r_periods02[j], u02[j], low02[j], sig02[j], 13])
    elif r_periods02.size == 0:
        det_periods.append([int(set1), 0, 0, 0, 0, 0, 0, 13])
    r_periods03, u03, low03, sig03 = same_periods(r_periods0, r_periods3, up0, low0, up3, low3, peaks0, hh0, tt0, yy0, peaks3, hh3, tt3, yy3, ntau=ntau, ngrid=ngrid, minfq=minfq, maxfq=maxfq)
    if r_periods03.size > 0 and u03.size > 0 and low03.size > 0 and sig03.size > 0:
        for j in range(len(r_periods03.ravel())):
            det_periods.append([int(set1), sampling0, sampling3, r_periods03[j], u03[j], low03[j], sig03[j], 14]) 
    elif r_periods03.size == 0:
        det_periods.append([int(set1), 0, 0, 0, 0, 0, 0, 14])
    return np.array(det_periods)



def process1_new(data_manager, set1, ntau=None, ngrid=None, provided_minfq=None, provided_maxfq=None, include_errors=True, parallel=False):
    """
    Processes and analyzes light curve data from a single object to detect common periods across different bands.

    The process involves:
    
    - Verifying the existence of the dataset.
    - Retrieving and processing light curve data for different bands.
    - Applying hybrid wavelet techniques to each band's light curve data.
    - Comparing periods detected in different bands to find common periods, if they do not differ more than 10%.
    - Compiling the results, including period values, errors, and significance, into a structured format.

    Parameters
    ----------
    set1 : int
        An identifier representing the dataset to be processed.
    ntau : int, optional
        Number of time delays in the wavelet analysis.
    ngrid : int, optional
        Number of grid points in the wavelet analysis.
    provided_minfq : float, optional
        Period correspondig to the Minimum frequency for analysis, default is calculated from data.
    provided_maxfq : float, optional
        Period corresponding to the Maximum frequency for analysis, default is calculated from data.
    include_errors : bool, optional
        Include magnitude errors in analysis. Defaults to True.
 
    Returns
    -------
    A list of dictionaries representing the results of the analysis performed on light curve data. Each dictionary contains:
    
        - objectid (int): Identifier of the object ID.
        - sampling_i (float): Mean sampling rate in the first band of the pair where a common period is detected.
        - sampling_j (float): Mean sampling rate in the second band in the pair.
        - period (float): Detected common period between the two bands. NaN if no period is detected.
        - upper_error (float): Upper error of the detected period. NaN if no period is detected.
        - lower_error (float): Lower error of the detected period. NaN if no period is detected.
        - significance (float): Measure of the statistical significance of the detected period. NaN if no period is detected.
        - label (str): Label identifying the pair of bands where the period was detected (e.g., '0-1', '1-2').

    Example Usage
    -------------
    # results = process1_new(data_manager, '1384142', ntau=80, ngrid=800, provided_minfq=2000, provided_maxfq=10, include_errors=False)
    # df = pd.DataFrame(results)
    # df.to_csv('light_curve_analysis.csv', index=False)
    """
    
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    light_curves_data = get_lc22(data_manager, set1, include_errors)
    if any(len(data) == 0 for data in light_curves_data if isinstance(data, np.ndarray)):
        print(f"Insufficient data for set ID {set1}.")
        return None

    tt0, yy0, tt1, yy1, tt2, yy2, tt3, yy3, sampling0, sampling1, sampling2, sampling3 = light_curves_data
    results = []
    for tt, yy in [(tt0, yy0), (tt1, yy1), (tt2, yy2), (tt3, yy3)]:
        wwz_matrix, corr, extent = hybrid2d(tt, yy, ntau=ntau, ngrid=ngrid, minfq=provided_minfq, maxfq=provided_maxfq, parallel=parallel)
        peaks, hh, r_periods, up, low = periods(set1, corr, ngrid=ngrid, plot=False, minfq=provided_minfq, maxfq=provided_maxfq)
        results.append((r_periods, up, low, peaks, hh))

    sampling_rates = [sampling0, sampling1, sampling2, sampling3]
    light_curve_labels = ['0', '1', '2', '3']

    det_periods = []
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            r_periods_i, up_i, low_i, peaks_i, hh_i = results[i]
            r_periods_j, up_j, low_j, peaks_j, hh_j = results[j]

            r_periods_common, u_common, low_common, sig_common = same_periods(
                r_periods_i, r_periods_j, up_i, low_i, up_j, low_j, peaks_i, hh_i, tt0, yy0, peaks_j, hh_j, tt1, yy1,
                ntau=ntau, ngrid=ngrid, minfq=provided_minfq, maxfq=provided_maxfq
            )

            if len(r_periods_common) == 0:
                det_periods.append({
                    "objectid": set1,
                    "sampling_i": sampling_rates[i],
                    "sampling_j": sampling_rates[j],
                    "period": np.nan,
                    "upper_error": np.nan,
                    "lower_error": np.nan,
                    "significance": np.nan,
                    "label": f"{light_curve_labels[i]}-{light_curve_labels[j]}"
                })
            else:
                for k in range(len(r_periods_common)):
                    det_periods.append({
                        "objectid": set1,
                        "sampling_i": sampling_rates[i],
                        "sampling_j": sampling_rates[j],
                        "period": r_periods_common[k],
                        "upper_error": u_common[k],
                        "lower_error": low_common[k],
                        "significance": sig_common[k],
                        "label": f"{light_curve_labels[i]}-{light_curve_labels[j]}"
                    })

    return det_periods






def process1(data_manager, set1, ntau=None, ngrid=None, provided_minfq=None, provided_maxfq=None, include_errors=True, parallel=False):
    """
    Processes and analyzes data related to light curves of a single object to detect common periods across different light curves.

    Parameters
    ----------
    set1 : int
        Identifier representing the dataset to be processed.
    ntau : int, optional
        Number of time delays in the wavelet analysis.
    ngrid : int, optional
        Number of grid points in the wavelet analysis.
    provided_minfq : float, optional
        Period corresponding to the Minimum frequency for analysis, default is calculated from data.
    provided_maxfq : float, optional
        Period corresponding to the Maximum frequency for analysis, default is calculated from data.
    include_errors : bool, optional
        Flag to include magnitude errors in analysis, defaults to True.

    Returns
    -------
    np.ndarray
        An array containing common periods and related data across light curves. This includes information on the periods detected in multiple bands, their errors, and significance levels. The focus is on identifying periods that do not differ more than 10% when detected in different bands, with emphasis on numerical values of periods, errors, and significance for a baseline band for comparison.

    Notes
    -----
    The function involves several steps:
    
    - Verifying the existence of the dataset.
    - Retrieving and processing light curve data from different bands.
    - Applying hybrid wavelet techniques to each band's data.
    - Comparing periods detected in different bands to find common periods, ensuring they do not differ more than 10%.
    - Compiling results into a structured format, including periods, errors, and significance for the baseline comparison band.
    """
    if set1 not in data_manager.fs_gp.groups:
        print(f"Set ID {set1} not found.")
        return None

    light_curves_data = get_lc22(data_manager, set1, include_errors)
    # Check if each array in light_curves_data is non-empty
    if any(len(data) == 0 for data in light_curves_data if isinstance(data, np.ndarray)):
        print(f"Insufficient data for set ID {set1}.")
        return None

    tt0, yy0, tt1, yy1, tt2, yy2, tt3, yy3, sampling0, sampling1, sampling2, sampling3 = light_curves_data
    det_periods = []

 #   # TODO CHECK THIS FUNCTION AS IT IS NOT USED YETFunction to get or calculate minfq and maxfq
 #   def get_or_estimate_freq(tt, known_minfq, known_maxfq):
 #       if known_minfq is None or known_maxfq is None:
 #           _, fmin, fmax = estimate_wavelet_periods(tt, ngrid)
 #           return 1/fmax, 1/fmin
 #       return known_minfq, known_maxfq

    # Analyze each light curve
    results = []
    for tt, yy in [(tt0, yy0), (tt1, yy1), (tt2, yy2), (tt3, yy3)]:
      #  local_minfq, local_maxfq = get_or_estimate_freq(tt, provided_minfq, provided_maxfq)
        wwz_matrix, corr, extent = hybrid2d(tt, yy, ntau=ntau, ngrid=ngrid, minfq=provided_minfq, maxfq=provided_maxfq, parallel=parallel)
        peaks, hh, r_periods, up, low = periods(set1, corr, ngrid=ngrid, plot=False, minfq=provided_minfq, maxfq=provided_maxfq)
        results.append((r_periods, up, low, peaks, hh))

    # Light curve labels (for clarity)
    light_curve_labels = ['0', '1', '2', '3']

    # Compare periods within the light curves of the same object
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            r_periods_i, up_i, low_i, peaks_i, hh_i = results[i]
            r_periods_j, up_j, low_j, peaks_j, hh_j = results[j]

            r_periods_common, u_common, low_common, sig_common = same_periods(
                r_periods_i, r_periods_j, up_i, low_i, up_j, low_j, peaks_i, hh_i, tt0, yy0, peaks_j, hh_j, tt1, yy1,
                ntau=ntau, ngrid=ngrid, minfq=provided_minfq, maxfq=provided_maxfq
            )

            if len(r_periods_common) > 0:
                for k in range(len(r_periods_common)):
                    det_periods.append([
                        set1, r_periods_common[k], u_common[k], low_common[k], sig_common[k], 
                        f"{light_curve_labels[i]}-{light_curve_labels[j]}"
                    ])

    return np.array(det_periods)




def same_periods(r_periods0, r_periods1, up0, low0, up1, low1, peaks0, hh0, tt0, yy0, peaks1, hh1, tt1, yy1, ntau, ngrid,minfq,maxfq):
    """
    Analyzes and identifies common periods between two sets of light curve data, 
    assessing their consistency and statistical significance based on a relative tolerance.
    Compares detected periods from two different light curve datasets to identify periods 
    consistently observed in both, using a specified relative tolerance level for similarity judgment.

    Parameters
    ----------
    r_periods0 : list
        Arrays of detected periods from the first light curve dataset.
    r_periods1 : list
        Arrays of detected periods from the second light curve dataset.
    up0 : list
        Arrays of upper error bounds for detected periods in the first dataset.
    low0 : list
        Arrays of lower error bounds for detected periods in the first dataset.
    up1 : list
        Arrays of upper error bounds for detected periods in the second dataset.
    low1 : list
        Arrays of lower error bounds for detected periods in the second dataset.
    peaks0, hh0, tt0, yy0 : list
        Supplementary data including peak information, correlation matrices, and time and magnitude arrays for the first dataset.
    peaks1, hh1, tt1, yy1 : list
        Supplementary data including peak information, correlation matrices, and time and magnitude arrays for the second dataset.
    ntau : int
        Number of time divisions for wavelet analysis.
    ngrid : int
        Grid size (frequency resolution) for the analysis.
    minfq : float
        Minimum frequency for the analysis.
    maxfq : float
        Maximum frequency for the analysis.

    Returns
    -------
    A tuple containing arrays of common periods and their associated statistical data:

        - r_periods_common (np.ndarray): Detected periods common to both datasets, determined within a 10% relative tolerance.
        - up_common, low_common (np.ndarray): Upper and lower error bounds for these common periods, indicating uncertainty ranges.
        - sig_common (np.ndarray): Significance values for each common period, assessed against shuffled data.

    Notes
    -----
    The function compares each period in one dataset against periods in the other dataset, using a relative tolerance of 10%. 
    This tolerance level allows for minor variations in period detection between datasets. The significance of each common period 
    is evaluated to determine if it is an intrinsic feature of the astronomical object or a result of random fluctuations.
    """
        # Convert inputs to numpy arrays for efficient computation
    try:
        r_periods0, r_periods1 = np.array(r_periods0), np.array(r_periods1)
        up0, low0, up1, low1 = np.array(up0), np.array(low0), np.array(up1), np.array(low1)
    except Exception as e:
        raise ValueError(f"Error converting inputs to numpy arrays: {e}")

    number_of_lcs = 50  # Number of LCs used for a simulation

    # Function to find common periods and calculate significance
    def find_common_periods_and_significance(rp0, rp1, up, low, peaks, hh, tt, yy, ntau, ngrid, minfq,maxfq):
        common_indices = np.where(np.isclose(rp0, rp1, rtol=1e-01))[0]
        r_periods = np.take(rp0, common_indices)
        up, low = np.take(up, common_indices), np.take(low, common_indices)
        sig = []

        if len(r_periods) > 0:
            for peak_of_interest in common_indices:
                try:
                    _, _, _, siger = signif_johnson(number_of_lcs, peak_of_interest, peaks, hh, tt, yy, ntau=ntau, ngrid=ngrid, f=2, peakHeight=0.6, minfq=minfq, maxfq=maxfq)
                    sig.append(1. - siger)
                except Exception as e:
                    print(f"Error in significance calculation: {e}")
                    sig.append(np.nan)  # Append NaN to indicate a failed calculation

        return np.array(r_periods), np.array(up), np.array(low), np.array(sig)

    # Ensure the return values from the function are numpy arrays
    if len(r_periods0) == len(r_periods1):
        return find_common_periods_and_significance(r_periods0, r_periods1, up0, low0, peaks0, hh0, tt0, yy0, ntau, ngrid, minfq,maxfq)
    elif len(r_periods0) < len(r_periods1):
        return find_common_periods_and_significance(np.resize(r_periods0, len(r_periods1)), r_periods1, up1, low1, peaks1, hh1, tt1, yy1, ntau, ngrid, minfq,maxfq)
    else:
        return find_common_periods_and_significance(np.resize(r_periods1, len(r_periods0)), r_periods0, up0, low0, peaks0, hh0, tt0, yy0, ntau, ngrid, minfq,maxfq)
