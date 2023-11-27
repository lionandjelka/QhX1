# -*- coding: utf-8 -*-
#
# Time-frequency analysis with superlets
# Based on 'Time-frequency super-resolution with superlets'
# by Moca et al., 2021 Nature Communications
#
# Implementation by Gregor Mönke: github.com/tensionhead
#


import numpy as np
from scipy.signal import fftconvolve


def superlet(data_arr, samplerate, scales, order_max, order_min=1, c_1=3, adaptive=False):
    """
    Performs Superlet Transform (SLT) on time-series data.

    This function computes either a multiplicative SLT or a fractional adaptive SLT (FASLT), 
    based on the 'adaptive' flag. Multiplicative SLT is recommended for analysis within a narrow 
    frequency band, while FASLT is suitable for a broader range of frequencies. The transform 
    combines multiple Morlet wavelets with varying cycles to achieve super-resolution in 
    time-frequency analysis.

    Parameters
    ----------
    data_arr : ndarray
        Uniformly sampled time-series data. The first dimension is treated as the time axis.
    samplerate : float
        Sampling rate of the time-series data in Hz.
    scales : ndarray
        Array of scales for the wavelet transform, ordered from high to low for `adaptive=True`.
    order_max : int
        Maximum order for the superlet set, dictating the highest number of cycles.
    order_min : int, optional
        Minimum order for the superlet set, default is 1.
    c_1 : int, optional
        Base number of cycles for the lowest-order Morlet wavelet, default is 3.
    adaptive : bool, optional
        Flag to choose between multiplicative SLT and FASLT, default is False.

    Returns
    -------
    ndarray: Geometric mean of the complex time-frequency representation of the input data.

    References
    ----------
    
    - `Moca, Vasile V., et al. 2021,Time-frequency super-resolution with superlets, Nat. Comm. 12.1, 1-18 <https://www.nature.com/articles/s41467-020-20539-9>`_.
    """
    # Function implementation...

    # adaptive SLT
    if adaptive:

        gmean_spec = FASLT(data_arr, samplerate, scales, order_max, order_min, c_1)

    # multiplicative SLT
    else:

        gmean_spec = multiplicativeSLT(
            data_arr, samplerate, scales, order_max, order_min, c_1
        )

    return gmean_spec


def multiplicativeSLT(data_arr, samplerate, scales, order_max, order_min=1, c_1=3):
    """
    Performs a multiplicative Superlet Transform on time-series data.

    This function computes the multiplicative Superlet Transform by combining Morlet wavelets
    with increasing cycles, resulting in a super-resolution time-frequency representation.

    Parameters
    ----------
    data_arr : ndarray
        Time-series data for analysis.
    samplerate : float
        Sampling rate of the data in Hz.
    scales : ndarray
        Array of scales for the wavelet transform.
    order_max : int
        Maximum order of the superlet set.
    order_min : int, optional
        Minimum order of the superlet set, default is 1.
    c_1 : int, optional
        Number of cycles for the base Morlet wavelet, default is 3.

    Returns
    -------
    ndarray: Result of the multiplicative Superlet Transform.
    """
    # Function implementation...

    dt = 1 / samplerate
    # create the complete multiplicative set spanning
    # order_min - order_max
    cycles = c_1 * np.arange(order_min, order_max + 1)
    order_num = order_max + 1 - order_min # number of different orders
    SL = [MorletSL(c) for c in cycles]

    # lowest order
    gmean_spec = cwtSL(data_arr, SL[0], scales, dt)
    gmean_spec = np.power(gmean_spec, 1 / order_num)

    for wavelet in SL[1:]:

        spec = cwtSL(data_arr, wavelet, scales, dt)
        gmean_spec *= np.power(spec, 1 / order_num)

    return gmean_spec


