import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pycbc.io import InferenceFile
import sys

print "Initialising..."

## Select file
folder=sys.argv[1]
folder="data/"+folder+"/"

## Combine inputs to form variables
data_name="output.hdf"

## Determine what parameters to plot
whatdo=raw_input("What parameters do you want to plot? \n")

## List of parameters
params=np.array(["q",
		"mchirp",
		"distance",
		"inclination",
		"polarization",
		"spin1_a",
		"spin1_polar",
		"spin2_a",
		"spin2_polar",
                "mass1",
                "mass2",
                "chi_p",
                "chi_eff"])

## Load in dictionary
dic_name="paramDict.npy"
dict_load=folder+dic_name
injected=np.load("%s" % dict_load).item()
num_walkers=int(injected["n_walkers"])
num_its=int(injected["n_its"])

## Function to extract posterior for a given parameter
def getParameter(parameter):
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

## Derive component masses from chirp mass and mass ratio
def componentMass(mass_param):
   mchirp=getParameter("mchirp")
   massratio=getParameter("q")
   q=1./massratio ## <-------- because q comes out inverted for some silly reason
   comp_mass=np.zeros(num_walkers)
   if mass_param=="mass1":
      for aa in range(num_walkers):
         comp_mass[aa]=mchirp[aa]*((1.+q[aa])**(1./5.))*(q[aa])**(2./5.)
   elif mass_param=="mass2":
      for aa in range(num_walkers):
         comp_mass[aa]=mchirp[aa]*((1.+q[aa])**(1./5.))*(q[aa])**(-3./5.)
   else:
      print "Mass parameter not recognised, you dun goofed"
   return comp_mass

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
   m1=componentMass("mass1")
   m2=componentMass("mass2")
   M=m1+m2
   
   ## Find spins along z-axis
   s1_z=m1*m1*s1_a*np.cos(s1_polar)
   s2_z=m2*m2*s2_a*np.cos(s2_polar)

   print "   Calculating derived parameters..."
   ## Do chi_eff now innit --- POTENTIAL ISSUE with L, don't have a value for it
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
   m1=componentMass("mass1")
   m2=componentMass("mass2")
   q=getParameter("q")
   q=1./q ## <<---------- mass ratio flip, only do this once

   ## Find Bs   
   B1=2.+(3./(2.*q))
   B2=2.+((3.*q)/2.)
   
   ## Find in-plane spin magnitudes
   s1_perp=m1*m1*s1_a*np.sin(s1_polar)
   s2_perp=m2*m2*s2_a*np.sin(s2_polar)

   ## Find args for max function
   arg1=B1*s1_perp
   arg2=B2*s2_perp

   print "   Calculating derived parameters..."
   ## Find chi_p now, have to loop cuz of the max function
   for aa in range(num_walkers):
      chi_p[aa]=(1./(B1[aa]*m1[aa]*m1[aa]))*max(arg1[aa],arg2[aa])
   return chi_p


## Extract parameter and plot posterior
def plotPosterior(parameter):

   if parameter=="mass1":
      parameter_values=componentMass(parameter)
      ## Also need to get injected value
      mchirp=injected["mchirp"]
      q=injected["q"]
      q=1./q ## <-- flip again, this is gonna get boring
      injected_value=mchirp*((1.+q)**(1./5.))*(q)**(2./5.)

   elif parameter=="mass2":
      parameter_values=componentMass(parameter)
      ## Also need to get injected value
      mchirp=injected["mchirp"]
      q=injected["q"]
      q=1./q ## <-- flip again, this is gonna get boring
      injected_value=mchirp*((1.+q)**(1./5.))*(q)**(-3./5.)

   elif parameter=="chi_eff":
      parameter_values=chi_effect()

      ## Find injected value
      mchirp=injected["mchirp"]
      q=injected["q"]
      q=1./q ## <-- flip again, this is gonna get boring
      m1=mchirp*((1.+q)**(1./5.))*(q)**(2./5.)
      m2=mchirp*((1.+q)**(1./5.))*(q)**(-3./5.)
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
      mchirp=injected["mchirp"]
      q=injected["q"]
      q=1./q ## <-- flip again, this is gonna get boring

      m1=mchirp*((1.+q)**(1./5.))*(q)**(2./5.)
      s1a=injected["spin1_a"]
      s2a=injected["spin2_a"]
      s1_polar=injected["spin1_polar"]
      s2_polar=injected["spin2_polar"]
      s1_per=m1*m1*s1a*np.sin(s1_polar)
      s2_per=m2*m2*s2a*np.sin(s2_polar)

      ## Find Bs   
      B1=2.+(3./(2.*q))
      B2=2.+((3.*q)/2.)

      chi_p=(1./(B1*m1*m1))*max((B1*s1_per,B2*s2_per))
      injected_value=chi_p

   elif parameter=="q":
      parameter_values=getParameter(parameter)
      parameter_values=1./parameter_values
      injected_value=injected["q"] ## Flip both of these..
      injected_value=1./injected_value

   else:
      parameter_values=getParameter(parameter)
      values=len(parameter_values)
      injected_value=injected[parameter]

   savename=folder+parameter   
   values=len(parameter_values)
   ## Find confidence intervals
   parameter_values=np.sort(parameter_values)
   lower_90=parameter_values[250]
   upper_90=parameter_values[4749]
   mean_val=np.average(parameter_values)
   
   ## Plot and save
   plt.figure()
   plt.title("%d data points" % (values))
   plt.hist(parameter_values,50)
   plt.axvline(x=injected_value,linewidth=2,color='r')
   plt.axvline(x=lower_90,linewidth=2,linestyle='dashed',color='k')
   plt.axvline(x=mean_val,linewidth=2, color='k')
   plt.axvline(x=upper_90,linewidth=2,linestyle='dashed',color='k')
   plt.xlabel("%s" % parameter)
   plt.savefig("%s.png" % savename)
   print "Plot saved as %s.png" % savename


## Execute
if whatdo=="all":
  print "Generating posteriors for all parameters..."
  for aa in range(len(params)):
    plotPosterior(params[aa])
else:
  print "Generating posterior for %s" % whatdo
  plotPosterior(whatdo)

print "DONE"
