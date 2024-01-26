from rpi_update import update
import os
from modules import write_json, load_json
from compatibility_check import main as compatibility_check


def main():
    compatibility_check()
    passed_rh_ver = os.getenv('RH_VERSION')
    config_file = "../updater-config.json"
    if os.path.exists(config_file):
        config = load_json(config_file)
        if passed_rh_ver in ['stable', 'beta', 'main']:
            config.rh_version = passed_rh_ver
            write_json(config, config_file)
        update(config, False)
    else:
        print("\n\n\t\tPlease install RotorHazard server first.\n\n"
              "\t\tType: './nh-install.sh 1'\n\n")


if __name__ == "__main__":
    main()
