from time import sleep
import os
from modules import clear_the_screen, Bcolors, logo_top, write_json
from pathlib import Path

def conf_new_ap():
    if os.path.exists(f"./ap-config.json"):
        print("\n\tLooks that you have Access Point already configured."
              "Do you want to change the configuration?")
        print("Current configuration:")




