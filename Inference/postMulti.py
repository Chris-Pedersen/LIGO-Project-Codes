import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

## Select file
folder="20170312-113543/"

## Combine inputs to form variables
data_name="output.hdf"

## Load in dictionary
dic_name="paramDict.npy"
dict_load=folder+dic_name
injected=np.load("%s" % dict_load).item()
num_walkers=int(injected["n_walkers"])
num_its=int(injected["n_its"])

def plotPosterior(parameter):
   ## Prepare to read in parameters
   savename=folder+parameter
   datafile=folder+data_name
   fp = InferenceFile("%s" % datafile, "r")
   injected_value=injected[parameter]
   
   ## Take last iteration of each walker
   parameter_values=np.array([])
   for aa in range(num_walkers):
      samples = fp.read_samples("%s" % parameter, walkers=aa)
      temp=getattr(samples,parameter)
      parameter_values=np.append(parameter_values,temp[-1])
   values=len(parameter_values)
   
   ## Find confidence intervals
   parameter_values=np.sort(parameter_values)
   lower_90=parameter_values[250]
   upper_90=parameter_values[4749]
   
   ## Plot and save
   plt.figure()
   plt.title("%d data points" % (values))
   plt.hist(parameter_values,50)
   plt.axvline(x=injected_value,linewidth=2,color='r')
   plt.axvline(x=lower_90,linewidth=2,linestyle='dashed',color='r')
   plt.axvline(x=upper_90,linewidth=2,linestyle='dashed',color='r')
   plt.xlabel("%s" % parameter)
   plt.savefig("%s.png" % savename)
   print "Plot saved as %s.png" % savename


## Execute
plotPosterior("q")

print "DONE"
