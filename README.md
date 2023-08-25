# Light_Curve_Temp_Profile

Tekano Mbonani: {mbonanits@ufs.ac.za, tekano.motsoari@gmail.com}

## System Docs

A **Python** code for fitting the flux variability of light-curves to extract flux rising and falling times. 
This is a private repository containing the project I developed for fitting the light-curves data points with exponential functions, in order to determine the temporal profiles of the variability. The goodness of the fit is assessed via the normalized Chi-squared of the model and data points.

## Software Requirements

You will need to install the following software on your system in order to run/edit the Python script.
* Mac OS/ Ubuntu 18.04 OS
* Python 3.7
* Textedit/ IDE - spyder or jupyter-notebook
* Python libraries
  * Numpy
  * Matplotlib
  * Scipy
  

### About the Data
The data used here was obtained from the ***Fermi*** Large Area Telescope (LAT) made available to the research public on https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/. The data comprise of gamma-ray (0.1-300 GeV) flux and photon energies from the blazar 3C 279, between February 16 and April 22, 2017.

### Code Output
 
 ![picture alt](https://github.com/T3kan0/Light_Curve_Temp_Profile/blob/main/3C279_Temp_Prof.png)
 ![picture alt](https://github.com/T3kan0/Light_Curve_Temp_Profile/blob/main/Opt_params.png)
