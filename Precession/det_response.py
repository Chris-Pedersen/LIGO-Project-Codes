import h5py
import copy
import argparse
from pycbc import DYN_RANGE_FAC, pnutils
from pycbc.io import InferenceFile
from pycbc.inference import option_utils
from pycbc.types import TimeSeries, FrequencySeries
from pycbc import strain as pystrain
from pycbc import waveform
import numpy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from pycbc.filter import match

parser = argparse.ArgumentParser()
parser.add_argument('--injection-file')
parser.add_argument('--output-file', required=True)
opts = parser.parse_args()

        
colors = {'H1': 'r', 'L1': 'g'}
for ifo in ['H1', 'L1']:
   injf = inject.InjectionSet(opts.injection_file)
   ti = injf.make_strain_from_inj_object(injf.table[0], wh_strain.delta_t, ifo, f_lower=gen.current_params['f_lower'])
   fi = ti.to_frequencyseries(delta_f=gen.current_params['delta_f'])
   if len(fi) < len(psd):
      fi.resize(len(psd))
   elif len(psd) < len(fi):
      fi = fi[:len(psd)]
   fi /= asd
   ti = fi.to_timeseries()
   ax.plot(ti.sample_times.numpy()-gps_time, ti.data, 'b-', lw=2, zorder=2)
   #ax.set_xlim(xmin, xmax)
   #ax.set_ylim(ylim)
   ax.set_ylabel('{} whitened strain'.format(ifo))
   #if ii == 2:
   #   ax.set_xlabel('GPS time - {} (s)'.format(gps_time))
