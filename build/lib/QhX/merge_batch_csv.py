# pylint: disable=R0801
"""
This module provides functionality to merge CSV files named 'result.csv' found in directories 
with specific batch sizes (e.g., folders ending in 'sz100', 'sz200'). The merged result is saved 
to a specified output file.

"""

import os
import sys
import pandas as pd

DEFAULT_SIZES = [100, 200]
DEFAULT_MERGED_FILENAME = 'merged_result.csv'

def check_endings(root, all_sizes):
    """
    Checks if a directory path ends with any of the specified batch size suffixes.

    Parameters:
        root (str): The directory path to check.
        all_sizes (list of int): The list of batch sizes to look for in directory endings.

    Returns:
        bool: True if the directory ends with one of the specified sizes, False otherwise.
    """
    for size in all_sizes:
        if root.endswith('sz' + str(size)):
            return True
    return False

def merge_batch_csv(all_sizes=None, directory=".", output_file=DEFAULT_MERGED_FILENAME):
    """
    Merges CSV files named 'result.csv' found in directories ending with szX, where X is a number 
    from all_sizes, into a single CSV file.

    Parameters:
        all_sizes (list of int, optional): List of all batch sizes whose folders we need to merge.
                                           Defaults to [100, 200].
        directory (str): The root directory to search for CSV files. Defaults to the current directory.
        output_file (str): The name of the output file where the merged results will be saved. 
                           Defaults to 'merged_result.csv'.

    Returns:
        int: The number of files successfully merged.
    """
    if all_sizes is None:
        all_sizes = DEFAULT_SIZES

    all_dfs = []  # List to store DataFrames
    cnt = 0  # Counter for files

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename == "result.csv" and check_endings(root, all_sizes):
                filepath = os.path.join(root, filename)
                df = pd.read_csv(filepath)
                all_dfs.append(df)
                cnt += 1

    # Concatenate all found DataFrames
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        merged_df.to_csv(output_file, index=False)
        print(f"All CSV files merged into '{output_file}' successfully! Counted {cnt} files.")
    else:
        print("No suitable CSV files found to merge.")

    return cnt

if __name__ == "__main__":
    # Initialize the all_sizes list from command-line arguments
    all_sizes = []
    for arg in sys.argv[1:]:
        try:
            all_sizes.append(int(arg))
        except ValueError as e:
            print(f'Warning: Skipping invalid argument "{arg}" - {e}')

    # Use default sizes if no valid sizes were provided
    if not all_sizes:
        all_sizes = DEFAULT_SIZES
    
    # Call the merge function
    merge_batch_csv(all_sizes)
