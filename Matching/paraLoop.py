from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
from lalsimulation import SimInspiralTransformPrecessingNewInitialConditions
import matplotlib.pyplot as plt
import numpy as np
import pickle

## Static parameters
savename="testdata.p"
approx="IMRPhenomPv2"
approx1="IMRPhenomPv2"
approx2="IMRPhenomPv2"
f_low = 25
sample_rate = 4096
savename="test.p"
mass1=45
mass2=40
MSUN_SI=1
## Parameter arrays
par1=np.linspace(45,46.99,100) # x axis
par1name="Parameter 1"
par2=np.linspace(25,55,100) # y axis
par2name="Parameter 2"
matchGrid=np.zeros((100,100))

## Spin parameters
phi_JL=0 ## Polarisation angle perhaps?
theta_z1=1.57
theta_z2=1.57
spin_z1=0
spin_z2=0
phi12=0 ## Don't know what parameter this is

## Save parameters for the plot axes and future reference
specs=np.array([mass1,mass2,approx,par1name,par2name])

def match_inc(par1,par2):
   # Allow masses to vary as parameters
   m1_1=par1
   m2_1=mass2
   m1_2=mass1
   m2_2=par2
   # Convert to precessing coords
   inc_1,s1x,s1y,s1z,s2x,s2y,s2z=SimInspiralTransformPrecessingNewInitialConditions(
                         0, #theta_JN
                         phi_JL, #phi_JL
                         theta_z1, #theta1
                         theta_z2, #theta2
                         phi12, #phi12
                         abs(spin_z1), #chi1
                         abs(spin_z2), #chi2
                         m1_1,
                         m2_1,
                         f_low,phiRef=0)

   inc_2,s1x_2,s1y_2,s1z_2,s2x_2,s2y_2,s2z_2=SimInspiralTransformPrecessingNewInitialConditions(
                         0, #theta_JN
                         phi_JL, #phi_JL
                         theta_z1, #theta1
                         theta_z2, #theta2
                         phi12, #phi12
                         abs(spin_z1), #chi1
                         spin_z2, #chi2
                         m1_2,
                         m2_2,
                         f_low,phiRef=0)

   # Generate the two waveforms to compare
   hp, hc = get_td_waveform(approximant=approx1,
                         mass1=m1_1,
                         mass2=m2_1,
                         spin1y=s1y,spin1x=s1x,spin1z=s1z,
                         spin2y=s2y,spin2x=s2x,spin2z=s2z,
                         f_lower=f_low,inclination=inc_1,
                         delta_t=1.0/sample_rate)
   sp, sc = get_td_waveform(approximant=approx2,
                         mass1=m1_2,
                         mass2=m2_2,
                         spin1y=s1y_2,spin1x=s1x_2,spin1z=s1z_2,
                         spin2y=s2y_2,spin2x=s2x_2,spin2z=s2z_2,
                         f_lower=f_low,inclination=inc_2,
                         delta_t=1.0/sample_rate)
   # Resize the waveforms to the same length
   tlen = max(len(sp), len(hp))
   sp.resize(tlen)
   hp.resize(tlen)
   # Generate the aLIGO ZDHP PSD
   delta_f = 1.0 / sp.duration
   flen = tlen/2 + 1
   psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)
   # Note: This takes a while the first time as an FFT plan is generated
   # subsequent calls are much faster.
   m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
   #print 'The match is: %1.3f' % m
   return m

for aa in range(len(par1)):
   for bb in range(len(par2)):
       matchGrid[bb][aa]=match_inc(par1[aa],par2[bb])

#Prepare data for savings
data=list([0,0,0,0])
data[0]=par1 # x axis
data[1]=par2 # y axis
data[2]=matchGrid
data[3]=specs
pickle.dump(data,open("%s" % savename,"wb"))
print "Data saved as %s" % savename

print "DONE"
