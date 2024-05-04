test_parallel_solver
=====================

The ``test_parallel_solver``  in the QhX package
-------------------------------------------------

.. automodule:: QhX.tests.test_parallel_solver
    :members:
    :undoc-members:
    :show-inheritance:

Overview
--------
The ``test_parallel_solver`` module of the QhX package provides unit testing for the ParallelSolver class. This includes the testing of proper processing of results of an input function, merging of results from multiple data subsets and proper creation of log files.

Key Aspects of the Tests
------------------------
- on local machine run test as:  pytest -s QhX/tests/test_parallel_solver.py
- on google run test as: !python -m unittest discover -s tests
- **Scope**: Tests cover the processing of a fake function that gives different output for several mock set IDs, generating log files, and local results for mock set IDs (data subsets).
- **Efficiency**: The test utilises a fake function without loading any large amounts of data, ensuring a completion in around 30s.
- **Results**: The unit test passes all assertions, several log files (no extension) are created, alongside the local ID-resuit.csv files and the mock results final csv.
