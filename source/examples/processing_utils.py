# processing_utils.py
import QhX
from QhX.data_manager import DataManager
from QhX.light_curve import get_lctiktok, get_lc22
from QhX.calculation import periods, signif_johnson
from QhX.algorithms.wavelets.wwtz import *
from QhX.detection import process1_new

def process1_wrapper(set_id, data_manager):
    """
    This function acts as a wrapper for the `process1_new` function, simplifying its usage.
    
    It prints the set ID being processed for logging purposes and calls `process1_new`
    with a predefined set of parameters.
    
    Parameters
    ----------
    set_id : int
        The unique identifier for the data set to process.
    data_manager : DataManager
        An instance of the DataManager class that handles the data involved in the process.

    Returns
    -------
    dict
        A dictionary containing the results of the `process1_new` processing, 
        structured according to the QhX detection module's specifications.

    Notes
    -----
    The parameters for the `process1_new` function, such as `ntau`, `ngrid`,
    `provided_minfq`, `provided_maxfq`, and `include_errors`, are preset within this wrapper.
    """
    print(f"Processing setid: {set_id}")  # Using print for visibility in Google Colab
    # Call the actual process1 function
    return QhX.detection.process1_new(data_manager, set_id, ntau=80, ngrid=200, provided_minfq=500, provided_maxfq=10, include_errors=False)

def process1_caller(args):
    """
    This function calls the `process1_wrapper` function with a set of arguments,
    facilitating its use with features like `multiprocessing.Pool.map`.

    Parameters
    ----------
    args : tuple
        A tuple containing the arguments for the `process1_wrapper` function.
        Expected to contain the following elements:
        - set_id (int): The set ID to process.
        - data_manager (DataManager): The DataManager instance for the data.

    Returns
    -------
    dict
        The result returned by the `process1_wrapper` function.

    Notes
    -----
    This function is particularly useful for parallel processing scenarios
    where the `process1_wrapper` function needs to be mapped over a sequence of arguments.
    """
    return process1_wrapper(*args)
