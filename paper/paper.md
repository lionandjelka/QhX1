---
title: '`QhX`: A Python package for periodicity detection in red noise'
tags:
  - Python
  - astronomy
  - variability
  - quasars variability
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
    affiliation: "1"
  - name: Mladen Nikolić
    orcid: 0009-0002-8943-2709
    affiliation: "1"
  - name: Saša Simić
    orcid: 0000-0001-7453-2016
    affiliation: "3"
  - name: Iva Čvorović Hajdinjak
    orcid: 0000-0001-9208-6574
    affiliation: "1"
  - name: Luka Č. Popović
    orcid: 0000-0003-2398-7664
    affiliation: "4"

affiliations:
  - name: University of Belgrade-Faculty of Mathematics, Studentski trg 16, Belgrade, Serbia
    index: "1"
  - name: Mathematical Institute of Serbian Academy of Science and Arts, Serbia
    index: "2"
  - name: Faculty of sciences, University of Kragujevac, Radoja Domanovića 12, Serbia
    index: "3"
  - name: Astronomical Observatory, Belgrade, Serbia
    index: "4"

date: 14 November 2024
bibliography: paper.bib
---



# Summary
`QhX` is a Python package for detecting periodicity in red noise time series, developed as an in-kind contribution to the Vera C. Rubin Observatory Legacy Survey of Space and Time [LSST, @ivezic2019]. Traditional Fourier-based methods often struggle with red noise, which is common in quasar light curves and other accreting objects. `QhX` addresses these challenges with its core 2D Hybrid method [@2018MNRASK]. Input data are mapped into a time-period plane via wavelet transforms, which are (auto)correlated to produce a correlation density map in a "period-period" plane. Statistical vetting incorporates significance, upper and lower error bounds, and the novel Intersection over Union (IoU) metric to evaluate the proximity and overlap of detected periods across bands and objects. In addition to a vetted numerical catalog, `QhX` dynamically visualizes periodicity across photometric bands and objects.



# Statement of need
![The left panel shows a 1D light curve with observational data (black error bars) and a model (blue line). `QhX` transforms the time-series  into the time-frequency domain and cross-correlates wavelet matrices to produce a 2D period-period correlation map (right), where clusters indicate periodic signals. After map integration, statistical vetting generates a numerical catalog of flagged periodic objects (bottom left) and a dynamic view of detected periods across objects and bands (bottom right). \label{fig:scheme}](simpleoverview.pdf)



Periodic variability spans a range of astronomical objects, from asteroids to quasars. Identifying meaningful signals is complicated by red noise [see, e.g., Figure 1 in @GAIA; @Kasliwal; @Kovacevic2022], which exhibits fractal-like patterns across time scales [@vio91; @belete18]. Non-stationary signals and unfavorable sampling [@2018Br; @2023arXiv231016896D] further obscure coherent patterns. Traditional time-frequency methods, constrained by the Fourier uncertainty principle [i.e., Gabor limit, @gabor47], often fail with such complex signals, highlighting the need for nonlinear approaches [@cohen1995time; @Abry1995].

`QhX` provides features specifically designed to address these challenges.
 The first feature is its core 2D Hybrid method (see Figure \ref{fig:scheme}), detailed in [@2018MNRASK], inspired by 2D Correlation Spectroscopy  [@NODA20; @10K]. By applying wavelet transforms, `QhX` maps time-series data into the time-frequency domain and (auto)correlates it, generating a period-period correlation density that enhances signal detection.
Secondly, `QhX` introduces an Intersection over Union (IoU) metric, combined with standard statistical measures (significance, upper and lower error bounds), to evaluate the overlap of detected periods across bands and objects. Each period is represented as the center of an "IoU ball," with its radius reflecting relative error, calculated as the mean of the upper and lower error bounds—analogous to a circular aperture in photometry [@Saxena2024].
Thirdly, `QhX` enhances traditional analysis by generating numerical and interactive visual catalogs that rank periodicity candidates by reliability. These interactive catalogs enable detailed inspection of signal consistency, offering greater interpretability than traditional static plots.



# QhX structure


![Schematic representation of the QhX package architecture.  \label{fig:QhXscheme}](qhxdiag.pdf)

`QhX` (Version 0.2.0) is an open-source package optimized for gappy quasar light curves but adaptable to other datasets. It supports both dynamic and fixed modes, with parallel processing capabilities for large-scale data. The modular design facilitates rapid experimentation by enabling easy swapping or modification of functions (see Figure \ref{fig:QhXscheme}), addressing diverse research needs. For fixed-only workflows, specialized functions such as `data_manager` offer minimal overhead and optimal performance, while `data_manager_dynamical` supports both dynamic and fixed configurations to handle more complex scenarios involving dynamic filters.

