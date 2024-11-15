---
title: '`QhX_dynamical`: A Python package for periodicity detection in red noise'
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


`QhX_dynamical` is a Python-based package developed for periodicity detection in red noise time series data, with a focus on the Vera C. Rubin Observatory Legacy Survey of Space and Time [LSST, @ivezic2019]. Traditional methods, such as those based on the Fourier Transform, often struggle with red noise signals, which are prevalent in real-world datasets.
The core of `QhX_dynamical` is a 2D Hybrid method [cross-correlation of wavelet transforms of light curves, @2018MNRASK]  that operates in a "period-period" phase space, capable of detecting oscillations in one or more light curves. The {`QhX_dynamical`} pipeline first transforms input data into a time-period plane via wavelets and then (auto)correlates the resulting wavelet matrices to obtain a correlation density in the period-period plane.
After integrating the correlation density, the final decision on detected periods is made by a statistical robovetter based on the significance, upper and lower errors of detected periods, and the Intersection over Union (IoU) metric for measuring the proximity and overlap of periods across bands.
Beyond compiling the numerical catalog of vetted periods, `QhX_dynamical` offers visualization across photometric bands using `QhX_dynamical`.

# Statement of need
![The left panel shows a 1D light curve with observational data (black error bars) and a model (blue line). QhX applies wavelet transforms to convert the time-series data (either observed or modeled) into the time-frequency domain, then cross-correlates wavelet transform matrices generating a correlation density map (right) in 2D peroiod-period phase space where clusters reveal consistent periodic signals. Resulting numerical  catalogs of flagged periodic objecta are obtained after integration of density maps and application of metrics.   \label{fig:scheme}](simpleoverview.pdf)

Periodic variability can be encountered across a wide range of astronomical objects, from asteroids and stars to quasars. However, identifying meaningful signals in these variable  sources is often complicated by red noise  [see, e.g., Figure 1 in @GAIA; @Kasliwal; @Kovacevic2022], which shows fractal-like patterns across time scales [@vio91; @belete18]. This, along with the non-stationary nature of signals and often unfavorable sampling [@2018Br; @2023arXiv231016896D], makes identifying coherent signals challenging. Traditional time-frequency analysis, limited by the Fourier uncertainty principle [i.e., Gabor limit, @gabor47], struggles with these complex signals, highlighting the need for a nonlinear approach [@cohen1995time; @Abry1995] for analyzing astronomical signals like quasar light curves.

QhX_dynamical provides a robust framework with features specifically designed to address these challenges.
The first feature of `QhX_dynamical` is its core 2D Hybrid method (see Figure \ref{fig:scheme}), detailed in [@2018MNRASK], with an analogy to 2D Correlation Spectroscopy  [@NODA20] discussed in @10K. 2D Hybrid method enables a nonlinear approach (via cross-correlation), expanding detection into a two-dimensional period-period phase space. By applying wavelet transforms, QhX_dynamical maps time-series data into a time-frequency domain, then (auto)correlates it to produce a correlation density in the period-period plane, enhancing detection in red noise-dominated data.


To further ensure robust detection, QhX_dynamical uses an innovative Intersection over Union (IoU) metric alongside standard statistical measures (significance and upper and lower error bounds) to assess the overlap of detected periods across optical bands and objects.  In addition to correlation density maps, each period is visualized as the center of an "IoU ball," with a radius that represents relative error, calculated as the mean of the upper and lower error bounds—similar to a circular aperture in photometry [@Saxena2024].

The third feature of QhX_dynamical introduces a novel approach beyond traditional periodogram and wavelet transform plots by generating both numerical and interactive visual catalogs. These catalogs rank periodicity candidates by reliability, allowing for interactive inspection of signal consistency—a level of interpretability that static plots cannot achieve.


# QhX structure


![Schematic representation of the QhX package architecture.  \label{fig:QhXscheme}](QhXdiag.png)


The `QhX_dynamical` package is a modular and extensible API (see Figure \ref{fig:QhXscheme}) designed for efficient detection and analysis of periodic signals in astronomical time series data, particularly for projects like LSST. Given that astronomical data analysis often requires rapid prototyping and experimentation with various algorithms, the modular design of QhX_dynamical enables users to easily swap or modify functions, supporting diverse research needs without the constraints of a fixed class structure.

