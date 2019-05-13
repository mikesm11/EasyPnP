from easypnp_networksys_cz.model import credentials, usercredentials, url
from easypnp_networksys_cz.pnp_apicem import pnp_apicem, apiapicem
from easypnp_networksys_cz.pnp_dnac import pnp_dnac, apidnac
from Lib import re


class Program:
    """ Class for managing program """

########################################################################################################################
                                                # SYSTEM METHODS #
########################################################################################################################

    @staticmethod
    def update_credentials():
        """ Method for updating credentials """
        while True:
            try:
                command = input("  Invalid or no credentials. Do you want to continue? (y/n): ")
                if command == "Y" or command == "y":
                    # Call to method from usercredentials.py to enter credentials
                    result = usercredentials.UserCredentials.prompt_credentials()
                    if result is None:
                        continue
                    # Save results to variables in credentials.py
                    credentials.Credentials.controller_username = result[0]
                    credentials.Credentials.controller_password = result[1]
                    return True
                elif command == "N" or command == "n":
                    return False
            except RuntimeError:
                continue

    @staticmethod
    def get_credentials(c_user=False, c_pass=False):
        """ Method for getting credentials """
        try:
            if c_user == True:
                # Return of username variable from credentials.py
                controller_username = credentials.Credentials.controller_username
                return controller_username
            if c_pass == True:
                # Return of password variable from credentials.py
                controller_password = credentials.Credentials.controller_password
                return controller_password
        except RuntimeError:
            pass

########################################################################################################################
                                                # APIC-EM METHODS #
