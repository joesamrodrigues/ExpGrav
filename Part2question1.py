# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 00:22:18 2023

@author: joesa
"""
import numpy as np                         # Importing numpy
import matplotlib                          # For plotting
import matplotlib.pyplot as plt                   
from pykat import finesse                  # Importing the pykat.finesse package
from pykat.commands import *               # Importing all packages in pykat.commands.

basekat=finesse.kat() #initialising finesse
basekat.verbose = False
basecode = """
l laser 1 0 n0 #laser (power=1W , wavelength offset=0, node 0)
s s1 1 n0 nc1 #Space (Length=1m)
m m1 0.999 0.001 0 nc1 nc2 #Mirror 1 (R1=0.999, T1=0.001, node 1, node 2)
s s2 1 nc2 nc3 # Space (Lenght=1m, node 2, node 3)
m m2 0.999 0.001 0 nc3 nc4 #Mirror 2 (R2=0.999, T2=0.001, node 3, node 4)
"""
basekat.parse(basecode) # Parsing the finesse-code


kat1=deepcopy(basekat)
plot_power_vs_tuning="""
#Photo detectors
pd refl nc1 #reflected field
pd circ nc2 #circulating field
pd tran nc4 #transmitted field

#plotting 
xaxis m2 phi lin -360 360 360 #varying the phase tuning in the end mirror m2
yaxis abs
"""
kat1.parse(plot_power_vs_tuning)
out1=kat1.run()
fig1=out1.plot(xlabel='Phase tuning of end mirror m2[deg]',
               ylabel='Power inside the cavity[Abs]',title='Power vs. Cavity tuning Fig1')


kat2=deepcopy(basekat)
plot_power_vs_tuning="""
pd refl nc1 #reflected field
pd circ nc2 #circulating field
pd tran nc4 #transmitted field

#plotting 
xaxis m2 phi lin 179.971 180.029 360 #varying the phase tuning in the end mirror m2
yaxis  abs
"""
kat2.parse(plot_power_vs_tuning)
out2=kat2.run()
fig2=out2.plot(xlabel='Phase tuning of end mirror m2[deg]',
               ylabel='Power inside the cavity[Abs]',title='Power vs. Cavity tuning Fig2')

kat3=deepcopy(basekat)
plot_power_vs_tuning="""
pd refl nc1 #reflected field
pd circ nc2 #circulating field
pd tran nc4 #transmitted field

#plotting 
xaxis m2 phi lin -360 360 360 #varying the phase tuning in the end mirror m2
yaxis log abs
"""
kat3.parse(plot_power_vs_tuning)
out3=kat3.run()
fig3=out3.plot(xlabel='Phase tuning of end mirror m2[deg]',
               ylabel='Power inside the cavity[Abs]',title='Power vs. Cavity tuning Fig3')

c=2.9979*1e8
L=1
r1=math.sqrt(0.999)
r2=math.sqrt(0.999)
FSR= c/(2*L) #Calculating the Free Spectral Range using the equation FSR=c/2L

#Calculating the Full width half maximum using FWHM=(2FSR/π)sin^-1((1-(r1r2))/(2√(r1r2)))
FWHM=(2*FSR/math.pi)*math.asin((1-(r1*r2))/(2*math.sqrt(r1*r2)))
 
fin=FSR/FWHM #Calculating Finesse using finesse=FSR/FWHM
print("Calculated FSR = ",FSR,"Hz")
print("Calculated FWHM = ", FWHM, "Hz")
print("Finesse = ",fin)

'''
Part II 1b] From the graph we see that the peaks are at 0 degree,180 degrees,360 degrees,...

            Reading from the graph in Fig 2, the distance between the half of the peak is 0.0577 degree (180.0288-179.9711).

            After calculating the FSR value using the equation FSR=c/2L, we get FSR=149895000.0 Hertz which is 180 degrees.

            If 180 degrees corresponds to 149895000.0 hertz then 0.0577 degree is 48049.675 Hz

            That is the FWHM. FWHM=48049.675 Hz
'''
