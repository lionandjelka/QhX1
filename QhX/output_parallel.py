import pandas as pd
import numpy as np
import math




def flatten_detected_periods(detected_periods):
    """Flatten the nested list of dictionaries of detected periods, skipping records with any NaN values."""
    flat_list = []
    for record in detected_periods:
        # Ensure all expected keys are present
        complete_record = {key: record.get(key, np.nan) for key in ['ID', 'Sampling_1', 'Sampling_2', 'Common period (Band1 & Band1)', 'Upper error bound', 'Lower error bound', 'Significance', 'Band1-Band2']}
        
        # Check if any value in the complete_record is NaN
        if all(value == value for value in complete_record.values()):  # NaN does not equal itself
            flat_list.append(complete_record)
        # If any value is NaN, this record will be skipped
    return flat_list

def calculate_iou(radius1, radius2, distance):
        """
        Calculates the Intersection over Union (IoU) for two circles given their radii and the distance between their centers.

        Parameters:
        -----------
        radius1 (float): Radius of the first circle.
        radius2 (float): Radius of the second circle.
        distance (float): Distance between the centers of the two circles.

        Returns:
        --------
        float: IoU value.
        """
        if distance > (radius1 + radius2):
            return 0
        elif distance <= abs(radius1 - radius2):
            return 1
        else:
            area1 = math.pi * radius1**2
            area2 = math.pi * radius2**2
            d = distance

            # Calculate intersection area
            part1 = math.acos((radius1**2 + d**2 - radius2**2) / (2 * radius1 * d))
            part2 = math.acos((radius2**2 + d**2 - radius1**2) / (2 * radius2 * d))
            intersection = part1 * radius1**2 + part2 * radius2**2 - 0.5 * (radius1**2 * math.sin(2 * part1) + radius2**2 * math.sin(2 * part2))

            union = area1 + area2 - intersection
            return intersection / union

    # Initialize list to hold DataFrame rows


def classify_periods(detected_periods):
    """
    Classifies periods based on IoU and other metrics, adjusted to work with specified column names.
    Assumes 'Band1' and 'Band2' columns are already present in the DataFrame.
    """
    # Flatten the list of dictionaries
    flat_list = flatten_detected_periods(detected_periods)

    # Convert flattened list to DataFrame
    df = pd.DataFrame(flat_list)
    # Check if 'Band1' and 'Band2' columns do not exist before attempting to split 'Band1-Band2'
    if 'Band1' not in df.columns or 'Band2' not in df.columns:
        df[['Band1', 'Band2']] = df['Band1-Band2'].str.split('-', expand=True)

    # Optionally, remove 'Band1-Band2' column if no longer needed
    df.drop(columns=['Band1-Band2'], inplace=True)
    
    rows_list = []
    for name in df['ID'].unique():
        quasar_data = df[df['ID'] == name]
        for i in range(len(quasar_data)):
            for j in range(i + 1, len(quasar_data)):
                row_i = quasar_data.iloc[i]
                row_j = quasar_data.iloc[j]
                iou, period_diff = np.nan, np.nan    
                # Check if necessary values are not NaN before calculating IoU and period difference
                if not pd.isna(row_i['Common period (Band1 & Band1)']) and not pd.isna(row_j['Common period (Band1 & Band1)']) and not pd.isna(row_i['Upper error bound']) and not pd.isna(row_i['Lower error bound']) and not pd.isna(row_j['Upper error bound']) and not pd.isna(row_j['Lower error bound']):
                    period_diff = abs(row_i['Common period (Band1 & Band1)'] - row_j['Common period (Band1 & Band1)']) / max(row_i['Common period (Band1 & Band1)'], 1e-7)  # Avoid division by zero
                    if period_diff <= 0.1:
                        radius_i = (row_i['Upper error bound'] + row_i['Lower error bound']) / 2
                        radius_j = (row_j['Upper error bound'] + row_j['Lower error bound']) / 2
                        distance = abs(row_i['Common period (Band1 & Band1)'] - row_j['Common period (Band1 & Band1)'])
                        iou = calculate_iou(radius_i, radius_j, distance)

                rows_list.append({
                    'ID': name,
                    'm3': row_i['Common period (Band1 & Band1)'],  # Adjusted to use 'Common period (Band1 & Band1)' directly
                    'm4': row_i['Lower error bound'],  
                    'm5': row_i['Upper error bound'],  
                    'm6': row_i['Significance'],  
                    'm7_1': row_i['Band1'],  
                    'm7_2': row_j['Band2'],  
                    'period_diff': period_diff,
                    'iou': iou
                })

    # Convert the list of processed rows into a DataFrame
    output_df = pd.DataFrame(rows_list)
    return output_df

def classify_period(row):
    """
    Classify the detected period as 'reliable', 'medium reliable', 'poor', or 'NAN'
    based on the significance of the detected period, the relative lower and upper errors,
    and the IoU of the error circles provided in function classify_periods.

    Parameters:
    -----------
    row (pd.Series): A row from the DataFrame containing detected period data.

    Returns:
    --------
    str: Classification of the period ('reliable', 'medium reliable', 'poor', 'NAN').
    """
    if pd.isna(row['m3']) or pd.isna(row['m4']) or pd.isna(row['m5']) or pd.isna(row['m6']) or pd.isna(row['iou']) or row['m3'] == 0:
        return 'NAN'
    
    rel_error_lower = abs(row['m4']) / row['m3'] if row['m4'] >= 0 else float('inf')
    rel_error_upper = abs(row['m5']) / row['m3'] if row['m5'] >= 0 else float('inf')
    consistent_period = row['period_diff'] < 0.1
    
    if row['m6'] >= 0.99 and rel_error_lower <= 0.1 and rel_error_upper <= 0.1 and row['iou'] >= 0.99 and consistent_period:
        return 'reliable'
    elif 0.5 <= row['m6'] < 0.99 and 0.1 < rel_error_lower <= 0.3 and 0.1 < rel_error_upper <= 0.3 and 0.8 <= row['iou'] < 0.99 and consistent_period:
        return 'medium reliable'
    else:
        return 'poor'

