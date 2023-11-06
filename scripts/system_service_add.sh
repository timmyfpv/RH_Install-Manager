echo "

[Unit]
Description=RotorHazard Server
After=multi-user.target

[Service]
User=pi
WorkingDirectory=/home/${1}/RotorHazard/src/server
ExecStart=/home/${1}/RotorHazard/src/server/venv/bin/python server.py

[Install]
WantedBy=multi-user.target

" | sudo tee -a /lib/systemd/system/rotorhazard.service