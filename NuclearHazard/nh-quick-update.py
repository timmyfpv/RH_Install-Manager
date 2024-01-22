from rpi_update import update
import os
import json
from types import SimpleNamespace as Namespace, SimpleNamespace
from compatibility_check import main as compatibility_check


def load_json(file_name):
    data = {}
    if os.path.exists(file_name):
        with open(file_name) as open_file:
            data = json.loads(open_file.read(), object_hook=lambda d: Namespace(**d))
    return data


def main():
    compatibility_check()
    # passed_install_step = os.getenv('INSTALL_STEP')
    config_file = "../updater-config.json"
    if os.path.exists(config_file):
        config = load_json(config_file)
        update(config, False)
    else:
        print("\n\n\t\tPlease install RotorHazard server first.\n\n"
              "\t\tType: './nh-install.sh 1'\n\n")


if __name__ == "__main__":
    main()
