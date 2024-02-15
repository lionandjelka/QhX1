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
                 save_results = True,
                 process_function = process1
                ):
        """
        Constructor takes:

        - num_workers : number of processes to start
        - proceess_function : processing function (data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors),
        - data_manager : data manager reference
        - delta_seconds : seconds for periodic time logging (None if not logging)
        - log_time, log_files : flags for logging time & sending output to files
        - save_results : saves results in separate files at the end of every ID processing
        """
        self.delta_seconds = delta_seconds
        self.num_workers = num_workers
        self.data_manager = data_manager
        self.process_function = process_function
        self.log_time = log_time
        self.log_files = log_files
        self.save_results = save_results

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
        start_time = datetime.now()
        print(f'Starting time for ID {set_id} : {start_time}\n')
        
        while e.wait(delta_seconds) == False:
            total_time += delta_seconds
            print(f'Processing {set_id}\nPID {os.getpid()}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')
        
        end_time = datetime.now()
        print(f'End time for ID {set_id} : {end_time}\nTotal time : {end_time - start_time}\n')

    def process_wrapper(self):
        """
        Wrapper for processing function, takes id of self.setids_div for setids list to process

        - Starts background logging thread if required
        - Processes data if data manager exists
        """
        stopper_event = None

        while not self.set_ids_.empty():
            try:
                set_id = self.set_ids_.get()
            except Exception as e:
                break
            try:
                if self.log_files:
                    logging_file = open(set_id, 'w')
                    sys.stdout = logging_file
                if self.log_time:
                    stopper_event = threading.Event()
                    daemon = threading.Thread(target = ParallelSolver.background_log, args = (set_id, stopper_event, self.delta_seconds))
                    daemon.start()

                result = str(self.process_function(self.data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, include_errors=False))
                if self.save_all_results_:
                    self.results_.put('ID ' + set_id + '\n\n' + result)
            except Exception as e:
                print('Error processing data : ' + str(e) + '\n')
            finally:
                if self.log_time:
                    stopper_event.set()
                    daemon.join()
                if self.log_files:
                    sys.stdout = sys.__stdout__
                    logging_file.close()
                if self.save_results:
                    saving_file = open(set_id + '-res', 'w')
                    saving_file.write(result)
                    saving_file.close()

    def process_ids(self, set_ids, results_file = None):	
        """
        Process ids using QhX function
        - setids : ids to process
        - save_results : filename of results file
        """
        self.results_ = Queue()
        self.set_ids_ = Queue()
        if results_file is not None:
            self.save_all_results_ = True
        else:
            self.save_all_results_ = False

        for id in set_ids:
            self.set_ids_.put(id)
        
        processes = [Process(target = self.process_wrapper) for i in range(self.num_workers)]
        
        for p in processes:
          p.start()
        for p in processes:
          p.join()

        if results_file is not None:
                try:
                    with open(results_file, 'w') as f:
                        while not self.results_.empty():
                            try:
                                result = self.results_.get()
                            except Exception as e:
                                break
                            f.write(result + '\n')
                except Exception as e:
                    print('Error while saving: \n'+ str(e))
