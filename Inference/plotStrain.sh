#!/bin/bash

#Specific run we're looking at
RUN=20170325-151901

python whitened.py --input-file jobs/${RUN}/output_white.hdf \
                   --parameters tc:1126259462.0 mchirp:18.25. q:0.5 \
                                spin1_a:0.9 \
                                spin1_azimuthal:0. \
                                spin1_polar:1.57 \
                                spin2_1:0.0 \
                                spin2_azimuthal:0. \
                                spin2_polar:0.0 \
                                distance:1000000 \
                                coa_phase:1.6 \
                                inclination:0. \
                                polarization:1.6 \
                                ra:2.21535724066 \
                                dec:-1.23649695537 \
                   --output-file testthis
                   
