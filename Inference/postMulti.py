import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile
import sys

## Select file
folder=sys.argv[1]
folder=folder+"/"

## Combine inputs to form variables
data_name="output.hdf"

## Determine what parameters to plot
whatdo=raw_input("What parameters do you want to plot? \n")

## List of parameters
params=np.array(["q",
		"mchirp",
		"distance",
		"inclination",
		"polarization",
		"spin1_a",
		"spin1_polar",
		"spin2_a",
		"spin2_polar"])

## Load in dictionary
dic_name="paramDict.npy"
dict_load=folder+dic_name
injected=np.load("%s" % dict_load).item()
num_walkers=int(injected["n_walkers"])
num_its=int(injected["n_its"])

## Function to extract posterior for a given parameter
def getParameter(parameter):
   ## Prepare to read in parameters
   savename=folder+parameter
   datafile=folder+data_name
   fp = InferenceFile("%s" % datafile, "r")
   
   ## Take last iteration of each walker
   parameter_values=np.array([])
   for aa in range(num_walkers):
      samples = fp.read_samples("%s" % parameter, walkers=aa)
      temp=getattr(samples,parameter)
      parameter_values=np.append(parameter_values,temp[-1])
   return parameter_values

## Derive component masses from chirp mass and mass ratio
def componentMass(mass_param):
   mchirp=getParameter("mchirp")
   massratio=getParameter("q")
   massratio=1/massratio ## <-------- because q comes out inverted for some silly reason
   comp_mass=np.zeros(num_walkers)
   if mass_param=="mass1":
      for aa in range(num_walkers):
         comp_mass[aa]=mchirp[aa]*((1+q[aa])^(1./5.))*(q[aa])^(2./5.)
   elif mass_param=="mass2":
      for aa in range(num_walkers):
         comp_mass[aa]=mchirp[aa]*((1+q[aa])^(1./5.))*(q[aa])^(-3./5.)
   else:
      print "Mass parameter not recognised, you dun goofed"
   return comp_mass

## Extract parameter and plot posterior
def plotPosterior(parameter):
   if parameter=="mass1":
      do this
   elif parameter=="mass2":
      do this
   elif parameter=="chi_eff":
      do this
   elif parameter=="chi_p":
      do this
   else:
      parameter_values=getParameter(parameter)
      values=len(parameter_values)
      injected_value=injected[parameter]
   
   ## Find confidence intervals
   parameter_values=np.sort(parameter_values)
   lower_90=parameter_values[250]
   upper_90=parameter_values[4749]
   mean_val=np.average(parameter_values)
   
   ## Plot and save
   plt.figure()
   plt.title("%d data points" % (values))
   plt.hist(parameter_values,50)
   plt.axvline(x=injected_value,linewidth=2,color='r')
   plt.axvline(x=lower_90,linewidth=2,linestyle='dashed',color='k')
   plt.axvline(x=mean_val,linewidth=2, color='k')
   plt.axvline(x=upper_90,linewidth=2,linestyle='dashed',color='k')
   plt.xlabel("%s" % parameter)
   plt.savefig("%s.png" % savename)
   print "Plot saved as %s.png" % savename


## Execute
if whatdo=="all":
  print "Generating posteriors for all parameters..."
  for aa in range(len(params)):
    plotPosterior(params[aa])
else:
  print "Generating posterior for %s" % whatdo
  plotPosterior(whatdo)

print "DONE"
