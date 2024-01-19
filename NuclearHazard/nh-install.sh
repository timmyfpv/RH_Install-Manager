#!/bin/bash
export PYTHONPATH=/home/"$USER"/RH_Install-Manager:$PYTHONPATH

sh ../rhim.sh no_start
export INSTALL_STEP="$1"
python3 ./nh-quick-install.py

