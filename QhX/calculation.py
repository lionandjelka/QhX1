from libwwz import wwt as libwwz_wwt
import numpy as np
import pandas as pd
from scipy.stats.mstats import mquantiles
from scipy import interpolate, optimize
from scipy.signal import find_peaks
from sklearn.utils import shuffle
from QhX.algorithms.wavelets.wwtz import *  
from QhX.utils.correlation import correlation_nd
import matplotlib.pyplot as plt




def get_full_width(x: np.ndarray, y: np.ndarray, peak: np.ndarray, height: float = 0.5) -> tuple:
    """
    Calculate the error of the determined period using the FWHM method and determine quantiles.    
    This function calculates the error of the determined period using the Full Width at Half Maximum (FWHM) method. 
    It is part of a post-mortem analysis to estimate the period uncertainty based on the Mean Noise Power Level (MNPL) in the vicinity of the peak. 
    The function detects the FWHM of a peak and then calculates the points between the 25th and 75th quantile to find MNPL.    

    Parameters:
    -----------
    - x (np.ndarray): An array containing the x-axis values (e.g., time).
    - y (np.ndarray): An array containing the corresponding y-axis values (e.g., intensity).
    - peak (np.ndarray): An array containing the indices of determined peaks.
    - height (float, optional): The fraction of the peak's maximum height to define the FWHM. Default is 0.5.

    Returns:
    --------
    tuple: A tuple containing six arrays of results:
    
    - er1: An array of lower x-values for quantiles.
    - er3: An array of upper x-values for quantiles.
    - quantiles: An array of quantiles (25th and 75th percentile) calculated from peak data.
    - phmax: An array of half the peak's maximum height.
    - x_lows: An array of lower x-values corresponding to the FWHM.
    - x_highs: An array of upper x-values corresponding to the FWHM.
    """
    er1, er3, quantiles, phmax, x_lows, x_highs = [], [], [], [], [], []

    for i in range(len(peak)):
        height_half_max = y[peak[i]] * height
        index_max = peak[i]

        # Find lower and upper bounds for the FWHM
        x_low, x_high = 0, 0
        tmp = index_max
        while tmp > 0:
            tmp -= 1
            if (y[tmp] - height_half_max) < 0:
                x_low = x[tmp + 1]
                break
        
        tmp = index_max
        while tmp < len(y) - 1:
            tmp += 1
            if (y[tmp] - height_half_max) < 0:
                x_high = x[tmp - 1]
                break

        # Calculate quantiles
        q25, q75, xer1, xer3 = 0, 0, 0, 0
        if index_max - 5 > 0:
            arr = y[(x >= x_low) & (x <= x_high)]
            q25, q75 = mquantiles(arr, [0.25, 0.75])

            # Interpolate to find x-values corresponding to quantiles
            inv_func = interpolate.interp1d(y[index_max - 5:index_max], x[index_max - 5:index_max], kind='cubic', fill_value="extrapolate")
            inv_func2 = interpolate.interp1d(y[index_max:index_max + 5], x[index_max:index_max + 5], kind='cubic', fill_value="extrapolate")
            xer1 = inv_func(q25)
            xer3 = inv_func2(q75)

        # Append results to respective lists
        er1.append(xer1)
        er3.append(xer3)
        quantiles.append([q25, q75])
        phmax.append(height_half_max)
        x_lows.append(x_low)
        x_highs.append(x_high)

    return er1, er3, quantiles, phmax, x_lows, x_highs

