import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pycbc.inference import distributions
import numpy as np

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
spina_dist=distributions.Uniform(spin1_a=(0.,1.),spin2_a=(0.,1.))

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
def chi_prec(q,mass1,mass2,s1_a,s1_polar,s2_a,s2_polar):
   chi_p=np.zeros(len(q))    ## <-- convention here so 0<q<1
   for aa in range(len(q)):  ## Standard chi_p function
      mass1=m1[aa]
      mass2=m2[aa]
      if mass2>mass1:
         hold=mass2
         mass2=mass1
         mass1=hold
      B1=2+((3*q[aa])/2)
      B2=2+(3/(q[aa]*2))
      spin1_plane=s1_a[aa]*np.sin(s1_polar[aa])
      spin2_plane=s2_a[aa]*np.sin(s2_polar[aa])
      arg1=B1*spin1_plane*mass1*mass1
      arg2=B2*spin2_plane*mass2*mass2
      chi_p[aa]=(max(arg1,arg2))/(mass1*mass1*B1)
   return chi_p
chi_p=chi_prec(q,m1,m2,s1_a,s1_polar,s1_a,s2_polar)

#q=1/q ###< _________________________---REMOVE AFTER
## Plot chi_p and component masses for sanity
n_bins=50
plt.figure()
fig, axes = plt.subplots(nrows=2, ncols=2)
ax0, ax1, ax2, ax3, = axes.flat
ax0.hist(m1, bins = n_bins)
ax1.hist(chi_p, bins = n_bins)
ax2.hist(s1_polar, bins = n_bins)
ax3.hist(q, bins = n_bins)
ax0.set_title('Mass 1')
ax1.set_title('chi_p')
ax2.set_title('s1_polar')
ax3.set_title('q')
plt.tight_layout()
plt.show("hold")
plt.savefig("priors_component.png")

## Save data
