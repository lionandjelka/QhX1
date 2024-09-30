# File: QhX/merge_csv_results.py

import os
import pandas as pd

def merge_csv_results(directory="/Users/andjelka/Downloads/qhx-batch", output_file="merged_result.csv"):
    """
    Merges CSV files named 'result.csv' found in directories ending with 'sz100' or 'sz200'
    into a single CSV file.

    Parameters:
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
            if filename == "result.csv" and (root.endswith("sz100") or root.endswith("sz200")):
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
    merge_csv_results()
