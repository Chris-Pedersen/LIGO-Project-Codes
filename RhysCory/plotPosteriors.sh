# Input inference folder
FOLDER=$1

ITER=11999 #Take last iteration - change this if you run with more
INPUT_FILE=${FOLDER}/output.hdf
OUTPUT_FILE=${FOLDER}/posteriors.png
pycbc_inference_plot_posterior \
    --iteration ${ITER} \
    --input-file ${INPUT_FILE} \
    --output-file ${OUTPUT_FILE} \
    --plot-scatter \
    --plot-marginal \
    --z-arg logplr \
    --parameters "dec*180/pi:$\delta$ (deg)" \
                 "polarization*180/pi:$\psi$ (deg)" \
                 mchirp q spin1_azimuthal spin1_polar \
                 spin2_azimuthal spin2_polar \
                 "inclination*180/pi:$\iota$ (deg)" distance \
                 "coa_phase*180/pi:$\phi_0$ (deg)" tc
