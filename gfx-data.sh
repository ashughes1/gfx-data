#!/bin/bash

DATE=$(date -v-4m +"%Y-%m-%d")
python ./gfx-data.py -d $DATE -s crashes-per-adi
