# define coalescence time, observed masses, and waveform parameters
TRIGGER_TIME=1126259462.0
INJ_APPROX=IMRPhenomPv2threePointFivePN
MASS1=55.
MASS2=10.
RA=2.21535724066
DEC=-1.23649695537
THETA_JN=1.25
## Inclination calculated manually currently using findTheta.py
INC=2.2
COA_PHASE=1.5
POLARIZATION=0.9
DISTANCE=200000 # in kpc
INJ_F_MIN=20.
TAPER="start"

# Spin parameters
MIN_SPIN1=0.9
MAX_SPIN1=0.9
MIN_KAPPA1=0.0
MAX_KAPPA1=0.0
MIN_SPIN2=0.0
MAX_SPIN2=0.0
MIN_KAPPA2=0.9
MAX_KAPPA2=0.9

# path of injection file that will be created in the example
INJ_PATH=injection.xml.gz


# lalapps_inspinj requires degrees on the command line
LONGITUDE=`python -c "import numpy; print ${RA} * 180/numpy.pi"`
LATITUDE=`python -c "import numpy; print ${DEC} * 180/numpy.pi"`
INC_inj=`python -c "import numpy; print ${INC} * 180/numpy.pi"`
POLARIZATION_inj=`python -c "import numpy; print ${POLARIZATION} * 180/numpy.pi"`
COA_PHASE_inj=`python -c "import numpy; print ${COA_PHASE} * 180/numpy.pi"`

# create injection file
lalapps_inspinj \
    --output ${INJ_PATH} \
    --seed 1000 \
    --f-lower ${INJ_F_MIN} \
    --waveform ${INJ_APPROX} \
    --amp-order 7 \
    --gps-start-time ${TRIGGER_TIME} \
    --gps-end-time ${TRIGGER_TIME} \
    --time-step 1 \
    --t-distr fixed \
    --l-distr fixed \
    --longitude ${LONGITUDE} \
    --latitude ${LATITUDE} \
    --d-distr uniform \
    --min-distance ${DISTANCE} \
    --max-distance ${DISTANCE} \
    --i-distr fixed \
    --fixed-inc ${INC_inj} \
    --coa-phase-distr fixed \
    --fixed-coa-phase ${COA_PHASE_inj} \
    --polarization ${POLARIZATION_inj} \
    --m-distr fixMasses \
    --fixed-mass1 ${MASS1} \
    --fixed-mass2 ${MASS2} \
    --taper-injection ${TAPER} \
    --enable-spin \
    --min-spin1 ${MIN_SPIN1} \
    --max-spin1 ${MAX_SPIN1} \
    --min-spin2 ${MIN_SPIN2} \
    --max-spin2 ${MAX_SPIN2} \
    --min-kappa1 ${MIN_KAPPA1} \
    --max-kappa1 ${MAX_KAPPA1} \

python det_response.py
