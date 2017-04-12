#!/bin/bash

#Specific run we're looking at
RUN=$1

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --min-xlim -2.5 \
                   --injection-file jobs/${RUN}/injection.xml.gz \
                   --output-file jobs/${RUN}/strain_plot25

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --min-xlim -1.5 \
                   --injection-file jobs/${RUN}/injection.xml.gz \
                   --output-file jobs/${RUN}/strain_plot15

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --min-xlim -1.0 \
                   --injection-file jobs/${RUN}/injection.xml.gz \
                   --output-file jobs/${RUN}/strain_plot10

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --min-xlim -0.5 \
                   --injection-file jobs/${RUN}/injection.xml.gz \
                   --output-file jobs/${RUN}/strain_plot05

python whitened.py --input-file jobs/${RUN}/output.hdf \
                   --plot-map-waveforms \
                   --min-xlim -0.2 \
                   --injection-file jobs/${RUN}/injection.xml.gz \
                   --output-file jobs/${RUN}/strain_plot02

# Rename dictionary
mv jobs/${RUN}/strain_plot_dic.npy jobs/${RUN}/mapDic.npy