def FASLT(data_arr, samplerate, scales, order_max, order_min=1, c_1=3):
    """
    Performs a Fractional Adaptive Superlet Transform (FASLT) on time-series data.

    FASLT computes a time-frequency representation using a set of Morlet wavelets with fractional
    orders. The order of wavelets increases linearly with frequency, allowing for a more adaptive
    analysis across a range of frequencies.

    Parameters
    ----------
    data_arr : ndarray
        Time-series data for analysis.
    samplerate : float
        Sampling rate of the data in Hz.
    scales : ndarray
        Array of scales for the wavelet transform.
    order_max : int
        Maximum order of the superlet set.
    order_min : int, optional
        Minimum order of the superlet set, default is 1.
    c_1 : int, optional
        Number of cycles for the base Morlet wavelet, default is 3.

    Returns
    -------
    ndarray: Result of the Fractional Adaptive Superlet Transform.
    """
    # Function implementation...

    dt = 1 / samplerate
    # frequencies of interest
    # from the scales for the SL Morlet
    fois = 1 / (2 * np.pi * scales)
    orders = compute_adaptive_order(fois, order_min, order_max)

    # create the complete superlet set from
    # all enclosed integer orders
    orders_int = np.int32(np.floor(orders))
    cycles = c_1 * np.unique(orders_int)
    SL = [MorletSL(c) for c in cycles]

    # every scale needs a different exponent
    # for the geometric mean
    exponents = 1 / (orders - order_min + 1)

    # which frequencies/scales use the same integer orders SL
    order_jumps = np.where(np.diff(orders_int))[0]
    # each frequency/scale will have its own multiplicative SL
    # which overlap -> higher orders have all the lower orders

    # the fractions
    alphas = orders % orders_int

    # 1st order
    # lowest order is needed for all scales/frequencies
    gmean_spec = cwtSL(data_arr, SL[0], scales, dt)  # 1st order <-> order_min
    # Geometric normalization according to scale dependent order
    gmean_spec = np.power(gmean_spec.T, exponents).T

    # we go to the next scale and order in any case..
    # but for order_max == 1 for which order_jumps is empty
    last_jump = 1

    for i, jump in enumerate(order_jumps):

        # relevant scales for the next order
        scales_o = scales[last_jump:]
        # order + 1 spec
        next_spec = cwtSL(data_arr, SL[i + 1], scales_o, dt)

        # which fractions for the current next_spec
        # in the interval [order, order+1)
        scale_span = slice(last_jump, jump + 1)
        gmean_spec[scale_span, :] *= np.power(
            next_spec[: jump - last_jump + 1].T,
            alphas[scale_span] * exponents[scale_span],
        ).T

        # multiply non-fractional next_spec for
        # all remaining scales/frequencies
        gmean_spec[jump + 1 :] *= np.power(
            next_spec[jump - last_jump + 1 :].T, exponents[jump + 1 :]
        ).T

        # go to the next [order, order+1) interval
        last_jump = jump + 1

    return gmean_spec


class MorletSL:
    def __init__(self, c_i=3, k_sd=5):
        """
        Represents a Morlet wavelet used in Superlet Transform.

        The Morlet wavelet in Superlet formulation has a specific number of cycles within 
        its Gaussian envelope, influencing its time and frequency resolution.

        Parameters
        ----------
        c_i : int, optional
            Number of cycles within the Gaussian envelope, default is 3.
        k_sd : int, optional
            Standard deviation of the Gaussian envelope, default is 5.
        """

    def __call__(self, *args, **kwargs):
        return self.time(*args, **kwargs)

    def time(self, t, s=1.0):
        """
        Computes the complex Morlet wavelet at a given time and scale.

        Parameters
        ----------
        -t (float): Time variable.
        -s (float, optional): Scale variable, default is 1.0.

        Returns
        -------
        complex: Value of the Morlet wavelet at the given time and scale.
        """
        # Function implementation...

        ts = t / s
        # scaled time spread parameter
        # also includes scale normalisation!
        B_c = self.k_sd / (s * self.c_i * (2 * np.pi) ** 1.5)

        output = B_c * np.exp(1j * ts)
        output *= np.exp(-0.5 * (self.k_sd * ts / (2 * np.pi * self.c_i)) ** 2)

        return output


def fourier_period(scale):
    """
    Calculates the approximate Fourier period for a given scale using Morlet wavelet.

    Parameters
    ----------
    -scale (float): Scale of the Morlet wavelet.

    Returns
    -------
    float
    Approximate Fourier period corresponding to the given scale.
    """
    # Function implementation...

    return 2 * np.pi * scale


def scale_from_period(period):
    """
    Determines the scale corresponding to a given Fourier period using Morlet wavelet.

    Parameters
    ----------
    -period (float): Fourier period.

    Returns
    -------
    float: Scale corresponding to the given Fourier period.
    """
    # Function implementation...

    return period / (2 * np.pi)


def cwtSL(data, wavelet, scales, dt):
    """
    Performs Continuous Wavelet Transform using a specified wavelet and scales.

    Parameters
    ----------
    - data : ndarray
         Time-series data for analysis.
    - wavelet : MorletSL
        Morlet wavelet object used for the transform.
    - scales : ndarray
        Array of scales for the wavelet transform.
    - dt : float
        Time step of the data.

    Returns
    -------
    ndarray: Continuous wavelet transform of the input data.
    """
    # Function implementation...

    # wavelets can be complex so output is complex
    output = np.zeros((len(scales),) + data.shape, dtype=np.complex64)

    # this checks if really a Superlet Wavelet is being used
    if not isinstance(wavelet, MorletSL):
        raise ValueError("Wavelet is not of MorletSL type!")

    # 1st axis is time
    slices = [None for _ in data.shape]
    slices[0] = slice(None)

    # compute in time
    for ind, scale in enumerate(scales):

        t = _get_superlet_support(scale, dt, wavelet.c_i)
        # sample wavelet and normalise
        norm = dt ** 0.5 / (4 * np.pi)
        wavelet_data = norm * wavelet(t, scale)  # this is an 1d array for sure!
        output[ind, :] = fftconvolve(data, wavelet_data[tuple(slices)], mode="same")

    return output


