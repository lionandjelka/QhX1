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
   - `detection` module identifies candidate periodic signals and assesses their validity using statistical measures (significance and upper and lower  error [@2019J]). The Intersection over Union (IoU) metric identifies overlapping periods across bands and objects.
   - Statistical vetting categorizes detected periods for each object and band as reliable, medium, or poor.
   

3. **Data Management**:
   - `data_manager` and `data_manager_dynamical` modules manage data flow, data loading, outlier removal, and format compatibility. 
   - `batch_processor` and `parallelization_solver` modules optimize task distribution across multiple processors.

4. **Visualization and Output**:
   - `plots` module includes tools for creating interactive visualizations, such as `interactive_plot`, which allows for exploring detected periodicities across bands and objects. For large datasets, `interactive_plot_large_files` enables in-depth inspection of signal consistency.
   - `output` and `output_parallel` modules handle result storage, supporting both single-threaded and parallelized workflows.

5. **Testing**:
   - `tests` module, containing `test_parallel` and `test_integrated`, validates the functionality across various processing setups.


# Representative Applications

The `QhX` method has been applied to:

-Quasar periodicity detection [@2018MNRASK; @2019ApJK; @2020OAstK; @2023AJF].
-Quasi-Periodic Oscillations detection [@2020MNRASK].
-Very Low-Frequency (VLF) signals variability in the vicinity of earthquakes [@mathKovacevic].
-`QhX` is [the LSST directable software in-kind contribution](https://www.lsst.org/scientists/international-drh-list).




# Acknowledgements

Funding was provided by the University of Belgrade - Faculty of Mathematics (the contract 451-03-66/2024-03/200104), Faculty of Sciences University of Kragujevac (451-03-65/2024-03/200122), and Astronomical Observatory Belgrade (contract 451-03-66/2024-
03/200002), through grants by the Ministry of Education, Science, and Technological Development of the Republic of Serbia. 




# References
