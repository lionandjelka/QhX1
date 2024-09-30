import holoviews as hv
import numpy as np
from holoviews import opts, dim
def create_interactive_plot(output_df):
    """
    Creates an interactive HoloViews plot from the output DataFrame.
    This function utilizes the HoloViews library to create an interactive plot. The plot 
    visualizes data from a DataFrame, which is expected to contain specific columns 
    related to object identification and various metrics.
    
    Parameters:
    -----------
    output_df (pd.DataFrame): DataFrame containing the data to be plotted. 
    The DataFrame is expected to have the following columns:
    
    - objectid: The Quasar ID, a unique identifier for each quasar in the database,
                e.g., LSST AGN Data Challenge database.
    - m1,m2: The mean sampling rates in  given bands where the periods are detected. 
             These values represent the average interval between successive observations in that band.                            
    - m3: The detected period in a given pair of bands. When a period is detected in two bands, 
          it is required that the detected values in these bands differ by less than 10% in relative error.
    - m4 and m5: The lower and upper errors of the detected period, respectively. Values are taken from the period in a band which
                 is serving as baseline for comparison, here u-band as arising closest to the SMBH and expect to have the strognest periodic signal
    - m6: The significance of the detected period as inferred from the baseline for comparison. 
          The significance is determined via the Johnson shuffling method, which assesses the likelihood of the period
          being a true signal as opposed to noise.
    - m7: The pair of bands where the period is detected. Bands are designated as u=0, g=1, r=2, i=3. 
          The pairs are represented as ug='0-1', ur='0-2', ui='0-3', etc. 
          The analysis often focuses on comparisons with respect to the u band, as it is expected to be the least deformed of all bands.
    - period_diff: difference between detected periods in two bands
    - iou: intersection over union metric
    - classification: poor, reliable, medium reliable, NAN
    
    Returns:
    --------
    hv.DynamicMap: An interactive HoloViews plot object that can be displayed in a Jupyter 
                   Notebook or other Python interactive environments.
    
    Example:
    --------
    Assuming `output_df` is a DataFrame with the required columns:
    
    >>> interactive_plot = create_interactive_plot(output_df)
    >>> interactive_plot  # This will display the plot in a Jupyter Notebook
    """
    # HoloViews and plot creation code remains unchanged...
    # Initialize HoloViews with the Bokeh backend for interactive plotting
    hv.extension('bokeh')

    # Convert the output DataFrame to a HoloViews Dataset
    dsr = hv.Dataset(output_df, kdims=['objectid'], vdims=['m3', 'm4', 'm5', 'm6', 'm7_1', 'm7_2', 'period_diff', 'iou', 'classification'])

    # Define plot options for appearance and interactivity
    popts = opts.Points(alpha=0.6,  # Transparency of the points
                        legend_position='right',  # Position of the legend
                        height=400,  # Height of the plot
                        width=600,  # Width of the plot
                        show_grid=True,  # Display a grid
                        color='classification',  # Color points by the 'classification' column
                        cmap='Set1',  # Color map for different classifications
                        line_color='black',  # Color of the outline of points
                        xlabel='objectid',  # Label for the x-axis
                        ylabel='m3 (period[days])',  # Label for the y-axis
                        size=100 * (np.abs(dim('m5') - dim('m4')) / (dim('m3') + 0.1)))  # Size of points based on relative error

    # Create an interactive plot, grouped by 'classification'
    hvapp = dsr.to(hv.Points, ['objectid', 'm3'], groupby='classification').opts(popts)

    # Return the interactive plot
    return hvapp
