from QhX.detection import process1

import os
import threading
import time
from multiprocessing import Pool
from datetime import datetime
from concurrent import futures

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
    print(f'Starting time for ID {set_id} : {cur_time}')
    while e.wait(delta_seconds) == False:
        total_time += delta_seconds
        print(f'Processing {set_id}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')
    cur_time = datetime.now()
    print(f'End time for ID {set_id} : {cur_time}\n')

def process1_wrapper(args):
    """
    Wrapper for processing function

    - Gets set ID, data manager reference, seconds for logging & logging flag
    - Starts background logging thread if required
    - Processes data if data manager exists
    """
    set_id, data_manager, delta_seconds, log_time = args 
    e = None
    if log_time:
        e = threading.Event()
        daemon = threading.Thread(target = background_log, args = (set_id, e, delta_seconds))
        daemon.start()
    time.sleep(10)
    res = None
    if data_manager is not None:
        res = process1(data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, include_errors=False)

    if log_time:
        e.set()
    return res

TIMEOUT = 1000.0

def process_ids(setids, data_manager, num_workers = 4, delta_seconds = 14.0, log_time = True, save_results = None, chunk_size = 5):	
    """
    Process ids using QhX function
    - setids : ids to process
    - data_manager : data manager provided
    - num_workers : maximum number of processes at one time
    - delta_seconds : time period for process logging
    - log_time : flag whether to log time
    - save_results : filename of results file
    - chunk_size : how many IDs to assign to one worker at once (use for larger files)
    """
    results = []
    
    with futures.ProcessPoolExecutor(max_workers = num_workers) as exe:
        results = exe.map(process1_wrapper, [(setids[i], data_manager, delta_seconds, log_time) for i in range(len(setids))])

        if save_results is not None:
            try:
                with open(save_results, 'w') as f:
                    for result in results:
                        f.write(result + '\n')
            except Exception as e:
                print('Error while saving: \n'+ str(e))

