import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

#Iteration to plot
iteration=4999
num_walkers=5000
parameter="distance"

#Read in file
datafile="20170228-225207/output.hdf"
fp = InferenceFile("%s" % datafile, "r")

parameter_values=np.array([])

for aa in range(num_walkers):
   samples = fp.read_samples("%s" % parameter, walkers=aa)
   temp=getattr(samples,parameter)
   temp=temp[::1000]
   for bb in range(len(temp)):
      parameter_values=np.append(parameter_values,temp[bb])

plt.figure()
plt.title("%d iterations" % len(parameter_values))
plt.hist(parameter_values,50)
plt.axvline(x=100,linewidth=2,color='r')
plt.xlabel("%s" % parameter)
plt.show("hold")

