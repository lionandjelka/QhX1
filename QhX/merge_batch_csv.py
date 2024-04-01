# File: QhX/merge_csv_results.py

import os
import pandas as pd
import sys

DEFAULT_SIZES = [100, 200]
DEFAULT_MERGED_FILENAME = 'merged_result.csv'

def check_endings(root, all_sizes):
    for size in all_sizes:
        if root.endswith('sz' + str(size)):
            return True
    return False

def merge_batch_csv(all_sizes=DEFAULT_SIZES, directory=".", output_file=DEFAULT_MERGED_FILENAME):
    """
    Merges CSV files named 'result.csv' found in directories ending with szX, where X is a number from all_sizes
    into a single CSV file.

    Parameters:
        all_sizes (list of int): The list of all batch sizes whose folders we need to merge
        directory (str): The root directory to search for CSV files. Defaults to the current directory.
        output_file (str): The name of the output file where the merged results will be saved. Defaults to 'merged_result.csv'.

    Returns:
        int: The number of files successfully merged.
    """
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
    # Example usage: python -m QhX.merge_csv_results
    all_sizes = []
    try:
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                all_sizes.append(int(sys.argv[i]))
    except Exception as e:
        print('Args parsing error ' + str(e))

    # Default all_sizes in case of no/invalid args
    if not all_sizes:
        all_sizes = DEFAULT_SIZES
    merge_batch_csv(all_sizes) # Call merge function
    
