TARGETDIR=20170228-225207
ITER=4999
INPUT_FILE=${TARGET}/output.hdf
OUTPUT_FILE=${TARGET}/scatter.png
pycbc_inference_plot_posterior \
    --iteration ${ITER} \
    --input-file ${INPUT_FILE} \
    --output-file ${OUTPUT_FILE} \
    --plot-scatter \
    --plot-marginal \
    --z-arg logplr \
    --parameters "ra" \
