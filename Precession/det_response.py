import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

injection_file_name="injection.xml.gz"
ii=0
fig = pyplot.figure()

xmin=-0.5
xmax=0.05

for ifo in ['H1', 'L1', 'V1']:
   ii+=1
   delta_t=1./2048
   fmin=20
   from pycbc import inject
   injf = inject.InjectionSet(injection_file_name)
   h = injf.make_strain_from_inj_object(injf.table[0], delta_t, ifo, f_lower=fmin)
   ax = fig.add_subplot(5,1,ii)
   ax.set_xlim(xmin, xmax)
   ax.plot(h.sample_times.numpy(), h)
   pyplot.title("%s" % ifo)
   #pyplot.xlim(-0.5,0.05)
pyplot.savefig("det_strain.png")
