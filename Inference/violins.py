import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile
import sys
from lalsimulation import SimInspiralTransformPrecessingNewInitialConditions
from pycbc.waveform import get_td_waveform

## This code aims to produce a spectrum of violin plots. My data
## runs covering a range of inclinations or phases, so the x axis
## will be either an inclination of phase. We are looking to plot
## chi_p posteriors as a function of these parameters, so along
## the y axis we will have chi_ps

## The code needs to loop over all data segments, load the hdf
## file, extract intrinsic parameters, find derived parameters
## then plot a load of posteriors resulting from that. Give that,
## a lot of the code can be ripped from posteriors.py and extended
## given that all we are actually doing is looping over posteriors
## instead of just plotting one of them.

## Too scrubby to use the import function as of yet, next time.
## So until then I'm going to do it the noob way and just copy
## paste the functions over.
## Going to modify posteriors.py to return a numpy array that
## can be historgrammed instead of plotting the posterior directly

## These can then be fed into whatever syntax is required to plot
## the violin plots

## Going to be a good nerd and make sure the code is not hard
## coded and can take argumnents for any parameter from the
## start, not just chi_p.


## Custom parameters
prefix="close_highMR_"

## Static parameters
data_name="output.hdf"

## Functions for derived parameters
## Function to extract posterior for a given parameter
def getParameter(parameter,folder):
   folder="final/"+folder+"/"
   ## Prepare to read in parameters
   datafile=folder+data_name
   fp = InferenceFile("%s" % datafile, "r")

   ## Take last iteration of each walker
   parameter_values=np.array([])
   for aa in range(num_walkers):
      samples = fp.read_samples("%s" % parameter, walkers=aa)
      temp=getattr(samples,parameter)
      parameter_values=np.append(parameter_values,temp[-1])
   return parameter_values

def chi_effect():
   ## chi_eff is given by (S1/m1+S2/m2) dot L/M where M is total mass
   ## So for this we need m1, m2, s1_a, s2_a, s1_polar, s2_polar... fak me
   chi_eff=np.zeros(num_walkers)
   print "   Extracting intrinsic parameters..."
   ## Generate arrays for each paramter
   s1_a=getParameter("spin1_a")
   s1_polar=getParameter("spin1_polar")
   s2_a=getParameter("spin2_a")
   s2_polar=getParameter("spin2_polar")
   m1=getParameter("mass1")
   m2=getParameter("mass2")
   M=m1+m2

   ## Find spins along z-axis
   s1_z=m1*m1*s1_a*np.cos(s1_polar)
   s2_z=m2*m2*s2_a*np.cos(s2_polar)

   print "   Calculating derived parameters..."
   chi_eff=(s1_z/m1+s2_z/m2)/M
   return chi_eff

def chi_prec():
   ## chi_p is given by (1/B1m1^2)*max(B1*S1perp,B2*S2perp)
   ## with B1=2+3/2q, B2=2+3q/2
   ## so we need m1, q, s1_a, s1_polar, s2_a, s2_polar
   ## NB chi_p should always be 0 < chi_p < 1
   chi_p=np.zeros(num_walkers)
   print "   Extracting intrinsic parameters..."
   ## Generate arrays for each parameter
   s1_a=getParameter("spin1_a")
   s1_polar=getParameter("spin1_polar")
   s2_a=getParameter("spin2_a")
   s2_polar=getParameter("spin2_polar")
   mass1=getParameter("mass1")
   mass2=getParameter("mass2")
   print "   Calculating derived parameters..."
   for aa in range(len(mass1)):  ## Standard chi_p function]
      if mass1[aa]>mass2[aa]:
         ratio=mass2[aa]/mass1[aa]
         B1=2+((3*ratio)/2)
         B2=2+(3/(ratio*2))
         spin1_plane=s1_a[aa]*np.sin(s1_polar[aa])
         spin2_plane=s2_a[aa]*np.sin(s2_polar[aa])
         arg1=B1*spin1_plane*mass1[aa]*mass1[aa]
         arg2=B2*spin2_plane*mass2[aa]*mass2[aa]
         chi_p[aa]=(max(arg1,arg2))/(mass1[aa]*mass1[aa]*B1)
      else:
         ratio=mass2[aa]/mass1[aa] # Modify function for inverted mass ratio
         B1=2+((3*ratio)/2)
         B2=2+(3/(ratio*2))
         spin1_plane=s1_a[aa]*np.sin(s1_polar[aa]) # Spin1 is smaller mass this time!
         spin2_plane=s2_a[aa]*np.sin(s2_polar[aa]) # Spin2 is larger mass this time!
         arg1=B1*spin1_plane*mass1[aa]*mass1[aa]   # Swap the B coefficients now as B1 should be on the larger mass
         arg2=B2*spin2_plane*mass2[aa]*mass2[aa]
         chi_p[aa]=(max(arg1,arg2))/(mass2[aa]*mass2[aa]*B2)
   return chi_p


