import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

#Select file and paramters
parameter="mchirp"
folder="20170302-190306/"
injected_value=0
m1=67.
m2=25.

#Walker number - should be sticking with 5000
num_walkers=5000

#Combine inputs to form variables
data_name="output.hdf"
savename=folder+parameter

#Read in file
datafile=folder+data_name
fp = InferenceFile("%s" % datafile, "r")

#Chirp mass function
def chirpMass(mass1,mass2):
   numer=(mass1*mass2)**(0.6)
   denom=(mass1+mass2)**(0.2)
   return numer/denom

if parameter=="mchirp":
   injected_value=chirpMass(m1,m2)
   print injected_value
elif parameter=="q":
   injected_value=m1/m2
   print injected_value

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

print "Plot saved as %s.png" % savename
print "DONE"
