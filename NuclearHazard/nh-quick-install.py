from rpi_update import installation
import os
import sys
import pwd
import json
from modules import write_json
from types import SimpleNamespace as Namespace, SimpleNamespace
from compatibility_check import main as compatibility_check


def name_check():
    username = pwd.getpwuid(os.getuid()).pw_name
    return username


def load_json(file_name):
    data = {}
    if os.path.exists(file_name):
        with open(file_name) as open_file:
            data = json.loads(open_file.read(), object_hook=lambda d: Namespace(**d))
    return data


def main():
    username = name_check()
    compatibility_check()
    passed_install_step = os.getenv('INSTALL_STEP')
    if passed_install_step not in ['1', '2', 'wifi']:
        print("\n\n\tPlease specify the install step with the ./nh-install.sh command:"
              "\n\t\t'./nh-install.sh 1' or './nh-install.sh 2' or './nh-install.sh wifi'\n")
        input("\n\t\tHit 'Enter' to exit.\n")
        sys.exit()
    config = load_json("./nh-updater-config.json")
    config.user = username
    write_json(config, "./nh-updater-config.json")
    installation(True, config, False, passed_install_step)


if __name__ == "__main__":
    main()
