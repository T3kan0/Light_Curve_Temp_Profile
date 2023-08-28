# Light_Curve_Temp_Profile

Tekano Mbonani

## System Docs 📃
A **Python** code for fitting time-series data with variability, in this case the flux variability of light-curves to extract flux rising and falling times. 
This is a public repository containing the project I developed for fitting the light-curves data points with exponential functions, in order to determine the temporal profiles of the variability. The goodness of the fit is assessed via the normalized Chi-squared of the model and data points.

## Software Requirements 🔌
You will need to install the following software on your system in order to run/edit the Python script.
* Mac OS/ Ubuntu 18.04 OS
* Python 3.7
* Textedit/ IDE - spyder or jupyter-notebook
* Python libraries
  * Numpy
  * Matplotlib
  * Scipy
  

### About the Data 💾 
The data used here was obtained from the ***Fermi*** Large Area Telescope (LAT) made available to the research public on https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/. The data comprise of gamma-ray (0.1-300 GeV) integral flux and photon energies from the blazar 3C 279, between February 16 and April 22, 2017. The data was analysed by myself, following standard unbinned likelihood methods, with standard ***Fermi*** science-tools.
### Profile Model 🧮
The fitting model is build with the following exponential function:

$F(t) = F_{c} + 2F_{0} \left( e^{\frac{t_{0} - t}{t_{r}}} +  e^{\frac{t - t_{0}}{t_{f}}} \right)^{-1}$,

where $F_{c}$ is a constant baseline flux, $F_{0}$ is a profile amplitude, $t_{0}$ is the approximate maximum time, $t_{f}$ and $t_{r}$ are the profile rise and fall times. The code can fit time-series data with profiles as many as there are in the variability, then combine them with $F_{c}$. The user must provide the code with initial, guess paramaters for the profile to be fit, the user must provide all the $F_{c}$, $F_{0}$, $t_{0}$, $t_{f}$, $t_{r}$ parameters.

### Code Output 📈 
When run, the code will produce a visualization of the fitted time-series, as well as the optimized output parameters from ***scipy.optimize***, see below. Additionally, the code makes use of the output rise and fall times to determine the skewness of the exponential profile and flux doubling times, i.e.,

$t_{d} = 24ln(2)t_{r}$ (hrs).

Additionally, the code calculates the Chi-Squared from the model and time-series data points. The Chi-squared is devided by the number of degrees of freedom in the model to determine the normalized Chi-squared. The visualization shows the flux variability as well as the gamma-ray energy that escaped during the flare, the pair of results can be used to determined the gamma-ray emission Doppler factors, the sizes of the gamma-ray emission regions, and their distances from the super-massive black hole of 3C 279.
 ![picture alt](https://github.com/T3kan0/Light_Curve_Temp_Profile/blob/main/3C279_Temp_Prof.png)
 ![picture alt](https://github.com/T3kan0/Light_Curve_Temp_Profile/blob/main/Opt_params.png)
