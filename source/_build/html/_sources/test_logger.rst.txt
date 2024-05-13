test_logger
=====================

The ``test_logger``  in the QhX package
-------------------------------------------------

.. automodule:: QhX.tests.test_logger
    :members:
    :undoc-members:
    :show-inheritance:

Overview
--------
The ``test_logger`` module of the QhX package provides unit testing for the Logger class. It simulates processing running for several seconds and outputing a test string, checking if a log file is created and if its contents are as expected.



Key Aspects of the Tests
------------------------
- on local machine run test as: pytest -s QhX/tests/test_logger.py
- on google run test as: !python -m unittest discover -s tests
- **Scope**: Tests cover starting logging, creating a log file and writing to it in different ways.
- **Efficiency**: The test sleeps the running thread in order to check if the logging thread will write output during this time. The expected time for the test should be around 3s, but may take longer due to file creation and editing.
- **Results**: The unit test passes all assertions, a test log file (no extension) is created.
