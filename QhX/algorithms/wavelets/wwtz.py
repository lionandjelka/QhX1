from libwwz import wwt as libwwz_wwt
import numpy as np
from QhX.utils.correlation import correlation_nd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import sys
import io
from traitlets.traitlets import Integer




def compute_frequency_grid(Nn, minfq=None, maxfq=None):
    """
    Computes the frequency grid for wavelet analysis given the periodis corresponding to  minimum and maximum frequencies.

    Parameters:
    -----------
    - Nn (int): Number of grid points for the frequency axis.
    - minfq (float, optional): period correspoding to the Minimum frequency value. If None, a default value should be defined elsewhere.
    - maxfq (float, optional): period corresponding to the Maximum frequency value. If None, a default value should be defined elsewhere.

    Returns:
    --------
    tuple: Contains the frequency step (df), minimum frequency (fmin), and maximum frequency (fmax) for the grid.

    Note:
    -----
    - The function assumes the input periods are in days so that freqeuncies are in days ^-1 (1/days).
    - If minfq or maxfq is None, ensure default values are set or passed to this function.
    - The function returns frequencies in the same units as periods corresponding to the minfq and maxfq.
    """

    # Ensure minfq and maxfq are not None. If None, default values should be used.
    if minfq is None or maxfq is None:
        raise ValueError("Minimum and maximum frequencies (minfq, maxfq) must be provided.")

    # Convert frequency bounds to periods (in days).
    fmin = 1 / minfq  # Minimum period (maximum frequency converted to period)
    fmax = 1 / maxfq  # Maximum period (minimum frequency converted to period)

    # Calculate the frequency step for the grid.
    df = (fmax - fmin) / Nn  # Step size between each frequency on the grid

    return df, fmin, fmax

# Example usage:
# df, fmin, fmax = compute_frequency_grid(1000, minfq=0.001, maxfq=0.01)
# This will compute the frequency grid for a given number of points and frequency range.



def estimate_wavelet_periods(time_series,  ngrid, known_period=None):
    """
    Estimate minimum and maximum periods for wavelet analysis.

    Parameters:
    -----------
    - time_series (array): Array of time points in your data.
    - sampling_rate (float): The sampling rate of your data (data points per time unit).
    - known_period (float, optional): A known period in your data, if any.

    Returns:
    --------
    tuple: (min_period, max_period) estimated periods for analysis.
    """
    sampling_rate=np.mean(np.diff(time_series))
    total_duration = max(time_series) - min(time_series)  # Total duration of your data

    # Estimate minimum period based on Nyquist frequency
    nyquist_period = 1 / (0.5 * sampling_rate)
    min_period = max(2 * nyquist_period, 0.1 * total_duration)  # At least twice the Nyquist limit

    # Estimate maximum period
    max_period = 0.5 * total_duration  # Typically half the total duration

    # If there's a known period, adjust min or max period accordingly
    if known_period:
        min_period = min(min_period, known_period / 2)
        max_period = max(max_period, known_period * 2)
    dp = (max_period - min_period) / ngrid

    return 1/dp, 1/max_period, 1/min_period



def inp_param(ntau, ngrid, minfq, maxfq, parallel=False, f=2):
    """
    Calculate the input parameters for WWZ (Weighted Wavelet Z-transform) analysis.

    Parameters:
    -----------
    - ntau (int): Number of time delays to use in the wavelet analysis.
    - ngrid (int): Number of grid points for frequency analysis.
    - minfq (float): period corresponding to the Minimum frequency for analysis.
    - maxfq (float): period corresponding to the Maximum frequency for analysis.
    - f (float): Frequency multiplier for calculating the decay constant. Default is 2.

    Returns:
    --------
    - ntau (int): Number of time delays.
    - frequency_parameters (list): List containing frequency parameters [freq_low, freq_high, freq_step, override].
    - decay_constant (float): Decay constant for the wavelet.
    - parallel (bool): Flag to enable parallel processing, will use all available cores.

    Note:
    -----
    - The decay constant is calculated based on the frequency 'f' and is used to define the shape of the analyzing wavelet.
    """

    # Compute frequency grid parameters
    df, fmin, fmax = compute_frequency_grid(ngrid, minfq, maxfq)
    
    # Set frequency bounds and step for the analysis
    frequency_low = fmin  # Lower bound of frequency range
    frequency_high = fmax  # Upper bound of frequency range
    frequency_steps = df   # Step size between each frequency value

    # Flag to override frequency bounds (default False). Setting to True will ignore the low and high frequency limitations
    override = False

    # Combine frequency parameters into a list
    frequency_parameters = [frequency_low, frequency_high, frequency_steps, override]

    # Calculate decay constant for the analyzing wavelet
    w = 2 * np.pi * f  # Angular frequency
    decay_constant = 1 / (2 * w**2)  # Decay constant for the wavelet

    return ntau, frequency_parameters, decay_constant, parallel

