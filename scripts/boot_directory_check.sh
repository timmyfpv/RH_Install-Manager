#!/bin/bash

if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
  echo "/boot/firmware"
else
  echo "/boot"
fi
