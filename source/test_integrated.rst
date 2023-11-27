test_integrated
===============

The ``test_integrated`` module in the QhX package
-------------------------------------------------

.. automodule:: QhX.tests.test_integrated
    :members:
    :undoc-members:
    :show-inheritance:

Overview
--------

The ``test_integrated`` module of the QhX package encompasses comprehensive tests designed to validate the core functionalities associated with the analysis of light curve data. This includes the rigorous testing of modules responsible for calculating Wavelet matrix coefficients, period detection, and assessing period significance in quasar light curves.

Key Aspects of the Tests
------------------------
- on local machine run test as:  pytest -s QhX/tests/test_integrated.py
- on google run test as:!python -m unittest discover -s tests
- **Scope**: Tests cover all essential functionalities related to the period analysis in light curves, 
  ensuring reliability and accuracy of the algorithms implemented in the QhX package.
- **Efficiency**: The testing procedure demonstrates the package's capability to process and analyze  light curve data efficiently. 
   The average execution time for the complete test suite is approximately 1 minute and 54 seconds, indicative of the package's optimized performance.
- **Results**: All tests within the module successfully pass, confirming the correct implementation and expected behavior of the period analysis algorithms.      This includes generating synthetic light curve, validation of the Hybrid2D and the estimation of period errors, significance using shuffled light curve simulations.

