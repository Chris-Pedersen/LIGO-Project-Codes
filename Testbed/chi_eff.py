import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pycbc.inference import distributions
import numpy as np
from numpy import random

#############################
# Need distributions for
# mass1 - uniform
# mass2 - uniform
# spin1_a - uniform
# spin1_polar - sinAngle
# spin2_a - uniform
# spin2_polar - sinAngle
#############################

dist_size=1000000

## Create distribution classes
mass_dist=distributions.Uniform(mass1=(1.,80.),mass2=(1.,80.))
polar_dist=distributions.SinAngle(s1_polar=(0,1),s2_polar=(0,1))
spina_dist=distributions.Uniform(spin1_a=(0.,.9),spin2_a=(0.,.9))

## Generate distribution arrays
mass_samples=mass_dist.rvs(size=dist_size)
polar_samples=polar_dist.rvs(size=dist_size)
spina_samples=spina_dist.rvs(size=dist_size)

## Spin magnitudes
s1_a=spina_samples["spin1_a"]
s2_a=spina_samples["spin2_a"]

## Spin angles
s1_polar=polar_samples["s1_polar"]
s2_polar=polar_samples["s2_polar"]
m1=mass_samples["mass1"]
m2=mass_samples["mass2"]
q=np.zeros(len(m1))

for aa in range(len(m1)):
   q[aa]=min(m1[aa]/m2[aa],m2[aa]/m1[aa])

## Find chi_p
def chi_e(mass1,mass2,s1_a,s1_polar,s2_a,s2_polar):
   M=mass1+mass2
   ## Find parallel spins
   s1_L=mass1*s1_a*np.cos(s1_polar)
   s2_L=mass2*s2_a*np.cos(s2_polar)
   return (s1_L+s2_L)/M
   

chi_eff=chi_e(m1,m2,s1_a,s1_polar,s2_a,s2_polar)

#q=1/q ###< _________________________---REMOVE AFTER
## Plot chi_p and component masses for sanity
n_bins=50
fig, axes = plt.subplots(nrows=4, ncols=2)
ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7 = axes.flat
ax0.hist(m1, bins = n_bins)
ax1.hist(m2, bins = n_bins)
ax2.hist(s1_polar, bins = n_bins)
ax3.hist(s1_a, bins = n_bins)
ax4.hist(s2_polar, bins = n_bins)
ax5.hist(s2_a, bins = n_bins)
ax6.hist(q, bins = n_bins)
ax7.hist(chi_eff, bins = n_bins)
ax0.set_title('Mass 1')
ax1.set_title('Mass 2')
ax2.set_title('s1_polar')
ax3.set_title('s1_a')
ax4.set_title('s2_polar')
ax5.set_title('s2_a')
ax6.set_title('q')
ax7.set_title('chi_eff')
plt.tight_layout()
plt.show("hold")
plt.savefig("priors_component.png")
print "DONE and plot saved"

## Save data
np.savetxt("chi_eff_prior.txt",chi_eff)
