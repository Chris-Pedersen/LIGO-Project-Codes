ITER=4999
INPUT_FILE=inference.hdf
OUTPUT_FILE=scatter.png
pycbc_inference_plot_posterior \
    --iteration ${ITER} \
    --input-file ${INPUT_FILE} \
    --output-file ${OUTPUT_FILE} \
    --plot-scatter \
    --plot-marginal \
    --z-arg logplr \
    --parameters "ra*12/pi:$\alpha$ (h)" \
                 "dec*180/pi:$\delta$ (deg)" \
                 "polarization*180/pi:$\psi$ (deg)" \
                 mchirp q spin1_a spin1_azimuthal spin1_polar \
                 spin2_a spin2_azimuthal spin2_polar \
                 "inclination*180/pi:$\iota$ (deg)" distance \
                 "coa_phase*180/pi:$\phi_0$ (deg)" tc
