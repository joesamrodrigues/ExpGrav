# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 12:06:57 2023

@author: joesa
"""
import numpy as np                         # Importing numpy
import matplotlib                          # For plotting
import matplotlib.pyplot as plt                   
from pykat import finesse                  # Importing the pykat.finesse package
from pykat.commands import *               # Importing all packages in pykat.commands.

basekat = finesse.kat()    # Initialising Finesse
basekat.verbose = False    # Tells Finesse to talk less
basecode = """
##Parameters##
const Pin 10            #laser power (10W)
const LX 2              #length of x arm (2 m)
const LY 2              #length of y arm (2 arm)

##laser and beam splitter ##
l laser $Pin 0 n0                       #laser
s s1 1 n0 nbsc                          #space from laser to beam splitter
bs BS 0.5 0.5 0 45 nbsc nbsY nbsX nbsd  #beam splitter(R=T=0.5, phi=0 deg, AoI=45 deg)

##X arm##
s LX $LX nbsX nmX1                      #space , BS to mX(2m)
m mX 0.9999 0.0001 0 nmX1 nmX2          #mirror mX(R=0.9999,T = 0.0001, phi = 0 deg)

##Y arm##
s LY $LY nbsY nmY1                      # space, BS to mY(2 m)
m mY 0.9999 0.0001 0 nmY1 nmY2          # mirror mY ( R=0.9999, T=0.0001, phi= 0 deg)

##Output port##
s sout 1 nbsd nout                      # Space, BS to output

"""
basekat.parse(basecode) #Parsing finesse code

kat1=deepcopy(basekat)
power_vs_Phi_tuning="""
pd tranAS nout              #transmitted field in the anti-symmteric port
pd tranS nbsc               #transmitted field in the symmetric port


#plotting 
xaxis mX phi lin -360 360 360 #varying the phase tuning in the end mirror mY
yaxis abs
"""
kat1.parse(power_vs_Phi_tuning)
out1=kat1.run()
fig1=out1.plot(xlabel='Phase tuning of end mirror mX[deg]',
               ylabel='Power at the AS and S port[W]',title='Power Anit-Symmetric vs. Phase tuning (Figure 1)')

'''
2a] Power at Symmetric and Anti-symmetric ports are inversly proportional to each other.
    Power at Anti-Symmetric port is at peak when the power in the Symmetric port is zero and vice-versa.

2b] 'xaxis' command is used to tune the specified parameter component into the desirable range that seems fit.
    'xaxis*' command is used to tune the specified parameter component into the desired range but this command 
    considers the previously defined range or parameter as an offset. Using asterisk does not overwrite the previous value.
    For example: 's s1 L 5 will' define the space length as 5 meters but using 'xaxis* s1 L lin 1 10 100' we can 
    change the range but this also considers the previous value as offset and adds it to the new values giving as 6 and 15 meters.
    If log is used instead of lin in the newly assigned values the previous value is multiplied to the new values.
'''

kat2 = finesse.kat()    # Initialising Finesse
kat2.verbose = False    # Tells Finesse to talk less
change_operating_point = """
##Parameters##
const Pin 10            #laser power (10W)
const LX 2              #length of x arm (2 m)
const LY 2              #length of y arm (2 arm)

##laser and beam splitter ##
l laser $Pin 0 n0                           #laser
s s1 1 n0 nbsc                              #space from laser to beam splitter
bs BS 0.5 0.5 0 45 nbsc nbsY nbsX nbsd      #beam splitter(R=T=0.5, phi=0 deg, AoI(angle of inclination)=45 deg)

##X arm##
s LX $LX nbsX nmX1                          #space , BS to mX(2m)
m mX 0.9999 0.0001 0 nmX1 nmX2              #mirror mX(R=0.9999,T = 0.0001, phi = 0 deg)

##Y arm##
s LY $LY nbsY nmY1                          # space, BS to mY(2 m)
m mY 0.9999 0.0001 90 nmY1 nmY2             # mirror mY ( R=0.9999, T=0.0001, phi= 0 deg)

##Output port##
s sout 1 nbsd nout                          # Space, BS to output

## Detectors ##
pd tranAS nout                              # transmitted field in the Anti-symmetric port
pd tranS nbsc                               #transmitted field in the symmetric port

## Simulation instructions ##

# Varying the differential arm length
xaxis mX phi lin -360 360 360               # range of phi of mX from -360 to 360 (360 steps) 
yaxis abs                                   # detector output magnitude
"""

kat2.parse(change_operating_point) # Parsing the FINESSE code
out2 = kat2.run() # Running the simulation
fig2 = out2.plot(xlabel='Phase tuning of end mirror mX[deg]',
                 ylabel='Power at the AS and S port[W]',title='Power Anit-Symmetric vs. Phase tuning (Figure 2)')

'''
I chose a phase of 90 degrees in mirror mY mirror in the arm LY because this creates 
a destructive interference with the light from the anti-symmetric port.
'''
