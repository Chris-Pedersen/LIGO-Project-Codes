import numpy as np
import matplotlib.pyplot as plt

inclinations=np.linspace(0,np.pi,6)
match_H1=np.array([0.99,0.98,0.91,0.87,0.97,0.99])
match_L1=np.array([0.99,0.99,0.93,0.82,0.93,0.99])
delta_mean=np.array([0.32,0.68,0.53,0.55,0.29,0.32])

marker=10
plt.figure()
plt.plot(inclinations,match_H1,'rx',ms=marker,label="H1 match")
plt.plot(inclinations,match_L1,'gx',ms=marker,label="L1 match")
plt.plot(inclinations,delta_mean,'bx',ms=marker,label="Inference inaccuracy")
plt.xlabel("Inclination")
plt.legend(loc="best")
plt.show("hold")
