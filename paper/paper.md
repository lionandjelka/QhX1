---
title: 'QhX: A Python package for periodicity detection in red noise'
tags:
  - Python
  - astronomy
  - variability
  - quasar variability
  - binary quasars
authors:
  - name: Andjelka B. Kovačević
    orcid: 0000-0001-5139-1978
    corresponding: true
    equal-contrib: true
    affiliation: "1"
  - name: Dragana Ilić
    orcid: 0000-0002-1134-4015
    affiliation: "1"
  - name: Momčilo Tošić
    equal-contrib: true
    affiliation: "1"
  - name: Marina Pavlović
    orcid: 0000-0001-5560-7051
    affiliation: "2"
  - name: Aman Raju
    orcid: 0000-0001-9339-0789
    affiliation: "3"
  - name: Mladen Nikolić
    orcid: 0009-0002-8943-2709
    affiliation: "1"
  - name: Saša Simić
    orcid: 0000-0001-7453-2016
    affiliation: "4"
  - given-names: Iva
    surname: Čvorović-Hajdinjak
    orcid: 0000-0001-9208-6574
    affiliation: "1"
  - name: Luka Č. Popović
    orcid: 0000-0003-2398-7664
    affiliation: "5"

affiliations:
  - name: University of Belgrade - Faculty of Mathematics, Studentski trg 16, Belgrade, Serbia
    index: "1"
  - name: Rubin Observatory Project Oﬃce, 950 N. Cherry Ave., Tucson, AZ 85719, USA
    index: "2"
  - name: DARK, Niels Bohr Institute, University of Copenhagen, Jagtvej 155, Copenhagen N, 2200, Denmark
    index: "3"
  - name: Faculty of sciences, University of Kragujevac, Radoja Domanovića 12, Serbia
    index: "4"
  - name: Astronomical Observatory, Belgrade, Volgina 7, 11000 Belgrade, Serbia
    index: "5"

date: 18 December 2025
bibliography: paper.bib
---



# Summary
`QhX` is a Python package for detecting periodicity in red noise time series, developed as an in-kind contribution to the Vera C. Rubin Observatory Legacy Survey of Space and Time [LSST, @ivezic2019]. Traditional Fourier-based methods often struggle with red noise, which is common in quasar light curves and other accreting objects. `QhX` addresses these challenges with its core 2-dimensional (2D) hybrid method [@2018MNRASK]. Input data are mapped into a time-period plane via wavelet transforms, which are (auto)correlated to produce a correlation density map in a "period-period" plane. Statistical vetting incorporates significance, upper and lower error bounds, and the novel intersection over union (IoU) metric to evaluate the proximity and overlap of detected periods across bands and objects. In addition to a vetted numerical catalog, `QhX` dynamically visualizes periodicity across photometric bands and objects.



# Statement of need
Periodic variability spans a range of astronomical objects, from asteroids to quasars. Identifying meaningful signals is complicated by red noise [see, for example, Figure 1 in @GAIA; @Kasliwal; @Kovacevic2022], which exhibits fractal-like patterns across time scales [@vio91; @belete18]. Non-stationary signals and unfavorable sampling [@2018Br; @2023arXiv231016896D] further obscure coherent patterns. Traditional time-frequency methods are often ineffective with such complex signals due to the Fourier–Gabor uncertainty limit [@gabor47], highlighting the need for nonlinear approaches [@cohen1995time; @Abry1995].

![The left panel shows a one-dimensional (1D) light curve of observational data (black error bars) and a model (blue line). `QhX` transforms the time-series data into the time-frequency domain and cross-correlates wavelet matrices to produce a 2D period-period correlation map (right). Clusters in this map indicate periodic signals. After map integration, statistical vetting generates a numerical catalog of flagged periodic objects (bottom left) and a dynamic view of detected periods across objects and bands (bottom right). \label{fig:scheme}](simpleoverview.pdf)

`QhX` provides features specifically designed to address these challenges.
 The first feature is its core 2D hybrid method (see \autoref{fig:scheme}), which is detailed in [@2018MNRASK] and inspired by 2D correlation spectroscopy [@NODA20; @10K]. By applying wavelet transforms, `QhX` maps time-series data into the time-frequency domain and (auto)correlates it, generating a period-period correlation density that enhances signal detection.
Secondly, `QhX` introduces an IoU metric, combined with standard statistical measures (significance, upper and lower error bounds), to evaluate the overlap of detected periods across bands and objects. Each period is represented as the center of an "IoU ball," with its radius reflecting relative error, calculated as the mean of the upper and lower error bounds and analogous to a circular aperture in photometry [@Saxena2024].
Finally, `QhX` enhances traditional analysis by generating numerical and interactive visual catalogs that rank periodicity candidates by reliability. These interactive catalogs enable detailed inspection of signal consistency and offer greater interpretability than traditional static plots.



# `QhX` structure

`QhX` (version 0.2.0) is an open-source package optimized for gappy quasar light curves, though it can be adapted to other datasets. It supports both dynamic and fixed modes, with parallel processing capabilities for large-scale data. The modular design facilitates rapid experimentation by enabling easy swapping or modification of functions (see \autoref{fig:QhXscheme}), addressing diverse research needs. For fixed-only workflows, specialized functions such as `data_manager` offer minimal overhead and optimal performance, while `data_manager_dynamical` supports both dynamic and fixed configurations to handle more complex scenarios involving dynamic filters.

