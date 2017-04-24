import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pycbc.waveform import get_td_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower

inc=1.56
psi=0.
apx="IMRPhenomPv2"
hp, hc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1z=0.0,
                                 spin1x=0.0,
                                 delta_t=1.0/4096,
                                 coa_phase=0.0,
                                 f_lower=20)


sp, sc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1x=0.0,
                                 spin1z=0.0,
                                 coa_phase=1.5,
                                 delta_t=1.0/4096,
                                 f_lower=20)


gp, gc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1x=0.9,
                                 spin1z=0.0,
                                 coa_phase=0.0,
                                 delta_t=1.0/4096,
                                 f_lower=20)

pp, pc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1x=0.9,
                                 spin1z=0.0,
                                 coa_phase=1.5,
                                 delta_t=1.0/4096,
                                 f_lower=20)

def mixPolars(plus,cross,psi):
   return plus*np.cos(2*psi)+cross*np.sin(2*psi)
h=mixPolars(hp,hc,psi)
s=mixPolars(sp,sc,psi)
g=mixPolars(gp,gc,psi)
p=mixPolars(pp,pc,psi)


## Match bit
# Resize the waveforms to the same length
tlen = max(len(s), len(h), len(g), len(p))
s.resize(tlen)
h.resize(tlen)
g.resize(tlen)
p.resize(tlen)
f_low=20
# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / sp.duration
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)
# ote: This takes a while the first time as an FFT plan is generated
# subsequent calls are much faster.
# Match the waveforms
m1, i = match(h, s, psd=psd, low_frequency_cutoff=f_low)
m2, i = match(g, p, psd=psd, low_frequency_cutoff=f_low)

lowlim=-2.
plt.figure(figsize=(10,5))
plt.title("Phase affect on precessing and non-precessing waveforms")
plt.subplot(1,2,1)
plt.plot(hp.sample_times, h,'r-', label="Phase=0.0")
plt.plot(sp.sample_times, s,'b-', label="Phase=1.5")
plt.ylabel('Strain')
plt.text(lowlim, min(h), 'Match=%.2f' % m1, ha='left', va='bottom', fontsize=12)
plt.xlim(lowlim,hp.sample_times[-1])
plt.legend(loc="best")
plt.ylabel('Strain')
plt.legend(loc="best")
plt.xlim(lowlim,hp.sample_times[-1])
plt.subplot(1,2,2)
plt.plot(gp.sample_times, g,'r-', label="Phase=0.0")
plt.plot(pp.sample_times, p,'b-', label="Phase=1.5")
plt.xlabel('Time (s)')
plt.text(lowlim, min(g), 'Match=%.2f' % m2, ha='left', va='bottom', fontsize=12)
plt.legend(loc="best")
plt.xlim(lowlim,hp.sample_times[-1])
plt.tight_layout()
plt.show("hold")
plt.savefig("phasefig.png")
