from easypnp_networksys_cz.model import credentials, isecredentials, sshcredentials, client, directory
from easypnp_networksys_cz.pnp_apicem import apiapicem
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xlrd import open_workbook
from shutil import copyfile
import requests.packages.urllib3
import base64
import os.path
import jinja2

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Disable warnings
#import urllib3
#import requests
#requests.packages.urllib3.disable_warnings()
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#logging.basicConfig(level=logging.INFO)


class PnP_APICEM:
    """ EasyPnP for APIC-EM controller class """
    template_file = "easypnp_networksys_cz/pnp_apicem/template/configuration_template.jnj"
    devices_tab = "easypnp_networksys_cz/pnp_apicem/devices/devices_tab.xlsx"
    configuration_folder = "easypnp_networksys_cz/pnp_apicem/configurations/"

########################################################################################################################
                                                    # DIALOG MENU #
########################################################################################################################

    @staticmethod
    def pnp_APICEM_menu_main(path):
        """ EasyPnP MAIN dialog """
        path = path + " > EasyPnP"
        while True:
            try:
                PnP_APICEM.pnp_APICEM_menu_main_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    try:
                        user_tab = directory.Directory.pick_file_dir("xlsx")
                        if user_tab is None:
                            print("  ERROR! File with devices was not uploaded!")
                        else:
                            copyfile(user_tab, PnP_APICEM.devices_tab)
                            print("  File with devices was uploaded!")
                    except Exception as e:
                        print("   Something's wrong: " + str(e))
                elif command == "2":
                    try:
                        user_template = directory.Directory.pick_file_dir("jnj")
                        if user_template is None:
                            print("  ERROR! File with template was not uploaded!")
                        else:
                            copyfile(user_template, PnP_APICEM.template_file)
                            print("  File with template was uploaded!")
                    except Exception as e:
                        print("   Something's wrong: " + str(e))
                elif command == "3":
                    PnP_APICEM.pnp_APICEM_menu_project(path)
                elif command == "4":
                    PnP_APICEM.pnp_APICEM_menu_configuration(path)
                elif command == "5":
                    PnP_APICEM.pnp_APICEM_menu_device(path)
                elif command == "6" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_APICEM_menu_main_dialog(path):
        print("\n" + path + ":\n",
              "1 - Upload XLS\n",
              "2 - Upload template\n",
              "3 - Project\n",
              "4 - Configuration\n",
              "5 - Device\n",
              "6 - Back")

    @staticmethod
    def pnp_APICEM_menu_project(path):
        """ EasyPnP PROJECT dialog """
        path = path + " > Project"
        while True:
            try:
                PnP_APICEM.pnp_APICEM_menu_project_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    PnP_APICEM.pnp_APICEM_get_project_for_list()
                elif command == "2":
                    PnP_APICEM.pnp_APICEM_create_project()
                elif command == "3":
                    PnP_APICEM.pnp_APICEM_get_project_for_delete()
                elif command == "4":
                    PnP_APICEM.pnp_APICEM_get_project_for_cleaning()
                elif command == "5" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_APICEM_menu_project_dialog(path):
        print("\n" + path + ":\n",
              "1 - List projects\n",
              "2 - Create project\n",
              "3 - Delete project\n",
              "4 - Clean project\n",
              "5 - Back")

    @staticmethod
    def pnp_APICEM_menu_configuration(path):
        """ EasyPnP CONFIGURATION dialog """
        path = path + " > Configuration"
        while True:
            try:
                PnP_APICEM.pnp_APICEM_menu_configuration_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    PnP_APICEM.pnp_APICEM_get_configuration_for_list()
                elif command == "2":
                    PnP_APICEM.pnp_APICEM_make_configuration_excel()
                elif command == "3":
                    PnP_APICEM.pnp_APICEM_upload_configuration()
                elif command == "4":
                    PnP_APICEM.pnp_APICEM_get_configuration_for_delete()
                elif command == "5" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_APICEM_menu_configuration_dialog(path):
        print("\n" + path + ":\n",
              "1 - List configurations\n",
              "2 - Make configurations\n",
              "3 - Upload configurations\n",
              "4 - Delete configurations\n",
              "5 - Back")

    @staticmethod
    def pnp_APICEM_menu_device(path):
        """ EasyPnP DEVICES dialog """
        path = path + " > Device"
        while True:
            try:
                PnP_APICEM.pnp_APICEM_menu_device_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    PnP_APICEM.pnp_APICEM_get_project_for_list_devices()
                elif command == "2":
                    PnP_APICEM.pnp_APICEM_menu_device_upload(path)
                elif command == "3":
                    PnP_APICEM.pnp_APICEM_get_project_for_deleting_devices(False)
                elif command == "4":
                    PnP_APICEM.pnp_APICEM_get_project_for_deleting_devices(True)
                elif command == "5" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_APICEM_menu_device_dialog(path):
        print("\n" + path + ":\n",
              "1 - View devices in project\n",
              "2 - Upload devices to project\n",
              "3 - Delete device from project\n",
              "4 - Mass deleting and reloading devices\n",
              "5 - Back")

    @staticmethod
    def pnp_APICEM_menu_device_upload(path):
        """ EasyPnP DEVICES UPLOAD dialog """
        path = path + " > Upload"
        while True:
            try:
                PnP_APICEM.pnp_APICEM_menu_device_upload_dialog(path)
                command = input(" Where do you want to upload (enter a number or q)? ")
                if command == "1":
                    PnP_APICEM.pnp_APICEM_get_project_for_post_devices()
                elif command == "2":
                    PnP_APICEM.pnp_APICEM_get_project_for_post_devices_toISE()
                elif command == "3" or command == "q" or command == "Q":
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_APICEM_menu_device_upload_dialog(path):
        print("\n" + path + ":\n",
              "1 - APIC-EM\n",
              "2 - APIC-EM and ISE\n",
              "3 - Back")

