import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pickle
import numpy as np

fname="s2_00z_plus"
fname2="s2_98z_plus"
fname3="s2_98p_plus"

levels = np.linspace(0, 1, 200)

#Data saved in the form of x values, y values, z values
x,y,z,specs=pickle.load(open("%s.p" % fname,"rb"))
x2,y,z2,specs=pickle.load(open("%s.p" % fname2,"rb"))
x3,y,z3,specs=pickle.load(open("%s.p" % fname3,"rb"))
m1=specs[0]
m2=specs[1]

plt.figure(figsize=(10,5))
plt.subplot(1,3,1)
plt.contourf(x,y,z,200,levels=levels,cmap="inferno")
plt.ylabel("Mass2")
plt.title("Spin2=0")
plt.xlabel("Inclination")
plt.subplot(1,3,2)
plt.contourf(x2,y,z2,200,levels=levels,cmap="inferno")
plt.xlabel("Inclination")
plt.title("Spin2 Aligned")
plt.subplot(1,3,3)
plt.contourf(x3,y,z3,200,levels=levels,cmap="inferno")
plt.xlabel("Inclination")
plt.title("Spin2 in-plane")
plt.tight_layout()
plt.show("hold")
plt.savefig("multi_mr.png")
print "DONE"
