# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:23:42 2023

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
const Pin 10                            #laser power (10W)
const LX 2                              #length of x arm (2 m)
const LY 2                              #length of y arm (2 arm)

##laser and beam splitter ##
l laser $Pin 0 n0                       #laser
s s1 0.5 n0 npr1                        #space from laser to power recycling mirror
m mpr 0.9995 0.0005 0 npr1 npr2         #power recycling mirror(R=0.9995, T=0.0005, phi=0 deg)
s s2 0.5 npr2 nbsc                      #space from power recycling mirror to beam splitter
bs BS 0.5 0.5 0 45 nbsc nbsY nbsX nbsd  #beam splitter(R=T=0.5, phi=0 deg, AoI=45 deg)

##X arm##
s LX $LX nbsX nmX1                      #space , BS to mX(2m)
m mX 0.9999 0.0001 0 nmX1 nmX2          #mirror mX(R=0.9999,T = 0.0001, phi = 0 deg)

##Y arm##
s LY $LY nbsY nmY1                      # space, BS to mY(2 m)
m mY 0.9999 0.0001 0 nmY1 nmY2          # mirror mY ( R=0.9999, T=0.0001, phi= 0 deg)

##Output port##
s sout 1 nbsd nout # Space, BS to output

"""
basekat.parse(basecode) #Parsing finesse code

kat1=deepcopy(basekat)
PR_power_vs_Phi_tuning="""
pd tranpr npr1                       #transmitted field to the laser
pd tranS  nbsc                       #power in the interferometer


#plotting 
xaxis mX phi lin -360 360 360       #varying the phase tuning in the end mirror mY
yaxis abs
"""
kat1.parse(PR_power_vs_Phi_tuning)
out1=kat1.run()
fig1=out1.plot(xlabel='Phase tuning of end mirror mX[deg]',ylabel='Power at laser & symmetric port[W]',title='Power vs. Phase tuning figure 1')

'''
3a] The correct phase of the power recycling mirror in order to get the resonant 
    enhancement of the power in the interferometer will be the odd multiples of π/2.
    As seen in the graph the power inside the interferometer is maximum at the odd multiples of π/2.
    Resonant enhancement is when the reflected light from the power recycling mirror 
    is superimposed with the incoming waves from the symmetric port.
    This in turn increases the time that the light stays inside the cavity, resonantly enhancing the power inside the interferometer.

3b] The maximum power inside the interferometer is 55700 W (from the graph).

3c] Maybe because of the thermal distortion and the limits of the materials used, losses occur. 
    That is the reason the power inside the Michelson interferometer is not infinite eventhough the laser is on most of the time.
    It also might be because of the resonant enhancement in the cavity, the cavity cannot capacitate more of the light from the laser.
    The minimum power reflected can be 
'''

kat2=deepcopy(basekat)
PR_power_vs_Phi_tuninga="""
##detector##
pd at_laser n0 #detector at laser

#plotting 
xaxis mX phi lin -360 360 360       #varying the phase tuning in the end mirror mY
yaxis abs
"""
kat2.parse(PR_power_vs_Phi_tuninga)
out2=kat2.run()
fig2=out2.plot(xlabel='Phase of the PR mirror [deg]',ylabel='Power transmitted back[W]',title='Power vs. Phase figure 2')
