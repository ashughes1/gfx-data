#!/bin/bash
source %%path_to_virtualenv%%/bin/activate
cd %%PATH_TO_VIRTUALENV%%/gfx-data
DATE=$(date -d last-week +%F)
echo "Processing data since $DATE..."
python gfx-data.py -d $DATE -s crashes-by-platform
python gfx-data.py -d $DATE -s crashes-by-vendor
deactivate