def periods(lcID, data, ngrid, plot=False, save=False, peakHeight=0.6, prominence=0.7, minfq=None, maxfq=None, xlim=None):
    """
    Perform period determination for the output of hybrid2d data.    
    This function analyzes correlation data to determine periods of a light curve.

    Parameters:
    -----------
    - lcID (int): ID of the light curve.
    - data (numpy.ndarray): Auto-correlation matrix.
    - ngrid (int): Number of values for controlling WWZ execution (see inp_param function).
    - plot (bool): True if a plot is desired, False otherwise.
    - save (bool): True to save the plot, False otherwise.
    - peakHeight (float): Maximum peak height for peak detection.
    - prominence (float): Prominence threshold for peak determination.
    - minfq (float, optional): Minimum frequency for analysis. Default is None.
    - maxfq (float, optional): Maximum frequency for analysis. Default is None.
    - xlim (tuple, optional): Set the x-axis limits for the plot. Default is None.

    Returns:
    --------
    A tuple containing:
    
    - idx_peaks (list): Indices of detected peaks.
    - yax (numpy.ndarray): Processed data.
    - r_peaks (list): Detected periods.
    - r_peaks_err_upper (list): Upper errors of corresponding periods.
    - r_peaks_err_lower (list): Lower errors of corresponding periods.
    """
    # Existing implementation remains unchanged...
    hh1 = np.rot90(data).T / np.rot90(data).T.max()
    hh1arr = np.rot90(hh1.T)
    hh1arr1 = np.abs(hh1arr).sum(1) / np.abs(hh1arr).sum(1).max()

    # Calculate frequency parameters
    fmin = 1 / minfq
    fmax = 1 / maxfq
    df = (fmax - fmin) / ngrid

    # Interpolate data to obtain more points
    osax = np.arange(start=fmin, stop=fmax + df, step=df)
    xax = np.arange(start=fmin, stop=fmax + df, step=df / 2)
    from scipy import interpolate
    f = interpolate.interp1d(osax, np.abs(hh1arr1), fill_value="extrapolate")
    yax = []
    for v in xax:
        yax.append(float(f(v)))
    yax = np.array(yax)

    # Finding peaks
    peaks, _ = find_peaks(yax, peakHeight, prominence=prominence)

    # Plotting if needed
    if plot:
        if xlim is not None:
            plt.xlim(xlim)
        plt.plot(xax, np.abs(yax))
        plt.axvline(xax[peaks[0]], ymin=0, ymax=1, linestyle='--', color='k')
        plt.title(str(lcID))
        plt.xlabel(r'Frequency [day$^{-1}$]')
        plt.ylabel(r"correlation")
        if save:
            plt.savefig(str(lcID) + 'stackd_h2d.png')

    # Get error estimates for each peak (period)
    error_upper, error_lower, quantiles, halfmax, x_lows, x_highs = get_full_width(xax, yax, peaks)

    if plot:
        plt.plot(xax, np.abs(yax))
        if xlim is not None:
            plt.xlim(xlim)
        plt.title(str(lcID))
        plt.xlabel(r'Frequency [day$^{-1}$]')
        plt.ylabel(r"correlation")

        for i in range(len(peaks)):
            plt.axvline(xax[peaks[i]], ymin=0, ymax=1, linestyle='--', color='black')
            plt.axhline(quantiles[i][0], linestyle='--', color='green')
            plt.axhline(quantiles[i][1], linestyle='--', color='red')
            plt.axvline(x_lows[i], ymin=0, ymax=1, linestyle='--', color='blue')
            plt.axvline(x_highs[i], ymin=0, ymax=1, linestyle='--', color='blue')
            plt.axhline(halfmax[i], linestyle='--', color='purple')

        if save:
            plt.savefig(str(lcID) + 'stackd_h2d_peaks.png')

    # Prepare the output
    r_peaks = []
    r_peaks_err_upper = []
    r_peaks_err_lower = []
    idx_peaks = []
    for i in range(len(peaks)):
        r_peaks.append(1 / xax[peaks[i]])
        idx_peaks.append(peaks[i])
        if error_upper[i] == 0:
            r_peaks_err_upper.append(-1)
        else:
            r_peaks_err_upper.append(np.abs(1 / xax[peaks[i]] - (1 / error_upper[i])))
        if error_lower[i] == 0:
            r_peaks_err_lower.append(-1)
        else:
            r_peaks_err_lower.append(np.abs(1 / xax[peaks[i]] - (1 / error_lower[i])))

    return idx_peaks, yax, r_peaks, r_peaks_err_upper, r_peaks_err_lower