########################################################################################################################

    @staticmethod
    def run_program_APICEM(path):
        """ Initialization method for APIC-EM """
        # Variable for menu name
        base_path = path
        # Create an instance of the Url class with the apicem_url parameter
        apicem_url = url.Url('apicem_url')
        # Show URL settings when address is not set, then continue or exit
        if not apicem_url.is_set():
            if not Program.APICEMUrlSettings(path, apicem_url):
                return
        # Save URL address in the __UrlController variable of the ApiAPICEM class
        apiapicem.ApiAPICEM.set_url(apicem_url.get_url())
        # Run APIC-EM dialog menu
        while True:
            # The variable informing about location in menu
            path = Program.__getAPICEMmenupath(base_path)
            try:
                # APIC-EM dialog menu
                Program.APICEMdialogMenu(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    # Create ticket
                    apiapicem.ApiAPICEM.api_get_user()
                elif command == "2":
                    # Show network devices
                    Program.APICEMgetNetworkDevices()
                elif command == "3":
                    # Start of EasyPnP
                    pnp_apicem.PnP_APICEM.pnp_APICEM_menu_main(path)
                elif command == "4":
                    # Go to settings
                    Program.APICEMUrlSettings(path, apicem_url)
                elif command == "5" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def __getAPICEMmenupath(path):
        """ Local method informing about location in menu """
        return path + ' > APIC-EM(' + apiapicem.ApiAPICEM.get_url() + ')'

    @staticmethod
    def APICEMdialogMenu(path):
        """ Method of APIC-EM dialog menu """
        print("\n" + path + ":\n",
              "1 - Create ticket\n",
              "2 - Network devices\n",
              "3 - EasyPnP\n",
              "4 - Settings\n",
              "5 - Back")

    @staticmethod
    def APICEMUrlSettings(path, apicem_url):
        """ Method for setting URL address """
        # Print location in menu
        print("\n" + path + " > Settings:")
        # If URL address has already been set, display it
        if apicem_url.is_set():
            print(" APIC-EM address: " + apicem_url.get_url())
        else:
            print(" APIC-EM address is not set, please configure before continue!")
        # Choice between IP or DNS address
        command = input(" 1 - IP\n 2 - DNS\n New controller (enter a number or q)? ")
        if command == "1":
            # Save IP address to ip_input variable
            ip_input = input("  New IP of controller: ")
            # Regular expression for validating of the entered IP address
            ip_pat = '^((\d|\d\d|1\d\d|[2][0-5][0-5])\.){3}(\d|\d\d|1\d\d|[2][0-5][0-5])$'
            # If IP address doesn't match, exit settings
            if not re.match(ip_pat, ip_input):
                print("   ERROR! Invalid IP format!")
                return False
            try:
                # Check whether this is the IP address of the selected controller type
                result = apiapicem.ApiAPICEM.api_connection(ip_input)
                # If not, exit settings
                if result == False:
                    return False
                # Otherwise save IP address to __UrlController variable and cache_config file as well
                else:
                    print("   Saved successfully!")
                    apicem_url.set_url(ip_input)
                    apiapicem.ApiAPICEM.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        elif command == "2":
            # Save DNS address to ip_input variable
            ip_input = input("  New DNS of controller: ")
            try:
                # Check whether this is the DNS address of the selected controller type
                result = apiapicem.ApiAPICEM.api_connection(ip_input)
                # If not, exit settings
                if result == False:
                    return False
                # Otherwise save DNS address to __UrlController variable and cache_config file as well
                else:
                    print("   Saved successfully!")
                    apicem_url.set_url(ip_input)
                    apiapicem.ApiAPICEM.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        # Exit of settings
        elif command == "q" or command == "Q":
            return True

    @staticmethod
    def APICEMgetNetworkDevices():
        """" Method for getting network devices connected to APIC-EM """
        # Save result of this API call into r_json variable
        r_json = apiapicem.ApiAPICEM.api_get_network_devices()
        if not r_json == False:
            print("\n" + "  View all devices in network:")
            # Variable for indexing devices
            countDev = 0
            # Print the table header
            print('   {!s:3}'.format('No:') + "   " + '{!s:15}'.format('Serial num:') + "   " + '{!s:20}'.format(
                'Platform:') + "   " + '{!s:30}'.format('Hostname:') + "   " + '{!s:50}'.format(
                'Series:') + "  " + '{!s:60}'.format('Uptime:'))
            try:
                # Print all devices
                for i in r_json["response"]:
                    countDev += 1
                    print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:15}'.format(i["serialNumber"]) + "   " + '{!s:20}'.format(
                        i["platformId"]) + "   " + '{!s:30}'.format(i["hostname"]) + "   " + '{!s:50}'.format(
                        i["series"]) + "  " + '{!s:60}'.format(str(i["upTime"])))
            except Exception as e:
                print("   Something's wrong: " + str(e))
            while True:
                # Select a specific device (using the index) to view interfaces
                cmd = input("  Which device do you want to see the interface (enter index or q for exit)? ")
                if cmd == "q" or cmd == "Q":
                    break
                # Create index
                try:
                    cmd = int(cmd)
                except ValueError:
                    # Next iteration
                    continue
                # If index exists
                try:
                    # Create additional variables according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        deviceID = r_json["response"][cmd - 1]["id"]
                        deviceHN = r_json["response"][cmd - 1]["hostname"]
                        # Print all interfaces of selected device
                        print("\n" + "  All interfaces of device with hostname " + deviceHN + ":")
                        Program.APICEMgetNetworkDevicesInterfaces(deviceID, False)
                        # Print only UP interfaces of selected device
                        print("  Only UP interfaces of device with hostname " + deviceHN + ":")
                        Program.APICEMgetNetworkDevicesInterfaces(deviceID, True)
                        break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def APICEMgetNetworkDevicesInterfaces(deviceID, upInt=False):
        """" Method for getting interfaces of selected network device connected to APIC-EM """
        # Save result of this API call into r_json variable
        r_json = apiapicem.ApiAPICEM.api_get_device_interface(deviceID)
        try:
            if upInt == False:
                # Variable for indexing interfaces
                countDev = 0
                # Print the table header
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
                    # Print all interfaces of selected device
                    for i in r_json["response"]:
                        countDev += 1
                        print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:35}'.format(i["portName"]) + "   " + '{!s:10}'.format(i["status"]) + "   " + '{!s:15}'.format(
                            str(i["ipv4Address"])) + "   " + '{!s:20}'.format(str(i["ipv4Mask"])) + "   " + '{!s:30}'.format(str(i["lastUpdated"])))
                except TypeError:
                    pass
            else:
                # Variable for indexing interfaces
                countDev = 0
                # Print the table header
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
                    # Print only UP interfaces of selected device
                    for i in r_json["response"]:
                        if i["status"] == "up":
                            countDev += 1
                            print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:35}'.format(i["portName"]) + "   " + '{!s:10}'.format(i["status"]) + "   " + '{!s:15}'.format(
                                str(i["ipv4Address"])) + "   " + '{!s:20}'.format(str(i["ipv4Mask"])) + "   " + '{!s:30}'.format(str(i["lastUpdated"])))
                        else:
                            continue
                except TypeError:
                    print("   WARNING! Is not possible to print information about None device!")
        except Exception as e:
            print("   Something's wrong: " + str(e))

