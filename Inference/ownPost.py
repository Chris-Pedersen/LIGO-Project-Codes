import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

#Select file and paramters
parameter="distance"
folder="20170228-225207/"

#Iteration range to sample
it_start=9950
it_end=9999
num_walkers=5000

#Combine inputs to form variables
data_name="output.hdf"
savename=folder+parameter

#Read in file
datafile=folder+data_name
print datafile
fp = InferenceFile("%s" % datafile, "r")

parameter_values=np.array([])

for aa in range(num_walkers):
   samples = fp.read_samples("%s" % parameter, walkers=aa)
   temp=getattr(samples,parameter)
   temp=temp[it_start:it_end]
   for bb in range(len(temp)):
      parameter_values=np.append(parameter_values,temp[bb])

values=len(parameter_values)

plt.figure()
plt.title("Iterations %d to %d; %d data points" % (it_start,it_end,values))
plt.hist(parameter_values,50)
plt.axvline(x=100,linewidth=2,color='r')
plt.xlabel("%s" % parameter)
plt.savefig("%s.png" % savename)
plt.show("hold")

