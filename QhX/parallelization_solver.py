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
from QhX.iparallelization_solver import *

# Default number of seconds to pass between time loggings
DEFAULT_LOG_PERIOD = 10
# CSV format results header
HEADER = "ID,Sampling_1,Sampling_2,Common period (Band1 & Band1),Upper error bound,Lower error bound,Significance,Band1-Band2\n"

class ParallelSolver(IParallelSolver):
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

        super().__init__(num_workers)
        self.delta_seconds = delta_seconds
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

    def aggregate_process_function_result(self, result):
        """
        Places the result dict into a string

        Parameters:
            result (dict, list): Result from QhX detection function
        """
        res = ""
        for row in result:
            # Get row values from array or dict
            row_values = row.values() if isinstance(row, dict) else row
            # Place row values into CSV formatted string
            res_string_tmp = ','.join([str(v) for v in row_values]) + "\n"
            # Append row to resulting string
            res += res_string_tmp
        return res

    def get_process_function_result(self, set_id):
        """
        Run the QhX detection function and return the result

        Parameters:
            set_id (str): Set ID to process
        """
        
        result = self.process_function(self.data_manager,
                                               set_id, 
                                               ntau=self.ntau, 
                                               ngrid=self.ngrid, 
                                               provided_minfq=self.provided_minfq, 
                                               provided_maxfq=self.provided_maxfq, 
                                               parallel=self.parallel_arithmetic, 
                                               include_errors=False)
        return result
    
    def maybe_begin_logging(self, set_id):
        """
        Starts a logging thread and opens a logging file, redirecting output to it

        Parameters:
            set_id (str): ID of set to be processed
        """
        logging_file = None
        # Open output log file
        if self.log_files:
            logging_file = open(set_id, 'w')
            sys.stdout = logging_file

        # Begin logging time if flag set
        if self.log_time:
            stopper_event = threading.Event()
            daemon = threading.Thread(target = ParallelSolver.background_log, args = (set_id, stopper_event, self.delta_seconds))
            daemon.start()
        
        return stopper_event, daemon, logging_file
    
    def maybe_stop_logging(self, stopper_event, logging_thread, logging_file):
        """
        Stops the logging thread gracefully

        Parameters:
            stopper_event (Event): Event to set to end logging
            logging_thread (Thread): Thread to join
            logging_file (file): File to close
        """
        # Stop background thread, close output file and write result to individual file if relevant flags are set
        if self.log_time:
            stopper_event.set()
            logging_thread.join()
        if self.log_files:
            sys.stdout = sys.__stdout__
            logging_file.close()

    def maybe_save_local_results(self, set_id, res_string):
        """
        Saves local results of set ID formed into a string

        Parameters:
            set_id (str): ID which was processed
            res_string (str): The string the result was aggregated into
        """
        # Save local results with header
        if self.save_results:
            saving_file = open(set_id + '-result.csv', 'w')
            saving_file.write(HEADER + res_string)
            saving_file.close()

    def maybe_save_results(self, results_file):
        """
        If results file is set, saves the full results queue to it.

        Parameters:
            result_file (str, optional): Filename of the result file
        """
        # Save results to results_file
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
        

