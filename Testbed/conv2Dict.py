import numpy as np
import sys

## Import temporary file
directory=sys.argv[1]
input_address=directory+"temp_par.txt"
fname="paramDict.py"
savename=directory+fname
input_params=np.loadtxt("%s" % input_address)

## Need to compute spins, chirp mass and mass ratio and
## add them to the dictionary
paramDict={"approx":input_params[0],
			"mass1":input_params[1],
			"mass2":input_params[2],
			"ra":input_params[3],
			"dec":input_params[4]
			"inclination":input_params[5],
			"phase":input_params[6],
			"polarization":input_params[7],
			"distance":input_params[8],
			"spin1_a":s1a,
			"spin1_polar":s1_polar,
			"spin2_a":s2a,
			"spin2_polar":s2_polar,
			"n_walkers":input_params[17],
			"n_its":input_params[18],
			"detectors":input_params[19]}

## Save dictionary in folder to be read by ownPost.py
np.save("&s" & savename, paramDict)