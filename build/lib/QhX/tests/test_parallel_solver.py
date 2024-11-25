import os
import gc
import threading
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import unittest
from QhX.parallelization_solver import ParallelSolver
from QhX import DataManagerDynamical, process1_new_dyn

class TestParallelSolver(unittest.TestCase):
    def setUp(self):
        print("Running setUp...")  # Debugging print
        agn_dc_mapping = {
            'column_mapping': {'flux': 'psMag', 'time': 'mjd', 'band': 'filter'},
            'group_by_key': 'objectId',
            'filter_mapping': {0: 0, 1: 1, 2: 2, 3: 3}
        }
        self.data_manager = DataManagerDynamical(
            column_mapping=agn_dc_mapping['column_mapping'],
            group_by_key=agn_dc_mapping['group_by_key'],
            filter_mapping=agn_dc_mapping['filter_mapping']
        )
        self.synthetic_data = self.create_synthetic_data()
        self.synthetic_data_file = 'synthetic_test_data.parquet'
        self.synthetic_data.to_parquet(self.synthetic_data_file)
        self.data_manager.load_data(self.synthetic_data_file)
        self.data_manager.group_data()
        self.solver = ParallelSolver(
            delta_seconds=12.0,
            num_workers=2,
            data_manager=self.data_manager,
            log_time=True,
            log_files=False,
            save_results=True,
            process_function=process1_new_dyn,
            parallel_arithmetic=True,
            ntau=80,
            ngrid=100,
            provided_minfq=500,
            provided_maxfq=10,
            mode='dynamical'
        )
        self.setids = ['1']

    def create_synthetic_data(self):
        np.random.seed(42)
        object_id = '1'
        num_measurements = 50
        mjd_values = np.linspace(50000, 50500, num=num_measurements)
        psMag_values = np.random.normal(loc=20.0, scale=0.5, size=num_measurements)
        psMagErr_values = np.random.uniform(0.02, 0.1, size=num_measurements)
        filter_values = np.tile([0, 1, 2, 3], int(num_measurements / 4) + 1)[:num_measurements]
        data = {
            'objectId': [object_id] * num_measurements,
            'mjd': mjd_values,
            'psMag': psMag_values,
            'psMagErr': psMagErr_values,
            'filter': filter_values
        }
        return pd.DataFrame(data)

    def test_parallel_solver_process_and_merge(self):
        print("Running test_parallel_solver_process_and_merge...")  # Debugging print
        try:
            self.solver.process_ids(set_ids=self.setids, results_file='1-reslut.csv')
            print("Solver processed IDs successfully.")  # Debugging print
        except Exception as e:
            self.fail(f"Error processing/saving data: {e}")

        if not os.path.exists('1-reslut.csv'):
            self.fail("Processed result file missing or cannot be read")

        # Read the processing result and check structure
        actual_df = pd.read_csv('1-reslut.csv')
        print("Actual DataFrame read successfully.")  # Debugging print

        # Check that the DataFrame has the expected columns
        expected_columns = [
            "ID", "Sampling_1", "Sampling_2", "Common period (Band1 & Band2)",
            "Upper error bound", "Lower error bound", "Significance", "Band1-Band2"
        ]
        self.assertListEqual(list(actual_df.columns), expected_columns)

        # Optional: Check if numerical values fall within expected ranges
        self.assertTrue((actual_df["Sampling_1"] > 0).all())
        self.assertTrue((actual_df["Sampling_2"] > 0).all())
        self.assertTrue((actual_df["Significance"].fillna(0) >= 0).all())  # Allow NaN, otherwise check non-negative

        # Print the result DataFrame for inspection
        print("\nContents of 1-reslut.csv:")
        print(actual_df.to_string(index=False))  # Print DataFrame without row indices
    

    def tearDown(self):
        print("Cleaning up...")  # Debugging print
        if hasattr(self.solver, 'executor') and self.solver.executor:
            try:
                self.solver.executor.shutdown(wait=True)
                print("Executor shutdown successfully.")  # Debugging print
            except Exception as e:
                print(f"Error during executor shutdown: {e}")
        if os.path.isfile(self.synthetic_data_file):
            os.remove(self.synthetic_data_file)
        if os.path.isfile('1-reslut.csv'):
            os.remove('1-reslut.csv')
        gc.collect()
        for thread in threading.enumerate():
            if thread.name != "MainThread":
                print(f"Thread {thread.name} is still active.")  # Debugging print

if __name__ == '__main__':
    unittest.main()
