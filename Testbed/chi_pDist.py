import matplotlib
matplotlib.use('Agg')
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
mass_dist=distributions.Uniform(q=(1.,5.),mchirp=(7.,40.))
polar_dist=distributions.SinAngle(s1_polar=(0,1),s2_polar=(0,1))
spina_dist=distributions.Uniform(spin1_a=(0.,1.),spin2_a=(0.,1.))

## Generate distribution arrays
mass_samples=mass_dist.rvs(size=dist_size)
polar_samples=polar_dist.rvs(size=dist_size)
spina_samples=spina_dist.rvs(size=dist_size)

## Mass arrays
mchirp=mass_samples["mchirp"]
q=mass_samples["q"]
q=1/q # <<--- flipping q, only do this once!!! ######

## Spin magnitudes
s1_a=spina_samples["spin1_a"]
s2_a=spina_samples["spin2_a"]

## Spin angles
s1_polar=polar_samples["s1_polar"]
s2_polar=polar_samples["s2_polar"]

## Find component masses
def getMasses(mchirp,q):
   mass1=np.zeros(len(mchirp))
   mass2=np.zeros(len(mchirp))
   for aa in range(len(mchirp)):
      mass1[aa]=mchirp[aa]*((1.+q[aa])**(1./5.))*(q[aa])**(-3./5.)
      mass2[aa]=mchirp[aa]*((1.+q[aa])**(1./5.))*(q[aa])**(2./5.))
   return mass1, mass2
m1,m2=getMasses(mchirp,q)

## Find chi_p
def chi_prec(q,mass1,mass2,s1_a,s1_polar,s2_a,s2_polar):
   chi_p=np.zeros(len(q))    ## <-- convention here so 0<q<1
   for aa in range(len(q)):  ## Standard chi_p function
      B1=2+((3*q[aa])/2)
      B2=2+(3/(q[aa]*2))
      spin1_plane=s1_a[aa]*np.sin(s1_polar[aa])
      spin2_plane=s2_a[aa]*np.sin(s2_polar[aa])
      arg1=B1*spin1_plane*m1[aa]*m1[aa]
      arg2=B2*spin2_plane*m2[aa]*m2[aa]
      chi_p[aa]=(1./(B1*m1[aa]*m1[aa]))*max(arg1,arg2)
   return chi_p
chi_p=chi_prec(q,m1,m2,s1_a,s1_polar,s1_a,s2_polar)

## Plot chi_p and component masses for sanity
print chi_p[1:10]

## Save data

'''
# We can make pairs of distributions together, instead of apart.
two_mass_distributions = distributions.Uniform(mass3=(1.6, 3.0),
                                               mass4=(1.6, 3.0))
two_mass_samples = two_mass_distributions.rvs(size=1000000)

# Choose 50 bins for the histogram subplots.
n_bins = 50

# Plot histograms of samples in subplots
fig, axes = plt.subplots(nrows=2, ncols=2)
ax0, ax1, ax2, ax3, = axes.flat

ax0.hist(mass1_samples['mass1'], bins = n_bins)
ax1.hist(mass2_samples['mass2'], bins = n_bins)
ax2.hist(two_mass_samples['mass3'], bins = n_bins)
ax3.hist(two_mass_samples['mass4'], bins = n_bins)

ax0.set_title('Mass 1 samples')
ax1.set_title('Mass 2 samples')
ax2.set_title('Mass 3 samples')
ax3.set_title('Mass 4 samples')

plt.tight_layout()
plt.savefig("distributions.png")
'''
