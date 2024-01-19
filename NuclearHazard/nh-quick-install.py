from rpi_update import installation
import os
import json
from types import SimpleNamespace as Namespace, SimpleNamespace
from user_folder_check import main as user_folder_check


def load_json(file_name):
    data = {}
    if os.path.exists(file_name):
        with open(file_name) as open_file:
            data = json.loads(open_file.read(), object_hook=lambda d: Namespace(**d))
    return data


def main():
    user_folder_check()
    passed_install_step = os.getenv('INSTALL_STEP')
    config = load_json("./nh-updater-config.json")
    installation(True, config, False, passed_install_step)


if __name__ == "__main__":
    main()
