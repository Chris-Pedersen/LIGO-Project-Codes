import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

#Pick parameter and file
parameter="inclination"
folder="20170301-215856/"
walker=45

#Set up composite variables
data_name="output.hdf"
datafile=folder+data_name

#Read file and print out length
fp = InferenceFile("%s" % datafile, "r")
samples = fp.read_samples("%s" % parameter, walkers=walker)
temp=getattr(samples,parameter)
print temp
