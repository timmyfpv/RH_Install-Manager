#!/bin/bash

boot_directory_check() {
  if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
    echo "/boot/firmware"
  else
    echo "/boot"
  fi
}

if [ "$1" == "shutdown_pin" ]; then

  boot_directory=$(boot_directory_check)

  sudo sed -i '/GPIO pin/d' "${boot_directory}"/config.txt
  sudo sed -i '/gpio-shutdown,gpio_pin/d' "${boot_directory}"/config.txt
  echo "
## GPIO pin - RH_Install-Manager ##
dtoverlay=gpio-shutdown,gpio_pin=$2,debounce=$3
  " | sudo tee -a "${boot_directory}"/config.txt
fi


if [ "$1" == "led" ]; then

  boot_directory=$(boot_directory_check)


  sudo sed -i '/ACT pin/d' "${boot_directory}"/config.txt
  sudo sed -i '/act-led/d' "${boot_directory}"/config.txt
  echo "
## ACT pin - RH_Install-Manager ##
dtoverlay=act-led,gpio=24
dtparam=act_led_trigger=heartbeat
  " | sudo tee -a "${boot_directory}"/config.txt
fi