########################################################################################################################
                                                # DNA-C METHODS #
########################################################################################################################

    @staticmethod
    def run_program_DNAC(path):
        """ Initialization method for DNA-C """
        # Variable for menu name
        base_path = path
        # Create an instance of the Url class with the dnac_url parameter
        dnac_url = url.Url('dnac_url')
        # Show URL settings when address is not set, then continue or exit
        if not dnac_url.is_set():
            if not Program.DNACUrlSettings(path, dnac_url):
                return
        # Save URL address in the __UrlController variable of the ApiDNAC class
        apidnac.ApiDNAC.set_url(dnac_url.get_url())
        # Run DNA-C dialog menu
        while True:
            # The variable informing about location in menu
            path = Program.__getDNACmenupath(base_path)
            try:
                # DNA-C dialog menu
                Program.DNACdialogMenu(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    # Create token
                    apidnac.ApiDNAC.api_get_host()
                elif command == "2":
                    # Show network devices
                    Program.DNACgetNetworkDevices()
                elif command == "3":
                    # Start of EasyPnP
                    pnp_dnac.PnP_DNAC.pnp_DNAC_menu_main(path)
                elif command == "4":
                    # Go to settings
                    Program.DNACUrlSettings(path, dnac_url)
                elif command == "5" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def __getDNACmenupath(path):
        """ Local method informing about location in menu """
        return path + ' > DNA-C(' + apidnac.ApiDNAC.get_url() + ')'

    @staticmethod
    def DNACdialogMenu(path):
        """ Method of DNA-C dialog menu """
        print("\n" + path + ":\n",
              "1 - Create token\n",
              "2 - Network devices\n",
              "3 - EasyPnP\n",
              "4 - Settings\n",
              "5 - Back")

    @staticmethod
    def DNACUrlSettings(path, dnac_url):
        """ Method for setting URL address """
        # Print location in menu
        print("\n" + path + " > Settings:")
        # If URL address has already been set, display it
        if dnac_url.is_set():
            print(" DNA-C address: " + dnac_url.get_url())
        else:
            print(" DNA-C address is not set, please configure before continue!")
        # Choice between IP or DNS address
        command = input(" 1 - IP\n 2 - DNS\n New controller (enter a number or q)? ")
        if command == "1":
            # Save IP address to ip_input variable
            ip_input = input("  New IP of controller: ")
            # Regular expression for validating of the entered IP address
            ip_pat = '^((\d|\d\d|1\d\d|[2][0-5][0-5])\.){3}(\d|\d\d|1\d\d|[2][0-5][0-5])$'
            # If IP address doesn't match, exit settings
            if not re.match(ip_pat, ip_input):
                print("   ERROR! Invalid IP format!")
                return False
            try:
                # Check whether this is the IP address of the selected controller type
                result = apidnac.ApiDNAC.api_connection(ip_input)
                # If not, exit settings
                if result == False:
                    return False
                # Otherwise save IP address to __UrlController variable and cache_config file as well
                else:
                    print("   Saved successfully!")
                    dnac_url.set_url(ip_input)
                    apidnac.ApiDNAC.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        elif command == "2":
            # Save DNS address to ip_input variable
            ip_input = input("  New DNS of controller: ")
            try:
                # Check whether this is the DNS address of the selected controller type
                result = apidnac.ApiDNAC.api_connection(ip_input)
                # If not, exit settings
                if result == False:
                    return False
                # Otherwise save DNS address to __UrlController variable and cache_config file as well
                else:
                    print("   Saved successfully!")
                    dnac_url.set_url(ip_input)
                    apidnac.ApiDNAC.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        # Exit of settings
        elif command == "q" or command == "Q":
            return True

    @staticmethod
    def DNACgetNetworkDevices():
        """" Method for getting network devices connected to DNA-C """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_network_devices()
        if not r_json == False:
            print("\n" + "  View all devices in network:")
            # Variable for indexing devices
            countDev = 0
            # Print the table header
            print('   {!s:3}'.format('No:') + "   " + '{!s:15}'.format('Serial num:') + "   " + '{!s:20}'.format(
                'Platform:') + "   " + '{!s:30}'.format('Hostname:') + "   " + '{!s:50}'.format(
                'Series:') + "  " + '{!s:60}'.format('Uptime:'))
            try:
                # Print all devices
                for i in r_json["response"]:
                    countDev += 1
                    print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:15}'.format(i["serialNumber"]) + "   " + '{!s:20}'.format(
                        i["platformId"]) + "   " + '{!s:30}'.format(i["hostname"]) + "   " + '{!s:50}'.format(
                        i["series"]) + "  " + '{!s:60}'.format(str(i["upTime"])))
            except Exception as e:
                print("   Something's wrong: " + str(e))
            while True:
                # Select a specific device (using the index) to view interfaces
                cmd = input("  Which device do you want to see the interface (enter index or q for exit)? ")
                if cmd == "q" or cmd == "Q":
                    break
                # Create index
                try:
                    cmd = int(cmd)
                except ValueError:
                    # Next iteration
                    continue
                # If index exists
                try:
                    # Create additional variables according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        deviceID = r_json["response"][cmd - 1]["id"]
                        deviceHN = r_json["response"][cmd - 1]["hostname"]
                        # Print all interfaces of selected device
                        print("\n" + "  All interfaces of device with hostname " + deviceHN + ":")
                        Program.DNACgetNetworkDevicesInterfaces(deviceID, False)
                        # Print only UP interfaces of selected device
                        print("  Only UP interfaces of device with hostname " + deviceHN + ":")
                        Program.DNACgetNetworkDevicesInterfaces(deviceID, True)
                        break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def DNACgetNetworkDevicesInterfaces(deviceID, upInt=False):
        """" Method for getting interfaces of selected network device connected to DNA-C """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_device_interface(deviceID)
        try:
            if upInt == False:
                # Variable for indexing interfaces
                countDev = 0
                # Print the table header
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
                    # Print all interfaces of selected device
                    for i in r_json["response"]:
                        countDev += 1
                        print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:35}'.format(i["portName"]) + "   " + '{!s:10}'.format(i["status"]) + "   " + '{!s:15}'.format(
                            str(i["ipv4Address"])) + "   " + '{!s:20}'.format(str(i["ipv4Mask"])) + "   " + '{!s:30}'.format(str(i["lastUpdated"])))
                except TypeError:
                    pass
            else:
                # Variable for indexing interfaces
                countDev = 0
                # Print the table header
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
                    # Print only UP interfaces of selected device
                    for i in r_json["response"]:
                        if i["status"] == "up":
                            countDev += 1
                            print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:35}'.format(i["portName"]) + "   " + '{!s:10}'.format(i["status"]) + "   " + '{!s:15}'.format(
                                str(i["ipv4Address"])) + "   " + '{!s:20}'.format(str(i["ipv4Mask"])) + "   " + '{!s:30}'.format(str(i["lastUpdated"])))
                        else:
                            continue
                except TypeError:
                    print("   WARNING! Is not possible to print information about None device!")
        except Exception as e:
            print("   Something's wrong: " + str(e))
