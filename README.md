# LIGO code repository
runference.sh needs to be used in conjunction with inference.ini, located in /Inference/configs. There are now two inference.inis, one in which component masses vary during the MCMC, the other in which mass ratio and chirp mass are the varying mass parameters. Inference runs auto generate their own folder named by the creation date and time, and contains the .hdf data file, a paramters.txt file containing injected values, and accompanied posteriors as .pngs

paraLoop.py and spinDegen.py generate pickled data files that can be read and plot in plotData.py, including x and y axis and axis labels. IndividualMatch.py allows two waveforms of differing paramters to be compared directly.

Testbed is where I put random shit that prob won't work but I might need to refer back to.

Variable args for MAP dictionary are:
['tc' 'mass1' 'mass2' 'spin1_a' 'spin1_azimuthal' 'spin1_polar' 'spin2_a'
 'spin2_azimuthal' 'spin2_polar' 'distance' 'coa_phase' 'inclination'
 'polarization' 'ra' 'dec']
 
Static args are:
{'delta_f': 0.0625, 'f_lower': 19.0, 'approximant': 'IMRPhenomPv2'}
