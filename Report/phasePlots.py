import matplotlib.pyplot as plt
from pycbc.waveform import get_td_waveform
inc=1.56
psi=0.
apx="IMRPhenomPv2"
hp, hc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1z=0.0,
                                 spin1x=0.2,
                                 delta_t=1.0/4096,
                                 f_lower=20)


sp, sc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1x=0.55,
                                 spin1z=0.0,
                                 delta_t=1.0/4096,
                                 f_lower=20)


gp, gc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1x=0.98,
                                 spin1z=0.0,
                                 delta_t=1.0/4096,
                                 f_lower=20)

pp, pc = get_td_waveform(approximant=apx,inclination=inc,
                                 mass1=30,
                                 mass2=10,
                                 spin1x=0.98,
                                 spin1z=0.0,
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
# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / sp.duration
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)
# ote: This takes a while the first time as an FFT plan is generated
# subsequent calls are much faster.
# Match the waveforms
m1, i = match(h, s, psd=psd, low_frequency_cutoff=f_low)
m2, i = match(g, p, psd=psd, low_frequency_cutoff=f_low)

lowlim=-2.45
plt.figure()
plt.subplot(1,2,1)
plt.title("Phase affect on precessing and non-precessing waveforms")
plt.plot(hp.sample_times, h, label="Phase=0.0")
plt.plot(sp.sample_times, s, label="Phase=1.5")
plt.ylabel('Strain')
plt.xlim(lowlim,hp.sample_times[-1])
plt.legend(loc="best")
plt.ylabel('Strain')
plt.legend(loc="best")
plt.xlim(lowlim,hp.sample_times[-1])
plt.subplot(1,2,2)
plt.plot(gp.sample_times, g, label="Phase=0.0")
plt.plot(pp.sample_times, p, label="Phase=1.5")
plt.xlabel('Time (s)')
plt.legend(loc="best")
plt.xlim(lowlim,hp.sample_times[-1])
plt.show("hold")
plt.savefig("precessfig")
