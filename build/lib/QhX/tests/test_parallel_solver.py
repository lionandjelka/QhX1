import unittest
from unittest.mock import Mock
import os
from QhX.parallelization_solver import *

# Define a fake function which returns setids given as all column values
def function_fake(*args, **kwargs):
    setid = 'fake'
    if len(args) > 1:
        setid = args[1]
    return [dict([(i, setid) for i, x in enumerate(HEADER.split(','))])]

class TestUnitParallelSolver(unittest.TestCase):
    def setUp(self):
        # Mock setids
        self.mock_setids = ['0','1','2','3']
        
        # Instance of ParallelSolver with file loggings
        self.solver = ParallelSolver(process_function=function_fake, log_files=True)
        
        # Expected result, to have a header and all lines with fake function results
        self.expected_result = HEADER +\
        '\n'.join([','.join(
           function_fake(None, setid)[0].values())
         for setid in self.mock_setids]) + '\n'
        
    def test_parallel_solver_process_and_merge(self):
        # Run the process ids
        self.solver.process_ids(set_ids=self.mock_setids, results_file='mock_results_file.csv')
        
        # Read the processing result from file
        process_result = None
        with open('mock_results_file.csv') as f:
            process_result = f.read()
            
        # Assert the presence of log files, process result data and its corectness
        for setid in self.mock_setids:
            self.assertTrue(os.path.isfile(setid), "Log file missing")
            print(f'\n\nLog file for {setid} created.',end='')

        self.assertIsNotNone(process_result, "Merged file missing or cannot be read")
        print('\n\nMerged results file present.')        
        
        # Assert sorted equality because working in different processes may lead to different set ID order in result file
        self.assertEqual(sorted(self.expected_result), sorted(process_result), "Merged result does not match expected result")
        print('\nMerged result file content correct.')

if __name__ == '__main__':
    unittest.main()

