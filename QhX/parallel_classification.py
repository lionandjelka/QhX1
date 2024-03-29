import pandas as pd
from QhX.output_parallel import classify_periods, classify_period

def process_csv_in_chunks(csv_file_path, chunk_size=10000, output_file_path='classified_periods.csv'):
    """
    Processes a CSV file in chunks, classifying periods for each chunk.

    Reads the specified CSV file in chunks of a specified size, applies
    classification to each chunk using the `classify_periods` function, further
    classifies each period within the chunk using `classify_period`, and
    compiles the results into a single DataFrame. The final DataFrame is then
    saved to a new CSV file.

    Parameters
    ----------
    csv_file_path : str
        The path to the CSV file to be processed.
    chunk_size : int, optional
        The number of rows per chunk to read from the CSV. Defaults to 10000.
    output_file_path : str, optional
        Path where the fully processed and classified CSV file will be saved.
        Defaults to 'classified_periods.csv'.

    Returns
    -------
    None
        This function does not return a value. It saves the processed and classified
        data directly to a CSV file specified by `output_file_path`.

    Example
    -------
    Below is an example of how to use the `process_csv_in_chunks` function:

    >>> csv_file_path = 'path/to/your/large_csv_file.csv'
    >>> output_file_path = 'path/to/save/classified_periods.csv'
    >>> process_csv_in_chunks(csv_file_path, chunk_size=10000, output_file_path=output_file_path)
    Processed and classified data saved to path/to/save/classified_periods.csv
    """
    final_processed_df = pd.DataFrame()

    for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
        classified_df = classify_periods(chunk.to_dict('records'))
        classified_df['classification'] = classified_df.apply(classify_period, axis=1)
        final_processed_df = pd.concat([final_processed_df, classified_df], ignore_index=True)

    final_processed_df.to_csv(output_file_path, index=False)
    print(f"Processed and classified data saved to {output_file_path}")