![Schematic representation of the `QhX` package architecture.  \label{fig:QhXscheme}](qhxdiag.pdf)

The package is organized as follows:

1. **Core**:
   - The `algorithms` module provides essential signal processing techniques, including the weighted wavelet Z-transform (`wwtz`) and prototype superlet transforms.
   - The `correlation` function within the `utils` module supports the 2D hybrid method by converting light curve data into wavelet matrices and creating correlation density via (auto)correlation.

2. **Signal detection and validation**:
   - The `detection` module identifies candidate periodic signals and assesses their validity using statistical measures such as significance and upper and lower error [@2019J]. The IoU metric identifies overlapping periods across bands and objects. To our knowledge, this is the first application of the IoU metric to quantify the overlap between detected and reference periods in astronomical time-series analysis.
   - Statistical vetting categorizes detected periods for each object and band as reliable, medium, or poor.

3. **Data management**:
   - `QhX` takes time-series data as input in a simple tabular format containing time, flux (or magnitude), and associated uncertainties. Examples in the documentation illustrate how to map data from other commonly used formats into this structure.

   - The `data_manager` and `data_manager_dynamical` modules manage data flow, data loading, outlier removal, and format compatibility. 
   - The `batch_processor` and `parallelization_solver` modules optimize task distribution across multiple processors.

4. **Visualization and output**:
   - The `plots` module includes tools for creating interactive visualizations. For example, `interactive_plot` allows one to explore detected periodicities across bands and objects. For large datasets, `interactive_plot_large_files` enables in-depth inspection of signal consistency.
   - The `output` and `output_parallel` modules handle result storage and support both single-threaded and parallelized workflows.

5. **Testing**:
   - The `tests` module, containing `test_parallel` and `test_integrated`, validates the functionality across various processing setups.


# Representative Applications

`QhX` has been benchmarked with respect to widely used periodicity detection software libraries across multiple domains. 

Applications of `QhX` to quasars demonstrate that its period estimates and significance assessments closely align with those obtained from established methods such as Lomb-Scargle, Generalized Extreme Value (GEV) analyses, and Bayesian evaluations. In  @2023AJF, applying  `QhX` to SDSS J2320+0024 yielded a period of $278.36^{+57.34}_{-25.21}$ days, with a significance level greater than 99\% as measured via the shuffling method and 90\% as measured via the GEV approach. A Lomb--Scargle periodogram applied to the same dataset produced a consistent period of 278 days at the same significance level. 
In @2019ApJK, `QhX` detected periods of $1972 \pm 254$ days (observed light curve) and $1873 \pm 250$ days (modeled light curve) for PG 1302--102, both within $1\sigma$ of the $1884 \pm 88$ day period reported by @Graham2015 using generalized Lomb-Scargle, wavelet, and autocorrelation methods. A Bayesian reanalysis by @Zhu2020 on an extended dataset for PG 1302--102 yielded a comparable quasi-period of 5.6 years, which was interpreted as quasiperiodic oscillations.
In the case of Mrk 231 [@2020MNRASK], the 2D hybrid method identified a characteristic period of $403$ days with a significance greater than 99.7\%, in agreement with a Lomb-Scargle periodogram result of $413$ days at a significance above 95\%. The slightly larger uncertainty in the `QhX`-derived period reflects the temporal variation of the periodicity, while the average oscillation power is comparable between the two methods. 
This method has also been validated in the context of damped oscillations in the changing-look quasar NGC 3516 [@2020OAstK], where experimental results demonstrated robustness against the combined effects of red noise and complex time-series structure. 

Beyond astrophysical applications, `QhX` has been applied to very low frequency (VLF) signal analysis for pre- and post-earthquake intervals [@mathKovacevic]. In the no-earthquake scenario (same date one year earlier), the topology of the `QhX` 2D hybrid maps exhibited distinct correlation cluster patterns compared to the earthquake-day records. Most intervals had detected periods below 111 seconds, and a 140-second signal was detected in the -2-hour segment. This signal closely matched the 147-second signal detected during the earthquake event. Comparison with Fast Fourier Transform (FFT) results [@nina2020] showed strong agreement before the earthquake for periods below 1.5 minutes, and convergence of both methods to similar values in subsequent intervals. Post-earthquake periods obtained with `QhX` were also consistent with the $<10$ seconds to few-hundred-second range reported in [@oh2018]. 

`QhX` is [an LSST directable software in-kind contribution](https://www.lsst.org/scientists/international-drh-list).




# Acknowledgements

Funding was provided by the University of Belgrade - Faculty of Mathematics (the contract 451-03-66/2024-03/200104), Faculty of Sciences University of Kragujevac (451-03-65/2024-03/200122), and Astronomical Observatory Belgrade (contract 451-03-66/2024-
03/200002), through grants by the Ministry of Education, Science, and Technological Development of the Republic of Serbia. 
`QhX` makes extensive use of several open-source scientific Python libraries.
Core numerical operations and statistical routines rely on NumPy [@numpy]
and SciPy [@scipy].
The weighted wavelet Z-transform calculations are performed using the libwwz
library [@libwwz].
Interactive visualization and exploratory analysis are implemented using
HoloViews [@holoviews] with Bokeh [@bokeh] as the plotting backend.
We gratefully acknowledge the developers and maintainers of these packages.




# References
