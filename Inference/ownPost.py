import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

#Select file and paramters
parameter="inclination"
folder="20170228-225207/"
injected_value=1.57

#Walker number - should be sticking with 5000
num_walkers=5000

#Combine inputs to form variables
data_name="output.hdf"
savename=folder+parameter

#Read in file
datafile=folder+data_name
fp = InferenceFile("%s" % datafile, "r")

#Take last iteration of each walker
parameter_values=np.array([])
for aa in range(num_walkers):
   samples = fp.read_samples("%s" % parameter, walkers=aa)
   temp=getattr(samples,parameter)
   parameter_values=np.append(parameter_values,temp[-1])

values=len(parameter_values)
#Plot and save
plt.figure()
plt.title("%d data points" % (values))
plt.hist(parameter_values,50)
plt.axvline(x=injected_value,linewidth=2,color='r')
plt.xlabel("%s" % parameter)
plt.savefig("%s.png" % savename)
plt.show("hold")

