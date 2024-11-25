Important Note
==============


QhX Version 0.2.0 
-------------------------------------
- Fully supports datasets with dynamic filter changes across observations. `dynamical_mode`  module  handles both dynamic and fixed configurations, enabling more complex workflows. Combining both modes in a single module allows easier upgrades if workflows evolve from fixed to dynamic or need to accommodate hybrid datasets.
- Some service modules outside `dynamical_mode` are dedicated to fixed-only workflows, providing less overhead in performance while retaining efficiency. 
- Integrates a parallel processing solver (``ParallelSolver``) to efficiently handle large datasets and computationally intensive tasks.
- Includes an advanced seeding mechanism for reproducibility, particularly for datasets with large object IDs.

Examples and Support for Both Modes
-----------------------------------
This documentation provides examples demonstrating the usage of both **dynamic** and **fixed** modes of ``QhX_dynamical``. For an example of the **dynamic mode**, refer to :ref:`dynamical_mode`.

License and Open-Source Information
-----------------------------------
``QhX`` is an open-source project licensed under the **MIT License**. You are free to use, modify, and distribute it in accordance with the terms of this license.

