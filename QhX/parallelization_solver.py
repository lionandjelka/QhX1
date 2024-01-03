from QhX.detection import process1

import sys
import threading
import time
import os
from multiprocessing import Process
from multiprocessing import Queue
from datetime import datetime

DEFAULT_NUM_WORKERS = 4
DEFAULT_LOG_PERIOD = 10 # seconds

class ParallelSolver():
    def __init__(self,
                 delta_seconds = DEFAULT_LOG_PERIOD, 
                 num_workers = DEFAULT_NUM_WORKERS,
                 data_manager = None,
                 log_time = True, 
                 log_files = False,
                 process_function = process1
                ):
        """
        Constructor takes:
        - Seconds for periodic logging
        - Number of processes
        - Flag for logging time & redirecting output to files
        - Processing function (data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors),
        - Data manager reference
        """
        self.delta_seconds = delta_seconds
        self.num_workers = num_workers
        self.data_manager = data_manager
        self.log_time = log_time
        self.log_files = log_files
        self.process_function = process_function

    @staticmethod
    def background_log(set_id, e : threading.Event, delta_seconds : float):
        """
        Function for time logging
        - Logs approx. process time every delta_seconds
        - End when e is triggered
        - Logs start & end system time
        Run in background thread
        """
        total_time = 0
        cur_time = datetime.now()
        print(f'Starting time for ID {set_id} : {cur_time}\n')
        
        while e.wait(delta_seconds) == False:
            total_time += delta_seconds
            print(f'Processing {set_id}\nPID {os.getpid()}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')
        
        cur_time = datetime.now()
        print(f'End time for ID {set_id} : {cur_time}\n')

    def process_wrapper(self, id):
        """
        Wrapper for processing function, takes id of self.setids_div for setids list to process

        
        - Starts background logging thread if required
        - Processes data if data manager exists
        """
        set_ids = self.setids_div[id]
        print('Starting processing ' + str(set_ids) + '\n\n')
        stopper_event = None

        for set_id in set_ids:
            print(set_id)
            try:
                if self.log_files:
                    logging_file = open(set_id, 'w')
                    sys.stdout = logging_file
                if self.log_time:
                    stopper_event = threading.Event()
                    daemon = threading.Thread(target = ParallelSolver.background_log, args = (set_id, stopper_event, self.delta_seconds))
                    daemon.start()
                self.results.put(self.process_function(self.data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, include_errors=False))
            except Exception as e:
                print('Error processing data : ' + str(e) + '\n')
            finally:
                if self.log_time:
                    stopper_event.set()
                    daemon.join()
                if self.log_files:
                    logging_file.close()


    def process_ids(self, setids, save_results = None):	
        """
        Process ids using QhX function
        - setids : ids to process
        - data_manager : data manager provided
        - num_workers : maximum number of processes at one time
        - delta_seconds : time period for process logging
        - log_time : flag whether to log time
        - save_results : filename of results file
        - chunk_size : how many IDs to assign to one worker at once (use for larger files)
        - tasks_per_child : how many tasks to spawn for each process before refreshing child processes
        - process_function : function used to process quasar data,
        takes arguments in form (data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors)
        """
        self.setids_div = []
        self.results = Queue()

        for i in range(self.num_workers):
            self.setids_div.append([setids[j] for j in range(i, len(setids), self.num_workers)])
        
        print('Divided sets : ' + str(self.setids_div) + '\n\n')

        processes = [Process(target = self.process_wrapper, args = (i,)) for i in range(self.num_workers)]
        
        for p in processes:
          p.start()
        for p in processes:
          p.join()

        if save_results is not None:
                try:
                    with open(save_results, 'w') as f:
                        for result in self.results:
                            f.write(result + '\n')
                except Exception as e:
                    print('Error while saving: \n'+ str(e))
