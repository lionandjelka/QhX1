# QhX: Quasar harmonics eXplorer

Framework for 2D Hybrid Method.

<ol>
  <li><a href="#intro">Introduction to package.</a></li>
  <li><a href="#inkind">Introduction to in-kind proposal.</a></li>
  <li><a href="#quick-links">Quick links</a></li>
</ol>

## Introduction to QhX package

The package will be separated into a few different modules:

1. In response to the inherent nonlinearity of the physical processes and signatures observed in quasar light curves, our package incorporates a method for detecting periodic variability through the cross-correlation of wavelet matrices. 2D Hybrid technique (Kovacevic et al 2018, 2019, Kovacevic et al 2020a, 2021) is based on the calculation of the Wavelet transforms of light curves (LC). These WTs are cross-correlated 𝑀 = 𝐶𝑜𝑟𝑟(𝑊𝑇(𝐿𝐶1), 𝑊𝑇(𝐿𝐶2)) and presented as 2D heatmaps (M). It is also possible to autocorrelate WT of one light curve with itself and obtain a detection of oscillations in one light curve. M provides information about the presence of coordinated or independent signals and relative directions of signal variations.

    Given a sample of quasar light curves, it provides:
    - Summary statistics, such as detected periods in at least two bands, where the reference band is the u band, with lower and upper errors, and significance.
    - Comparison statistics between detected periods in band pairs, such as Intersection over Union metric (IoU).
    - Quantification of the robustness of detected periods.
    - Numerical catalogue of objects with detected periods and flags related to robustness.
    - Visualization of numerical catalogue.

    For more information, please refer to the [documentation](https://lionandjelka.github.io/QhX1/introduction.html) for a usage guide.

## Quick Links

- [Introduction to package](#intro)
- [Introduction to in-kind proposal](#inkind)
- [Documentation](https://lionandjelka.github.io/QhX1/introduction.html)

## QhX Project History

### Foundation of the Method and Code Functions
- **Lead**: Andjelka Kovacevic, in-kind lead
- **Publications**:
  - [Kovacevic et al. 2018](https://ui.adsabs.harvard.edu/abs/2018MNRAS.475.2051K/abstract)
  - [Kovacevic et al. 2019](https://ui.adsabs.harvard.edu/abs/2019ApJ...871...32K/abstract)
  - [Kovacevic, Popovic, Ilic 2020](https://ui.adsabs.harvard.edu/abs/2020OAst...29...51K/abstract)

### Initial Modularization
- **Contributor**: Viktor Radovic, former in-kind postdoc

### Modules Enhancement, Expansion, Packaging, and Testing
- **Lead**: Andjelka Kovacevic
- **Publications**:
  - [Kovacevic et al. 2022](https://www.mdpi.com/2227-7390/10/22/4278)
  - Kovacevic 2024 (accepted)
  - Kovacevic et al. (in prep) 

### Parallelization
- **Contributor**: Momcilo Tosic, AI guest student under the mentorship of Andjelka Kovacevic
- **Publication**:
  - Kovacevic, Tosic, Ilic et al. (in prep) 

### Testing
- **Contributors**:
  - Momcilo Tosic
  - Vuk Ostojic
  - Andjelka Kovacevic within COST Action MW GAIA STSM 2023

![image](https://user-images.githubusercontent.com/78701856/191952700-d104bc04-72a4-4258-961b-2c139619e673.png)
