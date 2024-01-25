from rpi_update import installation
import os
import sys
import pwd
import json
from types import SimpleNamespace as Namespace, SimpleNamespace
from compatibility_check import main as compatibility_check


def name_check():
    username = pwd.getpwuid(os.getuid()).pw_name
    if username != "NuclearHazard":
        print("\n\n\t\tThis script assumes your username is 'NuclearHazard\n\n")
        input("Press Enter to exit")
        sys.exit()


def load_json(file_name):
    data = {}
    if os.path.exists(file_name):
        with open(file_name) as open_file:
            data = json.loads(open_file.read(), object_hook=lambda d: Namespace(**d))
    return data


def main():
    name_check()
    compatibility_check()
    passed_install_step = os.getenv('INSTALL_STEP')
    config = load_json("./nh-updater-config.json")
    installation(True, config, False, passed_install_step)


if __name__ == "__main__":
    main()