## Extract parameter and plot posterior
def getPosterior(parameter,folder):

   if parameter=="mchirp":
      ## Find chirp mass
      m1=getParameter("mass1")
      m2=getParameter("mass2")
      M=m1+m2
      parameter_values=((m1*m2)**(3./5.))/(M**(1./5.))

      ## Injected parameter
      m1_inj=injected["mass1"]
      m2_inj=injected["mass2"]
      M_inj=m1_inj+m2_inj
      injected_value=((m1_inj*m2_inj)**(3./5.))/(M_inj**(1./5.))

   elif parameter=="chi_eff":
      parameter_values=chi_effect()

      ## Find injected value
      m2=injected["mass2"]
      m1=injected["mass1"]
      s1a=injected["spin1_a"]
      s2a=injected["spin2_a"]
      s1_polar=injected["spin1_polar"]
      s2_polar=injected["spin2_polar"]
      s1z=m1*m1*s1a*np.cos(s1_polar)
      s2z=m2*m2*s2a*np.cos(s2_polar)
      chi_eff=(s1z/m1+s2z/m2)/(m1+m2)
      injected_value=chi_eff

   elif parameter=="chi_p":
      parameter_values=chi_prec()
      ## Derive injected value
      m1=injected["mass1"]
      m2=injected["mass1"]
      s1a=injected["spin1_a"]
      s2a=injected["spin2_a"]
      s1_polar=injected["spin1_polar"]
      s2_polar=injected["spin2_polar"]
      s1_per=m1*m1*s1a*np.sin(s1_polar)
      s2_per=m2*m2*s2a*np.sin(s2_polar)
      q=m2/m1

      ## Find Bs
      B1=2.+((q*3.)/2.)
      B2=2.+(3./(2.*q))

      chi_p=(1./(B1*m1*m1))*max((B1*s1_per,B2*s2_per))
      injected_value=chi_p

   elif parameter=="q":
      mass1=getParameter("mass1")
      mass2=getParameter("mass2")
      q=np.zeros(len(mass1))

      for aa in range(len(mass1)): ## Have to ensure 0<q<1 by making sure the larger mass is the denom
         q[aa]=min((mass1[aa]/mass2[aa]),(mass2[aa]/mass1[aa]))

      parameter_values=q
      ## Injected value
      injected_value=injected["mass2"]/injected["mass1"]

   ## Ensure m1>m2 in posteriors
   elif parameter=="mass1":
      mass1=getParameter("mass1")
      mass2=getParameter("mass2")
      parameter_values=np.zeros(len(mass1))
      for aa in range(len(mass1)):
         parameter_values[aa]=max(mass1[aa],mass2[aa])
      injected_value=max(injected["mass1"],injected["mass2"])
   ## Ensure m2>m1 in posteriors
   elif parameter=="mass2":
      mass1=getParameter("mass1")
      mass2=getParameter("mass2")
      parameter_values=np.zeros(len(mass1))
      for aa in range(len(mass1)):
         parameter_values[aa]=min(mass1[aa],mass2[aa])
      injected_value=min(injected["mass1"],injected["mass2"])

   elif parameter=="phase":
      parameter_values=getParameter("coa_phase")
      values=len(parameter_values)
      injected_value=injected[parameter]

   else:
      parameter_values=getParameter(parameter)
      values=len(parameter_values)
      injected_value=injected[parameter]

   parameter_values=np.sort(parameter_values)
   return parameter_values

## Will need to loop over hdf folders
## go a little something like

def violinMe(parameter,pref):
   for x_sample in range(1,5): ## Loop over samples of the x axis
      thisFolder=pref+x_xample  ## Select specific folder for this sample
      posterior=getPosterior(parameter,thisFolder ## Extract desired posterior from the hdf file

## Add violin plot functions - need to check documentation for this

