from time import sleep
import os
from modules import clear_the_screen, Bcolors, logo_top

homedir = os.path.expanduser('~')

clear_the_screen()

logo_top(False)

#Always define variables before using them.
conf_now_FLAG = 0

def conf_check():
    global conf_now_FLAG
    if os.path.exists("./updater-config.json"):
        print("\n\tLooks that you have OTA software already configured.")
        valid_options = ['y', 'yes', 'n', 'no']
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [yes/no]\t\t").strip()
            if cont_conf in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if cont_conf[0] == 'y' :
            conf_now_FLAG = 1
            pass
        if cont_conf[0] == 'n' :
            conf_now_FLAG = 0
    else:
        conf_now_FLAG = 1


conf_check()

if conf_now_FLAG:
    while True:
        print("""\n
Please type your configuration data. It can be modified later.
Default values are not automatically applied. Type them if needed.\n""")
        os.system("rm .wizarded-updater-config.json >/dev/null 2>&1")
        name = input("\nWhat is your user name on Raspberry Pi? [default: pi]\t\t\t")
        os.system("echo '{' | tee -a " + homedir + "/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
        os.system("echo '    \"pi_user\" : \"" + name + "\",' | tee -a " + homedir +
                  "/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
        while True:
            version = input(
                "\nWhat RotorHazard version will you use? [" + Bcolors.UNDERLINE + "stable" + Bcolors.ENDC +
                " | beta | master]\t\t")
            version_valid_options = ['master', 'stable', 'beta']
            if version not in version_valid_options:
                print("\nPlease enter correct value!")
            else:
                os.system(f"echo '    \"RH_version\" : \"{version}\",' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        debug_user = input("\nWhat is you user name on debugging OS? [default: racer]\t\t\t")
        os.system(f"echo '    \"debug_user\" : \"{debug_user}\",' \
         | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
        code = input("\nWhat is your country code? [default: GB]\t\t\t\t")
        os.system(f"echo '    \"country\" : \"{code}\",' \
         | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
        while True:
            nodes = input("\nHow many nodes will you use in your system? [min: 0/1 | max: 8]\t\t")
            if not nodes.isdigit() or int(nodes) > 8:
                print("\nPlease enter correct value!")
            else:
                os.system(f"echo '    \"nodes_number\" : {nodes},' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        while True:
            debug_mode = input("\nWill you use \"OTA\" software in a debug mode? [yes/no | default: no]\t")
            debug_mode_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if debug_mode not in debug_mode_allowed_values:
                print("\nPlease enter correct value!")
            else:
                debug_mode_val = '0'
                if debug_mode in ['yes', '1', 'y']:
                    debug_mode_val = '1'
                elif debug_mode in ['no', '0', 'n']:
                    debug_mode_val = '0'
                os.system(f"echo '    \"debug_mode\" : {debug_mode_val},' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        while True:
            pins_assign = input("\nPins assignment? [default/custom/PCB | default: default]\t\t")
            pins_valid_options = ['default', 'PCB', 'pcb', 'custom']
            if pins_assign not in pins_valid_options:
                print("\nPlease enter correct value!")
            else:
                os.system(f"echo '    \"pins_assignment\" : \"{pins_assign}\",' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        while True:
            no_pdf_val = '0'
            no_pdf = input("\nUpdates without PDF? [yes/no | default: yes]\t\t\t\t")
            no_pdf_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if no_pdf not in no_pdf_allowed_values:
                print("\nPlease enter correct value!")
            else:
                if no_pdf in ['yes', '1', 'y']:
                    no_pdf_val = '1'
                elif no_pdf in ['no', '0', 'n']:
                    no_pdf_val = '0'
                os.system(f"echo '    \"updates_without_pdf\" : {no_pdf_val},' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        while True:
            pi_4 = input("\nAre you using Raspberry Pi 4? [yes/no | default: no]\t\t\t")
            pi_4_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if pi_4 not in pi_4_allowed_values:
                print("\nPlease enter correct value!")
            else:
                pi_4_val = '0'
                if pi_4 in ['yes', '1', 'y']:
                    pi_4_val = '1'
                elif pi_4 in ['no', '0', 'n']:
                    pi_4_val = '0'
                os.system(f"echo '    \"pi_4_cfg\" : {pi_4_val},' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        while True:
            beta_tester = input("\nAre you a beta tester? [yes/no | default: no]\t\t\t\t")
            beta_tester_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if beta_tester not in beta_tester_allowed_values:
                print("\nPlease enter correct value!")
            else:
                beta_tester_val = '0'
                if beta_tester in ['yes', '1', 'y']:
                    beta_tester_val = '1'
                elif beta_tester in ['no', '0', 'n']:
                    beta_tester_val = '0'
                os.system(f"echo '    \"beta_tester\" : {beta_tester_val}' \
                 | tee -a {homedir}/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
                break
        os.system("echo '}' | tee -a " + homedir + "/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
        print("""\n\n\t\t\t""" + Bcolors.UNDERLINE + """CONFIGURATION""" + Bcolors.ENDC + """:\n\t
        User name: \t\t""" + name + """
        RotorHazard version: \t""" + version + """
        Debug user name: \t""" + debug_user + """
        Country code: \t\t""" + code + """
        Nodes amount: \t\t""" + nodes + """
        Debug mode: \t\t""" + debug_mode + """
        Pins assignment: \t""" + pins_assign + """
        Updates without PDF: \t""" + no_pdf + """
        Pi 4 user: \t\t""" + pi_4 + """
        Beta tester: \t\t""" + beta_tester + """\n\n\n""")
        print("Please check. Confirm? [yes/change/abort]\n")
        valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
        while True:
            selection = input().strip()
            if selection in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if selection == 'y' or selection == 'yes':
            os.system("mv .wizarded-updater-config.json updater-config.json")
            print("Configuration saved.\n")
            sleep(0.5)
            break
        if selection in ['change', 'n', 'no']:
            continue
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            break
else:
    os.system("exit")
