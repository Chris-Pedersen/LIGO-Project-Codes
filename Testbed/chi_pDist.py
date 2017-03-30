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

mchirp=mass_samples["mchirp"]
print mchirp[1:10]


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
