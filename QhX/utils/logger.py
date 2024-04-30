"""
Author:
-------
Momcilo Tosic
Astroinformatics student
Faculty of Mathematics, University of Belgrade
"""
import os
import sys
import threading
from datetime import datetime

# Default number of seconds to pass between time loggings
DEFAULT_LOG_PERIOD = 10

class Logger:
    """
    A class to manage logging an active process processing an object with an ID. Used by the parallelization_solver module.
    
    Attributes:
        log_files (bool): a flag whether io redirect print output into a file
        log_time (bool): a flag whether to log time every few seconds
        delta_seconds (float): delay between individual time log entries
    """
    def __init__(self, log_files : bool, log_time : bool, delta_seconds = DEFAULT_LOG_PERIOD):
        """ Initialize the (not yet started) Logger with the specified configuration """
        self.delta_seconds = delta_seconds
        self.log_time = log_time
        self.log_files = log_files
        self.started = False

    @staticmethod
    def background_log(set_id, e : threading.Event, delta_seconds : float):
        """
        Background thread body for logging the process time at regular intervals.

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
        
    def start(self, set_id):
        """
        Starts a logging thread and opens a logging file, redirecting output to it.
        
        Parameters:
            set_id (str): string of set/object name (ID)
        """
        self.logging_file = None
        
        # Open output log file and redirect output
        if self.log_files:
            self.logging_file = open(set_id, 'w')
            sys.stdout = self.logging_file

        # Begin logging time if flag set
        if self.log_time:
            # Create an event used as trigger to stop logging
            self.stopper_event = threading.Event()
            # Create an instance of the background logging thread
            self.logging_thread = threading.Thread(target = Logger.background_log, args = (set_id, self.stopper_event, self.delta_seconds))
            # Start the thread and set flag
            self.started = True
            self.logging_thread.start()
        
    def stop(self):
        """ Stops the logging waiting for the thread to finish. Throws if logger has not started. """
        if not self.started:
            raise Exception('Not started.')
            
        # Stop background thread, close output file and write result to individual file if relevant flags are set
        if self.log_time:
            self.stopper_event.set()
            self.logging_thread.join()
        if self.log_files:
            sys.stdout = sys.__stdout__
            self.logging_file.close()
        self.started = False
        
