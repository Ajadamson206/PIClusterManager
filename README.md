# PiClusterManager

## Installing Dependencies

Before running install **Python**, **Python Venv (Virtual Environment)**, and **Python Pip**

On **Linux** and **Mac**:

~~~~~~~~
chmod +x INSTALL.sh
./INSTALL.sh
~~~~~~~~

**NOTE: Windows is not officially supported, and is likely to not work**

On **Windows**:

~~~~~~~~
.\INSTALL.bat
~~~~~~~~

This will install all of the required python libraries

## Running the Project

After installation run

On **Linux** and **Mac**:

~~~~~~~~~~~~~~~~~~
source .venv/bin/activate
python3 cluster-manager.py -c {path to config file}
~~~~~~~~~~~~~~~~~~

On **Windows**:

~~~~~~~~~~~~~~~~~~
.venv\Scripts\activate.bat
python cluster-manager.py -c {path to config file}
~~~~~~~~~~~~~~~~~~