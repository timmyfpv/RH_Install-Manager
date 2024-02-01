#!/bin/bash

if [ "$1" == "shutdown_pin" ]; then

  if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
    boot_directory="/boot/firmware"
  else
    boot_directory="/boot"
  fi

  sudo sed -i '/GPIO pin/d' "$boot_directory"/config.txt
  sudo sed -i '/gpio-shutdown,gpio_pin/d' "$boot_directory"/config.txt
  echo "
## GPIO pin - RH_Install-Manager ##
dtoverlay=gpio-shutdown,gpio_pin=$2,debounce=$3
  " | sudo tee -a "$boot_directory"/config.txt
fi


if [ "$1" == "led" ]; then

  if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
    boot_directory="/boot/firmware"
  else
    boot_directory="/boot"
  fi

  sudo sed -i '/ACT pin/d' "$boot_directory"/config.txt
  sudo sed -i '/act-led/d' "$boot_directory"/config.txt
  echo "
## ACT pin - RH_Install-Manager ##
dtoverlay=act-led,gpio=24
dtparam=act_led_trigger=heartbeat
  " | sudo tee -a "$boot_directory"/config.txt
fi
