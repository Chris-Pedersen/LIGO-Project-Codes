#!/bin/bash

RUN=


python whitened.py --input-file jobs/${RUN}
                   --parameters mass1:30 mass2:15
                   --output-file testthis
                   
