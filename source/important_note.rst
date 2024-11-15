Important Note
==============

Distinction between QhX (Version 0.1.1) and QhX_dynamical (Version 0.1.0)
-------------------------------------------------------------------------

Both versions are standalone and can be used independently, depending on your dataset and computational requirements.

**QhX (Version 0.1.1)**
-----------------------
- Focused on analyzing datasets with consistent filter configurations.
- Ideal for static time-domain surveys where filter sets remain unchanged across observations.
- Includes tools for:
  - Photometric reverberation mapping.
  - Multi-periodicity detection within red noise environments.

**QhX_dynamical (Version 0.1.0)**
---------------------------------
- Extends the capabilities of `QhX` to support datasets with dynamic filter changes across observations.
- Fully supports fixed-mode functionalities when the mode is set to 'fixed', making it versatile for both dynamic and static datasets.
- Integrates a parallel processing solver (`ParallelSolver`) for efficient computation and handling of large datasets.
- Includes an advanced seeding mechanism for reproducibility, especially for datasets with large object IDs.

Usage Recommendations
---------------------
- **Use `QhX (0.1.1)`**: When your dataset has consistent filters across all observations and does not require dynamic processing.
- **Use `QhX_dynamical (0.1.0)`**: For flexible handling of datasets that may have variable filters or for when you prefer the option to switch between dynamic and fixed modes seamlessly.

Examples and Support for Both Modes
-----------------------------------
The usage examples in the documentation showcase how to implement both dynamic and fixed modes with `QhX_dynamical`.  Example for the **dynamical mode** of the package is given in :ref:`dynamical_mode`.

When using the fixed mode with `QhX_dynamical`, all functionalities from `QhX` (version 0.1.1) are available, providing complete compatibility and functionality in a single package.

License and Open-Source Information
-----------------------------------
Both `QhX` and `QhX_dynamical` are open-source projects licensed under the MIT License. You are free to use, modify, and distribute them under the terms of this license.


