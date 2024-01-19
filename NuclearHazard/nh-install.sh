#!/bin/bash
export PYTHONPATH=/home/"$USER"/RH_Install-Manager:$PYTHONPATH

sh ../rhim.sh no_start
if [ "$1" == "wifi" ]; then
  sh ./nh-wifi.sh
else
  export INSTALL_STEP="$1"
  python3 ./nh-quick-install.py
fi
