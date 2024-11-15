Large Test Data Setup Guide
===========================

Some test data files required by this package are too large to store in the GitHub repository. Follow the instructions below to download these files from Google Drive and set them up locally.

Download the Data Files
-----------------------

Download each of the following files:

- **GaiaQSOcandsLCNobsGgt900.pqt**: Download from [Google Drive link](https://drive.google.com/file/d/1lNMh2TW8Vo1keJG4NTd67rMmNRymnEwW/view?usp=sharing)

- **qhx-batch.zip**: Download from [Google Drive link](https://drive.google.com/file/d/16lSiNCNS3pX2raATTBl9CjIcechfXWvs/view?usp=sharing)

Setting Up the Data Directory
-----------------------------

1. **Locate the `data/` Directory**

   In your local clone of the repository, navigate to the main package directory where you should see a folder named `data/`. If the folder doesn’t exist, create it using:

   .. code-block:: bash

      mkdir data

2. **Move the Downloaded Files**

   After downloading, move the files to the `data/` directory. For example:

   .. code-block:: bash

      mv /path/to/Downloads/GaiaQSOcandsLCNobsGgt900.pqt data/
      mv /path/to/Downloads/qhx-batch.zip data/

3. **Verify the Files**

   Confirm that the files are in the correct location by listing the contents of the `data/` directory:

   .. code-block:: bash

      ls data/

   You should see:

   .. code-block:: text

      GaiaQSOcandsLCNobsGgt900.pqt
      qhx-batch.zip

Automated Setup Script (Optional)
---------------------------------

Also, you can use a script to automate this setup process. Save the following as `download_data.sh` in your package directory, then run it to download the files directly into the `data/` directory.

.. code-block:: bash

   #!/bin/bash

   # Create data directory if it doesn't exist
   mkdir -p data

   # Download files from Google Drive
   curl -L -o data/GaiaQSOcandsLCNobsGgt900.pqt "https://drive.google.com/file/d/1lNMh2TW8Vo1keJG4NTd67rMmNRymnEwW/view?usp=sharing"
   curl -L -o data/qhx-batch.zip "https://drive.google.com/file/d/16lSiNCNS3pX2raATTBl9CjIcechfXWvs/view?usp=sharing"

   echo "Files downloaded and placed in the data/ directory."

Run the script:

.. code-block:: bash

   bash download_data.sh



