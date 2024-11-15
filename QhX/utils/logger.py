"""
Author:
-------
Momcilo Tosic
Astroinformatics student
Faculty of Mathematics, University of Belgrade

Description:
------------
This module contains the Logger class, which is used to manage logging of an active
process that processes an object with a unique ID. The Logger can be used in conjunction
with the parallelization_solver module to log information to a file or periodically log
timestamps in a separate thread.

"""

import os
import sys
import threading
from datetime import datetime

# Default number of seconds to pass between time loggings
DEFAULT_LOG_PERIOD = 10

class Logger:
    """
    A class to manage logging an active process while processing an object with a unique ID. 
    This class is used by the parallelization_solver module.

    Attributes:
        log_files (bool): Flag indicating if output should be redirected to a log file.
        log_time (bool): Flag indicating if time logging should occur at regular intervals.
        delta_seconds (float): Delay between individual time log entries, in seconds.
        logging_file (file object): File object for logging, if log_files is True.
        stopper_event (threading.Event): Event to signal the logging thread to stop.
        logging_thread (threading.Thread): Thread instance for background logging.
        started (bool): Flag indicating whether the logging has started.
    """

    def __init__(self, log_files: bool, log_time: bool, delta_seconds=DEFAULT_LOG_PERIOD):
        """
        Initializes the Logger instance with specified logging configuration.

        Parameters:
            log_files (bool): If True, logs output to a file.
            log_time (bool): If True, logs time at regular intervals.
            delta_seconds (float): Interval between each time log entry.
        """
        self.delta_seconds = delta_seconds
        self.log_time = log_time
        self.log_files = log_files
        self.started = False
        self.logging_file = None            # Initialize logging_file here
        self.stopper_event = None           # Initialize stopper_event here
        self.logging_thread = None          # Initialize logging_thread here

    @staticmethod
    def background_log(set_id: str, e: threading.Event, delta_seconds: float):
        """
        Background thread function for logging the process time at regular intervals.

        Parameters:
            set_id (str): Identifier for the dataset being processed.
            e (threading.Event): Event to signal the thread to exit.
            delta_seconds (float): Time interval for each logging entry, in seconds.
        """
        # Log starting time
        total_time = 0
        start_time = datetime.now()
        print(f'Starting time for ID {set_id} : {start_time}\n')

        while not e.wait(delta_seconds):
            # Log elapsed time
            total_time += delta_seconds
            print(f'Processing {set_id}\nPID {os.getpid()}\nDuration: {total_time/delta_seconds} ticks\n{delta_seconds} seconds each\nTime so far {total_time}s\n')

        # Log finish time
        end_time = datetime.now()
        print(f'End time for ID {set_id} : {end_time}\nTotal time : {end_time - start_time}\n')

    def start(self, set_id: str):
        """
        Starts the logging process by initiating a logging thread and optionally redirecting output to a file.

        Parameters:
            set_id (str): Identifier for the dataset/object being processed.
        """
        # Open output log file and redirect output if log_files is enabled
        if self.log_files:
            self.logging_file = open(set_id, 'w')
            sys.stdout = self.logging_file

        # Start background logging if log_time is enabled
        if self.log_time:
            # Create an event to stop logging
            self.stopper_event = threading.Event()
            # Instantiate the background logging thread
            self.logging_thread = threading.Thread(target=Logger.background_log, args=(set_id, self.stopper_event, self.delta_seconds))
            # Start the thread and mark the logger as started
            self.started = True
            self.logging_thread.start()

    def stop(self):
        """
        Stops the logging process by terminating the logging thread and closing the log file if open.

        Raises:
            Exception: If the logger has not been started before calling stop.
        """
        if not self.started:
            raise Exception('Logger has not been started.')

        # Stop the background logging thread if it was started
        if self.log_time and self.stopper_event:
            self.stopper_event.set()
            self.logging_thread.join()
        
        # Close the logging file and reset stdout if log_files is enabled
        if self.log_files and self.logging_file:
            sys.stdout = sys.__stdout__
            self.logging_file.close()

        # Reset the started flag
        self.started = False
