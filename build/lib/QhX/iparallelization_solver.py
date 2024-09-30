"""
The `iparallelization_solver` interface is designed for parallel execution of an input function. 

This module defines the `IParallelSolver` class, which orchestrates the parallel execution of a 
general processing function on a data set consisting of multiple independent data subsets, here reffered to as set IDs.
It also declares a logging method (intended to start a separate logging thread).

Author:
-------
Momcilo Tosic
Astroinformatics student
Faculty of Mathematics, University of Belgrade
"""

from multiprocessing import Process
from multiprocessing import Queue

# Default number of processes to spawn
DEFAULT_NUM_WORKERS = 4

class IParallelSolver():
    """
    A class to manage parallel execution of data processing functions.
    
    Attributes:
        num_workers (int): Number of worker processes to spawn.
    """    
    def __init__(self,
                 num_workers = DEFAULT_NUM_WORKERS,
                ):
        """Initialize the ParallelSolver with the specified configuration."""

        self.num_workers = num_workers
    
    def process_wrapper(self):
        """
        Wrapper for the process function to integrate logging and result handling.
        """

        
        # Event used for stopping background log thread
        stopper_event = None
        
        # Go through unprocessed sets
        while not self.set_ids_.empty():
            # Safely pop from queue
            try:
                set_id = self.set_ids_.get()
            except Exception as e:
                break

            # If a throw happens before setting result
            res_string = ""

            try:
                # Maybe start logging
                self.maybe_begin_logging(set_id)

                # Call main processing function
                result = self.get_process_function_result(set_id)
                
                # Get results into formatted string
                res_string = self.aggregate_process_function_result(result)

                # Put results in unified results queue if flag is set
                if self.save_all_results_:
                    self.results_.put(res_string)
            except Exception as e:
                print('Error processing/saving data : ' + str(e) + '\n')
            finally:
                try:
                    # Maybe stop logging
                    self.maybe_stop_logging()

                    # Maybe save local results
                    self.maybe_save_local_results(set_id, res_string)
                except Exception as e:
                    print('Error stopping logs : ' + str(e))
        
    def process_ids(self, set_ids, results_file = None):	
        """
        Processes a list of set IDs using the configured process function in parallel.

        Parameters:
            set_ids (list of str): List of set IDs to process.
            results_file (str, optional): Path to save aggregated results.
        """


        # Unified output queue and input queue
        self.results_ = Queue()
        self.set_ids_ = Queue()

        # Set flag to save all results from unified queue
        if results_file is not None:
            self.save_all_results_ = True
        else:
            self.save_all_results_ = False

        # Fill input queue
        for id in set_ids:
            self.set_ids_.put(id)
        
        # Generate and start processes
        processes = [Process(target = self.process_wrapper) for i in range(self.num_workers)]
        for p in processes:
          p.start()
        for p in processes:
          p.join()

        # Save results to unified results file
        self.maybe_save_results(results_file)

    def aggregate_process_function_result(self, result):
        pass

    def get_process_function_result(self, set_id):
        pass

    def maybe_begin_logging(self, set_id):
        pass
    
    def maybe_stop_logging(self):
        pass

    def maybe_save_local_results(self, set_id, res_string):
        pass

    def maybe_save_results(self, results_file):
        pass
