from easypnp_networksys_cz.model import credentials, usercredentials, url
from easypnp_networksys_cz.pnp_apicem import pnp_apicem, apiapicem
from easypnp_networksys_cz.pnp_dnac import pnp_dnac, apidnac
from Lib import re


class Program:
    """ Program controller class """

########################################################################################################################
                                                    # GLOBAL #
########################################################################################################################

    @staticmethod
    def update_credentials():
        """ Update credentials """
        while True:
            try:
                command = input("  Invalid or no credentials. Do you want to continue? (y/n): ")
                if command == "Y" or command == "y":
                    result = usercredentials.UserCredentials.prompt_credentials()
                    if result is None:
                        continue
                    credentials.Credentials.controller_username = result[0]
                    credentials.Credentials.controller_password = result[1]
                    return True
                elif command == "N" or command == "n":
                    return False
            except RuntimeError:
                continue

    @staticmethod
    def get_credentials(c_user=False, c_pass=False):
        """ Get credentials """
        try:
            if c_user == True:
                controller_username = credentials.Credentials.controller_username
                return controller_username
            if c_pass == True:
                controller_password = credentials.Credentials.controller_password
                return controller_password
        except RuntimeError:
            pass

########################################################################################################################
                                                    # APIC-EM #
########################################################################################################################

    @staticmethod
    def run_program_APICEM(path):
        """ Controller method of program for APIC-EM """
        base_path = path
        # Show url settings when address is not set, then exit or continue
        apicem_url = url.Url('apicem_url')
        if not apicem_url.is_set():
            if not Program.APICEMUrlSettings(path, apicem_url):
                return
        apiapicem.ApiAPICEM.set_url(apicem_url.get_url())
        # Run APIC-EM dialog menu
        while True:
            path = Program.__getAPICEMmenupath(base_path)
            try:
                Program.APICEMdialogMenu(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    apiapicem.ApiAPICEM.api_get_user()
                elif command == "2":
                    Program.APICEMgetNetworkDevices()
                elif command == "3":
                    pnp_apicem.PnP_APICEM.pnp_APICEM_menu_main(path)
                elif command == "4":
                    Program.APICEMUrlSettings(path, apicem_url)
                elif command == "5" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def __getAPICEMmenupath(path):
        return path + ' > APIC-EM(' + apiapicem.ApiAPICEM.get_url() + ')'

    @staticmethod
    def APICEMUrlSettings(path, apicem_url):
        # Print menu with configuration
        print("\n" + path + " > Settings:")
        if apicem_url.is_set():
            print(" APIC-EM address: " + apicem_url.get_url())
        else:
            print(" APIC-EM address is not set, please configure before continue!")
        command = input(" 1 - IP\n 2 - DNS\n New controller (enter a number or q)? ")
        if command == "1":
            ip_input = input("  New IP of controller: ")
            ip_pat = '^((\d|\d\d|1\d\d|[2][0-5][0-5])\.){3}(\d|\d\d|1\d\d|[2][0-5][0-5])$'
            # Change IP if matches, otherwise exit settings
            if not re.match(ip_pat, ip_input):
                print("   ERROR! Invalid IP format!")
                return False
            try:
                result = apiapicem.ApiAPICEM.api_connection(ip_input)
                if result == False:
                    return False
                else:
                    print("   Saved successfully!")
                    apicem_url.set_url(ip_input)
                    apiapicem.ApiAPICEM.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        elif command == "2":
            ip_input = input("  New DNS of controller: ")
            try:
                result = apiapicem.ApiAPICEM.api_connection(ip_input)
                if result == False:
                    return False
                else:
                    print("   Saved successfully!")
                    apicem_url.set_url(ip_input)
                    apiapicem.ApiAPICEM.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        elif command == "q" or command == "Q":
            return True

    @staticmethod
    def APICEMdialogMenu(path):
        print("\n" + path + ":\n",
              "1 - Create ticket\n",
              "2 - Network devices\n",
              "3 - EasyPnP\n",
              "4 - Settings\n",
              "5 - Back")

    @staticmethod
    def APICEMgetNetworkDevices():
        """" Get network devices connected to APIC-EM """
        r_json = apiapicem.ApiAPICEM.api_get_network_devices()
        if not r_json == False:
            print("\n" + "  View all devices in network:")
            countDev = 0
            print('   {!s:3}'.format('No:') + "   " + '{!s:15}'.format('Serial num:') + "   " + '{!s:20}'.format(
                'Platform:') + "   " + '{!s:30}'.format('Hostname:') + "   " + '{!s:50}'.format(
                'Series:') + "  " + '{!s:60}'.format('Uptime:'))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:15}'.format(i["serialNumber"]) + "   " + '{!s:20}'.format(
                        i["platformId"]) + "   " + '{!s:30}'.format(i["hostname"]) + "   " + '{!s:50}'.format(
                        i["series"]) + "  " + '{!s:60}'.format(str(i["upTime"])))
            except Exception as e:
                print("   Something's wrong: " + str(e))
            while True:
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
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        deviceID = r_json["response"][cmd - 1]["id"]
                        deviceHN = r_json["response"][cmd - 1]["hostname"]
                        print("\n" + "  All interfaces of device with hostname " + deviceHN + ":")
                        Program.APICEMgetNetworkDevicesInterfaces(deviceID, False)
                        print("  Only UP interfaces of device with hostname " + deviceHN + ":")
                        Program.APICEMgetNetworkDevicesInterfaces(deviceID, True)
                        break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def APICEMgetNetworkDevicesInterfaces(deviceID, upInt=False):
        """" Get interfaces of network devices connected to APIC-EM """
        r_json = apiapicem.ApiAPICEM.api_get_device_interface(deviceID)
        try:
            if upInt == False:
                countDev = 0
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
                    for i in r_json["response"]:
                        countDev += 1
                        print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:35}'.format(i["portName"]) + "   " + '{!s:10}'.format(i["status"]) + "   " + '{!s:15}'.format(
                            str(i["ipv4Address"])) + "   " + '{!s:20}'.format(str(i["ipv4Mask"])) + "   " + '{!s:30}'.format(str(i["lastUpdated"])))
                except TypeError:
                    pass
            else:
                countDev = 0
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
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
                                                     # DNA-C #
