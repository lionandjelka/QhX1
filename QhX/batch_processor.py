"""
This module is designed for processing large datasets in parallel batches within the QhX package.
It facilitates the batch processing of datasets using multiple workers to speed up the analysis.

Functions:
    process_batches(batch_size, num_workers=25, start_i=0): Main function to process data in specified batch sizes using parallel workers.

Example usage as a script:
    $ python batch_processor.py 100 25 0
    This command will process the dataset in batches of 100, using 25 parallel workers, starting from index 0.
"""

from QhX.parallelization_solver import ParallelSolver  # Import the ParallelSolver class
from QhX.data_manager import DataManager  # Import the DataManager class for handling datasets
import sys  # System-specific parameters and functions
import os  # Miscellaneous operating system interfaces

def process_batches(batch_size, num_workers=25, start_i=0):
    """
    Processes data in batches using parallel processing.

    Args:
        batch_size (int): The number of data points to process in each batch.
        num_workers (int, optional): The number of parallel workers to use for processing. Defaults to 25.
        start_i (int, optional): The index from which to start processing the dataset. Defaults to 0.
    
    This function loads a dataset, groups the data as necessary, and then processes it in batches. 
    Each batch is processed in a new directory to keep the results organized.
    """

    # Initial logging to indicate batch processing start
    print(f'Starting testing in batches of size {batch_size}')
    
    # Load and prepare the dataset using DataManager
    data_manager = DataManager()
    fs_df = data_manager.load_fs_df('ForcedSourceTable.parquet')  # Load the dataset
    fs_gp = data_manager.group_fs_df()  # Optional grouping step, specific to dataset structure
    fs_df = data_manager.fs_df  # Access the DataFrame after any preprocessing

    # Log the DataFrame to console (optional)
    print(fs_df)

    # Retrieve unique identifiers from the dataset for batch processing
    setids = fs_df.objectId.unique().tolist()
    j = 0  # Counter for batch directories

    # Initialize the ParallelSolver with specific parameters
    solver = ParallelSolver(data_manager=data_manager, delta_seconds=15.0, num_workers=num_workers, log_files=True,
                            provided_minfq=500, provided_maxfq=10, ngrid=100, ntau=80)
    print(f'Tried num of workers {num_workers}')
    
    # Process each batch
    for i in range(start_i, len(setids), batch_size):
        try:
            # Attempt to create a directory for the current batch
            os.mkdir(f'batch{j}sz{batch_size}')
        except Exception as e:
            print(f'Error\n{e}\nfor batch {j}\nMoving to next batch\n')
            j += 1
            continue

        print(f'Batch {j}')  # Log the current batch being processed
        os.chdir(f'batch{j}sz{batch_size}')  # Change to the batch directory
        solver.process_ids(setids[i:min(i+batch_size, len(setids))], 'result.csv')  # Process the IDs in the batch
        j += 1  # Increment the batch counter
        print(os.getcwd())  # Log the current working directory
        os.chdir('..')  # Change back to the parent directory

if __name__ == "__main__":
    # Allow the module to be executed as a script with command-line arguments
    try:
        batch_size = int(sys.argv[1])  # Batch size is a required argument
        num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 25  # Optional num_workers argument
        start_i = int(sys.argv[3]) if len(sys.argv) > 3 else 0  # Optional start_i argument
    except Exception as e:
        print(f'Error: {e}')
        sys.exit("Invalid Arguments")

    process_batches(batch_size, num_workers, start_i)  # Call the main processing function with the arguments
