import numpy as np
import colorednoise as cn


def artificial_lc_sampled(mjd,t,y):
    """ 
    Returns a hypothetical light curve sampled in a given OpSim strategy.
    User needs to provide a reference light curve for sampling (usually a continous
    light curve with 1 day cadence, see LC_conti() function).
    
    Parameters:
    -----------
    mjd: np.array
        Modified Julian Date obtained from OpSim. It is the time of each sampling of the light curve
        during the LSST operation period in one of the filters and specified sky coordinates.
    t: np.array
        Days during the survey on which we had an observation for a continuous reference light curve.
    y: np.array
        Light curve magnitudes for continuous reference light curve.
     
    Returns:
    --------
    top: np.array
        Days during the survey when we had an observation (sampling) in a given OpSim strategy.
    yop: np.array
        Light curve magnitude taken from the reference light curve on days we had an observation 
        (sampling) in a given OpSim strategy.
    """
    
    # Convert MJD to survey days
    top=np.ceil(mjd-mjd.min())
    
    # Reference light curve sampling
    yop=[]
    for i in range(len(top)):
        abs_vals = np.abs(t-top[i])
        
        # Find matching days and their index
        bool_arr = abs_vals < 1
        if bool_arr.sum() != 0:
            index = (np.where(bool_arr)[0])[0]
            yop.append(y[index])
            
        # Case when we don't have a match
        elif bool_arr.sum() == 0:
            yop.append(-999)
    yop=np.asarray(yop)
    
    # Drop placeholder values (-999)
    top = mjd - mjd.min()
    top = top[yop!=-999]
    yop = yop[yop!=-999]
    
    
    
    
    return top,yop

def artificial_stochastic_mock_lc(T, deltatc=1, oscillations=True, A=0.14, noise=0.00005, z=0, frame='observed'):
    """ 
    Generate one artificial light curve using a stochastic model based on the Damped random walk (DRW)
    proccess. Parameters describing the model are characteristic amplitude ("logsig2" in code) and time 
    scale of the exponentially-decaying variability ("tau" in code), both infered from physical 
    quantities such are supermassive black hole mass and/or luminosity of the AGN. For further details
    regarding the model see Kovačević et al. (2021) and references therein.
    
    Parameters:
    -----------
    T: int
        Total time span of the light curve. It is recommended to generate light curves to be at least 
        10 times longer than their characteristic timescale (Kozłowski 2017). 
    deltatc: int, default=1
        Cadence (or sampling rate) - time interval between two consecutive samplings of the light 
        curve in days.
    oscillations: bool, default=True
        If True, light curve simulation will take an oscillatory signal into account.
    A: float, default=0.14
        Amplitude of the oscillatory signal in magnitudes (used only if oscillations=True).
    noise: float, default=0.00005
        Amount of noise to include in the light curve simulation.
    z: float, default=0
        Redshift.
    frame: {'observed', 'rest'}, default='observed'
        Frame of reference.
    
    Returns:
    --------
    tt: np.array
        Days when the light curve was sampled.
    yy: np.array
        Magnitudes of the simulated light curve.
        
    References:
    -----------

    - `Ivezić, Ž., et al. 2019, ApJ, 873, 111 <https://iopscience.iop.org/article/10.3847/1538-4357/ab042c>`_.
    - `Kelly, B.C., Bechtold, J., & Siemiginowska, A. 2009, ApJ, 698, 895 <https://iopscience.iop.org/article/10.1088/0004-637X/698/1/895>`_.
    - `Kozłowski, S. 2017, A&A, 597, A128 <https://www.aanda.org/articles/aa/full_html/2017/01/aa29890-16/aa29890-16.html>`_.
    - `Kovacevic A. B., Ilic D., Popovic L. C., Radovic V., Jankov I., Yoon I., Caplar N., et al., 2021, MNRAS, 505, 5012
      <https://ui.adsabs.harvard.edu/abs/2021MNRAS.505.5012K/abstract>`_.
    """
    
    # Constants
    const1 = 0.455*1.25*1e38
    const2 = np.sqrt(1e09)
    meanmag = 23.
    
    # Generating survey days 
    tt = np.arange(0, T, int(deltatc))
    times = tt.shape[0]
    
    # Generating log L_bol
    loglumbol = np.random.uniform(42.2,49,1)
    lumbol = np.power(10,loglumbol)

    # Calculate M_{SMBH}
    msmbh = np.power((lumbol * const2 / const1), 2 / 3.)
    
    # Calculate damping time scale (Eq 22, Kelly et al. 2009)
    logtau = -8.13 + 0.24 * np.log10(lumbol) + 0.34 * np.log10(1 + z)
    if frame == 'observed':
        # Converting to observed frame (Eq 17, Kelly et al. 2009)
        tau = np.power(10, logtau) * (1 + z)
    elif frame == 'rest':
        tau = np.power(10, logtau)
    
    # Calculate log sigma^2 - an amplitude of correlation decay (Eq 25, Kelly et al. 2009)
    logsig2 = 8 - 0.27 * np.log10(lumbol) + 0.47 * np.log10(1 + z)
    if frame == 'observed':
        # Converting to observed frame (Eq 18, Kelly et al. 2009)
        sig = np.sqrt(np.power(10, logsig2)) / np.sqrt(1 + z)
    elif frame == 'rest':
        sig = np.sqrt(np.power(10, logsig2))
          
    # OPTIONAL: Calculate the broad line region radius
    logrblr = 1.527 + 0.533 * np.log10(lumbol / 1e44)
    rblr = np.power(10, logrblr)
    rblr = rblr / 10
    
    # Calculating light curve magnitudes
    ss = np.zeros(times)
    ss[0] = meanmag # light curve is initialized
    SFCONST2 = sig * sig
    ratio = -deltatc / tau

    for i in range(1, times):
        ss[i] = np.random.normal(ss[i-1] * np.exp(ratio) + meanmag * (1 - np.exp(ratio)),
                                 np.sqrt(10 * 0.5 * tau * SFCONST2 * (1 - np.exp(2 * ratio))), 1)
        
    # Calculating error (Ivezic et al. 2019)
    gamma = 0.039
    m5 = 24.7
    x = np.zeros(ss.shape)
    x = np.power(10, 0.4 * (ss - m5))

    err = (0.005 * 0.005) + (0.04 - gamma) * x + gamma * x * x
    
    # Setting period type and value (modify these lines as needed)
    period_type = 'hardcoded'  # 'hardcoded' or 'physical'
    P_value = 0.001  # Only used if period_type is 'hardcoded', it should be in years

    # Final light curve with oscillations
    if oscillations:
        if period_type == 'physical':
            # Calculate underlying periodicity
            conver = 173.145 # convert from LightDays to AU
            lightdays = 10
            P_years = np.sqrt(((lightdays * conver) ** 3) / msmbh)
            P_days = P_years * 365.25
        else:
            P_days = P_value * 365.25
        
        # Calculating and adding oscillatory signal
        sinus = A * np.sin(2 * np.pi * tt / P_days)
        ss = ss + sinus
        yy = np.zeros(times)
        for i in range(times):
            # Adding error and noise to each magnitude value
            yy[i] = ss[i] + np.random.normal(0, ((noise * ss[i])), 1) + np.sqrt(err[i])
    
        return tt, yy, P_days
    
    # Final light curve without oscillations
    if not oscillations:
        yy = np.zeros(times)
        for i in range(times):
            # Adding error and noise to each magnitude value
            yy[i] = ss[i] + np.random.normal(0, ((noise * ss[i])), 1) + np.sqrt(err[i])
    
        return tt, yy
    
