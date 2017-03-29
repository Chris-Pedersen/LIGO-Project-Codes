#!/bin/bash

#Specific run we're looking at
RUN=$1

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --output-file jobs/${RUN}/strain_plot
