#!/bin/bash

if [ "$1" == "shutdown_pin" ]; then
  echo "
[GPIO pin - RH_Install-Manager]
dtoverlay=gpio-shutdown,gpio_pin=$2,debounce=$3
  " | sudo tee -a /boot/config.txt
fi
