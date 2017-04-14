import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile
import sys

print "Initialising..."

## Select file
folder=sys.argv[1]
#parameter=sys.argv[2]
folder="final/"+folder+"/"

## Combine inputs to form variables
data_name="output.hdf"
num_walkers=5000
no_steps=50

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
   int_step=np.linspace(0,19999,no_steps)
   for bb in range(no_steps):
      int_step[bb]=int(int_step[bb])
   means=np.zeros(no_steps)
   for aa in range(no_steps): ## Loop over iterations from start to finish
      print 100*aa/no_steps
      lower=getParameter(parameter,aa) ## Earlier iteration
      upper=getParameter(parameter,aa+1) ## Later iteration
      lower=np.mean(lower) ## Mean of earlier it
      upper=np.mean(upper) ## Mean of later it
      print lower
      means[aa]=abs(lower-upper) ## Relative change in mean
   ## Plot results
   savename=folder+parameter
   plt.figure()
   plt.plot(int_step,means,'bx')
   plt.title("Convergence of %s" % parameter)
   plt.xlabel("Iteration number")
   plt.ylabel("Relative change in mean")
   plt.grid()
   plt.show("hold")
   plt.savefig("%s_conv.png" % savename)

findMeans("ra")
findMeans("dec")