The package is organized as follows:

1. **Core**:
   - `algorithms` module provides essential signal-processing techniques, including the Weighted Wavelet Z-Transform (`wwtz`) and prototype superlet transforms.
   - `correlation` function within the `utils` module supports the 2D Hybrid method by converting light curve data into wavelet matrices and performing (auto)correlation, creating correlation density.

2. **Signal Detection and Validation**:
   - `detection` module identifies candidate periodic signals and assesses their validity using statistical measures (significance and upper and lower  error [@2019J]). The Intersection over Union (IoU) metric identifies overlapping periods across bands and objects. To our knowledge, this is the first application of the Intersection-over-Union (IoU) metric to quantify the overlap between detected and reference periods in astronomical time-series analysis.
   - Statistical vetting categorizes detected periods for each object and band as reliable, medium, or poor.
   

3. **Data Management**:
   - `QhX` assumes input time-series data in a simple tabular format containing time, flux (or magnitude), and associated uncertainties. Examples in the documentation illustrate how to map data from other commonly used formats into this structure.

   - `data_manager` and `data_manager_dynamical` modules manage data flow, data loading, outlier removal, and format compatibility. 
   - `batch_processor` and `parallelization_solver` modules optimize task distribution across multiple processors.

4. **Visualization and Output**:
   - `plots` module includes tools for creating interactive visualizations, such as `interactive_plot`, which allows for exploring detected periodicities across bands and objects. For large datasets, `interactive_plot_large_files` enables in-depth inspection of signal consistency.
   - `output` and `output_parallel` modules handle result storage, supporting both single-threaded and parallelized workflows.

5. **Testing**:
   - `tests` module, containing `test_parallel` and `test_integrated`, validates the functionality across various processing setups.


# Representative Applications

`QhX` has been benchmarked with respect to widely used periodicity detection software across multiple domains. In  @2023AJF, applying  `QhX` to SDSS J2320$+$0024 yielded a period of $278.36^{+57.34}_{-25.21}$ days, with a significance above 99\% measured via the shuffling method, and a 90\% significance from the Generalized Extreme Value (GEV) approach. A Lomb--Scargle periodogram applied to the same dataset produced a consistent period of 278~days at the same significance level. In @2019ApJK,`QhX` detected periods of $1972 \pm 254$~days (observed light curve) and $1873 \pm 250$ days (modeled light curve) for PG~1302--102, both within $1\sigma$ of the $1884 \pm 88$ day period reported by @Graham2015 using generalized Lomb--Scargle, wavelet, and autocorrelation methods; a Bayesian reanalysis by @Zhu2020 on an extended dataset for PG~1302--102 yielded a comparable quasi-period of 5.6 yr, interpreted as quasiperiodic oscillations. In the case of Mrk 231 [@2020MNRASK], the 2D hybrid method identified a characteristic period of $403$ days with a significance greater than 99.7\%, in agreement with a Lomb--Scargle periodogram result of $413$ days at a significance above 95\%; the slightly larger uncertainty in the `QhX`-derived period reflects the temporal variation of the periodicity, while the average oscillation power is comparable between the two methods. The method has also been validated in the context of damped oscillations in the changing-look quasar NGC 3516 [@2020OAstK], where experimental results demonstrated robustness against the combined effects of red noise and complex time-series structure. Beyond astrophysical applications, QhX has been applied to Very Low Frequency (VLF) signal analysis for pre- and post-earthquake intervals [@mathKovacevic]. In the no-earthquake scenario (same date one year earlier), the topology of QhX 2D hybrid maps exhibited distinct correlation cluster patterns compared to earthquake-day records, with detected periods below 111 s in most intervals and a $\sim 140$ s signal in the $-2$ h segment, closely matching a 147 s signal detected during the earthquake event. Comparison with Fast Fourier Transform (FFT) results [@nina2020] showed strong agreement before the earthquake for periods below 1.5 min, and convergence of both methods to similar values in subsequent intervals. Post-earthquake periods obtained with QhX were also consistent with the $<10$s to few-hundred-second range reported in [@oh2018]. 
`QhX` is [the LSST directable software in-kind contribution](https://www.lsst.org/scientists/international-drh-list).




# Acknowledgements

Funding was provided by the University of Belgrade - Faculty of Mathematics (the contract 451-03-66/2024-03/200104), Faculty of Sciences University of Kragujevac (451-03-65/2024-03/200122), and Astronomical Observatory Belgrade (contract 451-03-66/2024-
03/200002), through grants by the Ministry of Education, Science, and Technological Development of the Republic of Serbia. 




# References
