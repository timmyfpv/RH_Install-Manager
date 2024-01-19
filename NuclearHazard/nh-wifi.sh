#!/bin/bash

echo "if iwgetid -r | grep -q .; then
    echo "Wi-Fi network found. Not creating a hotspot."
else
    nmcli dev wifi hotspot ifname wlan0 ssid "NuclearHazard" password "nuclearhazard"
fi" | sudo tee -a /home/NuclearHazard/hotspot.sh
sudo chmod +x /home/NuclearHazard/hotspot.sh

echo "[Unit]
Description=Hotspot Service
After=NetworkManager.service
Wants=NetworkManager.service

[Service]
Type=simple
ExecStartPre=/bin/sleep 10
ExecStart=sudo /home/NuclearHazard/hotspot.sh
WorkingDirectory=/home/NuclearHazard/

[Install]
WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/hotspot.service
sudo systemctl enable hotspot.service


echo "

Automatic NuclearHazard AccessPoint enabled

"