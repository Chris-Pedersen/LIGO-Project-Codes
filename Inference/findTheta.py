from lalsimulation import SimInspiralTransformPrecessingNewInitialConditions
import numpy as np

## Input parameters
theta=0.
phi_JL_=0.
theta_z1=np.pi/2
theta_z2=0.
phi12=0.
spin_z1=0.9
spin_z2=0.
m1=30
m2=15
f_low=25


#Convert to precessing coords
inc_1,s1x,s1y,s1z,s2x,s2y,s2z=SimInspiralTransformPrecessingNewInitialConditions(
                      inc, #theta_JN
                      phi_JL, #phi_JL
                      theta_z1, #theta1
                      theta_z2, #theta2
                      phi12, #phi12
                      abs(spin_z1), #chi1
                      abs(spin_z2), #chi2
                      m1,
                      m2,
                      f_low,phiRef=0)

s1_a=np.sqrt(s1x**2+s1y**2+s1z**2)
s1_plane=np.sqrt(s1x**2+s1y**2)
s1_polar=np.arctan(s1z/s1_plane)
s1_polar=np.pi/2.-s1_polar

s2_a=np.sqrt(s2x**2+s2y**2+s2z**2)
s2_plane=np.sqrt(s2x**2+s2y**2)
s2_polar=np.arctan(s2z/s2_plane)
s2_polar=np.pi/2.-s2_polar

print "Inclination: %s \n" % inc_1
print "Spin1 magnitude: %s \n"" % s1_a
print "Spin1 polar: %s \n"" % s1_polar
print "Spin2 magnitude: %s \n"" % s2_a
print "Spin2 polar: %s \n" % s2_polar
