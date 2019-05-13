from easypnp_networksys_cz.model import credentials, isecredentials, sshcredentials, client, directory
from easypnp_networksys_cz.pnp_dnac import apidnac
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xlrd import open_workbook
from shutil import copyfile
import requests.packages.urllib3
import base64
import os.path
import jinja2

# Disable warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Logging for troubleshooting
#logging.basicConfig(level=logging.INFO)


class PnP_DNAC:
    """ Class for managing EasyPnP in DNA-C controller """
    # Variables that store the local path to specific files
    template_file = "easypnp_networksys_cz/pnp_dnac/template/configuration_template.jnj"
    devices_tab = "easypnp_networksys_cz/pnp_dnac/devices/devices_tab.xlsx"
    configuration_folder = "easypnp_networksys_cz/pnp_dnac/configurations/"

########################################################################################################################
                                                    # MENU #
########################################################################################################################

    @staticmethod
    def pnp_DNAC_menu_main(path):
        """ Method for EasyPnP MAIN dialog """
        # The variable informing about location in menu
        path = path + " > EasyPnP"
        # Run EasyPnP main menu
        while True:
            try:
                # Display EasyPnP main menu
                PnP_DNAC.pnp_DNAC_menu_main_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    # Select XLS table with defined devices
                    try:
                        # Save path to the file into user_tab variable (using method from Directory class)
                        user_tab = directory.Directory.pick_file_dir("xlsx")
                        if user_tab is None:
                            print("  ERROR! File with devices was not uploaded!")
                        else:
                            # Copy XLS table into local place
                            copyfile(user_tab, PnP_DNAC.devices_tab)
                            print("  File with devices was uploaded!")
                    except Exception as e:
                        print("   Something's wrong: " + str(e))
                elif command == "2":
                    # Select configuration template
                    try:
                        # Save path to the file into user_template variable (using method from Directory class)
                        user_template = directory.Directory.pick_file_dir("jnj")
                        if user_template is None:
                            print("  ERROR! File with template was not uploaded!")
                        else:
                            # Copy configuration template into local place
                            copyfile(user_template, PnP_DNAC.template_file)
                            print("  File with template was uploaded!")
                    except Exception as e:
                        print("   Something's wrong: " + str(e))
                elif command == "3":
                    # Display EasyPnP project menu
                    PnP_DNAC.pnp_DNAC_menu_project(path)
                elif command == "4":
                    # Display EasyPnP configuration menu
                    PnP_DNAC.pnp_DNAC_menu_configuration(path)
                elif command == "5":
                    # Display EasyPnP device menu
                    PnP_DNAC.pnp_DNAC_menu_device(path)
                elif command == "6" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_DNAC_menu_main_dialog(path):
        """ Method to display options of EasyPnP main menu """
        print("\n" + path + ":\n",
              "1 - Upload XLS\n",
              "2 - Upload template\n",
              "3 - Project\n",
              "4 - Configuration\n",
              "5 - Device\n",
              "6 - Back")

    @staticmethod
    def pnp_DNAC_menu_project(path):
        """ Method for EasyPnP PROJECT dialog """
        # The variable informing about location in menu
        path = path + " > Project"
        # Run EasyPnP project menu
        while True:
            try:
                # Display EasyPnP project menu
                PnP_DNAC.pnp_DNAC_menu_project_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    # List projects
                    PnP_DNAC.pnp_DNAC_get_project_for_list()
                elif command == "2":
                    # Create project
                    PnP_DNAC.pnp_DNAC_create_project()
                elif command == "3":
                    # Delete project
                    PnP_DNAC.pnp_DNAC_get_project_for_delete()
                elif command == "4":
                    # Clean project
                    PnP_DNAC.pnp_DNAC_get_project_for_cleaning()
                elif command == "5" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_DNAC_menu_project_dialog(path):
        """ Method to display options of EasyPnP project menu """
        print("\n" + path + ":\n",
              "1 - List projects\n",
              "2 - Create project\n",
              "3 - Delete project\n",
              "4 - Clean project\n",
              "5 - Back")

    @staticmethod
    def pnp_DNAC_menu_configuration(path):
        """ Method for EasyPnP CONFIGURATION dialog """
        # The variable informing about location in menu
        path = path + " > Configuration"
        # Run EasyPnP configuration menu
        while True:
            try:
                # Display EasyPnP configuration menu
                PnP_DNAC.pnp_DNAC_menu_configuration_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    # List configurations
                    PnP_DNAC.pnp_DNAC_get_configuration_for_list()
                elif command == "2":
                    # Make configurations
                    PnP_DNAC.pnp_DNAC_make_configuration_excel()
                elif command == "3":
                    # Upload configurations
                    PnP_DNAC.pnp_DNAC_upload_configuration()
                elif command == "4":
                    # Delete configurations
                    PnP_DNAC.pnp_DNAC_get_configuration_for_delete()
                elif command == "5" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_DNAC_menu_configuration_dialog(path):
        """ Method to display options of EasyPnP configuration menu """
        print("\n" + path + ":\n",
              "1 - List configurations\n",
              "2 - Make configurations\n",
              "3 - Upload configurations\n",
              "4 - Delete configurations\n",
              "5 - Back")

    @staticmethod
    def pnp_DNAC_menu_device(path):
        """ Method for EasyPnP DEVICES dialog """
        # The variable informing about location in menu
        path = path + " > Device"
        # Run EasyPnP devices menu
        while True:
            try:
                # Display EasyPnP devices menu
                PnP_DNAC.pnp_DNAC_menu_device_dialog(path)
                command = input(" What do you want to do (enter a number or q)? ")
                if command == "1":
                    # View devices in project
                    PnP_DNAC.pnp_DNAC_get_project_for_list_devices()
                elif command == "2":
                    # Upload devices to project
                    PnP_DNAC.pnp_DNAC_menu_device_upload(path)
                elif command == "3":
                    # Delete device from project
                    PnP_DNAC.pnp_DNAC_get_project_for_deleting_devices(False)
                elif command == "4":
                    # Mass deleting and reloading devices
                    PnP_DNAC.pnp_DNAC_get_project_for_deleting_devices(True)
                elif command == "5" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_DNAC_menu_device_dialog(path):
        """ Method to display options of EasyPnP devices menu """
        print("\n" + path + ":\n",
              "1 - View devices in project\n",
              "2 - Upload devices to project\n",
              "3 - Delete device from project\n",
              "4 - Mass deleting and reloading devices\n",
              "5 - Back")

    @staticmethod
    def pnp_DNAC_menu_device_upload(path):
        """ Method for EasyPnP UPLOAD DEVICES dialog """
        # The variable informing about location in menu
        path = path + " > Upload"
        while True:
            try:
                # Display EasyPnP upload devices menu
                PnP_DNAC.pnp_DNAC_menu_device_upload_dialog(path)
                command = input(" Where do you want to upload (enter a number or q)? ")
                if command == "1":
                    # Upload devices to DNA-C
                    PnP_DNAC.pnp_DNAC_get_project_for_post_devices()
                elif command == "2":
                    # Upload devices to DNA-C and ISE
                    PnP_DNAC.pnp_DNAC_get_project_for_post_devices_toISE()
                elif command == "3" or command == "q" or command == "Q":
                    # Go back
                    break
            except RuntimeError:
                continue

    @staticmethod
    def pnp_DNAC_menu_device_upload_dialog(path):
        """ Method to display options of EasyPnP upload devices menu """
        print("\n" + path + ":\n",
              "1 - DNA-C\n",
              "2 - DNA-C and ISE\n",
              "3 - Back")

