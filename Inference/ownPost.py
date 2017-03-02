import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile

datafile="20170228-225207/output.hdf"
parameter=mchirp

fp = InferenceFile("%s" % datafile, "r")
samples = fp.read_samples("mchirp", walkers=0)
print samples.mchirp
print len(samples.mchirp)

