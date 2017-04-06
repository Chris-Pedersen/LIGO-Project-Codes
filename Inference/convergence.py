#import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile
import sys

print "Initialising..."

## Select file
folder=sys.argv[1]
parameter=sys.argv[2]
folder="jobs/"+folder+"/"

## Combine inputs to form variables
data_name="output.hdf"
savename="convergences/convtest.png"

## Function to extract posterior for a given parameter
## at a given iteration
def getParameter(parameter,iteration):
   ## Prepare to read in parameters
   datafile=folder+data_name
   fp = InferenceFile("%s" % datafile, "r")
   
   ## Take last iteration of each walker
   parameter_values=np.array([])
   for aa in range(num_walkers):
      samples = fp.read_samples("%s" % parameter, walkers=aa)
      temp=getattr(samples,parameter)
      parameter_values=np.append(parameter_values,temp[iteration])
   return parameter_values

## Find relative change in mean for this parameter as a function of iteration
def findMeans(parameter):
   means=np.zeros(11)
   for aa in range(11): ## Loop over iterations from start to finish
      lower=getParameter(parameter,aa) ## Earlier iteration
      upper=getParameter(parameter,aa+1) ## Later iteration
      lower=np.mean(lower) ## Mean of earlier it
      upper=np.mean(upper) ## Mean of later it
      means[aa]=abs(lower-upper)/lower ## Relative change in mean
   return means
      
## Plot results
xaxis=np.linspace(1,12,11)
plt.figure()
plt.plot(xaxis,means,'bx')
plt.xlabel("Iteration number")
plt.ylabel("Relative change in mean")
plt.grid()
plt.savefig("%s" % savename)
