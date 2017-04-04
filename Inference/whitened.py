#! /usr/bin/env python

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

def get_ylim(data, times, tmin, tmax):
    selected = data[(times >= tmin) & (times < tmax)]
    return 1.1*selected.min(), 1.1*selected.max()


parser = argparse.ArgumentParser()
option_utils.add_inference_results_option_group(parser)
parser.add_argument('--injection-file')
parser.add_argument('--plot-map-waveforms', action='store_true', default=False)
parser.add_argument('--output-file', required=True)
opts = parser.parse_args()

fp, parameters, _, samples = option_utils.results_from_cli(opts)

fig = pyplot.figure()
ii = 0
colors = {'H1': 'r', 'L1': 'g'}
for ifo in ['H1', 'L1']:
    ii += 1
    ax = fig.add_subplot(int('21{}'.format(ii)))
    print ifo
    # get the psd
    print "loading psd"
    psd = FrequencySeries(fp['{}/psds/0'.format(ifo)][:],
        delta_f=fp['{}/psds/0'.format(ifo)].attrs['delta_f'])\
        /DYN_RANGE_FAC**2

    asd = FrequencySeries(numpy.sqrt(psd.numpy()), delta_f=psd.delta_f)
    # get the strain
    print "loading strain"
    stilde = FrequencySeries(fp['{}/stilde'.format(ifo)][:],
        delta_f=fp['{}/stilde'.format(ifo)].attrs['delta_f'],
        epoch=fp['{}/stilde'.format(ifo)].attrs['epoch'])

    print "whitening"
    wh_stilde = FrequencySeries(stilde / asd, delta_f=stilde.delta_f,
                                 epoch=stilde.epoch)
    wh_strain = wh_stilde.to_timeseries()

    # get the MAP values
    print "loading MAP values"
    llrs = fp.read_likelihood_stats(iteration=opts.iteration,
                                    thin_start=opts.thin_start,
                                    thin_end=opts.thin_end,
                                    thin_interval=opts.thin_interval)
    map_idx = (llrs.loglr + llrs.prior).argmax()
    map_values = samples[map_idx]
    varargs = fp.variable_args
    sargs = fp.static_args
    mapvals = [map_values[arg] for arg in varargs]

    print "generating map waveforms"
    genclass = waveform.select_waveform_generator(fp.static_args['approximant'])
    gen = waveform.FDomainDetFrameGenerator(
        genclass,
        detectors=['H1', 'L1'], epoch=stilde.epoch,
        variable_args=varargs,
        **sargs)
    fs = gen.generate(*map(float, mapvals))[ifo]
    if len(fs) < len(psd):
        fs.resize(len(psd))
    elif len(psd) < len(fs):
        fs = fs[:len(psd)]
    fs /= asd
    ts = fs.to_timeseries()

    print "plotting"

    try:
        gps_time = sargs['tc']
    except KeyError:
        gps_time = map_values['tc']
    xmin = -0.15 
    xmax = 0.05

    # whitened strain
    x = wh_strain.sample_times.numpy()-gps_time
    y = wh_strain
    ax.plot(x, y, colors[ifo], lw=1.5, zorder=1)
    ylim = get_ylim(y, x, xmin, xmax)

    if opts.plot_map_waveforms:
        ax.plot(ts.sample_times.numpy()-gps_time, ts.data, 'k', lw=2, zorder=2)

    if opts.injection_file:
        # get the injection values
        f = h5py.File(opts.injection_file, 'r')
        injvals = [f[p][()] for p in varargs]
        fi = gen.generate(*map(float, injvals))[ifo]
        if len(fi) < len(psd):
            fi.resize(len(psd))
        elif len(psd) < len(fi):
            fi = fi[:len(psd)]
        fi /= psd
        ti = fi.to_timeseries()
        ax.plot(ti.sample_times.numpy()-gps_time, ti.data, 'r', lw=2, zorder=2)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ylim)
    ax.set_ylabel('{} whitened strain'.format(ifo))
    if ii == 2:
        ax.set_xlabel('GPS time - {} (s)'.format(gps_time))


print varargs
print sargs
print "saving MAP values to dictionary"
MAPDic={}
for aa in range(len(varargs)):
    MAPDic[varargs[aa]]=mapvals[aa]

print "save dictionary"
savename=opts.output_file
savename=savename+"_dic"
numpy.save("%s" %  savename, MAPDic)

fp.close()
fig.savefig(opts.output_file, dpi=200, bbox_inches='tight')
