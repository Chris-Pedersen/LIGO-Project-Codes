import matplotlib.pyplot as plt
import pickle
import numpy as np

fname="s2_0_cross"

#Data saved in the form of x values, y values, z values
x,y,z,specs=pickle.load(open("%s.p" % fname,"rb"))
m1=specs[0]
m2=specs[1]

plt.figure()
plt.contourf(x,y,z,200,cmap="inferno")
plt.colorbar()
plt.clim(0.5,1)
plt.ylabel("Mass2")
plt.xlabel("Inclination")
plt.title("m1=%s, approx=%s" % (m1,specs[2]))
plt.show("hold")
plt.savefig("%s.png" % fname)
print "DONE"
