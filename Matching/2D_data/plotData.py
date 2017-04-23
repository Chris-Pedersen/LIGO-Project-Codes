import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pickle
import numpy as np

fname="phase_inc_mixed"

#Data saved in the form of x values, y values, z values
x,y,z,specs=pickle.load(open("%s.p" % fname,"rb"))
m1=specs[0]
m2=specs[1]

plt.figure()
plt.contourf(x,y,z,200,cmap="inferno")
plt.colorbar()
plt.ylabel("phase")
plt.xlabel("inclination")
plt.title("m1=%s, approx=%s" % (m1,specs[2]))
plt.show("hold")
plt.savefig("%s.png" % fname)
print "DONE"
