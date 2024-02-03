from modules import rhim_load_config, clear_the_screen, logo_top, Bcolors
from net_hotspot_manual_12 import net_hotspot_manual_12
from net_hotspot_auto_12 import net_hotspot_auto_12
from net_hotspot_manual_11 import net_hotspot_manual_11
from net_hotspot_auto_11 import net_hotspot_auto_11


def net_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        features_menu_content = """

                        {rmh}NETWORKING MENU{endc}{bold}

                            
                    1 - Setup hotspot - always on (Bookworm)
                    
                    2 - Setup automatic hotspot/Wi-Fi (Bookworm)
                    
                    3 - Setup hotspot - always on (Bullseye/Buster)
    
                    4 - Setup automatic hotspot/Wi-Fi (Bullseye/Buster)
    
            {yellow}e - Exit to main menu {endc}

                 """.format(rmh=Bcolors.RED_MENU_HEADER, yellow=Bcolors.YELLOW_S, bold=Bcolors.BOLD, endc=Bcolors.ENDC)
        print(features_menu_content)
        selection = input()
        if selection == '1':
            net_hotspot_manual_12()
        elif selection == '2':
            net_hotspot_auto_12()
        elif selection == '3':
            net_hotspot_manual_11(config)
        elif selection == '4':
            net_hotspot_auto_11(config)
        elif selection == 'e':
            break
    pass


def main():
    config = rhim_load_config()
    net_menu(config)


if __name__ == "__main__":
    main()
