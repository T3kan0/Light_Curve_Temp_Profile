#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:34:59 2020

@author: tekano
"""


#Import python library

import matplotlib.pyplot as plt # for visuals
import numpy as np # data preparation
from scipy.optimize import curve_fit # fitting library
#matplotlib.use('Qt5Agg')


#Upload the data

gamma = np.genfromtxt('3C279_2017_phaseII_12h_LC.asc', 
                      names = True,
                      autostrip=True, 
                      delimiter = '')

HE_Phot = np.genfromtxt('HE_0.75deg_evclass512_10GeV_gtsrcprob_LP_P8_UFS.txt', 
                        names = True, 
                        autostrip=True, 
                        delimiter = '')

# Functions for the individual exponential peaks/profiles, as well as for combining them to get the aggregated fit.
    
def peak(t, t0, F0, Tr, Tf): # Individual expo profiles
    

    exp = (2 * F0 / 
               (np.exp((t0 - t)/Tr) +
                np.exp((t - t0)/Tf)))
    return exp


def combine_peaks(t, *params):  # Combining profles
    params_nd = np.array(params).flatten()
#    print(params_nd)
    p_par = params_nd[1:].reshape(-1, 4)
    lc = np.zeros(shape=len(t))
#    print(params_nd[0])
    lc += params_nd[0]
    for i in p_par:
        lc += peak(t, i[0], i[1], i[2], i[3])
    
    return lc

# Data preparation

gamma = np.sort(gamma, order = 'MID_MJD')
mask = (gamma['MID_MJD'] >= 57823.75) & (gamma['MID_MJD'] <= 57855.25)
gammadat = gamma[mask]

# User input params: These are the initial/assumed parameters for the model.
params = np.array([57829.00, 1.0e-06, 1.0, 1.0],
                  [57834.10, 2.10e-06, 1.0, 1.10],
                  [57844.50, 4.50e-06, 0.4, 0.7],
                  [57845.50, 3.5e-06, 0.6, 0.1],
                  [57849.00, 4.2e-06, 0.6, 0.7],
                  [57851.10, 2.9e-06, 0.4, 0.7]
                   ])
params_f = params.flatten()
params_f = np.concatenate([[0.40e-6], params_f])

# Data Visualization

fig, (ax0, ax1) = plt.subplots(2, 1,
     sharex=True,
     gridspec_kw = {'height_ratios':[8.5,
                                     8.0],
                    'hspace': 0.15},
                     figsize=(8.5, 7))
ax0.axhline(params_f[0])
uplim = (gammadat['FitStat'] != 0) | (gammadat['NPRED'] <= 3.0)
gammadat['FluxErr'][uplim] = 5e-07
ax0.errorbar(gammadat['MID_MJD'],
                y=gammadat['Flux'],
                 yerr=gammadat['FluxErr'],
                 uplims=uplim,
                 fmt='o', 
                 c='black',
                 ms=1.3,
                 label = 'LAT')
ax0.ticklabel_format(style='sci', axis = 'y', scilimits = (0,0),
                         useMathText=True)
ax0.yaxis.offsetText.set_visible(True)
ax0.set_ylabel('F$_{\gamma}$ \n [' +
                   ax0.yaxis.get_offset_text().get_text() +
                   'ph cm$^{-2}$ s$^{-1}$]', fontsize= 14)
legends = ax0.legend(loc='upper left', shadow=False, fontsize='large')
legends.get_frame().set_facecolor('white')
plt.draw()
ax0.tick_params(axis='both', which='major', labelsize=13)

t_mask = (HE_Phot['TIME'] >= 57823.75) & (HE_Phot['TIME'] <= 57855.25)
HE_Phot = HE_Phot[t_mask]

mask5 = (HE_Phot['PROB'] <= 0.954500)
mask6 = ((HE_Phot['PROB'] > 0.954500) & (HE_Phot['PROB'] <= 0.997300))
mask7 = ((HE_Phot['PROB'] > 0.997300) & (HE_Phot['PROB'] <= 0.999958))
mask8 = (HE_Phot['PROB'] > 0.999958)

HE_Phot1 = HE_Phot[mask5]
HE_Phot2 = HE_Phot[mask6]
HE_Phot3 = HE_Phot[mask7]
HE_Phot4 = HE_Phot[mask8]

#print(np.average(HE_Phot4['E']), np.max(HE_Phot4['E']))

ax1.errorbar(HE_Phot2['TIME'],
                 y=HE_Phot2['E']/1000,
                 #yerr=opt['Flux_R_err'],
                 fmt='o', 
#                 uplims=up_lim,
                 c='blue',
                 ms=3.0,
                 label = '> 95.4500 % C.L.')

ax1.errorbar(HE_Phot3['TIME'],
                 y=HE_Phot3['E']/1000,
                 #yerr=opt['Flux_R_err'],
                 fmt='o', 
#                 uplims=up_lim,
                 c='green',
                 ms=3.0,
                 label = '> 99.7300 % C.L.')

ax1.errorbar(HE_Phot4['TIME'],
                 y=HE_Phot4['E']/1000,
                 #yerr=opt['Flux_R_err'],
                 fmt='o', 
#                 uplims=up_lim,
                 c='red',
                 ms=3.0,
                 label = '> 99.9958 % C.L.')

ax1.ticklabel_format(style='sci', axis = 'y', scilimits = (-3,3),
                         useMathText=True)
legends = ax1.legend(loc='upper left', shadow=False, fontsize='large')
legends.get_frame().set_facecolor('white')
plt.draw()
ax1.yaxis.offsetText.set_visible(True)
ax1.set_ylabel('Photon Energy (GeV)', 
#               ax2.yaxis.get_offset_text().get_text() +
               fontsize= 14)
ax1.tick_params(axis='both', which='major', labelsize=13)

# Fitting and Optimization of the model.

popt, pcov = curve_fit(combine_peaks,
                       gammadat['MID_MJD'],
                       gammadat['Flux'],
                       sigma=gammadat['FluxErr'],
                       p0=params_f,
                       absolute_sigma = True)


new_mjd = np.linspace(gammadat['MID_MJD'][0], 
                      gammadat['MID_MJD'][-1], 
                      10000)

fit = combine_peaks(new_mjd, 
                    popt) # Fitting the curves

chisq = sum(((gammadat['Flux'] 
              - combine_peaks(gammadat['MID_MJD'], 
                              popt)) / gammadat['FluxErr'])**2) # Chi-square of the fit.

ndf = len(gammadat['Flux']) - (4*6 + 1) 
norm_chisq = chisq / ndf # Normalized Chi-squared.

a = popt[1:].reshape(-1, 4)

dbl_time = np.log(2)*24*a[:,2]

tps = a[:,0] + (a[:,2]*a[:,3] / (a[:,2] + a[:,3])
                ) * np.log(a[:,3] / a[:,2])

skw_param = (a[:,3] - a[:,2])/(a[:,3] + a[:,2])  

# A look at the optimized parameters.

print('baseline Flux', popt[0], '\n', 'baseline FluxErr', np.sqrt(np.diag(pcov))[0])
print('optimized params', '\n', popt[1:].reshape(-1, 4))
print('optimized params error', '\n', np.sqrt(np.diag(pcov))[1:].reshape(-1, 4))
print('Skewness Parameters', '\n', skw_param)
print('doublng times', '\n' , dbl_time.reshape(1, 6))
print('peak_MJDs', '\n', tps)
print('chi-square:', chisq, '\n', 'ndf', ndf)
print('reduced chisq:', norm_chisq)

# Model Visualization

ax0.plot(new_mjd, fit, linestyle = 'solid', linewidth=2.0)
#plt.figtext(0.62, 0.82, 'Norm Chisq: %.2f'%norm_chisq, fontweight = 'bold')
for idx, i in enumerate(popt[1:].reshape(-1, 4)):
    test_2 = peak(new_mjd, i[0], i[1], i[2], i[3])
    ax0.plot(new_mjd, test_2, linestyle = 'solid', linewidth=0.5, label=('peak' + str(idx+1)))

ax1.set_xlabel('Time (MJD)', fontsize = 14)
plt.show()



















