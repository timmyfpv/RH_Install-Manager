#!/bin/bash

green="\033[92m"
red="\033[91m"
endc="\033[0m"

chipset_check() {

  if [ "$(~/RH_Install-Manager/scripts/pi_model_check.sh)" == "pi_4" ]; then
    printf "\n\n\t Raspberry Pi 4 chipset found \n\n"
  elif [ "$(~/RH_Install-Manager/scripts/pi_model_check.sh)" == "pi_5" ]; then
    printf "\n\n\t Raspberry Pi 5 chipset found \n\n"
  else
    printf "\n\n\t Generic Raspberry Pi chipset found \n\n"

  fi

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

  try manually enabling using 'sudo raspi-config' later
  please: disable end re-enable SSH interface
  than reboot

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

spi_enabling() {

  if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
    boot_directory="/boot/firmware"
  else
    boot_directory="/boot"
  fi

  sudo raspi-config nonint do_spi 0 || return 1

  echo "
# SPI enabled - RH_Install-Manager #

[all]
dtparam=spi=on
" | sudo tee -a "$boot_directory"/config.txt || return 1

  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf >>/dev/null 2>&1

  printf "
     $green -- SPI ENABLED -- $endc


  "
  sleep 3
  return 0
}

spi_error() {
  printf "
     $red -- SPI enabling error -- $endc

  try manually enabling using 'sudo raspi-config' later
  please: disable end re-enable SPI interface
  than reboot

  Hit 'Enter' to continue


  "
  read -r _
  sleep 2
}

i2c_enabling() {

  if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
    boot_directory="/boot/firmware"
  else
    boot_directory="/boot"
  fi

  sudo raspi-config nonint do_i2c 0 || return 1

  echo "
# I2C enabled - RH_Install-Manager #

[pi5]
dtparam=i2c_arm=on
dtoverlay=i2c1-pi5

[pi4]
dtparam=i2c_arm=on

[pi3]
dtparam=i2c_baudrate=75000
core_freq=250
i2c-bcm2708
i2c-dev
dtparam=i2c1=on
dtparam=i2c_arm=on
  " | sudo tee -a "$boot_directory"/config.txt || return 1
  #    sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1

  printf "
     $green -- I2C ENABLED -- $endc


     "
  sleep 3
  return 0
}

i2c_error() {
  printf "
     $red -- I2C enabling error -- $endc

  try manually enabling using 'sudo raspi-config' later
  please: disable end re-enable I2C interface
  than reboot

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

uart_enabling() {

  if [ "$(~/RH_Install-Manager/scripts/os_version_check.sh)" == "12" ]; then
    boot_directory="/boot/firmware"
  else
    boot_directory="/boot"
  fi

  sudo cp "$boot_directory"/config.txt "$boot_directory"/config.txt.dist || echo
  sudo cp "$boot_directory"/cmdline.txt "$boot_directory"/cmdline.txt.dist || echo

  sudo raspi-config nonint do_serial_hw 0 || return 1

  sudo sed -i 's/console=serial0,115200//g' "$boot_directory"/cmdline.txt || echo
  echo "
  console serial output disabled - requires REBOOT
  "
  sudo raspi-config nonint do_serial_cons 1 || return 1

  echo "
# UART enabled - RH_Install-Manager #

[pi5]
enable_uart=1
dtoverlay=miniuart-bt
dtoverlay=uart0-pi5

[all]
enable_uart=1
dtoverlay=miniuart-bt
  " | sudo tee -a "$boot_directory"/config.txt || return 1

  sleep 2

  printf "
     $green -- UART ENABLED -- $endc


     "
  sleep 3
  return 0
}

uart_error() {
  printf "
     $red -- UART enabling error -- $endc

  try manually enabling using 'sudo raspi-config'
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

  Process completed. Please reboot Raspberry Pi now.

  "
}

if [ "${1}" = "all" ]; then
  chipset_check || echo
  ssh_enabling || ssh_error
  spi_enabling || spi_error
  i2c_enabling || i2c_error
  uart_enabling || uart_error
fi
