import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

injection_file_name="injection.xml.gz"
ii=0
fig = pyplot.figure()

xmin=-3.05
xmax=3.05

for ifo in ['H1', 'L1', 'V1']:
   ii+=1
   delta_t=1./2048
   fmin=20
   from pycbc import inject
   injf = inject.InjectionSet(injection_file_name)
   h = injf.make_strain_from_inj_object(injf.table[0], delta_t, ifo, f_lower=fmin)
   ax = fig.add_subplot(3,1,ii)
   ax.plot(h.sample_times.numpy(), h)
   ax.set_xlim(h.sample_times[int(len(h.sample_times)/2.)], h.sample_times[-1])
   pyplot.title("%s" % ifo)
   #pyplot.xlim(xmin,xmax)
pyplot.xlabel("GPS Time (s)")
pyplot.savefig("det_strain.png")