def signif_johnson(numlc, peak, idx_peaks, yax, tt, yy, ntau, ngrid, f=2, peakHeight=0.6, minfq=None, maxfq=None, algorithm='wwz', method='linear', use_mag_errors=False, err_mag=None):
    """
    Assess the significance of detected peaks in light curve data using the Johnson method, 
    with an option to incorporate magnitude errors into the analysis.
    This function performs a significance test on the peaks detected in a light curve. It 
    compares the peak power against the power of red noise (background noise) to determine 
    the likelihood that the peak is a true signal rather than noise. The analysis can be 
    enhanced by incorporating magnitude errors, which adds robustness to the significance 
    estimation.

    Parameters:
    -----------
    - numlc (int): Number of light curves to analyze.
    - peak (int): Index of the peak for which significance is being calculated.
    - idx_peaks (np.ndarray): Array of indices of detected peaks.
    - yax (np.ndarray): Array of processed data corresponding to the peaks.
    - tt (np.ndarray): Array of time stamps for the light curve.
    - yy (np.ndarray): Array of magnitude values of the light curve.
    - ntau (int): Number of time divisions for the analysis.
    - ngrid (int): Grid size for frequency analysis.
    - f (float, optional): Frequency parameter for the analysis algorithm. Default is 2.
    - peakHeight (float, optional): Threshold for peak height. Default is 0.6.
    - minfq (float, optional): Minimum frequency for analysis. Default is 1500.
    - maxfq (float, optional): Maximum frequency for analysis. Default is 10.
    - algorithm (str, optional): Name of the analysis algorithm to use. Default is 'wwz'.
    - method (str, optional): Interpolation method for the analysis. Default is 'linear'.
    - use_mag_errors (bool, optional): Flag to indicate whether to use magnitude errors. Default is False.
    - err_mag (np.ndarray, optional): Array of magnitude errors. Required if use_mag_errors is True.
 
    Returns:
    --------
    tuple: A tuple containing the following elements:
    
    - bins (list): List of peak power values.
    - bins11 (list): List of red noise power values at the peak positions.
    - count / numlc (float): Fraction of cases where peak power is larger than red noise power.
    - count11 / numlc (float): Fraction of cases where red noise power is larger than peak power.
    """
  # Interpolation parameters (similar to periods function)
    fmin = 1 / minfq
    fmax = 1 / maxfq
    df = (fmax - fmin) / ngrid
    osax = np.arange(start=fmin, stop=fmax + df, step=df)
    xax = np.arange(start=fmin, stop=fmax + df, step=df / 2)
  
    idxrep = idx_peaks[peak]
    count = 0.  # Peak power larger than red noise peak power
    count11 = 0.  # Peak power of red noise larger than observed peak power
    bins11 = []
    bins = []

    for i in range(numlc):
        if use_mag_errors:
            if err_mag is None:
                raise ValueError("Magnitude errors (err_mag) must be provided if use_mag_errors is True")
            # Combine magnitudes and errors into a single array and shuffle
            mag_err_combined = np.column_stack((yy, err_mag))
            np.random.shuffle(mag_err_combined)
            shuffled_yy, shuffled_err_mag = mag_err_combined[:, 0], mag_err_combined[:, 1]
            y = shuffled_yy + np.random.normal(0, shuffled_err_mag)
        else:
            y = shuffle(yy)

        # WWZ analysis or other algorithm using 'y'
        ntau, params, decay_constant, parallel = inp_param(ntau=ntau, ngrid=ngrid, f=2, minfq=minfq, maxfq=maxfq)
        if algorithm == 'wwz':
            wwt_removedx = libwwz_wwt(timestamps=tt,
                                      magnitudes=y,
                                      time_divisions=ntau,
                                      freq_params=params,
                                      decay_constant=decay_constant,
                                      method='linear',
                                      parallel=parallel)
        corr1x = correlation_nd(np.rot90(wwt_removedx[2]), np.rot90(wwt_removedx[2]))
        hhx = np.rot90(corr1x).T / corr1x.max()
        hh1x = np.rot90(hhx.T)
        hh1xarr = np.abs(hh1x).sum(1) / np.abs(hh1x).sum(1).max()
        f = interpolate.interp1d(osax, hh1xarr, fill_value="extrapolate")
        interpolated_hh1xarr = f(xax)
        
        # Ensure idxrep is within bounds for interpolated array
        if idxrep >= len(interpolated_hh1xarr):
            print(f"Index {idxrep} out of bounds for interpolated_hh1xarr with size {len(interpolated_hh1xarr)}")
            continue
            
        # Append original yax value at idxrep
        bins.append(yax[idxrep])
        
        # Compare original yax value against interpolated hh1xarr
        if yax[idxrep] / interpolated_hh1xarr[idxrep] > 1.:
            count += 1.
        else:
            count11 += 1.
            bins11.append(interpolated_hh1xarr[idxrep])

    return bins, bins11, count / numlc, count11 / numlc
