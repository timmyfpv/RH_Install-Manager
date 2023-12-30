#!/bin/bash
# $1 is linux user name
# $2 is actual version of RotorHazard to get.

sudo apt-get update && sudo apt-get --with-new-pkgs upgrade -y
sudo apt autoremove -y
sudo apt install wget python3 python*-venv ntp htop libjpeg-dev libffi-dev build-essential git scons swig zip i2c-tools python3-smbus python3-smbus2 python3-pip python3-dev iptables -y
sudo apt install python3-rpi.gpio -y || echo "-- no python-rpi.gpio module found - available only on Pi --" #is this redundant?
sudo rm -r /home/"${1}"/temp.zip >/dev/null 2>&1 # in case of weird sys config or previous unsuccessful installations
cd /home/"${1}" || exit
python -m venv ~/.venv || (printf "\switched to python3 command\n\n" && python3 -m venv ~/.venv) # required when 'python' is command is not recognized as 'python3

if [ -d "/home/${1}/RotorHazard" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard" "/home/${1}/RotorHazard_$(date +%Y%m%d%H%M)" || exit 1
fi
if [ -d "/home/${1}/RotorHazard-${2}" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard-${2}" "/home/${1}/RotorHazard_${2}_$(date +%Y%m%d%H%M)" || exit 1
fi