def _get_superlet_support(scale, dt, cycles):
    """
    Determines the effective support for the convolution in the Superlet Transform.

    The function calculates the number of points needed to capture the wavelet,
    based on the scale and the number of cycles.

    Parameters
    ----------
    - scale (float):
        Scale of the wavelet.
    - dt (float):
        Time step of the data.
    - cycles (int):
        Number of cycles in the wavelet.

    Returns
    -------
    ndarray: Array of time points for the effective support of the wavelet.
    """
    # Function implementation...

    # number of points needed to capture wavelet
    M = 10 * scale * cycles / dt
    # times to use, centred at zero
    t = np.arange((-M + 1) / 2.0, (M + 1) / 2.0) * dt

    return t


def compute_adaptive_order(freq, order_min, order_max):
    """
    Computes the superlet order for given frequencies in the Fractional Adaptive SLT.

    This is a linear mapping between the minimal and maximal order onto the 
    respective minimal and maximal frequencies.

    Parameters
    ----------
    - freq (ndarray):
        Array of frequencies of interest.
    - order_min (int):
        Minimal order in the superlet set.
    - order_max (int):
        Maximal order in the superlet set.

    Returns
    -------
    ndarray: Array of computed orders for the given frequencies.
    """
    # Function implementation...

    f_min, f_max = freq[0], freq[-1]

    assert f_min < f_max

    order = (order_max - order_min) * (freq - f_min) / (f_max - f_min)

    # return np.int32(order_min + np.rint(order))
    return order_min + order


# ---------------------------------------------------------
# Some test data akin to figure 3 of the source publication
# ---------------------------------------------------------


def gen_superlet_testdata(freqs=[20, 40, 60], cycles=11, fs=1000, eps=0):
    """
    Generates test data for superlet analysis, consisting of harmonic superpositions.

    This function creates a signal composed of multiple oscillations with specified 
    frequencies. Each oscillation is a few-cycle harmonic with an optional addition 
    of white noise. It is useful for demonstrating and testing superlet transform 
    functionality.

    Parameters
    ----------
    - freqs (list of float, optional):
        Frequencies of the oscillations to be included in the signal.
        Default is [20, 40, 60] Hz.
    - cycles (int, optional):
        Number of cycles for each oscillation. Default is 11.
    - fs (int, optional):
        Sampling frequency in Hz. Default is 1000 Hz.
    - eps (float, optional):
        Standard deviation of additive white noise. Default is 0 (no noise).

    Returns
    -------
    ndarray: Generated 1D signal array containing harmonic superpositions with optional noise.

    Examples
    --------
    
    >>> import numpy as np
    >>> from mymodule import gen_superlet_testdata
    >>> signal = gen_superlet_testdata(freqs=[20, 40, 60], cycles=10, fs=1000, eps=0.1)
    """
  
    # Function implementation...

    signal = []
    for freq in freqs:

        # 10 cycles of f1
        tvec = np.arange(cycles / freq, step=1 / fs)

        harmonic = np.cos(2 * np.pi * freq * tvec)
        f_neighbor = np.cos(2 * np.pi * (freq + 10) * tvec)
        packet = harmonic + f_neighbor

        # 2 cycles time neighbor
        delta_t = np.zeros(int(2 / freq * fs))

        # 5 cycles break
        pad = np.zeros(int(5 / freq * fs))

        signal.extend([pad, packet, delta_t, harmonic])

    # stack the packets together with some padding
    signal.append(pad)
    signal = np.concatenate(signal)

    # additive white noise
    if eps > 0:
        signal = np.random.randn(len(signal)) * eps + signal

    return signal


if __name__ == "__main__":

    # to get sth for the eyes ;)
    import matplotlib.pyplot as ppl

    fs = 1000  # sampling frequency
    A = 10 # amplitude
    signal = A * gen_superlet_testdata(fs=fs, eps=0)  # 20Hz, 40Hz and 60Hz
    
    # frequencies of interest in Hz
    foi = np.linspace(1, 100, 50)
    scales = scale_from_period(1 / foi)

    spec = superlet(
        signal,
        samplerate=fs,
        scales=scales,
        order_max=30,
        order_min=1,
        c_1=5,
        adaptive=True,
    )

    # amplitude scalogram
    ampls = np.abs(spec)

    fig, (ax1, ax2) = ppl.subplots(2, 1,
                                   sharex=True,
                                   gridspec_kw={"height_ratios": [1, 3]},
                                   figsize=(6, 6))

    ax1.plot(np.arange(signal.size) / fs, signal, c='cornflowerblue')
    ax1.set_ylabel('signal (a.u.)')
    
    extent = [0, len(signal) / fs, foi[0], foi[-1]]
    im = ax2.imshow(ampls, cmap="magma", aspect="auto", extent=extent, origin='lower')
    
    ppl.colorbar(im,ax = ax2, orientation='horizontal',
                 shrink=0.7, pad=0.2, label='amplitude (a.u.)')
    
    ax2.plot([0, len(signal) / fs], [20, 20], "--", c='0.5')
    ax2.plot([0, len(signal) / fs], [40, 40], "--", c='0.5')
    ax2.plot([0, len(signal) / fs], [60, 60], "--", c='0.5')
    
    ax2.set_xlabel("time (s)")    
    ax2.set_ylabel("frequency (Hz)")

    fig.tight_layout()