########################################################################################################################

    @staticmethod
    def run_program_DNAC(path):
        """ Controller method of program for DNA-C """
        base_path = path
        # Show url settings when address is not set, then exit or continue
        dnac_url = url.Url('dnac_url')
        if not dnac_url.is_set():
            if not Program.DNACUrlSettings(path, dnac_url):
                return
        apidnac.ApiDNAC.set_url(dnac_url.get_url())
        # Run DNA-C dialog menu
        while True:
            path = Program.__getDNACmenupath(base_path)
            try:
                Program.DNACdialogMenu(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    apidnac.ApiDNAC.api_get_host()
                elif command == "2":
                    Program.DNACgetNetworkDevices()
                elif command == "3":
                    pnp_dnac.PnP_DNAC.pnp_DNAC_menu_main(path)
                elif command == "4":
                    Program.DNACUrlSettings(path, dnac_url)
                elif command == "5" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def __getDNACmenupath(path):
        return path + ' > DNA-C(' + apidnac.ApiDNAC.get_url() + ')'

    @staticmethod
    def DNACUrlSettings(path, dnac_url):
        # Print menu with configuration
        print("\n" + path + " > Settings:")
        if dnac_url.is_set():
            print(" DNA-C address: " + dnac_url.get_url())
        else:
            print(" DNA-C address is not set, please configure before continue!")
        command = input(" 1 - IP\n 2 - DNS\n New controller (enter a number or q)? ")
        if command == "1":
            ip_input = input("  New IP of controller: ")
            ip_pat = '^((\d|\d\d|1\d\d|[2][0-5][0-5])\.){3}(\d|\d\d|1\d\d|[2][0-5][0-5])$'
            # Change IP if matches, otherwise exit settings
            if not re.match(ip_pat, ip_input):
                print("   ERROR! Invalid IP format!")
                return False
            try:
                result = apidnac.ApiDNAC.api_connection(ip_input)
                if result == False:
                    return False
                else:
                    print("   Saved successfully!")
                    dnac_url.set_url(ip_input)
                    apidnac.ApiDNAC.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        elif command == "2":
            ip_input = input("  New DNS of controller: ")
            try:
                result = apidnac.ApiDNAC.api_connection(ip_input)
                if result == False:
                    return False
                else:
                    print("   Saved successfully!")
                    dnac_url.set_url(ip_input)
                    apidnac.ApiDNAC.set_url(ip_input)
                    return True
            except Exception as e:
                print("   Something's wrong: " + str(e))
        elif command == "q" or command == "Q":
            return True

    @staticmethod
    def DNACdialogMenu(path):
        print("\n" + path + ":\n",
              "1 - Create token\n",
              "2 - Network devices\n",
              "3 - EasyPnP\n",
              "4 - Settings\n",
              "5 - Back")

    @staticmethod
    def DNACgetNetworkDevices():
        """" Get network devices connected to DNA-C """
        r_json = apidnac.ApiDNAC.api_get_network_devices()
        if not r_json == False:
            print("\n" + "  View all devices in network:")
            countDev = 0
            print('   {!s:3}'.format('No:') + "   " + '{!s:15}'.format('Serial num:') + "   " + '{!s:20}'.format(
                'Platform:') + "   " + '{!s:30}'.format('Hostname:') + "   " + '{!s:50}'.format(
                'Series:') + "  " + '{!s:60}'.format('Uptime:'))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:15}'.format(i["serialNumber"]) + "   " + '{!s:20}'.format(
                        i["platformId"]) + "   " + '{!s:30}'.format(i["hostname"]) + "   " + '{!s:50}'.format(
                        i["series"]) + "  " + '{!s:60}'.format(str(i["upTime"])))
            except Exception as e:
                print("   Something's wrong: " + str(e))
            while True:
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
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        deviceID = r_json["response"][cmd - 1]["id"]
                        deviceHN = r_json["response"][cmd - 1]["hostname"]
                        print("\n" + "  All interfaces of device with hostname " + deviceHN + ":")
                        Program.DNACgetNetworkDevicesInterfaces(deviceID, False)
                        print("  Only UP interfaces of device with hostname " + deviceHN + ":")
                        Program.DNACgetNetworkDevicesInterfaces(deviceID, True)
                        break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def DNACgetNetworkDevicesInterfaces(deviceID, upInt=False):
        """" Get interfaces of network devices connected to DNA-C """
        r_json = apidnac.ApiDNAC.api_get_device_interface(deviceID)
        try:
            if upInt == False:
                countDev = 0
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
                    for i in r_json["response"]:
                        countDev += 1
                        print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:35}'.format(i["portName"]) + "   " + '{!s:10}'.format(i["status"]) + "   " + '{!s:15}'.format(
                            str(i["ipv4Address"])) + "   " + '{!s:20}'.format(str(i["ipv4Mask"])) + "   " + '{!s:30}'.format(str(i["lastUpdated"])))
                except TypeError:
                    pass
            else:
                countDev = 0
                print('   {!s:3}'.format('No:') + "   " + '{!s:35}'.format('Interface:') + "   " + '{!s:10}'.format('State:') + "   " + '{!s:15}'.format(
                    'IP address:') + "   " + '{!s:20}'.format('IP mask:') + "   " + '{!s:30}'.format('Updated:'))
                try:
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
