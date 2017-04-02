#import matplotlib
#matplotlib.use('Agg')
from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt
from lalsimulation import SimInspiralTransformPrecessingNewInitialConditions
import numpy as np
import sys

approx1="IMRPhenomPv2"
approx2="IMRPhenomPv2"

## Select file
folder=sys.argv[1]
folder="jobs/"+folder+"/"

## Load in dictionaries
inj_name="paramDict.npy"
inj_load=folder+inj_name
injected=np.load("%s" % inj_load).item()
map_name="mapDic.npy"
map_load=folder+map_name
map_vals=np.load("%s" % map_load).item()

#Convert to precessing coords
inc_1,s1x,s1y,s1z,s2x,s2y,s2z=SimInspiralTransformPrecessingNewInitialConditions(
                      injected["theta_JN], #theta_JN
                      0, #phi_JL
                      injected["spin1_polar"], #theta1
                      injected["spin2_polar"], #theta2
                      0, #phi12
                      injected["spin1_a"], #chi1
                      injected["spin2_a"], #chi2
                      injected["mass1"]*2e30,
                      injected["mass2"]*2e30,
                      injected["inj_f_min"],phiRef=0)


# Injected waveform
hp, hc = get_td_waveform(approximant=approx1,
                      mass1=injected["mass1"],
                      mass2=injected["mass2"],
                      spin1y=s1y,spin1x=s1x,spin1z=s1z,
                      spin2y=s2y,spin2x=s2x,spin2z=s2z,
                      f_lower=f_low,inclination=inc_1,
                      delta_t=1.0/sample_rate)

# MAP waveform
sp, sc = get_td_waveform(approximant=approx2,
                      mass1=m1_2,
                      mass2=m2_2,
                      spin1y=s1y_2,spin1x=s1x_2,spin1z=s1z_2,
                      spin2y=s2y_2,spin2x=s2x_2,spin2z=s2z_2,
                      f_lower=f_low,inclination=inc_2,
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
plt.plot(hp.sample_times,hp,'b-',label="in-plane spin = %1.2f" % spin_z1)#  % approx1)
plt.plot(sp.sample_times,sp,'r-',label="in-plane spin = %1.2f" % spin_z1_2)# % approx2)
plt.xlabel("Time (s)")
plt.ylabel("Strain")
plt.title("m1=%1.0f,m2=%1.0f,Inc=%1.2f, Match = %1.3f" % (m1_1,m2_1,inc,m))
plt.legend(loc="best")
plt.xlim(hp.sample_times[0],hp.sample_times[-1])
plt.savefig("testIndi.png")
plt.show("hold")
