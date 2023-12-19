from QhX.detection import process1

import os
import threading
import time
from multiprocessing import Pool
from datetime import datetime

def background_log(set_id, e : threading.Event, delta_seconds : float):
    total_time = 0
    cur_time = datetime.now()
    print(f'Starting time for ID {set_id} : {cur_time}')
    while e.wait(delta_seconds) == False:
        total_time += delta_seconds
        print(f'Processing {set_id}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')
    cur_time = datetime.now()
    print(f'End time for ID {set_id} : {cur_time}\n')

def process1_wrapper(set_id, data_manager, delta_seconds : float, log_time : bool):
    e = None
    if log_time:
        e = threading.Event()
        daemon = threading.Thread(target = background_log, args = (set_id, e, delta_seconds))
        daemon.start()
    time.sleep(20)
    res = None
    #res = process1(data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, include_errors=False)
    #print(data_manager)
    if log_time:
        e.set()
    return res

TIMEOUT = 1000.0

def process_ids(setids, data_manager, num_workers = 4, delta_seconds = 14.0, log_time = True, save_results = None, chunk_size = 5):	

    pool = Pool(processes = num_workers)
    
    results = pool.starmap(process1_wrapper, [(setids[i], data_manager, delta_seconds, log_time) for i in range(len(setids))], chunksize = chunk_size)
    for result in results:
        print(result)
    
    if save_results is not None:
        try:
            with open(save_results, 'w') as f:
                for result in results:
                    f.write(result + '\n')
        except Exception as e:
            print('Error while saving: \n'+ str(e))

