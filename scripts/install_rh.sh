#!/bin/bash
# $1 is linux user name
# $2 is actual version of RotorHazard to get.

red="\033[91m"
yellow="\033[93m"
green="\033[92m"
endc="\033[0m"

add_ons_info_show() {
  printf "\n\n   Installing additional software may take few minutes \n\n\n"
}

sudo apt-get update && sudo apt-get --with-new-pkgs upgrade -y
sudo apt autoremove -y
sudo apt install wget python3 python*-venv ntp htop libjpeg-dev libffi-dev build-essential git scons swig zip i2c-tools python3-smbus python3-pip python3-dev iptables -y
sudo apt install python3-rpi.gpio -y || echo "-- no python-rpi.gpio module found - available only on Pi --" #is this redundant?
sudo rm -r /home/"${1}"/temp.zip >/dev/null 2>&1 # in case of weird sys config or previous unsuccessful installations
cd /home/"${1}" || exit
if [ -d "/home/${1}/RotorHazard" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard" "/home/${1}/RotorHazard_$(date +%Y%m%d%H%M)" || exit 1
fi
if [ -d "/home/${1}/RotorHazard-${2}" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard-${2}" "/home/${1}/RotorHazard_${2}_$(date +%Y%m%d%H%M)" || exit 1
fi
cd /home/"${1}" || exit
wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"${2}" -O temp.zip
unzip temp.zip
rm temp.zip
rm ~/wget* >/dev/null 2>&1
mv /home/"${1}"/RotorHazard-* /home/"${1}"/RotorHazard || exit 1
add_ons_info_show
cd /home/"${1}"/RotorHazard/src/server || echo "$red missing RotorHazard directory"
python -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install cffi pillow
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
cd /home/"${1}" || exit

# added because of the broken Adafruit_GPIO compatibility on Raspbian 11 Bullseye
(sudo sed -i 's/UNKNOWN          = 0/UNKNOWN          = 1/' /usr/local/lib/python3*/dist-packages/Adafruit_GPIO/Platform.py && \
printf "\n $green Adafruit_GPIO compatibility is now OK $endc \n\n\n" && sleep 1) || \
(printf "$endc \nAdafruit_GPIO compatibility file probably missing \n\n $endc" && sleep 2)

java_installation()
{
if [[ $(~/RH_Install-Manager/scripts/pi_model_check.sh) == "pi_zero"  ]]; then
  sudo apt-get install openjdk-8-jdk-headless -y
else
  sudo apt-get install openjdk-17-jdk-headless -y
fi
}

java_installation

# run as a service
sudo rm /lib/systemd/system/rotorhazard.service >/dev/null 2>&1

# system service add
echo
cd /home/"${1}"/RH_Install-Manager/scripts/ || exit
sudo ./system_service_add.sh "${1}"
echo

sudo chmod 644 /lib/systemd/system/rotorhazard.service
sudo systemctl daemon-reload
sudo systemctl enable rotorhazard.service
echo


# port forwarding
cd /home/"${1}"/RH_Install-Manager/scripts/ || exit
sudo ./iptables_conf.sh