########################################################################################################################
                                                    # PROJECT #
########################################################################################################################

    @staticmethod
    def pnp_DNAC_get_project_for_list():
        """" Method for listing all project """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")

    @staticmethod
    def pnp_DNAC_create_project():
        """" Method for creating project """
        # Save entered name of project into project_name variable
        project_name = input("  Enter name of your new project (or q for exit): ")
        if project_name == "q" or project_name == "Q":
            pass
        else:
            # Use the API call method with project_name parameter to create a project
            apidnac.ApiDNAC.api_create_pnp_project(project_name)

    @staticmethod
    def pnp_DNAC_get_project_for_delete():
        """" Method for getting all projects for deleting """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific project (using the index) for deleting
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
                    # Create projectID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        # Call the method with projectID parameter to safe delete a project
                        PnP_DNAC.pnp_DNAC_safe_delete_project(projectID)
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_safe_delete_project(projectID):
        """" Method for safe deleting project """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project_devices(projectID, False)
        # If project is empty
        if r_json["response"] == []:
            # Use the API call method with projectID parameter to delete a project
            apidnac.ApiDNAC.api_delete_pnp_project(projectID)
        # If project isn't empty
        else:
            command = input("   WARNING! Project is not empty! Do you want to delete project with all assigned devices and configurations (y/n)? ")
            if command == "Y" or command == "y":
                # First call the method with projectID parameter to safe clean a project
                PnP_DNAC.pnp_DNAC_safe_clean_project(projectID, False)
                # Then use the API call method with projectID parameter to delete a project
                apidnac.ApiDNAC.api_delete_pnp_project(projectID, False)
                # Print information about successful deleting of project
                print("    Project was successfully deleted!")
            elif command == "N" or command == "n":
                pass

    @staticmethod
    def pnp_DNAC_get_project_for_cleaning():
        """" Method for getting all projects for cleaning """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific project (using the index) for cleaning
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
                    # Create projectID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        # Call the method with projectID parameter to safe clean a project
                        PnP_DNAC.pnp_DNAC_safe_clean_project(projectID)
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_safe_clean_project(projectID, printResp=True):
        """" Method for safe cleaning project """
        # Save result of this API call into r_json variable
        if printResp:
            r_json = apidnac.ApiDNAC.api_get_pnp_project_devices(projectID)
        else:
            r_json = apidnac.ApiDNAC.api_get_pnp_project_devices(projectID, False)
        try:
            # If project isn't empty
            if not r_json["response"] == []:
                try:
                    for i in r_json["response"]:
                        # Use the API call method and delete all devices associated with the project (using deviceID variable)
                        if i.get("id"):
                            deviceID = i["id"]
                            apidnac.ApiDNAC.api_delete_pnp_project_devices(projectID, deviceID, False)
                        # Call the method and delete all devices associated with the project (using serialNO variable)
                        if i.get("serialNumber"):
                            serialNO = i["serialNumber"]
                            PnP_DNAC.pnp_DNAC_get_devices_for_delete(serialNO, False)
                        # Use the API call method and delete all configurations associated with the project (using configurationID variable)
                        if i.get("configId"):
                            configurationID = i["configId"]
                            apidnac.ApiDNAC.api_delete_pnp_configuration(configurationID, False, False, True)
                except Exception as e:
                    print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))
                # Print information about successful deleting of devices and configurations
                print("   All devices from project were successfully deleted!") if printResp else print("    All devices from project were successfully deleted!")
                print("   All assigned configurations to project were successfully deleted!") if printResp else print("    All assigned configurations to project were successfully deleted!")
            else:
                # Print information about successful cleaning of project
                print("   Project is already clean!")
        except Exception as e:
            print("   Something's wrong: " + str(e))

