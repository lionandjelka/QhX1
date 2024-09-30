Installation
============

The QhX package can be installed along with its necessary dependencies using pip. Ensure that you have Python and pip installed on your system before proceeding.

Installing with pip
-------------------

You can install the package directly from PyPI  using the following command:

.. code-block:: bash

    pip install QhX

Users can install QhX by cloning its repository and installing it manually:

.. code-block:: bash

    git clone https://github.com/lionandjelka/QhX1.git
    cd QhX
    pip install .

Requirements
------------

QhX requires the following packages to be installed:

- numpy
- pandas
- scipy
- scikit-learn
- scikit-optimize
- libwwz
- colorednoise
- tqdm
- pyarrow
- panel
- hvplot
- datashader
- bokeh
- dask[dataframe]
- traitlets


These dependencies should be automatically installed when installing QhX using pip. However, if you need to install them manually, you can use the following command:

.. code-block:: bash

    pip install numpy pandas scipy scikit-learn scikit-optimize libwwz colorednoise tqdm pyarrow panel hvplot datashader bokeh dask[dataframe] traitlets


Alternatively, if you have a `requirements.txt` file in your repository, you can install all the dependencies using:

.. code-block:: bash

    pip install -r requirements.txt



After installation, you can import QhX in your Python environment to start using it.
