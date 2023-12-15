from time import sleep
import os
import json
from pathlib import Path
from modules import clear_the_screen, logo_top


def conf_check():
    home_dir = str(Path.home())
    conf_now_flag = 1
    ap_config = {}  # Initialize ap_config as an empty dictionary

    if os.path.exists(f"{home_dir}/RH_Install-Manager/ap-config.json"):
        with open(f"{home_dir}/RH_Install-Manager/ap-config.json", "r") as json_file:
            ap_config = json.load(json_file)

        ssid = ap_config.get("WIFI", {}).get("SSID")
        password = ap_config.get("WIFI", {}).get("PASSWORD")

        print("""\n\tLooks like you have AccessPoint already configured.
              \n\n\t\tCurrent configuration:""")
        print(f"\n\n\t\tSSID (hotspot name): {ssid}")
        print(f"\n\t\tPassword (password): {password}")
        print("\n\n")

        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [y/n]\t\t").lower()
            if not cont_conf:
                print("Answer defaulted to: yes")
                break
            elif cont_conf[0] == 'y':
                conf_now_flag = True
                break
            elif cont_conf[0] == 'n':
                conf_now_flag = False
                break
            else:
                print("\nToo big fingers :( wrong command. Try again! :)")

    return conf_now_flag


def save_config_os(ssid, password):
    os.system("sudo nmcli con delete hotspot")
    os.system(f"sudo nmcli con add con-name hotspot ifname wlan0 type wifi ssid {ssid}")
    os.system(f"sudo nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk")
    os.system(f"sudo nmcli con modify hotspot wifi-sec.psk '{password}'")
    os.system(f"sudo nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared")
    print("\n\n\tHotspot configuration data has been saved\n")
    sleep(3)


def do_config():
    clear_the_screen()
    logo_top(False)

    home_dir = str(Path.home())
    conf_now_flag = conf_check()

    if conf_now_flag:
        clear_the_screen()
        logo_top(False)
        ap_config = {}

        print("""\n
            Enter hotspot configuration:
""")

        ssid = input("\n\t\tEnter SSID:                         ")
        ap_config["WIFI"] = {"SSID": ssid}

        while True:
            password = input("\n\t\tEnter Password (min. 8 characters): ")
            if len(password) < 8:
                print("\n\t\tPassword should be at least 8 characters long")
            else:
                break

        ap_config["WIFI"]["PASSWORD"] = password

        ap_configuration_summary = f"""\n\n
            WIFI SSID:          {ap_config["WIFI"]["SSID"]}
            WIFI Password:      {ap_config["WIFI"]["PASSWORD"]}

            Please check. Confirm? [yes/change/abort]\n"""
        print(ap_configuration_summary)

        valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
        while True:
            selection = input().strip()
            if selection in valid_options:
                break
            else:
                print("\nToo big fingers ;) - please type yes/abort/change")
        if selection[0] == 'y':
            with open(f"{home_dir}/RH_Install-Manager/ap-config.json", "w") as json_file:
                json.dump(ap_config, json_file, indent=4)
            save_config_os(ssid, password)
            sleep(1)
            conf_now_flag = 0
        if selection in ['change', 'n', 'no']:
            conf_now_flag = 1
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            conf_now_flag = 0

    return conf_now_flag


def ap_config():
    config_now = 1
    while config_now:
        config_now = do_config()


def main():
    ap_config()


if __name__ == "__main__":
    main()
