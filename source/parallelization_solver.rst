Parallelization Solver module
=============================

The ``parallelization_solver`` module is designed for parallel processing of data sets, using multiprocessing. Below is the documentation for the module and its classes.

.. automodule:: QhX.parallelization_solver
   :members:
   :undoc-members:
   :show-inheritance:


Example Usage
-------------

The following example demonstrates how to use the `ParallelSolver` class with the `DataManagerDynamical` class for parallel processing in the dynamical mode.

.. code-block:: python

    import QhX
    import numpy as np
    import pandas as pd
    from QhX.parallelization_solver import ParallelSolver
    from QhX import DataManagerDynamical, get_lc_dyn, process1_new_dyn

    # Define mappings for AGN DC data
    agn_dc_mapping = {
        'column_mapping': {'flux': 'psMag', 'time': 'mjd', 'band': 'filter'},  # Map AGN DC columns
        'group_by_key': 'objectId',  # Group by 'objectId' for AGN DC
        'filter_mapping': {0: 0, 1: 1, 2: 2, 3: 3}  # Map AGN DC filters
    }

    # Initialize the DataManager with AGN DC mappings
    data_manager_agn_dc = DataManagerDynamical(
        column_mapping=agn_dc_mapping['column_mapping'],
        group_by_key=agn_dc_mapping['group_by_key'],
        filter_mapping=agn_dc_mapping['filter_mapping']
    )

    # Load data from a remote source
    data_manager_agn_dc.load_data('https://zenodo.org/record/6878414/files/ForcedSourceTable.parquet')
    data_manager_agn_dc.group_data()

    # Setup and run the parallel solver
    setids = ['0458387']
    solver_dynamical = ParallelSolver(
        delta_seconds=12.0, num_workers=4, data_manager=data_manager_agn_dc, log_time=True, log_files=False,
        save_results=True, process_function=process1_new_dyn, parallel_arithmetic=True, ntau=80, ngrid=100,
        provided_minfq=500, provided_maxfq=10, mode='dynamical'
    )
    solver_dynamical.process_ids(setids, 'results2.csv')

    # Print the results
    with open('results2.csv') as results_file:
        print(results_file.read())

.. note::
    Ensure the data file is correctly accessible at the URL or path specified for loading. This example uses data available online for demonstration.