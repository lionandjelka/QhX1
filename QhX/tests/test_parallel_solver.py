import unittest
from unittest.mock import Mock
import os
from QhX.parallelization_solver import *

class TestUnitParallelSolver(unittest.TestCase):
    def setUp(self):
        # Create mock function to return string values from header
        mock_function = Mock()
        args = {'return_value': [dict([(i, x) for i, x in enumerate(HEADER.split(','))])]}
        mock_function.configure_mock(**args)
	
        # Two mock setids
        self.mock_setids = ['0','1']
        # One line of mock result
        mock_result = ','.join(mock_function()[0].values())
        
        # Instance of ParallelSolver with file loggings
        self.solver = ParallelSolver(process_function=mock_function, log_files=True)
        
        # Expected result, to have a header and all outputs
        self.expected_result = HEADER + '\n'.join([mock_result for setid in self.mock_setids]) + '\n'
        
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
        self.assertIsNotNone(process_result, "Merged file missing or cannot be read")
        self.assertEqual(self.expected_result,process_result, "Merged result does not match expected result")

if __name__ == '__main__':
    unittest.main()

