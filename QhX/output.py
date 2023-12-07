import pandas as pd
import numpy as np
import math




def flatten_detected_periods(detected_periods):
    """Flatten the nested list of dictionaries and insert NaN for empty lists."""
    flat_list = []
    for sublist in detected_periods:
        if sublist:  # Check if the sublist is not empty
            flat_list.extend(sublist)
        else:
            # Append a dictionary with NaN values if the sublist is empty
            flat_list.append({key: np.nan for key in ['objectid', 'sampling_i', 'sampling_j', 'period', 'upper_error', 'lower_error', 'significance', 'label']})
    return flat_list


def classify_periods(detected_periods):
    """
    Calculates IoU and compile other metrics (low errors,  upper errors, significance of detected period, and band pairs) for each quasar ID.
    It computes Intersection Over Union (IoU) and other relevant metrics for each quasar ID based
    on detected periods in different band pairs, while preserving NaN values.

    Parameters:
    -----------
    detected_periods (list of dict): List of dictionaries containing detected period data.

    Returns:
    --------
    pd.DataFrame: DataFrame containing the classification results.
    """
    # Flatten the list of dictionaries
    flat_list = flatten_detected_periods(detected_periods)

    # Convert flattened list to DataFrame
    df = pd.DataFrame(flat_list)
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
    rows_list = []

    # Process each unique quasar ID
    for name in df['objectid'].unique():
        quasar_data = df[df['objectid'] == name]

        for i in range(len(quasar_data)):
            for j in range(i + 1, len(quasar_data)):
                row_i = quasar_data.iloc[i]
                row_j = quasar_data.iloc[j]

                # Initialize IoU and period difference
                iou, period_diff = np.nan, np.nan

                # Check if all necessary values are present to calculate IoU and period difference
                if not pd.isna(row_i['period']) and not pd.isna(row_j['period']) and not pd.isna(row_i['upper_error']) and not pd.isna(row_i['lower_error']) and not pd.isna(row_j['upper_error']) and not pd.isna(row_j['lower_error']):
                    # Calculate relative difference in detected periods
                    period_diff = abs(row_i['period'] - row_j['period']) / row_i['period']

                    if period_diff <= 0.1:
                        # Calculate IoU
                        radius_i = (row_i['upper_error'] + row_i['lower_error']) / 2
                        radius_j = (row_j['upper_error'] + row_j['lower_error']) / 2
                        distance = abs(row_i['period'] - row_j['period'])
                        iou = calculate_iou(radius_i, radius_j, distance)

                # Add row to list
                rows_list.append({
                    'objectid': name,
                    'm3': row_i['period'],
                    'm4': row_i['lower_error'],
                    'm5': row_i['upper_error'],
                    'm6': row_i['significance'],
                    'm7_1': row_i['label'],
                    'm7_2': row_j['label'],
                    'period_diff': period_diff,
                    'iou': iou
                })

    # Convert list of rows to DataFrame
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
    # Check for NaN values
    if pd.isna(row['m3']) or pd.isna(row['m4']) or pd.isna(row['m5']) or pd.isna(row['m6']) or pd.isna(row['iou']):
        return 'NAN'

    # Check if m3 (period) is zero to avoid division by zero
    if row['m3'] == 0:
        return 'NAN'

    # Calculate relative errors
    rel_error_lower = row['m4'] / row['m3']
    rel_error_upper = row['m5'] / row['m3']

    # Classify based on criteria
    if row['m6'] >= 0.99 and rel_error_lower <= 0.1 and rel_error_upper <= 0.1 and row['iou'] >= 0.99:
        return 'reliable'
    elif 0.5 <= row['m6'] < 0.99 and 0.1 < rel_error_lower <= 0.3 and 0.1 < rel_error_upper <= 0.3 and 0.8 <= row['iou'] < 0.99:
        return 'medium reliable'
    else:
        return 'poor'

