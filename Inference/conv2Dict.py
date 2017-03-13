import numpy as np
import sys

################################################
# Parameters are saved in the following order:
# 0 approximant
# 1 mass1
# 2 mass2
# 3 ra
# 4 dec
# 5 inclination
# 6 phase
# 7 polarisation
# 8 distance
# 9 min spin1
# 10 max spin1
# 11 min kappa1
# 12 max kappa1
# 13 min spin2
# 14 max spin2
# 15 min kappa2
# 16 max kappa2
# 17 number of walkers
# 18 number of iterations
# 19 detectors used <---- NOT YET
#################################################

## Import temporary file
directory=sys.argv[1]
input_address=directory+"/temp_par.txt"
fname="/paramDict"
savename=directory+fname
input_params=np.genfromtxt("%s" % input_address,dtype=None)

## Find chirp mass
def chirpMass(mass1,mass2):
   numer=(mass1*mass2)**(0.6)
   denom=(mass1+mass2)**(0.2)
   return numer/denom

## Determine chirp mass and mass ratio
mratio=float(input_params[1])/float(input_params[2])
chirp=chirpMass(float(input_params[1]),float(input_params[2]))

## Need to compute spins, chirp mass and mass ratio and
## add them to the dictionary

## Compute spin magnitudes (average of min and max)
s1a=np.mean(np.array([float(input_params[9]),float(input_params[10])]))
s2a=np.mean(np.array([float(input_params[13]),float(input_params[14])]))

## Spin angles
s1_kappa=np.mean(np.array([float(input_params[11]),float(input_params[12])]))
s2_kappa=np.mean(np.array([float(input_params[15]),float(input_params[16])]))
s1_polar=np.arccos(s1_kappa)
s2_polar=np.arccos(s2_kappa)

paramDict={"approx":input_params[0],
			"mass1":float(input_params[1]),
			"mass2":float(input_params[2]),
			"ra":float(input_params[3]),
			"dec":float(input_params[4]),
			"inclination":float(input_params[5]),
			"phase":float(input_params[6]),
			"polarization":float(input_params[7]),
			"distance":0.001*float(input_params[8]), #Convert from kpc to Mpc
			"spin1_a":s1a,
			"spin1_polar":s1_polar,
			"spin2_a":s2a,
			"spin2_polar":s2_polar,
			"n_walkers":float(input_params[17]),
			"n_its":float(input_params[18]),
			"mchirp":chirp,
			"q":mratio}

## Save dictionary in folder to be read by ownPost.py
np.save("%s" % savename, paramDict)
