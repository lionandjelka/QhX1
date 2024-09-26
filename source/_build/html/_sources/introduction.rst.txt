Motivation
============

Variability in astronomical sources can manifest in multiple forms, intrinsic or extrinsic. Intrinsic variability may be caused by changes in the physical conditions, such as those observed in Cepheid Variables or stellar flares, or it may be accretion-induced, as seen in cataclysmic variables and Active Galactic Nuclei (AGN). Extrinsic variability, on the other hand, results from geometrical factors.

AGN, in particular, are known to exhibit variability of about 10% across various timescales, ranging from less than an hour to several years. This variability is not uniform across all AGN, presenting a wide spectrum of stochastic behavior. In response to the complex nature of the processes governing these variations, and the nonlinearity observed in quasar light curves, our package—Quasar harmonic eXplorer (QhX)—has been developed to include a method for detecting periodic variability through the cross-correlation of wavelet transforms of quasar light curves in pairs of bands.

.. image:: /_static/LSSTtimedominmining.png
   :alt: LSST time-domain mining diagram
   :align: center

Theoretical background
=======================

Quasar emission often exhibits red noise, which manifests as self-similar patterns over varying time scales. This characteristic makes it difficult to identify clear signals of quasi-periodic oscillations (QPO) or binary systems due to the Fourier uncertainty principle. To address these challenges, we have developed a pipeline for **nonlinear periodicity detection**.

Traditional periodograms transform time-domain signals into the frequency domain. While effective for stationary frequency spectra, this method falls short when handling non-stationary signals, which are common in quasar light curves. 
The cornerstone of our approach is the **2DHybrid method**. Distinct from traditional Fourier methods, the 2DHybrid technique auto or cross-correlates wavelet matrices from one or two signals, transforming them into a two-dimensional domain of period correlations. We specifically use the **Weighted Wavelet Z-transform (WWZ)**, which is highly effective in uncovering periodicities within quasar light curves. The cross-correlation of wavelet  matrices of signals, :math:`x(t)` and :math:`y(t)`, is defined by:

.. math::

   C(a, b) = \int_{-\infty}^{\infty} W_x(a, b) \cdot W_y^*(a, b) \, db

where :math:`W_x(a, b)` and :math:`W_y(a, b)` are the wavelet transforms of the signals at scale :math:`a` and translation :math:`b`. :math:`W_y^*(a, b)` denotes the complex conjugate of :math:`W_y(a, b)`. This operation introduces nonlinearity by integrating over the translation parameter :math:`b`, allowing for the detection of complex, multicomponent signals.

Additionally, the **Gabor limit** can be assessed using the WWZ transform's frequency (:math:`f`) and time (:math:`\tau`) data, ensuring the reliability of detected periodicities:

.. math::

   \hat{GL} = \Delta \tau \cdot \Delta f < \frac{1}{4\pi}

where :math:`\Delta f_i = f_{i+1} - f_i` and :math:`\Delta f = \frac{1}{m}\sum_{i=1}^{m-1} \Delta f_i`, and similarly for :math:`\Delta \tau`.

Below is the image that demonstrates the workflow of the 2DHybrid method from data input to output:

.. image:: _static/2DHybrid_method.png
   :alt: 2DHybrid method workflow
   :width: 700px
   :align: center

**Figure Description**:
The image visually outlines the 2DHybrid method used in our pipeline, from the **raw or preprocessed data** to the final **catalog of flagged periodic objects**:

1. **Raw Data or Preprocessed Data**: Displays a plot of a **1D light curve**, highlighting observed data, mean model, and confidence intervals.
2. **2DHybrid Method (Period-Period Domain)**: Shows the transformation from 1D light curves to a **2D period-period correlation plane**. It details main diagonal and off-diagonal correlation clusters, which represent potential periodic components detected by the method.
3. **Catalog of Flagged Periodic Objects**: Depicts the output as a **catalog of detected periodic objects**, listing detected periods with parameters such as name, period values, and reliability classifications.

Key Features
------------

1. Our pipeline transforms input data into a time-period plane using wavelet transforms, then (auto)correlates the resulting wavelet matrices to generate a correlation density in the period-period domain. This allows for the identification of distinct periodic components in quasar light curves, which manifest as "islands" in the correlation map. The numerical values are obtained by integrating correlation maps along one of dimensions.

2. **Intersection over Union (IoU) Metric**: We introduce the IoU metric to evaluate the overlap of detected periods across multiple bands. Alongside traditional statistical measures like significance and error margins, the IoU metric helps to quantify the confidence of each detection. Each detected period is visualized within an "IoU ball," where the radius reflects relative error, providing a clear and intuitive representation of the detected signals.

3. **Numerical and dynamic visual catalogs**: The pipeline generates comprehensive results files in both CSV and visual formats. Using HoloViews, we offer dynamic visualizations of periodicity candidates, stratified across bands based on statistical vetting, making it easier to assess and explore the results.

Performance and Scalability
---------------------------

We  tested **Quasar harmonic eXplorer (QhX)** across the **LSST AGN Data Challenge** and **GAIA DR3**. These tests were conducted on platforms ranging from the the in-house high-performance computing (HPC) stations to  **ATOS AI Platform** with four Nvidia servers and 120k cores,and personal devices, ensuring cross-platform compatibility. 

.. figure:: _static/inhouse.png
   :align: left
   :width: 50%
   :alt: Specifications of the In-House High-Performance Computing System

   **Figure: In-House HPC System Specifications**. Detailed here are the specifications of our in-house HPC system, the HPE ProLiant DL380 Gen10 server, which represents a smaller-scale, yet highly capable, computing resource. Equipped with dual Intel Xeon processors and 64GB of memory, this system supports a variety of computational tasks, ideal for preliminary testing and smaller data sets before scaling up to larger platforms.


