from time import sleep
import os
import json
import time
from configparser import ConfigParser

parser = ConfigParser()

def parser_write():
    try:
        with open(f'/home/{user}/.ota_markers/ota_config.txt', 'w') as configfile:
            parser.write(configfile)
    except IOError as up:
        print("Config file does not exist and could not be created.")


os.system("pwd >.my_pwd")
with open('.my_pwd', 'r') as file:
    myhomedir = file.read().replace('\n', '')
os.system("rm ./.my_pwd")

cfgdir1 = str(myhomedir+'/RH-ota/updater-config.json')
cfgdir2 = str(myhomedir+'/RH-ota/distr-updater-config.json')


def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False


if os.path.exists(myhomedir+"/RH-ota/updater-config.json"):
    with open(cfgdir1) as config_file:
        data = json.load(config_file)
else:
    with open(cfgdir2) as config_file:
        data = json.load(config_file)


def internet_check():
    print("\nPlease wait - checking internet connection state...\n")
    global internet_FLAG
    before_millis = int(round(time.time() * 1000))
    os.system(". "+myhomedir+"/RH-ota/open_scripts.sh; net_check")
    while True:
        now_millis = int(round(time.time() * 1000))
        time_passed = (now_millis - before_millis)
        if os.path.exists("./index.html"):
            internet_FLAG = 1
            break
        elif time_passed > 10100:
            internet_FLAG = 0
            break
    os.system(f"rm {myhomedir}/RH-ota/index.html > /dev/null 2>&1")
    os.system(f"rm {myhomedir}/RH-ota/wget-log* > /dev/null 2>&1")
    os.system(f"rm {myhomedir}/index.html > /dev/null 2>&1")
    os.system(f"rm {myhomedir}/wget-log* > /dev/null 2>&1")


if os.path.exists(cfgdir1):
    config_file_exists = True
    if data['debug_mode']:
        linux_testing = True
    else:
        linux_testing = False

    if linux_testing:
        user = data['debug_user']
    else:
        user = data['pi_user']
else:
    config_file_exists = False

if config_file_exists:
    if check_if_string_in_file(myhomedir+'/RH-ota/updater-config.json', 'updates_without_pdf'):
        if data['updates_without_pdf']:
            no_pdf_update = True
        else:
            no_pdf_update = False
    else:
        no_pdf_update = False
else: 
    no_pdf_update = False


if config_file_exists:
    if check_if_string_in_file(myhomedir+'/RH-ota/updater-config.json', 'beta_tester'):
        if data['beta_tester']:
            beta_tester_update = True
        else:
            beta_tester_update = False
    else:
        beta_tester_update = False
else:
    beta_tester_update = False


def debug_info():
    if config_file_exists:
        print("config_file_exists = True")
    else:
        print("config_file_exists = False")
    if no_pdf_update:
        print("no_pdf_update = True")
    else:
        print("no_pdf_update = False")
    sleep(1)
# debug_info()


def old_version_check():
    os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.old_version")
    os.system("sed -i 's/updater_version = //' ~/.ota_markers/.old_version")
    os.system("sed -i 's/#.*/ /' ~/.ota_markers/.old_version")
    f = open(f"{myhomedir}/.ota_markers/.old_version", "r")
    for line in f:
        global old_version_name
        old_version_name = line


def new_version_check():
    os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.new_version")
    os.system("sed -i 's/updater_version = //' ~/.ota_markers/.new_version")
    os.system("sed -i 's/#.*/ /' ~/.ota_markers/.new_version")
    f = open(f"{myhomedir}/.ota_markers/.new_version", "r")
    for line in f:
        global new_version_name
        new_version_name = line


def main():
    parser.read(myhomedir+'/.ota_markers/ota_config.txt')
    internet_check()
    if not internet_FLAG:
        print("\nLooks like you don't have internet connection. Update canceled.\n")
        sleep(2)
    else:
        print("\nInternet connection - OK\n")
        sleep(1.5)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")   # resolves compatibility issues
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")         # resolves compatibility issues
        old_version_check()
        print("\nThis time update process may take longer due to python3 implementation\n")
        if not parser.getint('added_functions', 'python3_installed'):
            if not os.system("sudo apt install python3 python3-pip"):
                parser.set('added_functions', 'python3_installed', '1')
                parser_write()
            else:
                print("\n\nPlease install python3 manually and start updating process again\n\n")
                print("Also change 'python3_installed' to value 1 in ~/.ota_markers/ota_config.txt.\n\n")
                input("\nOK? Press 'Enter'")
        if not parser.getint('added_functions', 'configparser_installed'):
            if not os.system("pip3 install configparser"):
                parser.set('added_functions', 'configparser_installed', '1')
                parser_write()
            else:
                print("\n\nPlease install configparser manually via pip and start updating process again\n")
                print("Also change 'configparser_installed' to value 1 in ~/.ota_markers/ota_config.txt.\n\n")
                input("\nOK? Press 'Enter'")
                main()
        print(f"\n\n\n\t Please wait: updating process from version {old_version_name}\n\n")
        sleep(2)
        if config_file_exists:
            os.system("cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
        if not no_pdf_update:
            print("Update will contain PDF file - may be changed in config file.\n")
            os.system("sudo rm -rf ~/RH-ota*")
            os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
            os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/main_stable -O tempota.zip")
            os.system("unzip tempota.zip")
            os.system("rm tempota.zip")
            os.system("mv RH-ota-* RH-ota")
        if no_pdf_update:
            print("Update won't contain PDF file - may be changed in config file.\n")
            os.system("sudo rm -rf ~/RH-ota*")
            os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
            os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/no_pdf -O tempota.zip")
            os.system("unzip tempota.zip")
            os.system("rm tempota.zip")
            os.system("mv RH-ota-* RH-ota")
        if beta_tester_update:
            print("Update won't contain PDF file - may be changed in config file.\n")
            os.system("sudo rm -rf ~/RH-ota*")
            os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
            os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip")
            os.system("unzip tempota.zip")
            os.system("rm tempota.zip")
            os.system("mv RH-ota-* RH-ota")
        if config_file_exists:
            os.system("cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
        new_version_check()
        print(f"\n\n\n\t RotorHazard OTA Manager updated to version {new_version_name}\n\t\tYou may check update-notes.\n\n")
        sleep(1)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")   # resolves compatibility issues
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")         # resolves compatibility issues
        if new_version_name != old_version_name:
            os.system("echo OTA was updated > ~/.ota_markers/.was_updated")


main()
