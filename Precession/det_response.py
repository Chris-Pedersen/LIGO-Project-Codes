from matplotlib import pyplot

injection_file_name="injection.xml.gz"
ii=0
fig = pyplot.figure()


for ifo in ['H1', 'L1', 'V1','I1','K1']:
   ii+=1
   delta_t=1./2048
   fmin=20
   from pycbc import inject
   injf = inject.InjectionSet(injection_file_name)
   h = injf.make_strain_from_inj_object(injf.table[0], delta_t, ifo, f_lower=fmin)
   ax = fig.add_subplot(5,1,ii)
   ax.plot(h.sample_times.numpy(), h)
   ax.set_xlim(h.sample_times[int(len(h.sample_times)/2.)], h.sample_times[-1])
   pyplot.title("%s" % ifo)
   pyplot.ylabel("Strain")
   #pyplot.xlim(xmin,xmax)
pyplot.xlabel("GPS Time (s)")
pyplot.tight_layout()
pyplot.show("hold")
pyplot.savefig("det_strain.png")
print "Figure saved as det_strain.png"