.. figure:: _static/atos.png
   :align: left
   :width: 50%
   :alt: Specifications of the ATOS AI Platform

   **Figure: ATOS AI Platform Specifications**. Detailed here are the specifications for the NVIDIA DGX A100 320GB system utilized on the ATOS AI Platform, where our pipeline has been extensively tested. This high-performance setup includes eight NVIDIA A100 GPUs and 1TB of system memory, providing substantial computational power for large-scale machine learning and deep learning workloads.


QhX Project History
===================

Foundation of the Method and Code Functions
-------------------------------------------
- **Lead**: Andjelka Kovacevic, in-kind lead
- **Publications**:
  - `Kovacevic et al. 2018 <https://ui.adsabs.harvard.edu/abs/2018MNRAS.475.2051K/abstract>`_
  - `Kovacevic et al. 2019 <https://ui.adsabs.harvard.edu/abs/2019ApJ...871...32K/abstract>`_
  - `Kovacevic, Popovic, Ilic 2020 <https://ui.adsabs.harvard.edu/abs/2020OAst...29...51K/abstract>`_

Initial Modularization
----------------------
- **Contributor**: Viktor Radovic, former in-kind postdoc

Modules Enhancement, Expansion, Packaging, and Testing
------------------------------------------------------
- **Lead**: Andjelka Kovacevic
- **Publications**:
  - `Kovacevic et al. 2022 <https://www.mdpi.com/2227-7390/10/22/4278>`_
  - `Kovacevic 2024 (accepted)
  - `Kovacevic et al. (in prep)` 

Parallelization
---------------
- **Contributor**: Momcilo Tosic, AI guest student under the mentorship of Andjelka Kovacevic
- **Publication**:
  - `Kovacevic, Tosic, Ilic et al. (in prep)` 

Testing
-------
- **Contributors**:
  - Momcilo Tosic
  - Vuk Ostojic
  - Andjelka Kovacevic within COST Action MW GAIA STSM 2023










QhX Package Overview
====================

The QhX package is structured into several modules, each with a specific role as indicated in the architecture diagram below.

.. image:: /_static/diagram.png
   :alt: QhX package architecture diagram
   :align: center

We adopt a modular approach to ensure optimal organization, scalability, and maintainability. By segmenting functionality into distinct modules, we prioritize the separation of concerns, allowing each part of the package to focus on specific aspects of data processing or analysis. This modularity not only facilitates parallel development—enabling different teams to work on separate components simultaneously—but also enhances the scalability of our system, as individual modules can be optimized or redeveloped independently to improve performance and resource management.

Furthermore, the modular design enhances the reusability of our code. Modules crafted for particular tasks can be easily integrated across different parts of the project or reused in future projects, provided they have well-defined interfaces. This approach simplifies testing and maintenance, as each module can be tested and debugged in isolation, reducing the complexity involved in managing a large codebase. Additionally, our modular architecture offers flexibility in integration, making it straightforward to incorporate various components or third-party modules, ensuring they interact seamlessly through established interfaces.


Main Modules
------------

- **Algorithms Module**
  This module encompasses two algorithmic strategies: ``wavelets`` and ``superlets``. The ``superlets`` submodule further divides into ``superlet`` and ``superlets``.

- **Utilities Module**
  The ``utils`` module contains essential utility functions, such as ``mock_lc`` for simulating individual red noise light curves for tests and ``correlation`` for statistical correlation operations on matrices of wavelet coefficients.

- **Plots Module**
  The ``plots`` module is designed for data visualization, with components for ``interactive_plot`` and ``reg`` for interactive plotting and simple plotting of mock light curves, respectively.

Core Components
---------------

- **Light Curve Handling**
  The ``light_curve`` processes and returns light curves with an option to include magnitude errors for a given set ID.
  Also, it identifies and removes outliers from a light curve based on a Z-score threshold or Median Absolute Deviation (MAD).
  It can optionally consider errors in flux measurements for a more nuanced outlier detection.

- **Parallelization Components**
  ``parallelization_solver`` and ``iparallelization_solver`` perform parallel computations on High Performance Computing sources using the data as structured as in given examples (``parallelization_solver``) and on more generalized input (``iparallelization_solver``).

- **Detection and Calculation**
  These components, along with the ``data_manager``, form the backbone of the package's data processing capabilities. ``Calculation`` estimates the error of the determined period using the FWHM method. It also uses a 2D Hybrid method to analyze correlation data of wavelet transforms of light curves to determine periods. Significance is determined through `Johnson et al. 2018 <https://academic.oup.com/mnras/article/484/1/19/5256646>`_ method by simulating a given number of artificial red noise light curves.
  ``Detection`` compares periods detected in different bands to find common periods, if they do not differ more than 10%.
  It compiles the results, including period values, errors, and significance, into a structured format.

- **Batch Processing**
  The ``batch_processor`` and ``merge_batch_csv`` handle the processing of data obtained on HPC in batches and the merging of outputs into a single CSV file.

Output Modules
--------------

The ``output`` and ``output_parallel`` modules, although not directly connected to others in the diagram, serve as end points for the system's process flow.
The first module handles serialized data and calculates the `Intersection over Union metric <_static/IoU_metric.pdf>`_.  It also classifies individually
detected periods in band pairs as 'reliable', 'medium reliable', 'poor', or 'NAN' based on the significance of the detected period, the relative lower and
upper errors, and the IoU of the error circles provided. The second module classifies and aggregates results from batches obtained from HPC.

