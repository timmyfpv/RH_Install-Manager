from modules import load_json
from rpi_update import installation


def main():
    config = load_json("./nh-updater-config.json")
    installation(True, config, False)


if __name__ == "__main__":
    main()
