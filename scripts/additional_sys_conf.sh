#!/bin/bash

if [ "$1" == "shutdown_pin" ]; then
  sed -i '/gpio-shutdown,gpio_pin/d' /boot/config.txt
  echo "
[GPIO pin - RH_Install-Manager]
dtoverlay=gpio-shutdown,gpio_pin=$2,debounce=$3
  " | sudo tee -a /boot/config.txt
fi

if [ "$1" == "led" ]; then
  sed -i '/act-led/d' /boot/config.txt
  echo "
[ACT pin - RH_Install-Manager]
dtoverlay=act-led,gpio=24
dtparam=act_led_trigger=heartbeat
  " | sudo tee -a /boot/config.txt
fi
