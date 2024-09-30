Quick Start Tutorial
====================

Getting started with QhX is simple. Follow the steps below to begin analyzing quasar light curves.

Step 1: Installation
--------------------

First, install the QhX package if you have not already. You can do this using pip:

.. code-block:: bash

    pip install QhX

Or, if you are installing from the source:

.. code-block:: bash

    git clone https://github.com/lionandjelka/QhX1.git
    cd QhX
    pip install .

Step 2: Running Tests
---------------------

Once you have installed the `QhX` package, it is important to run the tests to verify that everything is working correctly in your environment. This section explains how to do that.

### 1. Ensure `pytest` is Installed

To run the tests, you need `pytest`. You can install it using `pip`:

.. code-block:: bash

    pip install pytest

### 2. Check Where the Package is Installed

To confirm where the `QhX` package is installed, use the following command:

.. code-block:: bash

    pip show QhX

This command will display the installation path of the `QhX` package. You can use this path to locate the tests, if necessary.

### 3. Running the Tests

#### Option 1: Running Tests from the Installed Package Directory

If you are in the directory where the package is installed, you can directly run the tests using:

.. code-block:: bash

    pytest -s QhX/tests/test_integrated.py

#### Option 2: Running Tests from Anywhere

If you are not in the package installation directory, you can specify the full path to the tests. Use the path obtained in step 2, and run:

.. code-block:: bash

    python -m pytest -s /path/to/your/package/QhX/tests/test_integrated.py

This will run the tests regardless of your current directory, as long as the package is installed.

### 4. Using Verbose Mode

For more detailed test output, you can add the `-v` flag for verbose mode:

.. code-block:: bash

    pytest -v -s QhX/tests/test_integrated.py

This will provide more information about each test that is executed.

### Notes

- Make sure that you are using the correct Python environment where the `QhX` package is installed.
- You can also run `pytest` as a Python module to ensure it's using the correct environment:

.. code-block:: bash

    python -m pytest -s QhX/tests/test_integrated.py


You should see output similar to the following, indicating that the tests have passed:

.. code-block:: text


    ====================================================== test session starts ======================================================
    platform darwin -- Python 3.10.9, pytest-7.1.2, pluggy-1.0.0
    rootdir: /Users/andjelka/Documents/QhX1
    plugins: anyio-3.5.0
    collected 2 items                                                                                                                

    QhX/tests/test_integrated.py Running integrated  test on simulation of single light curve, and functionalities of modules
    for Wavelet matrix coefficients calculations and period and its significance calculation. This may take time about 500-800 seconds...
    *** Starting Weighted Wavelet Z-transform ***

    Pseudo sample frequency (median) is  0.203
    largest tau window is  46.124
    8.05 seconds has passed to complete Weighted Wavelet Z-transform 

    *** Starting Weighted Wavelet Z-transform ***

    Pseudo sample frequency (median) is  0.203
    largest tau window is  46.124
    8.49 seconds has passed to complete Weighted Wavelet Z-transform 
    .
    .
    .
    results of individual testings of modules for period detection and significance
    simulated period in days 100
    list of periods in days [100.47726701833716]
    upper and lower errors in days [3.3403584182233317] [1.6831563583308196]
    number of simulated shuffled light curves 10
    experimental significance 1.0
    
    ================================================= 1 passed in 114.15s (0:01:54) =================================================
    
For more advanced users, you may test the logger and parallel solver classes:

.. code-block:: bash

    os@ubuntu:~/Desktop/qhx_astro/QhX1$ cd QhX/tests; pytest -s test_logger.py
    
You should see output resembling this:

.. code-block:: text

   ================================== test session starts ==================================
   platform linux -- Python 3.10.11, pytest-8.1.1, pluggy-1.4.0
   rootdir: /home/os/Desktop/qhx_astro/QhX1
   plugins: anyio-4.3.0
   collected 1 item                                                                        
   
   test_logger.py 
   
   Log file created.
   
   Time log found in file.
   
   Output log found in file.
   .
   
   ================================== 1 passed in 27.56s ===================================

For the parallel solver (note we are in the QhX1 folder again):

.. code-block:: bash

    os@ubuntu:~/Desktop/qhx_astro/QhX1$ cd QhX/tests; pytest -s test_parallel_solver.py
    
The output should look similar to this:

.. code-block:: text

    ================================== test session starts ==================================
    platform linux -- Python 3.10.11, pytest-8.1.1, pluggy-1.4.0
    rootdir: /home/os/Desktop/qhx_astro/QhX1
    plugins: anyio-4.3.0
    collected 1 item                                                                        
    
    test_parallel_solver.py 
    
    Log file for 0 created.
    
    Log file for 1 created.
    
    Log file for 2 created.
    
    Log file for 3 created.

    Merged results file present.
    
    Merged result file content correct.
    .
    
    ================================== 1 passed in 23.84s ===================================

Step 3: Importing the Package
-----------------------------

Once QhX is installed, and you have confirmed that the tests pass, you can import it into your Python script or interactive session:

.. code-block:: python

    import QhX
	import numpy as np
	import pandas as pd

Step 4: Loading Data
--------------------

Load your light curve data into QhX. For example importing parquet LSST AGN Data Challange:

.. code-block:: python

    from QhX.data_manager import DataManager
	data_manager = DataManager()
	fs_df = data_manager.load_fs_df('https://zenodo.org/record/6878414/files/ForcedSourceTable.parquet')
	fs_gp = data_manager.group_fs_df()
	
You should see the message like this, indicating that parquet is loaded

.. code-block:: text

    Forced source data loaded successfully.
    Forced source data grouped successfully.

