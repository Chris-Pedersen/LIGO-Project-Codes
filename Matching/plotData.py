import matplotlib.pyplot as plt
import pickle
import numpy as np

#Data saved in the form of x values, y values, z values
x,y,z,specs=pickle.load(open("precessmatch.p","rb"))
m1=specs[0]
m2=specs[1]

levels=np.array([0.97])

plt.figure()
con=plt.contour(x,y,z,1,levels=levels)
cf=plt.contourf(x,y,z,200,cmap="inferno")
plt.colorbar(cf)
plt.clabel(con)
plt.xlabel("%s" % specs[3])
plt.ylabel("%s" % specs[4])
plt.title("m1=%s,m2=%s, approx=%s" % (m1,m2,specs[2]))
plt.show("hold")

print z[5]

print "DONE"
