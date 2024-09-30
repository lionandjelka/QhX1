# Superlet package included in this package
# Reference: Implementation by Gregor Mönke: github.com/tensionhead
import numpy as np
from .superlet import superlet, scale_from_period
from QhX.utils.correlation import correlation_nd

def superlets_methods(tt, mag, ntau, minfq=10, maxfq=500):
    """
    Perform a hybrid 2D method using superlets on time-series data.

    This function applies the superlet transform to the provided time-series data and 
    then computes a correlation matrix using the resulting transformed data. It's 
    particularly useful for time-frequency analysis with high resolution.

    Parameters
    ----------
    - tt : list or ndarray
        Array of time data points.
    - mag : list or ndarray
        Array of magnitude values corresponding to the time data.
    - ntau : int
        Number of time divisions for the analysis. Controls the resolution in time.
    - minfq : float, optional
        Minimum frequency of interest. Default is 10.
    -maxfq : float, optional
        Maximum frequency of interest. Default is 500.

    Returns
    -------
    -ndarray
        Correlation matrix derived from the superlet transform of the input data.
    -extent : list
        Extent of the correlation matrix values, given as [min, max, min, max].

    Examples
    --------
    >>> tt = np.linspace(0, 10, 1000)
    >>> mag = np.sin(tt)
    >>> corr, extent = superlets_methods(tt, mag, 100)
    """
    # Function implementation...
    
    mx = (tt.max()-tt.min())/2.
    mn = np.min(np.diff(tt))
    fmin = 1./minfq
    fmax = 1./maxfq
    df = (fmax-fmin) / ntau
    flist=np.arange(fmin, fmax + df, df)
    
    print(scale_from_period(1/flist))
    # Superlet calculation
    gg=superlet(
        mag,
        samplerate=1/np.diff(tt).mean(),
        scales=scale_from_period(1/flist),
        order_max=100,
        order_min = 1,
        c_1=3,
        adaptive=True,
    )
    
    # Hybrid 2D method
    gg1=np.abs(gg)
    corr = correlation_nd(gg1, gg1)
    extentmin=np.min(corr)
    extentmax=np.max(corr)

    extent=[extentmin,extentmax,extentmin,extentmax]
    

    return  corr,  extent