########################################################################################################################
                                                    # PROJECT #
########################################################################################################################

    @staticmethod
    def pnp_APICEM_get_project_for_list():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")

    @staticmethod
    def pnp_APICEM_create_project():
        project_name = input("  Enter name of your new project (or q for exit): ")
        if project_name == "q" or project_name == "Q":
            pass
        else:
            apiapicem.ApiAPICEM.api_create_pnp_project(project_name)

    @staticmethod
    def pnp_APICEM_get_project_for_delete():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  Which PnP project do you want to delete (enter index or q for exit)? ")
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
                        projectID = r_json["response"][cmd - 1]["id"]
                        PnP_APICEM.pnp_APICEM_safe_delete_project(projectID)
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_safe_delete_project(projectID):
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project_devices(projectID, False)
        if r_json["response"] == []:
            apiapicem.ApiAPICEM.api_delete_pnp_project(projectID)
        else:
            command = input("   WARNING! Project is not empty! Do you want to delete project with all assigned devices and configurations (y/n)? ")
            if command == "Y" or command == "y":
                PnP_APICEM.pnp_APICEM_safe_clean_project(projectID, False)
                apiapicem.ApiAPICEM.api_delete_pnp_project(projectID, False)
                print("    Project was successfully deleted!")
            elif command == "N" or command == "n":
                pass

    @staticmethod
    def pnp_APICEM_get_project_for_cleaning():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  Which PnP project do you want to clean (enter index or q for exit)? ")
                if cmd == "q" or cmd == "Q":
                    break
                # Create index
                try:
                    cmd = int(cmd)
                except ValueError:
                    #  Next iteration
                    continue
                # If index exists
                try:
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        PnP_APICEM.pnp_APICEM_safe_clean_project(projectID)
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_safe_clean_project(projectID, printResp=True):
        if printResp:
            r_json = apiapicem.ApiAPICEM.api_get_pnp_project_devices(projectID)
        else:
            r_json = apiapicem.ApiAPICEM.api_get_pnp_project_devices(projectID, False)
        try:
            if not r_json["response"] == []:
                try:
                    for i in r_json["response"]:
                        # Deleting devices in project
                        if i.get("id"):
                            deviceID = i["id"]
                            apiapicem.ApiAPICEM.api_delete_pnp_project_devices(projectID, deviceID, False)
                        # Deleting devices
                        if i.get("serialNumber"):
                            serialNO = i["serialNumber"]
                            PnP_APICEM.pnp_APICEM_get_devices_for_delete(serialNO, False)
                        # Deleting configurations from APIC-EM
                        if i.get("configId"):
                            configurationID = i["configId"]
                            apiapicem.ApiAPICEM.api_delete_pnp_configuration(configurationID, False, False, True)
                except Exception as e:
                    print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))
                print("   All devices from project were successfully deleted!") if printResp else print("    All devices from project were successfully deleted!")
                print("   All assigned configurations to project were successfully deleted!") if printResp else print("    All assigned configurations to project were successfully deleted!")
            else:
                print("   Project is already clean!")
        except Exception as e:
            print("   Something's wrong: " + str(e))

