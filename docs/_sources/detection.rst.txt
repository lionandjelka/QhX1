detection
=======================

This module contains functions for processing and analyzing light curve data, including detecting common periods across different bands and simulating damped oscillations in light curves.

Differences between `process1_new` and `process1`
-------------------------------------------------

Both `process1_new` and `process1` are designed to process and analyze light curve data to detect common periods across different light curve bands. However, there are several key differences in how the two functions operate and return results:

1. **Return Format**:
   - **`process1_new`**: Returns a list of dictionaries. Each dictionary contains comprehensive information about detected periods, errors, significance, and sampling rates. This structured format is more user-friendly for data manipulation, especially in formats like JSON or Pandas DataFrames.
   - **`process1`**: Returns a NumPy array. This format is more compact and efficient but provides only numerical data without the metadata (e.g., object IDs and sampling rates). It is ideal for computational efficiency but less flexible for detailed data analysis.

2. **Result Compilation**:
   - **`process1_new`**: The results are returned as dictionaries that contain metadata such as object IDs and sampling rates. This format is more useful for tasks requiring additional context, visualization, or exporting to files.
   - **`process1`**: Focuses on returning numerical data (such as period values and errors), making it more suitable for tasks that require a straightforward, efficient output.

3. **Data Structure**:
   - **`process1_new`**: Provides structured data in the form of dictionaries, where each detected period is associated with the band pair it was detected in, making it easier to interpret.
   - **`process1`**: Returns a NumPy array without explicit labels, requiring the user to know the order of values returned, which may complicate interpretation.

4. **Usability**:
   - **`process1_new`**: Best for detailed and flexible data manipulation, such as exporting results or visualization.
   - **`process1`**: Best for cases where computational performance is more important than having detailed, structured data.

In summary, `process1_new` is ideal for tasks requiring detailed output and flexible data handling, while `process1` is optimized for efficient numerical processing.

process1tiktok
--------------

The `process1tiktok` function is an experimental function that processes and analyzes light curve data while simulating damped oscillations. This function is useful for testing how these injected signals are detected and how damping factors affect the detected periods.

This function simulates a signal with damping factors applied to both its amplitude and frequency. It can inject this simulated signal into real light curve data and attempt to detect periods using wavelet techniques.

### Parameters

- **data_manager** : object
  The data manager that handles access to the dataset.

- **set1** : int
  Identifier representing the dataset to be processed.

- **initial_period** : float
  The initial period of the signal injected into the light curve data.

- **damping_factor_amplitude** : float
  Damping factor that modifies the amplitude of the injected signal over time.

- **damping_factor_frequency** : float
  Damping factor that modifies the frequency of the injected signal over time.

- **snr** : float, optional
  Signal-to-noise ratio of the injected signal. Default is None.

- **inject_signal** : bool, optional
  If `True`, the function will inject the damped oscillating signal into the light curve data. Default is `False`.

- **ntau** : int, optional
  Number of time delays for wavelet analysis. Default is None.

- **ngrid** : int, optional
  Number of grid points for wavelet analysis. Default is None.

- **minfq** : float, optional
  Minimum frequency for the wavelet analysis. If `None`, it is estimated from the data.

- **maxfq** : float, optional
  Maximum frequency for the wavelet analysis. If `None`, it is estimated from the data.

- **parallel** : bool, optional
  If `True`, the function will enable parallel processing to speed up calculations. Default is `False`.

### Returns

A NumPy array containing the detected common periods and related data across the light curves. The array has the following structure:

- **set1** (int): Identifier of the object.
- **sampling_i** (float): Sampling rate for the first band in the pair.
- **sampling_j** (float): Sampling rate for the second band in the pair.
- **period** (float): The detected common period, or 0 if no period was detected.
- **upper_error** (float): The upper bound of the period's error, or 0 if no period was detected.
- **lower_error** (float): The lower bound of the period's error, or 0 if no period was detected.
- **significance** (float): The statistical significance of the detected period, or 0 if no period was detected.
- **label** (int): A label identifying the pair of light curves.

### Example Usage

This example shows how to use the `process1tiktok` function to simulate a damped oscillation and detect its period:

.. code-block:: python

    results = process1tiktok(data_manager, '1384142', initial_period=5.0, damping_factor_amplitude=0.2, damping_factor_frequency=0.1, snr=30, inject_signal=True)
    np.savetxt('light_curve_tiktok_analysis.csv', results, delimiter=',')

.. automodule:: QhX.detection
    :members:
    :undoc-members:
    :show-inheritance:
