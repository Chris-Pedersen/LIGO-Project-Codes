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
sample_rate = 4096

# Load injected parameters
folder=sys.argv[1]
folder="jobs/"+folder+"/"
injname=folder+"paramDict.npy"
injected=np.load("%s" % injname).item()

# Load MAP parameters
MAPname=folder+"mapDic.npy"
maps=np.load("%s" % MAPname).item()

#Convert to precessing coords
inc_1,s1x,s1y,s1z,s2x,s2y,s2z=SimInspiralTransformPrecessingNewInitialConditions(
                      injected["theta_JN"], #theta_JN
                      0, #phi_JL << ---- not sure how to compare this with MAP..
                      injected["spin1_polar"], #theta1
                      injected["spin2_polar"], #theta2
                      0, #phi12  << ---- doesn't really affect results much
                      injected["spin1_a"], #chi1
                      injected["spin2_a"], #chi2
                      injected["mass1"]*2e30,
                      injected["mass2"]*2e30,
                      injected["inj_f_min"],phiRef=0)

# Generate injected waveform
hp, hc = get_td_waveform(approximant=approx1,
                      mass1=injected["mass1"],
                      mass2=injected["mass2"],
                      spin1y=s1y,spin1x=s1x,spin1z=s1z,
                      spin2y=s2y,spin2x=s2x,spin2z=s2z,
                      f_lower=injected["inj_f_min"],inclination=inc_1,
                      distance=injected["distance"]
                      delta_t=1.0/sample_rate)

# Find spin angles from MAP Cartesian values
s1_a=maps["spin1_a"]
s2_a=maps["spin2_a"]
s1x_map=s1_a*np.cos(maps["spin1_azimuthal"])*np.sin(maps["spin1_polar"])
s1y_map=s1_a*np.sin(maps["spin1_azimuthal"])*np.sin(maps["spin1_polar"])
s1z_map=s1_a*np.cos(maps["spin1_polar"])
s2x_map=s2_a*np.cos(maps["spin2_azimuthal"])*np.sin(maps["spin2_polar"])
s2y_map=s2_a*np.sin(maps["spin2_azimuthal"])*np.sin(maps["spin2_polar"])
s2z_map=s2_a*np.cos(maps["spin2_polar"])

# Generate MAP waveform
sp, sc = get_td_waveform(approximant=approx2,
                      mass1=maps["mass1"],
                      mass2=maps["mass2"],
                      distance=maps["distance"],
                      spin1y=s1y_map,spin1x=s1x_map,spin1z=s1z_map,
                      spin2y=s2y_map,spin2x=s2x_map,spin2z=s2z_map,
                      f_lower=19.,inclination=maps["inclination"],
                      delta_t=1.0/sample_rate)

## Mix polarisation angles
psi_1=injected["polarization"]
psi_2=maps["polarization"]
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
m, i = match(h, s, psd=psd, low_frequency_cutoff=f_low)

print 'The match is: %1.3f' % m
plt.figure()
plt.plot(hp.sample_times,hp,'b-',label="Injected")
plt.plot(sp.sample_times,sp,'r-',label="MAP waveform")
plt.xlabel("Time (s)")
plt.ylabel("Strain")
plt.title("Comparison of injected and recovered waveforms")
plt.legend(loc="best")
plt.xlim(hp.sample_times[0],hp.sample_times[-1])
plt.savefig("%s.png" % folder+"injMap")
plt.show("hold")

