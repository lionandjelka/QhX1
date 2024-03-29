merge_batch_csv Module
======================

The ``merge_batch_csv`` module provides functionality for merging CSV files generated from batch processes into a single consolidated CSV file. This is particularly useful for analyzing results that are split across multiple batch output files.

.. automodule:: QhX.merge_batch_csv
   :members:
   :undoc-members:
   :show-inheritance:

Usage
-----

The ``merge_batch_csv`` function can be executed directly as a standalone script or imported into another Python script.

**As a Standalone Script:**

Navigate to the package directory and execute:

.. code-block:: bash

    cd path/to/QhX
    python -m merge_batch_csv

**Importing in Python Scripts:**

.. code-block:: python

    from QhX.merge_batch_csv import merge_batch_csv
    
    directory_to_search = "./data"
    output_file_name = "final_merged_results.csv"
    
    merge_batch_csv(directory=directory_to_search, output_file=output_file_name)
    
    print("CSV files have been merged successfully.")

Parameters
----------

- **directory** (str): The root directory to search for CSV files. Defaults to the current directory.
- **output_file** (str): The filename for the merged CSV. Defaults to 'merged_result.csv'.

