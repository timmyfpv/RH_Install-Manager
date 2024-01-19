from rpi_update import installation
import os
import json
from types import SimpleNamespace as Namespace, SimpleNamespace


def load_json(file_name):
    data = {}
    if os.path.exists(file_name):
        with open(file_name) as open_file:
            data = json.loads(open_file.read(), object_hook=lambda d: Namespace(**d))
    return data


def main():
    config = load_json("./nh-updater-config.json")
    installation(True, config, False)


if __name__ == "__main__":
    main()
