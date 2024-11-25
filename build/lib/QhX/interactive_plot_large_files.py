"""
interactive_plot_large_files.py

This module is designed to facilitate the creation of interactive visualizations for large datasets, specifically
tailored for the analysis of periodic phenomena in astronomical observations. It leverages the HoloViews and Bokeh
libraries to render dynamic, interactive plots that support efficient exploration of vast amounts of data through
decimation, rasterization, and dynamic spreading techniques.

The core functionality is encapsulated in the `create_interactive_plot_large` function, which processes a CSV file
containing period analysis results and generates an interactive plot. This visualization aids in the identification
of patterns, outliers, and correlations within the data, offering insights into the underlying astronomical phenomena.

Requirements:
- pandas: For loading and processing the CSV data.
- HoloViews: For constructing interactive visualizations.
- datashader: For rasterizing large datasets to enhance performance.
- bokeh: For backend rendering of interactive plots.

Example usage can be found at the bottom of this module, illustrating how to generate and display an interactive plot
from a CSV file containing large dataset period analysis results.
"""

import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from holoviews.operation.datashader import datashade, dynspread, rasterize
hv.extension('bokeh')

def create_interactive_plot_large(file_path):
    """
    Generates an interactive plot from a specified CSV file containing large datasets of period analysis results.
    It employs decimation, rasterization, and dynamic spreading to manage large data volumes efficiently, ensuring
    interactive performance and clarity in data visualization.

    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing the dataset for visualization. Expected columns include detected periods,
        error bounds, significance, band identifiers, period differences, IoU scores, and classifications.

    Returns:
    --------
    hv.DynamicMap
        An interactive HoloViews plot object that can be displayed in Jupyter Notebooks or exported as an HTML file
        for broader analysis and exploration.

    Example:
    --------
    >>> interactive_plot = create_interactive_plot_large('path_to_large_dataset.csv')
    >>> hv.save(interactive_plot, 'interactive_visualization.html', backend='bokeh')

    Note:
    -----
    This function is specifically optimized for large datasets, applying techniques such as decimation and rasterization
    to maintain performance without compromising the ability to discern patterns and outliers in the data.
    """
    # Load dataset
    df = pd.read_csv(file_path)

    # Define plot options
    plot_opts = opts.Points(width=800, height=400, color='classification', cmap='Category10', size=8, tools=['hover'], alpha=0.5)

    # Convert DataFrame to HoloViews Dataset
    hv_dataset = hv.Dataset(df, ['ID', 'm3'], ['m4', 'm5', 'm6', 'm7_1', 'm7_2', 'period_diff', 'iou', 'classification'])

    # Create scatter plot
    scatter = hv.Scatter(hv_dataset)

    # Apply decimation for performance
    decimated = rasterize(scatter, aggregator='any')

    # Apply dynamic spreading to make sparse data more visible
    spread = dynspread(decimated, max_px=5, threshold=0.5)

    # Return interactive plot with applied options
    return spread.opts(plot_opts)

if __name__ == "__main__":
    # Example usage
    file_path = 'your_large_dataset.csv'
    interactive_plot = create_interactive_plot_large(file_path)
    display(interactive_plot)

