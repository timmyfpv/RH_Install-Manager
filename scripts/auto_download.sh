#!/bin/bash

white=""
green="\033[92m"
red="\033[91m"
endc="\033[0m"

script() {
  printf "
$white

RotorHazard Install-Manager software will be downloaded automatically


$endc "
sleep 2

  (sudo apt update && sudo apt install curl wget unzip -y) || echo "no wget or curl download target"
  cd ~ || return 1
  mv RH_Install-Manager* RH_Install-Manager.old 2 >/dev/null &>1 #TODO in case of non-empty directories
  mv temprhim.zip temprhim.zip.old 2 >/dev/null &>1              #TODO in case of non-empty directories
  wget https://codeload.github.com/RotorHazard/Install-Manager/zip/stable -O temprhim.zip || return 1
  unzip temprhim.zip || return 1
  rm temprhim.zip || return 1
  mv RH_Install-Manager-* RH_Install-Manager || return 1
  cd ~/RH_Install-Manager

  printf "
$green
Program downloaded successfully. It will open now...
$endc

"
sleep 3

./rhim.sh

}

script || printf "
$red
errors encountered - try manual installation -> more info od GitHub
$endc

"
