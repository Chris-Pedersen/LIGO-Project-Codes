import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

parameter="inclination"
folder="20170228-225207/"

datafile=folder+data_name
fp = InferenceFile("%s" % datafile, "r")
samples = fp.read_samples("%s" % parameter, walkers=aa)
temp=getattr(samples,parameter)
print len(temp)