########################################################################################################################
                                                 # CONFIGURATION #
########################################################################################################################

    @staticmethod
    def pnp_APICEM_get_configuration_for_list():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_configuration()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:40}'.format("Name:") + "   " + '{!s:10}'.format(
                "Size:") + "   " + '{!s:10}'.format("Format:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:40}'.format(i["name"]) + "   "  + '{!s:10}'.format(
                        str(i["fileSize"])) + "   "  + '{!s:10}'.format(str(i["fileFormat"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")

    @staticmethod
    def pnp_APICEM_make_configuration_excel():
        if not os.path.isfile(PnP_APICEM.template_file):
            if not os.path.isfile(PnP_APICEM.devices_tab):
                print("  ERROR! The table of devices was not loaded correctly!")
                print("  ERROR! The template was not loaded correctly!")
                return
            print("  ERROR! The template was not loaded correctly!")
            return
        try:
            templateLoader = jinja2.FileSystemLoader(searchpath=".")
            templateEnvironment = jinja2.Environment(loader=templateLoader)
            templateFinal = templateEnvironment.get_template(PnP_APICEM.template_file)
        except Exception as e:
            print("  Something's wrong: " + str(e))
        # Creating configurations for rows in devices_tab
        try:
            data_set = PnP_APICEM.pnp_APICEM_read_excel(PnP_APICEM.devices_tab)
            try:
                cycle = 0
                number = 0
                for i in data_set:
                    outputText = templateFinal.render(i)
                    configuration_path = PnP_APICEM.configuration_folder + i['hostName'] + '_configuration'
                    configuration_name = i['hostName'] + '_configuration'
                    cycle += 1
                    if os.path.isfile(configuration_path):
                        print("  File " + configuration_name + " has already been created in the past, rewriting!")
                        number += 1
                        try:
                            with open(configuration_path, 'w') as configuration_file:
                                configuration_file.write(outputText)
                        except Exception as e:
                            print("  Something's wrong: " + str(e))
                    else:
                        try:
                            with open(configuration_path, 'w') as configuration_file:
                                configuration_file.write(outputText)
                            print("  File " + configuration_name + " was successfully created!")
                            number += 1
                        except Exception as e:
                            print("  Something's wrong: " + str(e))
                print("\n" + "   STATS! Successfully created configurations: " + str(number) + " / " + str(cycle))
            except Exception as e:
                print("  Something's wrong: " + str(e))
        except Exception as e:
            print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_read_excel(devices_tab):
        # Loading data from excel
        excel = open_workbook(devices_tab)
        data = []
        for s in excel.sheets():
            for row in range(1, s.nrows):
                col_names = s.row(0)
                col_value = {}
                for name, col in zip(col_names, range(s.ncols)):
                    value = s.cell(row, col).value
                    try:
                        value = str(int(value))
                    except:
                        pass
                    col_value.setdefault(name.value, value)
                data.append(col_value)
        return data

    @staticmethod
    def pnp_APICEM_upload_configuration():
        # Reading configurations
        if not os.listdir(PnP_APICEM.configuration_folder):
            print("  WARNING! There are no configurations in folder! First make configurations!")
        else:
            try:
                cycle = 0
                number = 0
                for configuration_file in os.listdir(PnP_APICEM.configuration_folder):
                    configuration_path = PnP_APICEM.configuration_folder + "" + configuration_file
                    cycle += 1
                    try:
                        if (os.path.isfile(configuration_path)) and (not configuration_file.startswith('.')):
                            number = apiapicem.ApiAPICEM.api_upload_pnp_configuration(configuration_path, configuration_file, number)
                            if number == False:
                                return False
                        else:
                            print("  Folder with configurations does not exist!")
                    except Exception as e:
                        print("  Something's wrong: " + str(e))
                print("\n" + "   STATS! Successfully uploaded configurations: " + str(number) + " / " + str(cycle))
            except Exception as e:
                print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_get_configuration_for_delete():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_configuration()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:40}'.format("Name:") + "   " + '{!s:10}'.format(
                "Size:") + "   " + '{!s:10}'.format("Format:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:40}'.format(i["name"]) + "   " + '{!s:10}'.format(
                        str(i["fileSize"])) + "   " + '{!s:10}'.format(str(i["fileFormat"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  Which PnP configuration do you want to delete (enter index / 0 for all / q for exit)? ")
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
                        configurationID = r_json["response"][cmd - 1]["id"]
                        apiapicem.ApiAPICEM.api_delete_pnp_configuration(configurationID, True, False, False)
                except Exception as e:
                    print("  Something's wrong: " + str(e))
                try:
                    if cmd == 0:
                        for i in r_json["response"]:
                            configurationID = i.get("id")
                            apiapicem.ApiAPICEM.api_delete_pnp_configuration(configurationID, False, False, False)
                            continue
                        print("   <Response [200]>")
                        print("   All configurations were successfully deleted!")
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

########################################################################################################################
                                                    # DEVICE #
########################################################################################################################

    @staticmethod
    def pnp_APICEM_get_project_for_list_devices():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  In which PnP project do you want to see the devices (enter index or q for exit)? ")
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
                        projectID = r_json["response"][cmd - 1]["id"]
                        PnP_APICEM.pnp_APICEM_print_project_devices_for_list(projectID)
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_print_project_devices_for_list(projectID):
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project_devices(projectID)
        countDev = 0
        print('   {!s:3}'.format("No:") + "   " + '{!s:20}'.format("Hostname:") + "   " + '{!s:25}'.format(
            "Platform:") + "   " + '{!s:18}'.format("Serial num:") + "   " + '{!s:25}'.format(
            "State:") + "   " + '{!s:10}'.format("PKI:") + "   " + '{!s:20}'.format("Updated:"))
        try:
            for i in r_json["response"]:
                countDev += 1
                lastContact = i.get('lastContact')
                lastContact = '{!s:20}'.format(lastContact) if lastContact else '{!s:20}'.format("")
                print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["hostName"]) + "   " + '{!s:25}'.format(
                    i["platformId"]) + "   " + '{!s:18}'.format(i["serialNumber"]) + "   " + '{!s:25}'.format(
                    i["state"]) + "   " + '{!s:10}'.format(i["pkiEnabled"]) + "   " + lastContact)
        except TypeError:
            print("   WARNING! Is not possible to print information!")

    @staticmethod
    def pnp_APICEM_get_project_for_deleting_devices(reload=True):
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  In which PnP project do you want to see the devices (enter index or q for exit)? ")
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
                        projectID = r_json["response"][cmd - 1]["id"]
                        if reload == False:
                            PnP_APICEM.pnp_APICEM_print_project_devices_for_deleting(projectID)
                            break
                        else:
                            PnP_APICEM.pnp_APICEM_print_project_devices_for_reloading(projectID)
                            break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_print_project_devices_for_deleting(projectID):
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project_devices(projectID)
        countDev = 0
        deviceID = []
        configurationID = []
        serialNO = []
        print('   {!s:3}'.format("No:") + "   " + '{!s:20}'.format("Hostname:") + "   " + '{!s:25}'.format(
            "Platform:") + "   " + '{!s:18}'.format("Serial num:") + "   " + '{!s:25}'.format(
            "State:") + "   " + '{!s:10}'.format("PKI:") + "   " + '{!s:20}'.format("Updated:"))
        try:
            for i in r_json["response"]:
                countDev += 1
                lastContact = i.get('lastContact')
                lastContact = '{!s:20}'.format(lastContact) if lastContact else '{!s:20}'.format("")
                print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["hostName"]) + "   " + '{!s:25}'.format(
                    i["platformId"]) + "   " + '{!s:18}'.format(i["serialNumber"]) + "   " + '{!s:25}'.format(
                    i["state"]) + "   " + '{!s:10}'.format(i["pkiEnabled"]) + "   " + lastContact)
        except TypeError:
            print("   WARNING! Is not possible to print information!")
        try:
            if not r_json["response"] == []:
                while True:
                    cmd = input("   Which PnP device do you want to delete (enter index or q for exit)? ")
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
                            if not r_json["response"][cmd - 1].get("id") == None:
                                deviceID = r_json["response"][cmd - 1]["id"]
                            if not r_json["response"][cmd - 1].get("configId") == None:
                                configurationID = r_json["response"][cmd - 1]["configId"]
                            if not r_json["response"][cmd - 1].get("serialNumber") == None:
                                serialNO = r_json["response"][cmd - 1]["serialNumber"]
                            while True:
                                cmd2 = input("    Do you want to clean and reload device as well (y/n/q for exit)? ")
                                if cmd2 == "q" or cmd2 == "Q":
                                    break
                                if cmd2 == "n" or cmd2 == "N":
                                    if not deviceID == []:
                                        apiapicem.ApiAPICEM.api_delete_pnp_project_devices(projectID, deviceID, True)
                                    if not configurationID == []:
                                        apiapicem.ApiAPICEM.api_delete_pnp_configuration(configurationID, False, True, False)
                                    if not serialNO == []:
                                        PnP_APICEM.pnp_APICEM_get_devices_for_delete(serialNO, False)
                                    break
                                if cmd2 == "y" or cmd2 == "Y":
                                    PnP_APICEM.pnp_APICEM_get_SSH_infomation()
                                    result = client.Client.ssh_access(credentials.Credentials.ssh_address, credentials.Credentials.ssh_username, credentials.Credentials.ssh_password, True)
                                    if result == True:
                                        if not deviceID == []:
                                            apiapicem.ApiAPICEM.api_delete_pnp_project_devices(projectID, deviceID, False)
                                        if not configurationID == []:
                                            apiapicem.ApiAPICEM.api_delete_pnp_configuration(configurationID, False, True, False)
                                        if not serialNO == []:
                                            PnP_APICEM.pnp_APICEM_get_devices_for_delete(serialNO, False)
                                        print("     Device " + r_json["response"][cmd - 1]["hostName"] + " was successfully deleted, cleaned and reloaded!")
                                        break
                                    else:
                                        print("     ERROR! Connection to device " +  r_json["response"][cmd - 1]["hostName"] + " failed!")
                                        print("     ERROR! Device was not successfully deleted, cleaned and reloaded!")
                                        break
                    except Exception as e:
                        print("  Something's wrong: " + str(e))
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_print_project_devices_for_reloading(projectID):
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project_devices(projectID)
        countDev = 0
        print('   {!s:3}'.format("No:") + "   " + '{!s:20}'.format("Hostname:") + "   " + '{!s:25}'.format(
            "Platform:") + "   " + '{!s:18}'.format("Serial num:") + "   " + '{!s:25}'.format(
            "State:") + "   " + '{!s:10}'.format("PKI:") + "   " + '{!s:20}'.format("Updated:"))
        try:
            for i in r_json["response"]:
                countDev += 1
                lastContact = i.get('lastContact')
                lastContact = '{!s:20}'.format(lastContact) if lastContact else '{!s:20}'.format("")
                print('   {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["hostName"]) + "   " + '{!s:25}'.format(
                    i["platformId"]) + "   " + '{!s:18}'.format(i["serialNumber"]) + "   " + '{!s:25}'.format(
                    i["state"]) + "   " + '{!s:10}'.format(i["pkiEnabled"]) + "   " + lastContact)
        except TypeError:
            print("   WARNING! Is not possible to print information!")
        try:
            if not r_json["response"] == []:
                while True:
                    try:
                        cmd = input("   Do you want to try delete, clean and reload all these devices (y/n)? ")
                        if cmd == "n" or cmd == "N":
                            break
                        if cmd == "y" or cmd == "Y":
                            PnP_APICEM.pnp_APICEM_mass_devices_reloading(r_json, projectID)
                            break
                    except Exception as e:
                        print("   Something's wrong: " + str(e))
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_mass_devices_reloading(r_json, projectID):
        helpList = r_json['response']
        for x in helpList:
            dId = x.get("id")
            cId = x.get("configId")
            sId = x.get("serialNumber")
            if dId == None:
                x.update({"id": ""})
            if cId == None:
                x.update({"configId": ""})
            if sId == None:
                x.update({"serialNumber": ""})
        #print("File list " + json.dumps(helpList, indent=2))
        deviceTuple = [(device['hostName'], device['id']) for device in helpList]
        configurationTuple = [(configuration['hostName'], configuration['configId']) for configuration in helpList]
        serialTuple = [(serial['hostName'], serial['serialNumber']) for serial in helpList]
        try:
            if not os.path.isfile(PnP_APICEM.devices_tab):
                print("    ERROR! The table of devices was not loaded correctly!")
                return
            else:
                data_set = PnP_APICEM.pnp_APICEM_read_excel(PnP_APICEM.devices_tab)
                cycle = 0
                number = 0
                try:
                    for i in data_set:
                        cycle += 1
                        try:
                            serialNum = [sn for hn, sn in serialTuple if hn == i["hostName"]][0]
                            if not serialNum == i["serialNumber"]:
                                print("    ERROR! SN of device " + i["hostName"] + " in table does not match with SN of device in project!")
                                continue
                            else:
                                deviceID = [dev for hn, dev in deviceTuple if hn == i["hostName"]][0]
                                configurationID = [cn for hn, cn in configurationTuple if hn == i["hostName"]][0]
                        except Exception as e:
                            print("    ERROR! Device " + i["hostName"] + " in table does not match with device in project!")
                            continue
                        try:
                            if i["ipAddress"] == "":
                                print('    ERROR! Item "ipAddress" for device ' + i["hostName"] + ' is not defined in the xls table!')
                                continue
                            if i["userName"] == "":
                                print('    ERROR! Item "userName" for device ' + i["hostName"] + ' is not defined in the xls table!')
                                continue
                            if i["passWord"] == "":
                                print('    ERROR! Item "passWord" for device ' + i["hostName"] + ' is not defined in the xls table!')
                                continue
                            #print("    " + i["ipAddress"], i["userName"], i["passWord"])
                        except Exception:
                            print("    INFO! Process was stopped! Please upload the correct table of these devices with items (ipAddress, userName, passWord)!")
                            break
                        result = client.Client.ssh_access(i["ipAddress"], i["userName"], i["passWord"], False)
                        if result == True:
                            if not deviceID == "":
                                apiapicem.ApiAPICEM.api_delete_pnp_project_devices(projectID, deviceID, False)
                            if not configurationID == "":
                                apiapicem.ApiAPICEM.api_delete_pnp_configuration(configurationID, False, False, True)
                            if not serialNum == "":
                                PnP_APICEM.pnp_APICEM_get_devices_for_delete(serialNum, False)
                            number += 1
                            print("    Device " + i["hostName"] + " was successfully deleted, cleaned and reloaded!")
                            continue
                        else:
                            print("    ERROR! Connection to device " + i["hostName"] + " failed!")
                            continue
                    print("\n" + "     STATS! Successfully deleted, cleaned and reloaded devices: " + str(number) + " / " + str(cycle))
                except Exception as e:
                    print("    Something's wrong: " + str(e))
        except Exception as e:
            print("    Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_get_SSH_infomation():
        while True:
            try:
                result = sshcredentials.SSHCredentials.prompt_credentials()
                credentials.Credentials.ssh_address = result[0]
                credentials.Credentials.ssh_username = result[1]
                credentials.Credentials.ssh_password = result[2]
                return True
            except RuntimeError:
                continue

    @staticmethod
    def pnp_APICEM_get_devices_for_delete(serialNO, printResp=True):
        r_json = apiapicem.ApiAPICEM.api_get_pnp_devices(False)
        if not r_json["response"] == []:
            try:
                for i in r_json["response"]:
                    # Deleting devices
                    if i.get("serialNumber") == serialNO:
                        deviceID = i["id"]
                        apiapicem.ApiAPICEM.api_delete_pnp_devices(deviceID, False)
            except Exception as e:
                print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_get_project_for_post_devices():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  In which PnP project do you want to create the devices (enter index or q for exit)? ")
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
                        projectID = r_json["response"][cmd - 1]["id"]
                        if not os.path.isfile(PnP_APICEM.devices_tab):
                            print("   ERROR! The table of devices was not loaded correctly!")
                            return
                        else:
                            data_set = PnP_APICEM.pnp_APICEM_read_excel(PnP_APICEM.devices_tab)
                            apiapicem.ApiAPICEM.api_post_pnp_project_devices(projectID, data_set)
                            break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_get_project_for_post_devices_toISE():
        r_json = apiapicem.ApiAPICEM.api_get_pnp_project()
        if not r_json == False:
            countDev = 0
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                cmd = input("  In which PnP project do you want to create the devices (enter index or q for exit)? ")
                if cmd == "q" or cmd == "Q":
                    break
                # Create index
                try:
                    cmd = int(cmd)
                except ValueError:
                    #  Next iteration
                    continue
                # If index exists
                try:
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        if PnP_APICEM.pnp_APICEM_get_ISE_infomation() == False:
                            break
                        if not os.path.isfile(PnP_APICEM.devices_tab):
                            print("   ERROR! The table of devices was not loaded correctly!")
                            return
                        else:
                            data_set = PnP_APICEM.pnp_APICEM_read_excel(PnP_APICEM.devices_tab)
                            ise_url = "https://" + credentials.Credentials.ise_address + ":9060/ers/config/networkdevice"
                            ise_credentials = (credentials.Credentials.ise_username + ":" + credentials.Credentials.ise_password).encode("utf-8")
                            ise_credentials_b64 = (base64.b64encode(ise_credentials)).decode("utf-8")
                            apiapicem.ApiAPICEM.api_post_pnp_project_devices_toISE(projectID, data_set, ise_credentials_b64, ise_url)
                            break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_APICEM_get_ISE_infomation():
        while True:
            try:
                command = input("   WARNING! You have chosen to create the devices to the ISE as well. Do you want to continue (y/n)? ")
                if command == "Y" or command == "y":
                    if not credentials.Credentials.ise_address == "" and not credentials.Credentials.ise_username == "" and not credentials.Credentials.ise_password == "":
                        command = input("   IP and credentials for ISE have already been set. Do you want to enter a new information (y/n)? ")
                        if command == "Y" or command == "y":
                            pass
                        elif command == "N" or command == "n":
                            return True
                    result = isecredentials.ISECredentials.prompt_credentials()
                    if result is None:
                        continue
                    credentials.Credentials.ise_address = result[0]
                    credentials.Credentials.ise_username = result[1]
                    credentials.Credentials.ise_password = result[2]
                    return True
                elif command == "N" or command == "n":
                    return False
            except RuntimeError:
                continue