########################################################################################################################
                                                # CONFIGURATION #
########################################################################################################################

    @staticmethod
    def pnp_DNAC_get_configuration_for_list():
        """" Method for listing all configurations """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_configuration()
        if not r_json == False:
            # Variable for indexing configurations
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:40}'.format("Name:") + "   " + '{!s:10}'.format(
                "Size:") + "   " + '{!s:10}'.format("Format:"))
            try:
                # Print all configurations
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:40}'.format(i["name"]) + "   " + '{!s:10}'.format(
                        str(i["fileSize"])) + "   " + '{!s:10}'.format(str(i["fileFormat"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")

    @staticmethod
    def pnp_DNAC_make_configuration_excel():
        """" Method for making configurations """
        # If the XLS table or the template isn't loaded, print an error
        if not os.path.isfile(PnP_DNAC.devices_tab) or not os.path.isfile(PnP_DNAC.template_file):
            if not os.path.isfile(PnP_DNAC.devices_tab):
                print("  ERROR! The table of devices was not loaded correctly!")
            if not os.path.isfile(PnP_DNAC.template_file):
                print("  ERROR! The template was not loaded correctly!")
            return
        try:
            # Load data from the template using jinja2 packages
            templateLoader = jinja2.FileSystemLoader(searchpath=".")
            templateEnvironment = jinja2.Environment(loader=templateLoader)
            templateFinal = templateEnvironment.get_template(PnP_DNAC.template_file)
        except Exception as e:
            print("  Something's wrong: " + str(e))
        try:
            # Load data from the XLS table using the method described below
            data_set = PnP_DNAC.pnp_DNAC_read_excel(PnP_DNAC.devices_tab)
            try:
                # Variables for final stats
                cycle = 0
                number = 0
                # Run the cycle for creating configurations according to rows in XLS table ("data_set" is the list of dictionaries)
                for i in data_set:
                    # Go through the template and fill in all the variables according to the first dictionary in the list ("data set")
                    outputText = templateFinal.render(i)
                    # Create variables related to the created configuration
                    configuration_path = PnP_DNAC.configuration_folder + i['hostName'] + '_configuration'
                    configuration_name = i['hostName'] + '_configuration'
                    cycle += 1
                    # If configuration (with the same name) has already been created, rewrite it
                    if os.path.isfile(configuration_path):
                        # Print notification
                        print("  File " + configuration_name + " has already been created in the past, rewriting!")
                        number += 1
                        try:
                            # Rewrite the configuration inside the local folder
                            with open(configuration_path, 'w') as configuration_file:
                                configuration_file.write(outputText)
                        except Exception as e:
                            print("  Something's wrong: " + str(e))
                    else:
                        try:
                            # Save the created configuration into the local folder
                            with open(configuration_path, 'w') as configuration_file:
                                configuration_file.write(outputText)
                            # Print information about successful creating of configuration
                            print("  File " + configuration_name + " was successfully created!")
                            number += 1
                        except Exception as e:
                            print("  Something's wrong: " + str(e))
                # Print the stats about creating of configurations
                print("\n" + "   STATS! Successfully created configurations: " + str(number) + " / " + str(cycle))
            except Exception as e:
                print("  Something's wrong: " + str(e))
        except Exception as e:
            print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_read_excel(devices_tab):
        """" Method for reading XLS table """
        # Load the data from the XLS table using xlrd packages (module open_workbook)
        excel = open_workbook(devices_tab)
        # Create an empty list ("data")
        data = []
        # Run the cycle for filling in the list ("data")
        for s in excel.sheets():
            # For every row in XLS table
            for row in range(1, s.nrows):
                # Fill in the list ("col_names") with zero-row column names ("hostName", "serialNumber" etc)
                col_names = s.row(0)
                # Create an empty dictionary
                col_value = {}
                # For every column name from "col_names" list
                for name, col in zip(col_names, range(s.ncols)):
                    # Save column value of this row into the "value" variable
                    value = s.cell(row, col).value
                    # Transform this value to string type
                    try:
                        value = str(int(value))
                    except:
                        pass
                    # Append couple (column name : column value) into the dictionary ("col_value")
                    col_value.setdefault(name.value, value)
                # Append created dictionary ("col_value") to the list ("data") and continue by next row
                data.append(col_value)
        # Return list of dictionaries ("data")
        return data

    @staticmethod
    def pnp_DNAC_upload_configuration():
        """" Method for uploading configurations """
        # Check if there are configurations in the local folder
        if not os.listdir(PnP_DNAC.configuration_folder):
            print("  WARNING! There are no configurations in folder! First make configurations!")
        else:
            try:
                # Variables for final stats
                cycle = 0
                number = 0
                # Run the cycle and load the first configuration from the local folder
                for configuration_file in os.listdir(PnP_DNAC.configuration_folder):
                    # Create new variable using the path of local folder and name of configuration file
                    configuration_path = PnP_DNAC.configuration_folder + "" + configuration_file
                    cycle += 1
                    try:
                        # If file exists and doesn't start with dot
                        if (os.path.isfile(configuration_path)) and (not configuration_file.startswith('.')):
                            # Use the API call method with relevant parameters to upload configuration
                            number = apidnac.ApiDNAC.api_upload_pnp_configuration(configuration_path, configuration_file, number)
                            if number == False:
                                return False
                        # Otherwise print warning notification
                        else:
                            print("  WARNING! Folder with configurations does not exist!")
                    except Exception as e:
                        print("  Something's wrong: " + str(e))
                # Print the stats about uploading of configurations
                print("\n" + "   STATS! Successfully uploaded configurations: " + str(number) + " / " + str(cycle))
            except Exception as e:
                print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_get_configuration_for_delete():
        """" Method for getting all configurations for deleting """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_configuration()
        if not r_json == False:
            # Variable for indexing configurations
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:40}'.format("Name:") + "   " + '{!s:10}'.format(
                "Size:") + "   " + '{!s:10}'.format("Format:"))
            try:
                # Print all configurations
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:40}'.format(i["name"]) + "   " + '{!s:10}'.format(
                        str(i["fileSize"])) + "   " + '{!s:10}'.format(str(i["fileFormat"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific configuration (using the specific index or 0 for all configurations) for deleting
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
                    # Create configurationID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        configurationID = r_json["response"][cmd - 1]["id"]
                        # Use the API call method with relevant parameters to delete configuration
                        apidnac.ApiDNAC.api_delete_pnp_configuration(configurationID, True, False, False)
                except Exception as e:
                    print("  Something's wrong: " + str(e))
                try:
                    if cmd == 0:
                        # Run the cycle for deleting all configurations
                        for i in r_json["response"]:
                            # Create configurationID variable
                            configurationID = i.get("id")
                            # Use the API call method with relevant parameters to delete configuration
                            apidnac.ApiDNAC.api_delete_pnp_configuration(configurationID, False, False, False)
                            # And continue with deleting next configuration
                            continue
                        # Print information about successful deleting of all configurations
                        print("   <Response [200]>")
                        print("   All configurations were successfully deleted!")
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

########################################################################################################################
                                                    # DEVICE #
########################################################################################################################

    @staticmethod
    def pnp_DNAC_get_project_for_list_devices():
        """" Method for getting all projects for listing devices """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific project (using the index) where you want to see the devices
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
                    # Create projectID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        # Call the method with projectID parameter to list devices of specific project
                        PnP_DNAC.pnp_DNAC_print_project_devices_for_list(projectID)
                        break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_print_project_devices_for_list(projectID):
        """" Method for listing devices of specific project """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project_devices(projectID)
        # Variable for indexing devices
        countDev = 0
        # Print the table header
        print('   {!s:3}'.format("No:") + "   " + '{!s:20}'.format("Hostname:") + "   " + '{!s:25}'.format(
            "Platform:") + "   " + '{!s:18}'.format("Serial num:") + "   " + '{!s:25}'.format(
            "State:") + "   " + '{!s:10}'.format("PKI:") + "   " + '{!s:20}'.format("Updated:"))
        try:
            # Print all devices of specific project
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
    def pnp_DNAC_get_project_for_deleting_devices(reload=True):
        """" Method for getting all projects for deleting devices """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific project (using the index) where you want to see the devices
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
                    # Create projectID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        # If you just want to delete the device
                        if reload == False:
                            # Call the method with projectID parameter to delete device of specific project
                            PnP_DNAC.pnp_DNAC_print_project_devices_for_deleting(projectID)
                            break
                        # If you want to delete the device and reload as well
                        else:
                            # Call the method with projectID parameter to reload device of specific project
                            PnP_DNAC.pnp_DNAC_print_project_devices_for_reloading(projectID)
                            break
                except Exception as e:
                    print("  Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_print_project_devices_for_deleting(projectID):
        """" Method for deleting devices of specific project """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project_devices(projectID)
        # Variable for indexing devices
        countDev = 0
        # Create empty lists
        deviceID = []
        configurationID = []
        serialNO = []
        # Print the table header
        print('   {!s:3}'.format("No:") + "   " + '{!s:20}'.format("Hostname:") + "   " + '{!s:25}'.format(
            "Platform:") + "   " + '{!s:18}'.format("Serial num:") + "   " + '{!s:25}'.format(
            "State:") + "   " + '{!s:10}'.format("PKI:") + "   " + '{!s:20}'.format("Updated:"))
        try:
            # Print all devices of specific project
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
            # If response from API call isn't empty
            if not r_json["response"] == []:
                while True:
                    # Select a specific device (using the index) for deleting
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
                        # If parameters exist, then create necessary variables according to the selected index
                        if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                            if not r_json["response"][cmd - 1].get("id") == None:
                                # Create deviceID variable according to the selected index
                                deviceID = r_json["response"][cmd - 1]["id"]
                            if not r_json["response"][cmd - 1].get("configId") == None:
                                # Create configurationID variable according to the selected index
                                configurationID = r_json["response"][cmd - 1]["configId"]
                            if not r_json["response"][cmd - 1].get("serialNumber") == None:
                                # Create serialNO variable according to the selected index
                                serialNO = r_json["response"][cmd - 1]["serialNumber"]
                            while True:
                                # Do you want to clean and reload device as well?
                                cmd2 = input("    Do you want to clean and reload device as well (y/n/q for exit)? ")
                                # If you want to exit
                                if cmd2 == "q" or cmd2 == "Q":
                                    break
                                # If you just want to delete the device
                                if cmd2 == "n" or cmd2 == "N":
                                    if not deviceID == []:
                                        # Use the API call method with relevant parameters to delete device of selected project
                                        apidnac.ApiDNAC.api_delete_pnp_project_devices(projectID, deviceID, True)
                                    if not configurationID == []:
                                        # Use the API call method with relevant parameters to delete configuration
                                        apidnac.ApiDNAC.api_delete_pnp_configuration(configurationID, False, True, False)
                                    if not serialNO == []:
                                        # Call the method with relevant parameters to delete device from DNA-C
                                        PnP_DNAC.pnp_DNAC_get_devices_for_delete(serialNO, False)
                                    break
                                # If you want to delete the device and reload as well
                                if cmd2 == "y" or cmd2 == "Y":
                                    # Call the method for getting SSH credentials
                                    PnP_DNAC.pnp_DNAC_get_SSH_infomation()
                                    # Call the method with relevant parameters for connecting to the device
                                    result = client.Client.ssh_access(credentials.Credentials.ssh_address, credentials.Credentials.ssh_username, credentials.Credentials.ssh_password, True)
                                    # If device was successfully cleaned and reloaded
                                    if result == True:
                                        if not deviceID == []:
                                            # Use the API call method with relevant parameters to delete device of selected project
                                            apidnac.ApiDNAC.api_delete_pnp_project_devices(projectID, deviceID, False)
                                        if not configurationID == []:
                                            # Use the API call method with relevant parameters to delete configuration
                                            apidnac.ApiDNAC.api_delete_pnp_configuration(configurationID, False, True, False)
                                        if not serialNO == []:
                                            # Call the method with relevant parameters to delete device from DNA-C
                                            PnP_DNAC.pnp_DNAC_get_devices_for_delete(serialNO, False)
                                        # Print a success notification
                                        print("     Device " + r_json["response"][cmd - 1]["hostName"] + " was successfully deleted, cleaned and reloaded!")
                                        break
                                    else:
                                        # Print an error notification
                                        print("     ERROR! Connection to device " +  r_json["response"][cmd - 1]["hostName"] + " failed!")
                                        print("     ERROR! Device was not successfully deleted, cleaned and reloaded!")
                                        break
                    except Exception as e:
                        print("  Something's wrong: " + str(e))
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_print_project_devices_for_reloading(projectID):
        """" Method for reloading devices of specific project """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project_devices(projectID)
        # Variable for indexing devices
        countDev = 0
        # Print the table header
        print('   {!s:3}'.format("No:") + "   " + '{!s:20}'.format("Hostname:") + "   " + '{!s:25}'.format(
            "Platform:") + "   " + '{!s:18}'.format("Serial num:") + "   " + '{!s:25}'.format(
            "State:") + "   " + '{!s:10}'.format("PKI:") + "   " + '{!s:20}'.format("Updated:"))
        try:
            # Print all devices of specific project
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
            # If response from API call isn't empty
            if not r_json["response"] == []:
                while True:
                    try:
                        # Do you want to delete, clean and reload all devices of selected project?
                        cmd = input("   Do you want to try delete, clean and reload all these devices (y/n)? ")
                        # If you want to exit
                        if cmd == "n" or cmd == "N":
                            break
                        # If you want to delete, clean and reload all devices of selected project
                        if cmd == "y" or cmd == "Y":
                            # Call the method for mass deleting devices of selected project
                            PnP_DNAC.pnp_DNAC_mass_devices_reloading(r_json, projectID)
                            break
                    except Exception as e:
                        print("   Something's wrong: " + str(e))
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_mass_devices_reloading(r_json, projectID):
        """" Method for mass deleting devices of selected project """
        # Save response from API call to the helpList
        helpList = r_json['response']
        # Run the cycle for filling in missing parameters of the helpList
        for x in helpList:
            dId = x.get("id")
            cId = x.get("configId")
            sId = x.get("serialNumber")
            # If the some parameter is missing in the helpList, create it
            if dId == None:
                x.update({"id": ""})
            if cId == None:
                x.update({"configId": ""})
            if sId == None:
                x.update({"serialNumber": ""})
        #print("File list " + json.dumps(helpList, indent=2))
        # Create tuple in format [("hostName", "id"),...]
        deviceTuple = [(device['hostName'], device['id']) for device in helpList]
        # Create tuple in format [("hostName", "configId"),...]
        configurationTuple = [(configuration['hostName'], configuration['configId']) for configuration in helpList]
        # Create tuple in format [("hostName", "serialNumber"),...]
        serialTuple = [(serial['hostName'], serial['serialNumber']) for serial in helpList]
        try:
            # Check if the XLS table is loaded
            if not os.path.isfile(PnP_DNAC.devices_tab):
                print("    ERROR! The table of devices was not loaded correctly!")
                return
            else:
                # Load data from the XLS table
                data_set = PnP_DNAC.pnp_DNAC_read_excel(PnP_DNAC.devices_tab)
                # Variables for final stats
                cycle = 0
                number = 0
                try:
                    # Run the cycle for deleting devices according to rows in XLS table ("data_set" is the list of dictionaries)
                    for i in data_set:
                        cycle += 1
                        try:
                            # Create a serialNum variable by comparing dictionary in list (data_set) and tuple (serialTuple)
                            serialNum = [sn for hn, sn in serialTuple if hn == i["hostName"]][0]
                            # If no match is found
                            if not serialNum == i["serialNumber"]:
                                # Print an error notification
                                print("    ERROR! SN of device " + i["hostName"] + " in table does not match with SN of device in project!")
                                continue
                            else:
                                # Create a deviceID variable by comparing dictionary in list (data_set) and tuple (deviceTuple)
                                deviceID = [dev for hn, dev in deviceTuple if hn == i["hostName"]][0]
                                # Create a configurationID variable by comparing dictionary in list (data_set) and tuple (configurationTuple)
                                configurationID = [cn for hn, cn in configurationTuple if hn == i["hostName"]][0]
                        except Exception as e:
                            print("    ERROR! Device " + i["hostName"] + " in table does not match with device in project!")
                            continue
                        try:
                            # Check if "ipAddress" parameter is defined in the XLS table (resp. in the data_set list)
                            if i["ipAddress"] == "":
                                print('    ERROR! Item "ipAddress" for device ' + i["hostName"] + ' is not defined in the xls table!')
                                continue
                            # Check if "userName" parameter is defined in the XLS table (resp. in the data_set list)
                            if i["userName"] == "":
                                print('    ERROR! Item "userName" for device ' + i["hostName"] + ' is not defined in the xls table!')
                                continue
                            # Check if "passWord" parameter is defined in the XLS table (resp. in the data_set list)
                            if i["passWord"] == "":
                                print('    ERROR! Item "passWord" for device ' + i["hostName"] + ' is not defined in the xls table!')
                                continue
                            #print("    " + i["ipAddress"], i["userName"], i["passWord"])
                        except Exception:
                            # Print an information notification
                            print("    INFO! Process was stopped! Please upload the correct table of these devices with items (ipAddress, userName, passWord)!")
                            break
                        # Call the method with relevant parameters for connecting to the device
                        result = client.Client.ssh_access(i["ipAddress"], i["userName"], i["passWord"], False)
                        # If device was successfully cleaned and reloaded
                        if result == True:
                            if not deviceID == "":
                                # Use the API call method with relevant parameters to delete device of selected project
                                apidnac.ApiDNAC.api_delete_pnp_project_devices(projectID, deviceID, False)
                            if not configurationID == "":
                                # Use the API call method with relevant parameters to delete configuration
                                apidnac.ApiDNAC.api_delete_pnp_configuration(configurationID, False, False, True)
                            if not serialNum == "":
                                # Call the method with relevant parameters to delete device from DNA-C
                                PnP_DNAC.pnp_DNAC_get_devices_for_delete(serialNum, False)
                            number += 1
                            # Print a success notification
                            print("    Device " + i["hostName"] + " was successfully deleted, cleaned and reloaded!")
                            continue
                        else:
                            # Print an error notification
                            print("    ERROR! Connection to device " + i["hostName"] + " failed!")
                            continue
                    # Print the stats about mass deleting devices of selected project
                    print("\n" + "     STATS! Successfully deleted, cleaned and reloaded devices: " + str(number) + " / " + str(cycle))
                except Exception as e:
                    print("    Something's wrong: " + str(e))
        except Exception as e:
            print("    Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_get_SSH_infomation():
        """ Method for getting SSH credentials """
        while True:
            try:
                # Call to method from sshcredentials.py to enter SSH credentials
                result = sshcredentials.SSHCredentials.prompt_credentials()
                # Save results to variables in credentials.py
                credentials.Credentials.ssh_address = result[0]
                credentials.Credentials.ssh_username = result[1]
                credentials.Credentials.ssh_password = result[2]
                return True
            except RuntimeError:
                continue

    @staticmethod
    def pnp_DNAC_get_devices_for_delete(serialNO, printResp=True):
        """" Method for deleting devices from DNA-C """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_devices(False)
        # If response from API call isn't empty
        if not r_json["response"] == []:
            try:
                # Run the cycle for deleting
                for i in r_json["response"]:
                    # If SN of device in DNA-C matches SN of device you want to delete
                    if i.get("serialNumber") == serialNO:
                        deviceID = i["id"]
                        # Use the API call method with deviceID parameter to delete device from DNA-C
                        apidnac.ApiDNAC.api_delete_pnp_devices(deviceID, False)
            except Exception as e:
                print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_get_project_for_post_devices():
        """" Method for getting all projects for posting devices to DNA-C """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific project (using the index) where you want to create the devices
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
                    # Create projectID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        # Check if the XLS table is loaded
                        if not os.path.isfile(PnP_DNAC.devices_tab):
                            print("   ERROR! The table of devices was not loaded correctly!")
                            return
                        else:
                            # Load data from the XLS table
                            data_set = PnP_DNAC.pnp_DNAC_read_excel(PnP_DNAC.devices_tab)
                            # Use the API call method with relevant parameters to create the devices in selected project
                            apidnac.ApiDNAC.api_post_pnp_project_devices(projectID, data_set)
                            break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_get_project_for_post_devices_toISE():
        """" Method for getting all projects for posting devices to DNA-C and ISE """
        # Save result of this API call into r_json variable
        r_json = apidnac.ApiDNAC.api_get_pnp_project()
        if not r_json == False:
            # Variable for indexing projects
            countDev = 0
            # Print the table header
            print('  {!s:3}'.format("No:") + "   " + '{!s:20}'.format("State:") + "   " + '{!s:26}'.format(
                "Name:") + "   " + '{!s:8}'.format("Devices:") + "   " + '{!s:15}'.format(
                "Created:") + "   " + '{!s:30}'.format("Updated:"))
            try:
                # Print all projects
                for i in r_json["response"]:
                    countDev += 1
                    print('  {!s:3}'.format(str(countDev)) + "   " + '{!s:20}'.format(i["state"]) + "   " + '{!s:26}'.format(
                        i["siteName"]) + "   " + '{!s:8}'.format(str(i["deviceCount"])) + "   " + '{!s:15}'.format(
                        i["provisionedBy"]) + "   " + '{!s:30}'.format(str(i["provisionedOn"])))
            except TypeError:
                print("  WARNING! Is not possible to print information!")
            while True:
                # Select a specific project (using the index) where you want to create the devices
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
                    # Create projectID variable according to the selected index
                    if (cmd - 1 >= 0) and (cmd - 1 < len(r_json["response"])):
                        projectID = r_json["response"][cmd - 1]["id"]
                        # Call the method for getting ISE credentials
                        if PnP_DNAC.pnp_DNAC_get_ISE_infomation() == False:
                            break
                        # Check if the XLS table is loaded
                        if not os.path.isfile(PnP_DNAC.devices_tab):
                            print("   ERROR! The table of devices was not loaded correctly!")
                            return
                        else:
                            # Load data from the XLS table
                            data_set = PnP_DNAC.pnp_DNAC_read_excel(PnP_DNAC.devices_tab)
                            # Create ise_url variable to create devices in ISE
                            ise_url = "https://" + credentials.Credentials.ise_address + ":9060/ers/config/networkdevice"
                            # Create ise_credentials variable by encoding to utf-8
                            ise_credentials = (credentials.Credentials.ise_username + ":" + credentials.Credentials.ise_password).encode("utf-8")
                            # Transform ise_credentials to hash by base64 encoding
                            ise_credentials_b64 = (base64.b64encode(ise_credentials)).decode("utf-8")
                            # Use the API call method with relevant parameters to create the devices in DNA-C and ISE
                            apidnac.ApiDNAC.api_post_pnp_project_devices_toISE(projectID, data_set, ise_credentials_b64, ise_url)
                            break
                except Exception as e:
                    print("   Something's wrong: " + str(e))

    @staticmethod
    def pnp_DNAC_get_ISE_infomation():
        """ Method for getting ISE credentials """
        while True:
            try:
                # Print a warning notification
                command = input("   WARNING! You have chosen to create the devices to the ISE as well. Do you want to continue (y/n)? ")
                if command == "Y" or command == "y":
                    # Check if ISE credentials have already been set
                    if not credentials.Credentials.ise_address == "" and not credentials.Credentials.ise_username == "" and not credentials.Credentials.ise_password == "":
                        command = input("   IP and credentials for ISE have already been set. Do you want to enter a new information (y/n)? ")
                        if command == "Y" or command == "y":
                            pass
                        elif command == "N" or command == "n":
                            return True
                    # Call to method from isercredentials.py to enter ISE credentials
                    result = isecredentials.ISECredentials.prompt_credentials()
                    if result is None:
                        continue
                    # Save results to variables in credentials.py
                    credentials.Credentials.ise_address = result[0]
                    credentials.Credentials.ise_username = result[1]
                    credentials.Credentials.ise_password = result[2]
                    return True
                elif command == "N" or command == "n":
                    return False
            except RuntimeError:
                continue
