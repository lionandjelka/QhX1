"""
Author:

Momcilo Tosic
Astroinformatics student
Faculty of Mathematics, Uni of Belgrade

"""
from QhX.detection import process1

import sys
import threading
import time
import os
from multiprocessing import Process
from multiprocessing import Queue
from datetime import datetime

# Default number of processes to spawn
DEFAULT_NUM_WORKERS = 4
# Default number of seconds to pass between time loggings
DEFAULT_LOG_PERIOD = 10
# csv format results header
HEADER = "Set ID,Common period (Band1 & Band2),Upper error bound,Lower error bound,Significance,Band1-Band2\n"

"""
ParallelSolver runs an assigned processing function on all set IDs (string) in parameter list, using data from assigned
DataManager instance, with possible time & process logging.
Saves individual results or in one single file (or both).

Example usage:

from QhX.detection import process1
from QhX.parallelization_solver import *
from QhX.data_manager import DataManager

data_manager = DataManager()
fs_df = data_manager.load_fs_df('ForcedSourceTable.parquet')
fs_gp = data_manager.group_fs_df()
fs_df = data_manager.fs_df

setids = ['1384177', '1384184', '1460382']
solver = ParallelSolver(data_manager=data_manager, delta_seconds=12.0, num_workers=2, log_files=True)
solver.process_ids(setids, 'results')
"""

class ParallelSolver():
    def __init__(self,
                 delta_seconds = DEFAULT_LOG_PERIOD, 
                 num_workers = DEFAULT_NUM_WORKERS,
                 data_manager = None,
                 log_time = True, 
                 log_files = False,
                 save_results = True,
                 process_function = process1,
                 parallel_arithmetic = False
                ):
        """
        Constructor takes:

        - num_workers : number of processes to start
        - process_function : processing function that takes in (data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors, parallel),
        - data_manager : data manager reference
        - delta_seconds : seconds for periodic time logging (None if not logging)
        - log_time, log_files : flags for logging time & sending output to files
        - save_results : saves results in separate files at the end of every ID processing
        - parallel_arithmetic : whether to set parallel flag of process_function (one function call will make use of ALL cores)
        """
        self.delta_seconds = delta_seconds
        self.num_workers = num_workers
        self.data_manager = data_manager
        self.process_function = process_function
        self.log_time = log_time
        self.log_files = log_files
        self.save_results = save_results
        self.parallel_arithmetic = parallel_arithmetic

    @staticmethod
    def background_log(set_id, e : threading.Event, delta_seconds : float):
        """
        Function for time logging
        - Logs approx. process time every delta_seconds
        - End when e is triggered
        - Logs start & end system time
        Run in background thread
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
        Wrapper for processing function, takes id of self.setids_div for setids list to process

        - Starts background logging thread if required
        - Processes data if data manager exists
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

                # Call main processing fnc
                result = self.process_function(self.data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, parallel=self.parallel_arithmetic, include_errors=False)
                
                # Get results into formatted string
                res_string = ""
                for row in result:
                    res_string_tmp = ""
                    for entry in row:
                        res_string_tmp += str(entry) + ","
                    res_string_tmp = res_string_tmp[:-1] + "\n"
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
        Process ids using QhX function
        - setids : ids to process
        - save_results : filename of results file ( preffered .csv )
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
