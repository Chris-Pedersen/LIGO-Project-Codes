#!/bin/bash

#Specific run we're looking at
RUN=20170325-151901

python whitened.py --input-file jobs/${RUN}/output_white.hdf \
                   --parameters mass1:30. mass2:15. distance=100000. \
                   --output-file testthis
                   
