import unittest
import time
from QhX.utils.logger import *

class TestUnitLogger(unittest.TestCase):
        
    def test_logger_both_flags(self):
        # Create instace of logger
        logger = Logger(True, True, 1)
        setid = 'TEST'
        
        logger.start(setid)
        print('REDIRECT')
        time.sleep(3) # should log 2 as total time at some point
        logger.stop()
            
        # Assert the presence of log file, and its contents
        self.assertTrue(os.path.isfile(setid), "Log file missing")
        
        with open(setid) as log_file:
            res = log_file.read()
            self.assertIn('2', res)
            self.assertIn('REDIRECT', res)

if __name__ == '__main__':
    unittest.main()

