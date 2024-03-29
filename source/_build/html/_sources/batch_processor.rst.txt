Batch Processor Module
======================

.. module:: QhX.batch_processor

The ``batch_processor`` module is part of the QhX package, designed for processing large datasets in parallel batches. It uses ``DataManager`` for data loading and preprocessing, and the ``ParallelSolver`` for executing data processing tasks in parallel.

Overview
--------

The module allows for the processing of data in specified batch sizes using a predetermined number of parallel workers. It aims to enhance processing efficiency when dealing with large datasets.

Functions
---------

.. autofunction:: QhX.batch_processor.process_batches

This function is responsible for orchestrating the batch processing workflow. It involves loading and optionally grouping the dataset, splitting it into batches, and processing each batch in parallel.

Usage
-----

The module can be used as a standalone script or imported into other scripts or modules within the QhX package. When executed as a script, it requires the batch size as a mandatory argument, with optional arguments for the number of workers and the starting index for processing.

.. code-block:: bash

    python -m QhX.batch_processor 100 25 0

This command processes the dataset in batches of 100 using 25 parallel workers, starting from the first record.

Installation and Requirements
-----------------------------

Ensure that the QhX package is properly installed and configured in your environment. The ``batch_processor`` module depends on other components of the QhX package, such as ``DataManager`` and ``ParallelSolver``.

See Also
--------

- :doc:`data_manager`
- :doc:`parallelization_solver`

