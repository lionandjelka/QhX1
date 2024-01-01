from QhX.detection import process1

import sys
import threading
import time
import os
from multiprocessing import Pool
from datetime import datetime
from concurrent import futures

DEFAULT_NUM_WORKERS = 4
DEFAULT_CHUNK_SIZE = 5
DEFAULT_LOG_PERIOD = 10 # seconds

def background_log(set_id, e : threading.Event, delta_seconds : float):
    """
    Function for time logging
    - Logs approx. process time every delta_seconds
    - End when e is triggered
    - Logs start & end system time
    Run in background thread for QhX processes
    """
    total_time = 0
    cur_time = datetime.now()
    print(f'Starting time for ID {set_id} : {cur_time}\n')
    
    while e.wait(delta_seconds) == False:
        total_time += delta_seconds
        print(f'Processing {set_id}\nPID {os.getpid()}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')
    
    cur_time = datetime.now()
    print(f'End time for ID {set_id} : {cur_time}\n')

def process_wrapper(args):
    """
    Wrapper for processing function

    - Gets processing function (data_manager, set_id, ntau, ngrid, provided_minfq, provided_maxfq, include_errors),
    - set ID, data manager reference,
    - seconds for periodic logging, whether to log flag & redirect to files flag
    - Starts background logging thread if required
    - Processes data if data manager exists
    """
    process_function, set_id, data_manager, delta_seconds, log_time, log_files = args
    
    stopper_event = None
    log_txt_file = None
    res = None

    if log_files:
        logging_file = open(set_id, 'w')
        sys.stdout = logging_file
    if log_time:
        stopper_event = threading.Event()
        daemon = threading.Thread(target = background_log, args = (set_id, stopper_event, delta_seconds))
        daemon.start()

    try:
        res = process_function(data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, include_errors=False)
    except Exception as e:
        print('Error processing data : ' + str(e))
    finally:
        
        if log_time:
            stopper_event.set()
            daemon.join()
        if log_files:
            logging_file.close()

    return res

def process_ids(setids, data_manager, 
                num_workers = DEFAULT_NUM_WORKERS, delta_seconds = DEFAULT_LOG_PERIOD, 
                log_time = True, save_results = None, 
                log_files = False, chunk_size = DEFAULT_CHUNK_SIZE, tasks_per_child = 1000,
                process_function = process1):	
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
    results = []
    
    with futures.ProcessPoolExecutor(max_workers = num_workers,maxtasksperchild=1000) as exe:
        results = exe.map(process_wrapper, [(process_function, setids[i], data_manager, delta_seconds, log_time, log_files) for i in range(len(setids))])

        if save_results is not None:
            try:
                with open(save_results, 'w') as f:
                    for result in results:
                        f.write(result + '\n')
            except Exception as e:
                print('Error while saving: \n'+ str(e))

