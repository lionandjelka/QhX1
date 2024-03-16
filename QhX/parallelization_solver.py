"""
The `parallelization_solver` module is designed for parallel processing of astronomical data sets. 
It utilizes multiprocessing to expedite the processing of large data sets across multiple CPUs.

This module defines the `ParallelSolver` class, which orchestrates the parallel execution of a 
specified processing function across different subsets of data. It features mechanisms for time 
logging and result aggregation, facilitating comprehensive analysis workflows.

Example usage:
--------------
    from QhX.detection import process1
    from QhX.parallelization_solver import ParallelSolver
    from QhX.data_manager import DataManager

    data_manager = DataManager()
    fs_df = data_manager.load_fs_df('ForcedSourceTable.parquet')
    fs_gp = data_manager.group_fs_df()
    fs_df = data_manager.fs_df

    setids = ['1384177', '1384184', '1460382']
    solver = ParallelSolver(data_manager=data_manager, delta_seconds=12.0, num_workers=2, log_files=True)
    solver.process_ids(setids, 'results.csv')

Author:
-------
Momcilo Tosic
Astroinformatics student
Faculty of Mathematics, University of Belgrade
"""


import sys
import threading
import time
import os
from multiprocessing import Process
from multiprocessing import Queue
from datetime import datetime
from QhX.detection import *

# Default number of processes to spawn
DEFAULT_NUM_WORKERS = 4
# Default number of seconds to pass between time loggings
DEFAULT_LOG_PERIOD = 10
# CSV format results header
HEADER = "ID,Sampling_1,Sampling_2,Common period (Band1 & Band1),Upper error bound,Lower error bound,Significance,Band1-Band2\n"

class ParallelSolver():
    """
    A class to manage parallel execution of data processing functions.
    
    Attributes:
        delta_seconds (float): Interval in seconds between log messages.
        num_workers (int): Number of worker processes to spawn.
        data_manager (DataManager): Instance of DataManager for data retrieval.
        log_time (bool): Enable/disable time logging.
        log_files (bool): Enable/disable logging to files.
        save_results (bool): Enable/disable saving of results to files.
        process_function (function): Data processing function to be parallelized.
        parallel_arithmetic (bool): Use parallel arithmetic within processing function.
        ntau (int): Parameter ntau for process_function. 
        ngrid (int): Parameter ngrid for process_function.
        provided_minfq (int): Parameter provided_minfq for process_function.
        provided_maxfq (int): Parameters provided_maxfq for process_function.
    """    
    def __init__(self,
                 delta_seconds = DEFAULT_LOG_PERIOD, 
                 num_workers = DEFAULT_NUM_WORKERS,
                 data_manager = None,
                 log_time = True, 
                 log_files = False,
                 save_results = True,
                 process_function = process1_new,
                 parallel_arithmetic = False,
                 ntau =  DEFAULT_NTAU,
                 ngrid = DEFAULT_NGRID, 
                 provided_minfq = DEFAULT_PROVIDED_MINFQ, 
                 provided_maxfq = DEFAULT_PROVIDED_MAXFQ
                ):
        """Initialize the ParallelSolver with the specified configuration."""

        self.delta_seconds = delta_seconds
        self.num_workers = num_workers
        self.data_manager = data_manager
        self.process_function = process_function
        self.log_time = log_time
        self.log_files = log_files
        self.save_results = save_results
        self.parallel_arithmetic = parallel_arithmetic
        self.ntau = ntau
        self.ngrid = ngrid
        self.provided_minfq = provided_minfq
        self.provided_maxfq = provided_maxfq

    @staticmethod
    def background_log(set_id, e : threading.Event, delta_seconds : float):
        """
        Background thread for logging the process time at regular intervals.

        Parameters:
            set_id (str): Identifier for the data set being processed.
            e (threading.Event): Event to signal the thread to exit.
            delta_seconds (float): Time interval for logging.
        """

        # Log starting time
        total_time = 0
        start_time = datetime.now()
        print(f'Starting time for ID {set_id} : {start_time}\n')
        
        while e.wait(delta_seconds) == False:
            # Log how much time passed so far
            total_time += delta_seconds
            print(f'Processing {set_id}\nPID {os.getpid()}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')
        
        # Log finish time
        end_time = datetime.now()
        print(f'End time for ID {set_id} : {end_time}\nTotal time : {end_time - start_time}\n')

    def process_wrapper(self):
        """
        Wrapper for the process function to integrate logging and result handling.
          
        Performed tasks:
         Starts background logging thread if required
         Processes data if data manager exists
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
                # Open output log file
                if self.log_files:
                    logging_file = open(set_id, 'w')
                    sys.stdout = logging_file

                # Begin logging time if flag set
                if self.log_time:
                    stopper_event = threading.Event()
                    daemon = threading.Thread(target = ParallelSolver.background_log, args = (set_id, stopper_event, self.delta_seconds))
                    daemon.start()

                # Call main processing function
                result = self.process_function(self.data_manager,
                                               set_id, 
                                               ntau=self.ntau, 
                                               ngrid=self.ngrid, 
                                               provided_minfq=self.provided_minfq, 
                                               provided_maxfq=self.provided_maxfq, 
                                               parallel=self.parallel_arithmetic, 
                                               include_errors=False)
                
                # Get results into formatted string
                res_string = ""
                for row in result:
                    # Get row values from array or dict
                    row_values = row.values() if isinstance(row, dict) else row
                    # Place row values into CSV formatted string
                    res_string_tmp = ','.join([str(v) for v in row_values]) + "\n"
                    # Append row to resulting string
                    res_string += res_string_tmp

                # Put results in unified results queue if flag is set
                if self.save_all_results_:
                    self.results_.put(res_string)
            except Exception as e:
                print('Error processing/saving data : ' + str(e) + '\n')
            finally:
                # Stop background thread, close output file and write result to individual file if relevant flags are set
                if self.log_time:
                    stopper_event.set()
                    daemon.join()
                if self.log_files:
                    sys.stdout = sys.__stdout__
                    logging_file.close()
                if self.save_results:
                    saving_file = open(set_id + '-result.csv', 'w')
                    saving_file.write(HEADER + res_string)
                    saving_file.close()
        
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
        if results_file is not None:
                try:
                    with open(results_file, 'w') as f:

                        # Header for CSV
                        f.write(HEADER)
                        while not self.results_.empty():
                            try:
                                result = self.results_.get()
                            except Exception as e:
                                break
                            f.write(result)
                except Exception as e:
                    print('Error while saving: \n'+ str(e))
