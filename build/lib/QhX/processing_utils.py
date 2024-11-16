
"""
processing_utils.py

This module provides functionality for parallel processing of data tasks using threading, on your local
computer, if it is more handy than using our procedure for parallelization on HPC.

Key Points:

Non-picklable Objects:
    Objects like DataManager that cannot be pickled (a requirement for multiprocessing) are handled
    efficiently using a threading approach (like with ThreadPool) because threads share the same memory
    space. This is particularly useful for objects that maintain state or have open connections (like
    database connections) that are not easily serialized.

I/O-Bound Tasks:
    For tasks that are I/O-bound (e.g., network data fetching, file reading, database querying), threading
    can significantly improve performance. While Python's GIL (Global Interpreter Lock) prevents
    CPU-bound tasks from running in parallel in a multi-threaded environment, it allows I/O-bound tasks
    to execute concurrently.

Shared Resources:
    Threading is beneficial when using shared resources (like a shared DataManager instance) across
    different tasks without the need to initiate them separately for each task. Since all threads
    access the same memory space, a resource can be initialized once and used across all threads,
    enhancing memory efficiency.

CPU-Bound Tasks with GIL Limitations:
    Although threading in Python is not ideal for CPU-bound tasks due to the GIL, it can be advantageous
    for tasks that involve calling out to external applications or libraries that release the GIL
    (e.g., operations in NumPy, pandas, or I/O operations).

Rapid Task Switching Needs:
    Applications that benefit from rapid switching between tasks (e.g., handling multiple quick I/O
    operations concurrently) can leverage threading to facilitate this without the overhead of process
    creation and inter-process communication.
"""


# Import necessary threading components
from multiprocessing.dummy import Pool as ThreadPool

# Import functions for both fixed and dynamical modes
from QhX.detection import process1_new
from QhX.dynamical_mode import process1_new_dyn

def process_pool(args):
    """
    This function is called by each thread in the pool, unpacking the arguments
    and passing them to the appropriate processing function based on the mode.

    Args:
        args (tuple): A tuple containing all the parameters needed for the
                      processing function. This should include:
                      - set_id (str)
                      - data_manager (DataManager object)
                      - ntau (int)
                      - ngrid (int)
                      - provided_minfq (float)
                      - provided_maxfq (float)
                      - include_errors (bool)
                      - mode (str): Either 'fixed' or 'dynamical' to determine which function to call.

    Returns:
        dict: The result from the appropriate processing function.
    """
    # Unpack the arguments
    set_id, data_manager, ntau, ngrid, provided_minfq, provided_maxfq, include_errors, mode = args

    # Call the appropriate processing function based on the mode
    if mode == 'fixed':
        return process1_new(data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors)
    elif mode == 'dynamical':
        return process1_new_dyn(data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors)
    else:
        raise ValueError(f"Unknown mode: {mode}")

def parallel_pool(setids, data_manager, ntau, ngrid, provided_minfq, provided_maxfq, include_errors, mode='fixed', num_threads=2):
    """
    Sets up the thread pool and manages the parallel execution of the processing function.

    Args:
        setids (list of str): List of dataset identifiers to be processed.
        data_manager (DataManager): The DataManager instance to use for processing.
        ntau (int): Number of tau intervals.
        ngrid (int): Number of grid points.
        provided_minfq (float): Period in days for calculating minimum frequency parameter for processing.
        provided_maxfq (float): Period in days for calculating  maximum frequency parameter for processing.
        include_errors (bool): Flag to indicate whether to include error of magnitudes handling.
        mode (str): Either 'fixed' or 'dynamical' to select which processing function to use.
        num_threads (int): Number of threads to use for parallel processing.

    Returns:
        list: A list of results from processing each dataset identifier.
    """
    # Create a tuple for each set_id, pairing it with all other necessary parameters
    args = [(set_id, data_manager, ntau, ngrid, provided_minfq, provided_maxfq, include_errors, mode) for set_id in setids]

    # Initialize the ThreadPool with the specified number of threads
    with ThreadPool(num_threads) as pool:
        # Map the process_pool function to each tuple of arguments
        results = pool.map(process_pool, args)

    return results

# If this script is executed directly (rather than imported as a module), run a test
if __name__ == "__main__":
    # Example set IDs and parameters for the processing function
    setids = ['1385092', '1385097']

    # Parameters for the processing function
    ntau = 80
    ngrid = 80
    provided_minfq = 200
    provided_maxfq = 10
    include_errors = False

    # Test the fixed mode
    print("Testing Fixed Filter Mode:")
    results_fixed = parallel_pool(setids, data_manager, ntau, ngrid, provided_minfq, provided_maxfq, include_errors, mode='fixed', num_threads=2)
    for result in results_fixed:
        print(result)

    # Test the dynamical mode
    print("Testing Dynamical Filter Mode:")
    results_dynamical = parallel_pool(setids, data_manager_dyn, ntau, ngrid, provided_minfq, provided_maxfq, include_errors, mode='dynamical', num_threads=2)
    for result in results_dynamical:
        print(result)