def remove_fraction_with_seed(data, fraction, seed=0):
    """
    removes a fraction of data at random with given seed.
    
    Parameters:
    -----------
    - data: data to remove
    - fraction: fraction to remove
    - seed: seed for randomness
    
    Returns:
    --------
    
     data with fraction removed
    """
    n_to_remove = int(len(data) * fraction)
    np.random.seed(seed)

    return np.delete(data, np.random.choice(np.arange(len(data)), n_to_remove, replace=False))

def simple_mock_lc( time_interval, num_points, frequency, amplitude, percent, magnitude = 20, time_unit = 'year', exp = 1.8, mjd_start = 52000):
    
    beta = exp # the exponent
    
    x= cn.powerlaw_psd_gaussian(beta, num_points)
    rng = np.random.RandomState(0)
    
    
    if time_unit == 'year':
        time_interval = time_interval * 365
    elif time_unit == 'day':
        time_interval = time_interval
    elif time_unit == 'hour':
        time_interval = (time_interval/24.0)*365
    elif time_unit == 'minute':
        time_interval = (time_interval/(24.0*60))*365
    else:
        time_interval = (time_interval/(24.0*3600))*365
        
    t = mjd_start + time_interval * rng.rand(num_points)
    
    t1=np.sort(t)
    x = x + 1
    x_std=(x-np.mean(x))/np.std(x)
    
    # TODO: biranje za nivo X
    mag = magnitude + amplitude * np.max(x_std) * np.sin(2 * np.pi * t1 / frequency) + x_std
    
    tt=t1-t1.min()
    
    tt = remove_fraction_with_seed(tt, percent)
    mag = remove_fraction_with_seed(mag, percent)

    
    return tt, mag