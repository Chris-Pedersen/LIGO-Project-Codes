import matplotlib
matplotlib.use('Agg')
from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt
from lalsimulation import SimInspiralTransformPrecessingNewInitialConditions
import numpy as np
import sys

savename="indi"


approx1="IMRPhenomPv2"
approx2="IMRPhenomPv2"

## Masses
m1_1=55.
m2_1=15.
m1_2=55.
m2_2=15.

## Inclination
inc_1=1.55
inc_2=1.55

## Polarisation
psi_1=np.pi/2.
psi_2=np.pi/2.

## Spin parameters
s1x=0.
s1y=0.
s1z=0.
s2x=0.
s2y=0.
s2z=0.95

## Spin parameters for 2nd waveform
s1x_2=0.15
s1y_2=0.
s1z_2=0.
s2x_2=0.
s2y_2=0.
s2z_2=0.95

## Phase
phase1=np.pi
phase2=np.pi

f_low=20
sample_rate=4096

## For legend
spin_z1=np.sqrt(s1x**2+s1y**2)
spin_z1_2=np.sqrt(s1x_2**2+s1y_2**2)

# Injected waveform
hp, hc = get_td_waveform(approximant=approx1,
                      mass1=m1_1,
                      mass2=m2_1,
                      spin1y=s1y,spin1x=s1x,spin1z=s1z,
                      spin2y=s2y,spin2x=s2x,spin2z=s2z,
                      f_lower=f_low,inclination=inc_1,
                      coa_phase=phase1,
                      delta_t=1.0/sample_rate)

# MAP waveform
sp, sc = get_td_waveform(approximant=approx2,
                      mass1=m1_2,
                      mass2=m2_2,
                      spin1y=s1y_2,spin1x=s1x_2,spin1z=s1z_2,
                      spin2y=s2y_2,spin2x=s2x_2,spin2z=s2z_2,
                      f_lower=f_low,inclination=inc_2,
                      coa_phase=phase2,
                      delta_t=1.0/sample_rate)

# Mix polarisations
h=hp*np.cos(2*psi_1)+hc*np.sin(2*psi_1)
s=sp*np.cos(2*psi_2)+sc*np.sin(2*psi_2)

# Resize the waveforms to the same length
tlen = max(len(s), len(h))
s.resize(tlen)
h.resize(tlen)
# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / sp.duration
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)
# ote: This takes a while the first time as an FFT plan is generated
# subsequent calls are much faster.
# Match the waveforms
m, i = match(h, s, psd=psd, low_frequency_cutoff=f_low)

print 'The match is: %1.3f' % m
plt.figure()
plt.plot(hp.sample_times,h,'b-',label="phi = %1.2f" % phase1)
plt.plot(sp.sample_times,s,'r-',label="phi = %1.2f" % phase2)
plt.xlabel("Time (s)")
plt.ylabel("Strain")
plt.title("m1=%1.0f,m2=%1.0f,Inc=%1.2f, Match = %1.3f" % (m1_1,m2_1,inc_1,m))
plt.legend(loc="best")
plt.xlim(hp.sample_times[0],hp.sample_times[-1])
plt.savefig("Individuals/%s.png" % savename)
plt.show("hold")