.. code-block:: python   

    td_objects=data_manager.load_object_df("https://zenodo.org/record/6878414/files/ObjectTable.parquet")
    #Find quasars IDs
    setindexqso=td_objects[(td_objects["class"].eq("Qso"))].index

.. code-block:: text

    Object data loaded and processed successfully.

.. code-block:: text

  	##FIND quasars indices and transform to arrays
	setindexnew=data_manager.get_qso(setindexqso)
	setindexnew=np.array(setindexnew)
	df = pd.DataFrame({'objectId': setindexnew})
	df.set_index('objectId', inplace=True)
	setidnew=df.index 
	
Importing light curve of one object ID=1384142

.. code-block:: python

    from QhX.light_curve import get_lctiktok, get_lc22
    light_curves_data = get_lc22(data_manager, '1384142', include_errors=False)

Step 5: Analyzing the Light Curve
---------------------------------

With the data loaded, you can start analyzing the light curve:

.. code-block:: python

   from QhX.calculation import *
   from QhX.detection import *
   # Ensure to import or define other necessary functions like hybrid2d, periods, same_periods, etc.
   from QhX.algorithms.wavelets.wwtz import *
   process1_results = process1_new(data_manager, '1384142', ntau=80, ngrid=800, provided_minfq=2000, provided_maxfq=10, include_errors=True)
   
The output dictionary `process1_results` contains:

.. code-block:: text

    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.08568965517243,
     'period': 446.179587283882,
     'upper_error': 26.594480680527795,
     'lower_error': 22.513862402711993,
     'significance': 0.98,
     'label': '0-1'},
    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.08568965517243,
     'period': 446.179587283882,
     'upper_error': 35.654914195946844,
     'lower_error': 17.127186682281263,
     'significance': 1.0,
     'label': '0-2'},
    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.87666666666669,
     'period': 446.179587283882,
     'upper_error': 30.9002280462837,
     'lower_error': 20.398836831717233,
     'significance': 1.0,
     'label': '0-3'},
    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.08568965517243,
     'period': 472.39444936522017,
     'upper_error': 26.594480680527795,
     'lower_error': 22.513862402711993,
     'significance': 1.0,
     'label': '1-2'},
    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.87666666666669,
     'period': 472.39444936522017,
     'upper_error': 26.594480680527795,
     'lower_error': 22.513862402711993,
     'significance': 1.0,
     'label': '1-3'},
    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.87666666666669,
     'period': 308.999613750483,
     'upper_error': 22.17397677238779,
     'lower_error': 3.746728576973794,
     'significance': 0.98,
     'label': '1-3'},
    {'objectid': '1384142',
     'sampling_i': 45.08568965517243,
     'sampling_j': 45.87666666666669,
     'period': 472.39444936522017,
     'upper_error': 30.9002280462837,
     'lower_error': 20.398836831717233,
     'significance': 0.94,
     'label': '2-3'}

Step 6: Viewing Results
-----------------------

Finally, examine the results of your analysis. Important that process1_results will be suplied as a list of dictionaries:

.. code-block:: python

    from QhX.output import classify_periods, classify_period
    outt=classify_periods([process1_results])
	outt['classification'] =outt.apply(classify_period, axis=1)
	print(outt)
	
This will print the detected periods, their errors, significance levels, iou metric, difference among detected periods, flags.

.. table:: Example Analysis Results
   :widths: auto
   :name: example-results

   +-------+----------+------------------+------------------+------------------+------+-----+-----+-------------+------+---------------+
   | index | objectid |        m3        |        m4        |        m5        |  m6  | m7_1| m7_2| period_diff | iou  | classification|
   +=======+==========+==================+==================+==================+======+=====+=====+=============+======+===============+
   |   0   |  1384142 | 446.179587283882 | 22.5138624027119 | 26.5944806805277 | 0.98 | 0-1 | 0-2 |     0.0     | 1.0  |     poor      |
   +-------+----------+------------------+------------------+------------------+------+-----+-----+-------------+------+---------------+
   |   1   |  1384142 | 446.179587283882 | 22.5138624027119 | 26.5944806805277 | 0.98 | 0-1 | 0-3 |     0.0     | 1.0  |     poor      |
   +-------+----------+------------------+------------------+------------------+------+-----+-----+-------------+------+---------------+
   |   2   |  1384142 | 446.179587283882 | 22.5138624027119 | 26.5944806805277 | 0.98 | 0-1 | 1-2 |   0.05875   | 0.215|     poor      |
   +-------+----------+------------------+------------------+------------------+------+-----+-----+-------------+------+---------------+
   |   3   |  1384142 | 446.179587283882 | 22.5138624027119 | 26.5944806805277 | 0.98 | 0-1 | 1-3 |   0.05875   | 0.215|     poor      |
   +-------+----------+------------------+------------------+------------------+------+-----+-----+-------------+------+---------------+
   |   4   |  1384142 | 446.179587283882 | 22.5138624027119 | 26.5944806805277 | 0.98 | 0-1 | 1-3 |   0.30745   | NaN  |     NAN       |
   +-------+----------+------------------+------------------+------------------+------+-----+-----+-------------+------+---------------+

This table shows an example of the output from the QhX package after analyzing light curve data. The `objectid` column represents the identifier for the object, while `m3` is period. m4, and m5 are upper and lower errors, m6 is significance, to m7_1 and `m7_2` columns are the pairs of bands. The `period_diff` column indicates the difference between detected periods, `iou` is the intersection over union of the period errors, and the `classification` column categorizes the reliability of the detected period.

Further Exploration
-------------------

Now that you've had a taste of what QhX can do, explore the documentation to learn more about the available modules and functions. You can also check out the Examples section for more detailed use cases and advanced features.