# Example usage:
# ntau, freq_params, decay_const, parallel = inp_param(80, 800, 0.001, 0.1)
# This will set up parameters for WWZ analysis with specified values.


def wwt1(tt, mag, ntau, ngrid, minfq, maxfq, parallel=False, f=2, method='linear'):
    """
    Calculate the Weighted Wavelet Z-transform (WWZ) of a given time series signal.

    Parameters:
    -----------
    - tt (list): List of time data points.
    - mag (list): List of magnitude values corresponding to time points in 'tt'.
    - ntau (int): Number of time divisions for WWZ analysis.
    - ngrid (int): Grid size for frequency analysis in WWZ.
    - minfq (float): period corresponidng to the Minimum frequency for WWZ analysis.
    - maxfq (float): period corresponidng to the maximum frequency for WWZ analysis.
    - f (float): Frequency multiplier for calculating the decay constant in WWZ. Default is 2.
    - method (str): Method for frequency analysis, either 'linear' or 'octave'. Default is 'linear'.

    Returns:
    --------
    - WWZ  matrix coefficients: The result of WWZ analysis as provided by the 'libwwz' library.

    Notes:
    ------
     - The 'method' parameter allows selection between linear and octave frequency scaling.
    """

    # Compute input parameters for WWZ analysis
    ntau, params, decay_constant, parallel = inp_param(ntau, ngrid, minfq, maxfq, parallel, f)

    # Perform WWZ analysis using libwwz library
    return libwwz_wwt(timestamps=tt, magnitudes=mag,
                      time_divisions=ntau,
                      freq_params=params,
                      decay_constant=decay_constant,
                      method=method,
                      parallel=parallel)

# Example usage:
# tt and mag are lists of time and magnitude data points.
# result = wwt(tt, mag, 80, 800, 0.001, 0.1)
# This performs WWZ analysis on the provided time series data.


def hybrid2d(tt, mag, ntau, ngrid, minfq, maxfq, parallel=False, f=2, method='linear'):
    """
    Perform a hybrid 2D analysis involving WWZ (Weighted Wavelet Z-transform) and auto-correlation on light curve data.

    This function computes the WWZ transformation of the input light curve data and then performs an auto-correlation analysis on the result. 
    The frequency range for the analysis can be specified, as well as the decay constant and interpolation method for WWZ.

    Parameters:
    -----------
    - tt: array_like
        Array of time data for the light curve.
    - mag: array_like
        Array of magnitude values corresponding to the time data.
    - ntau: int
        Number of time divisions for the WWZ analysis.
    - ngrid: int
        Number of grid points (frequency resolution) for the WWZ analysis.
    - minfq: float
        Minimum frequency (or corresponding period) for WWZ analysis.
    - maxfq: float
        Maximum frequency (or corresponding period) for WWZ analysis.
    - f: float, optional
        Decay constant for the analyzing wavelet in WWZ, by default 2.
    - method: str, optional
        Interpolation method used in WWZ ('linear' or 'octave'), by default 'linear'.

    Returns:
    --------
    A tuple containing:
    
    - WWZ matrix: The WWZ analysis result.
    - Auto-correlation matrix: The result of auto-correlation analysis.
    - Frequency range extent: The extent of the frequency range for plotting.

    Examples:
    ---------
    >>> tt = [0, 1, 2, 3, 4]
    >>> mag = [10, 11, 12, 13, 14]
    >>> wwz_result, acorr_result, freq_extent = hybrid2d(tt, mag, 100, 50, 0.1, 1.0)
    """

    # Function implementation
    # ...

    # Perform WWZ analysis on the data using the wwt function
    wwz_matrix = wwt1(tt, mag, ntau, ngrid, minfq, maxfq, parallel, f, method)

    # Auto-correlate the WWZ matrix
    # np.rot90 rotates the matrix by 90 degrees to align time and frequency axes as needed
    corr = correlation_nd(np.rot90(wwz_matrix[2]), np.rot90(wwz_matrix[2]))

    # Determine the extent (range) of the frequency axis for plotting purposes
    extent_min = np.min(wwz_matrix[1])  # Minimum frequency from the WWZ result
    extent_max = np.max(wwz_matrix[1])  # Maximum frequency from the WWZ result
    extent = [extent_min, extent_max, extent_min, extent_max]

    # Return the WWZ matrix, auto-correlation matrix, and the extent of frequency range
    return wwz_matrix, corr, extent