def aggregate_classifications(group):
    """
    Aggregates individual period classifications within a group, determining a final
    classification for each unique object ID based on the individual classifications
    of its periods.

    Parameters:
    -----------
    group : pd.DataFrame
        A subset of the original DataFrame grouped by object ID, containing all period
        detections and their individual classifications for that ID.

    Returns:
    --------
    pd.DataFrame
        The input DataFrame with an additional column 'final_classification' representing
        the aggregated classification result for each object ID.
    """
    if 'individual_classification' not in group.columns:
        group['individual_classification'] = group.apply(classify_period, axis=1)
    
    if group['individual_classification'].nunique() == 1:
        group['final_classification'] = group['individual_classification'].iloc[0]
    elif 'reliable' in group['individual_classification'].values:
        group['final_classification'] = 'inconsistent but some reliable'
    else:
        group['final_classification'] = 'inconsistent and poor'
    
    return group

def group_periods(data):
    """
    The process of classifying periods for all detected periods in a dataset.
    It applies individual classifications and then aggregates these classifications for each
    object ID.

    Parameters:
    -----------
    data : pd.DataFrame
        The dataset containing detected periods along with necessary metrics (significance,
        relative errors, IoU) for classification.

    Returns:
    --------
    pd.DataFrame
        The input DataFrame enhanced with an 'individual_classification' column for each period
        and a 'final_classification' for each object ID.
    """
    grouped = data.groupby('ID', as_index=False).apply(aggregate_classifications).reset_index(drop=True)
    return grouped

def process_chunk(chunk):
    """
    Processes a chunk of the dataset by applying period classification logic. This function
    is intended for use in a chunk-wise processing of large datasets that do not fit into
    memory entirely.

    Parameters:
    -----------
    chunk : pd.DataFrame
        A chunk of the original large dataset, containing a subset of the detected periods.

    Returns:
    --------
    pd.DataFrame
        The chunk with period classifications applied, ready for further aggregation.
    """
    return group_periods(chunk)

def aggregate_statistics(classified_data):
    """
    Aggregates statistics for object IDs classified as 'reliable' or 'medium reliable', calculating
    mean values for period, relative errors, significance, and IoU.

    Parameters:
    -----------
    classified_data : pd.DataFrame
        The dataset with 'final_classification' determined for each object ID.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing aggregated statistics for each 'reliable' and 'medium reliable'
        classified object ID.
    """
    # Filter data for relevant classifications
    filtered_data = classified_data[classified_data['final_classification'].isin(['reliable', 'medium reliable'])]
    
    # Calculate additional statistics
    stats = filtered_data.groupby(['ID', 'final_classification']).agg(
        mean_period=('m3', 'mean'),
        mean_lower_error=('m4', 'mean'),
        mean_upper_error=('m5', 'mean'),
        mean_significance=('m6', 'mean'),
        mean_iou=('iou', 'mean')
    ).reset_index()
    
    return stats

def save_to_csv(data, file_path):
    """
    Saves the provided DataFrame to a CSV file at the specified file path.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to be saved.
    file_path : str
        The path where the CSV file will be saved.
    """
    data.to_csv(file_path, index=False)

def process_large_dataset(file_path, chunksize=10000):
    """
    Processes a large dataset by reading it in chunks, classifying periods, and then
    aggregating results both within and across chunks. This approach allows for handling
    datasets too large to fit into memory.

    Parameters:
    -----------
    file_path : str
        The path to the large dataset file.
    chunksize : int, optional
        The number of rows per chunk to use when reading the dataset.

    Returns:
    --------
    tuple of (pd.DataFrame, pd.DataFrame)
        A tuple containing two DataFrames: the first with combined classified data from all
        chunks, and the second with aggregated statistics for 'reliable' and 'medium reliable'
        object IDs.
    """
    aggregated_chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        processed_chunk = process_chunk(chunk)
        aggregated_chunks.append(processed_chunk)

    # Combine processed chunks and classify aggregated data
    combined_data = pd.concat(aggregated_chunks, ignore_index=True)
    aggregated_stats = aggregate_statistics(combined_data)
    
    return combined_data, aggregated_stats

if __name__ == "__main__":
    # Demonstration of module functionality using a specified file path for a large dataset of INDIVIDUALLY CLASSIFIED periods.
    """
    Usage
    file_path = 'path/to/your/individual_classified_dataset.csv'
    
    Process the dataset and obtain aggregated statistics
    combined_data, aggregated_stats = process_large_dataset(file_path)
    
    Optionally, save the combined classified data and aggregated statistics to CSV files
    combined_data_path = 'path/to/your/combined_classified_data.csv'
    aggregated_stats_path = 'path/to/your/aggregated_statistics.csv'
    
    save_to_csv(combined_data, combined_data_path)
    save_to_csv(aggregated_stats, aggregated_stats_path)
    
    print(f"Combined classified data saved to {combined_data_path}")
    print(f"Aggregated statistics saved to {aggregated_stats_path}")
    """