#!/bin/bash

### Automatic Pi model detection script checks for Pi Zero, Pi 4 or defaults to Pi 3
### Raspberry Pi 0 -          BCM2835
### Raspberry Pi 1 -          BCM2835
### Raspberry Pi 2 -          BCM2836/7
### Raspberry Pi 3 B -        BCM2837A0/B0
### Raspberry Pi 3 A+/B+ -    BCM2837A0/B0
### Raspberry Pi 4 -          BCM2711

pi_model_check()
{
pi_version=$(echo "$(tr -d '\0' < /proc/device-tree/compatible)" | rev | awk -F"," '{print $1}' | rev | xargs)
if [[ $pi_version == "bcm2835" ]]; then
  echo "Raspberry_Pi_0"
elif [[ $pi_version == "bcm2711" ]]; then
  echo "Raspberry_Pi_4"
else
  echo "Raspberry_Pi_3"
fi
}

green="\033[92m"
red="\033[91m"
endc="\033[0m"

pi_model_check_error() {
  printf "
     $red -- automatic Pi model detection error -- $endc

  If you are using Raspberry Pi 4 please edit file '/boot/config.txt'
  and change line 'core_freq=250' to '#core_freq=250'.

  If you are using any other Pi model please ignore that message.

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

ssh_enabling() {
  sudo systemctl enable ssh || return 1
  sudo systemctl start ssh || return 1
  printf "
     $green -- SSH ENABLED -- $endc


  "
  sleep 3
  return 0
}

ssh_error() {
  printf "
     $red -- SSH enabling error -- $endc

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable SSH interface
  than reboot

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

spi_enabling() {
  echo "
[SPI enabled - RH-OTA]
dtparam=spi=on
" | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1
  printf "
     $green -- SPI ENABLED -- $endc


  "
  sleep 3
  return 0
}

spi_error() {
  printf "
     $red -- SPI enabling error -- $endc

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable SPI interface
  than reboot

  Hit 'Enter' to continue


  "
  read -r _
  sleep 2
}

i2c_enabling() {
  pi_model_check || pi_model_check_error
 if [ "$pi_4_found" = true ] ; then
    echo "
Raspberry Pi 4 chipset found
    "
    #sudo sed -i 's/dtparam=i2c/#dtparam=i2c/' /boot/config.txt || return 1
    echo "
[I2C enabled - RH-OTA]
dtparam=i2c_arm=on
  " | sudo tee -a /boot/config.txt || return 1

else
  echo "
[I2C enabled - RH-OTA]
dtparam=i2c_baudrate=75000
core_freq=250
i2c-bcm2708
i2c-dev
dtparam=i2c1=on
dtparam=i2c_arm=on
  " | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1

  fi
  printf "
     $green -- I2C ENABLED -- $endc


     "
  sleep 3
  return 0
}

i2c_error() {
  printf "
     $red -- I2C enabling error -- $endc

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable I2C interface
  than reboot

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

uart_enabling() {
  sudo cp /boot/cmdline.txt /boot/cmdline.txt.dist
  sudo cp /boot/config.txt /boot/config.txt.dist
  echo "
[UART enabled - RH-OTA]
enable_uart=1
  " | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt || return 1
  printf "
     $green -- UART ENABLED -- $endc


     "
  sleep 3
  return 0
}

uart_error() {
  printf "
     $red -- UART enabling error -- $endc

  try manual enabling with 'sudo raspi config'
  please: disable end re-enable UART interface
  than reboot

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

if [ "${1}" = "ssh" ]; then
  ssh_enabling || ssh_error
fi

if [ "${1}" = "spi" ]; then
  spi_enabling || spi_error
fi

if [ "${1}" = "i2c" ]; then
  i2c_enabling || i2c_error
fi

if [ "${1}" = "uart" ]; then
  uart_enabling || uart_error
fi

reboot_message() {
  echo "

  Process completed. Please reboot Raspberry now.

  "
}

if [ "${1}" = "all" ]; then
  ssh_enabling || ssh_error
  spi_enabling || spi_error
  i2c_enabling || i2c_error
  uart_enabling || uart_error
fi
