#!/bin/bash

#Specific run we're looking at
RUN=$1

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --injection-file jobs/${RUN}/injection.xml.gz \
                   --output-file jobs/${RUN}/strain_plot

# Rename dictionary
mv jobs/${RUN}/strain_plot_dic.npy jobs/${RUN}/mapDic.npy
