Introduction
============

Variability in astronomical sources can manifest in multiple forms, intrinsic or extrinsic. Intrinsic variability may be caused by changes in the physical conditions, such as those observed in Cepheid Variables or stellar flares, or it may be accretion-induced, as seen in cataclysmic variables and Active Galactic Nuclei (AGN). Extrinsic variability, on the other hand, results from geometrical factors.

AGN, in particular, are known to exhibit variability of about 10% across various timescales, ranging from less than an hour to several years. This variability is not uniform across all AGN, presenting a wide spectrum of stochastic behavior. In response to the complex nature of the processes governing these variations, and the nonlinearity observed in quasar light curves, our package—Quasar harmonic eXplorer (QhX)—has been developed to include  a method for detecting periodic variability through the cross-correlation of wavelet transforms of quasar light curves in pairs of bands.

.. image:: /_static/LSSTtimedominmining.png
   :alt: descriptive text for image
   :align: center


Package Architecture
--------------------

High-Level Architecture consists of data_manager, light_curve, core, output, and auxiliary modules.  
Below, Figure illustrates the modular structure of the QhX package. Data management is handled by the data_manager module, which is responsible for loading, grouping, and retrieving data. The light_curve module processes this data and feeds it into the core analytical components, calculation and detection, within the core module. Results from the core processing are then passed to the output module for classification. The algorithms module contains complex analytical tools like wavelet transforms and superlet calculations, supported by plots and utils as auxiliary modules for visualization and utility functions, respectively. Together, these interconnected modules form the backbone of QhX's functionality.

.. image:: /_static/diagram.png
   :alt: descriptive text for image
   :align: center

The purpose of this documentation is to guide users through the features and functionalities of QhX, facilitating the exploration and analysis of quasar light curves with an emphasis on periodic variability detection and analysis.