The package is organized into interconnected modules, each fulfilling a specialized role:

1. **Core Algorithms**:
   - The `algorithms` module provides essential signal-processing techniques, including the Weighted Wavelet Z-Transform (`wwtz`) and prototype superlet transforms, which enable robust analysis of continuous time series data.
   - The `correlation` function within the `utils` module supports the 2D Hybrid method by converting light curve data into wavelet matrices and performing (auto)correlation, creating correlation density maps that highlight periodicity as main diagonal clusters in the period-period phase space.

2. **Signal Detection and Validation**:
   - The `detection` module identifies candidate periodic signals and assesses their validity using statistical measures, including significance testing and error calculations, informed by methods developed with the LSST community [@2019J]. The Intersection over Union (IoU) metric is applied to ensure robust detection across bands and objects.
   - `Robovetters`, or statistical validation tools, finalize the reliability of detected periods, adding an additional layer of quality control.

3. **Data Management**:
   - The `data_manager` and `data_manager_dynamical` modules manage data flow, handling tasks like data loading, outlier removal, and format compatibility. They also support custom data loaders to process various data formats.
   - The `batch_processor` and `parallelization_solver` modules optimize task distribution across multiple processors, boosting computational efficiency for large datasets.

4. **Visualization and Output**:
   - The `plots` module includes tools for creating interactive visualizations, such as `interactive_plot`, which allows for exploring detected periodicities across bands and objects. For large datasets, `interactive_plot_large_files` enables in-depth inspection of signal consistency.
   - The `output` and `output_parallel` modules handle result storage, supporting both single-threaded and parallelized workflows.

5. **Testing and Validation**:
   - The `tests` module, with functions like `test_parallel` and `test_integrated`, validates the functionality of different components, ensuring robustness across various processing setups.

 `QhX_dynamical` (Version 0.1.0) is a standalone, open-source package designed for handling datasets with varying numbers of filters across surveys. It offers both dynamic and fixed modes, along with parallel processing capabilities for large datasets. The `dynamical_mode.py` module offers optional inclusion of observational errors, enhancing the accuracy of periodic signal detection across multiple bands.


# Representative Applications

The `QhX_dynamical` method has been applied to various studies, including:

- **Quasar Periodicity**: Investigating periodic signals in various quasars [@2018MNRASK; @2019ApJK; @2020OAstK; @2023AJF].
- **Quasi-Periodic Oscillations**: Analyzing oscillations in  quasars [@2020MNRASK].
- **Very Low-Frequency Signals**: Detecting VLF signals variability before, during and after  earthquakes [@mathKovacevic].

Additionally, the `QhX_dynamical` pipeline is listed as [a directable software in-kind contribution](https://www.lsst.org/scientists/international-drh-list) to the LSST project, highlighting its role  in the LSST.

## Documentation and Tutorials

Comprehensive documentation for `QhX_dynamical, available at [Github Pages](https://lsst-ser-sag-s1.github.io/QhX_new_dynamical/), includes several example notebooks:

- **Basic Tutorial**: Introduces the fundamentals of `QhX_dynamical` using a mock light curve, helping new users get started quickly.
- **Parallel Processing Example**: Demonstrates how to perform parallel processing with quasar light curves from the [LSST AGN Data Challenge database](https://github.com/RichardsGroup/AGN_DataChallenge), showcasing the software's capability to handle large datasets efficiently.
- **Task Distribution**: Showcases how to distribute tasks across multiple processors using the `QhX_dynamical` module, enhancing computational performance.
- **Merging Large Files**: Provides guidance on handling extensive datasets by merging large files, which is essential for high-volume data analysis.
- **Visualization of Large Datasets**: Illustrates how to visualize large files obtained from High-Performance Computing (HPC) environments, enabling effective interpretation of results.

These examples ensure users have practical guidance on effectively utilizing `QhX_dynamical` for both simple and complex analyses.






# Acknowledgements

Authors  acknowledge funding provided by the University of Belgrade - Faculty of Mathematics (the contract 451-03-66/2024-03/200104), Faculty of Sciencies University of Kragujevac (451-03-65/2024-03/200122), and Astronomical Observatory Belgrade () through the grants by the Ministry of Science, Technological Development and Innovation of the Republic of Serbia.




# References
