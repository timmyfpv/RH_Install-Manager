from modules import rhim_load_config
import os


def net_auto_ap():

    os.system("scripts/net_hotspot_auto_12.sh")


def main():
    config = rhim_load_config()
    net_auto_ap()


if __name__ == "__main__":
    main()
