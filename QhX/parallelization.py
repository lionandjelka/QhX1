# parametrize

import os

from tqdm.contrib.concurrent import process_map  # or import tqdm for tqdm
import threading

from time import sleep

DELTA_SECONDS = 15.0
NUM_NODES = 2
semaphore = threading.Semaphore(NUM_NODES)

def background_logs(set_id, e : threading.Event):
  total_time = 0
  while e.wait(DELTA_SECONDS) == False:
    total_time += DELTA_SECONDS
    print(f'Processing {set_id}\nDuration: {total_time/DELTA_SECONDS} ticks\n{DELTA_SECONDS} seconds each\nTime so far {total_time}s\n')

def process1_wrapper(set_id):
    semaphore.acquire()
    # No need for print, tqdm will handle the progress display
    e = threading.Event()
    daemon = threading.Thread(target = background_logs, args = (set_id, e))
    daemon.start()
    res = process1(data_manager, set_id, ntau=80, ngrid=100, provided_minfq=2000, provided_maxfq=10, include_errors=False)
    e.set()
    semaphore.release()
    return res

setids = ['1384177', '1384184']

process1_results = process_map(process1_wrapper, setids)

# Results are already in process1_results, you can process or print them as needed
for result in process1_results:
    print(result)

