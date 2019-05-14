from easypnp_networksys_cz import program
from easypnp_networksys_cz.pnp_apicem import ticket
import json
import requests


class ApiAPICEM:
    # Local variables
    __ticket = ticket.Ticket()
    __urlController = ''
    __urlControllerAPI = ''

    @staticmethod
    def set_url(new_url):
        """ Method to set local variables related to URL address of the controller """
        ApiAPICEM.__urlController = new_url
        ApiAPICEM.__urlControllerAPI = "https://" + new_url + "/"

    @staticmethod
    def get_url():
        """ Method to return URL address of the controller """
        return ApiAPICEM.__urlController

########################################################################################################################
                                                    # PnP API calls - SYSTEM #
########################################################################################################################

    @staticmethod
    def api_connection(first_url):
        """ Method tries connection to APIC-EM """
        try:
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json"}
                # Create a payload for POST method
                payload = {"username": program.Program.get_credentials(c_user=True, c_pass=False), "password": program.Program.get_credentials(c_user=False, c_pass=True)}
                # API call
                response = requests.post('https://' + first_url + '/api/v1/ticket', data=json.dumps(payload), headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns a response
                if r_json.get('response'):
                    return True
        except Exception:
            print("   ERROR! Connection to APIC-EM is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_get_user():
        """ Method gets a user basic info """
        try:
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/user', headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    return False
                # Otherwise print a notification
                else:
                    print("  " + str(response))
                    print("  Ticket is still valid!")
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to APIC-EM is not working! Enter correct IP address!")

    @staticmethod
    def api_get_ticket():
        """ Method asks for possible credentials and gets a new valid ticket """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json"}
                # Create a payload for POST method
                payload = {"username": program.Program.get_credentials(c_user=True,c_pass=False), "password": program.Program.get_credentials(c_user=False,c_pass=True)}
                # API call
                response = requests.post(ApiAPICEM.__urlControllerAPI + 'api/v1/ticket', data=json.dumps(payload), headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if r_json.get('response') and r_json['response'].get('errorCode'):
                    # If the response code is 403
                    if response.status_code == 403:
                        print("  Response status code 403 = access is denied by controller!")
                        pass
                    # Call the method for setting valid credentials
                    state = program.Program.update_credentials()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    elif state == False:
                        raise RuntimeError()
                    continue
                # Otherwise print a success notification
                else:
                    print("  Ticket was successfully created!")
                # Return a new valid ticket
                return r_json['response']['serviceTicket']
        except Exception:
            print("  ERROR! Ticket was not created!")








    @staticmethod
    def api_get_network_devices():
        """ Method gets all network devices """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                    # Create a header with instruction
                    header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                    # API call
                    response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/network-device', headers=header, verify=False)
                    # Transform a response to JSON format
                    r_json = response.json()
                    # If the request call returns an error code
                    if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                        # Call the method for creating new ticket
                        ApiAPICEM.__ticket.get_new_ticket()
                        # Subtract the counter
                        counter -= 1
                        if counter < 0:
                            raise RuntimeError()
                        continue
                    # Return the response in JSON format
                    return r_json
        except Exception as e:
            print("  ERROR! Connection to APIC-EM is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_get_device_interface(deviceID):
        """ Method gets all interfaces of selected device """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/interface/network-device/' + deviceID, headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

########################################################################################################################
                                                 # PnP API calls - PROJECT #
########################################################################################################################

    @staticmethod
    def api_get_pnp_project():
        """ Method gets all PnP projects """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project', headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to APIC-EM is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_create_pnp_project(project_name):
        """ Method creates a PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # Create a payload for POST method
                payload = "[{\"siteName\": \"" + project_name + "\"}]"
                # API call
                response = requests.post(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project', data=payload, headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # If the response code is 202
                if response.status_code == 202:
                    print("   New project " + project_name + " was successfully created!")
                    pass
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   ERROR! Connection to APIC-EM is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_delete_pnp_project(projectID, printResp=True):
        """ Method deletes a PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.delete(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project/' + projectID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else print("    " + str(response))
                # If the response code is 202 and printResp is True
                if response.status_code == 202 and printResp:
                    print("   Project was successfully deleted!")
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))

########################################################################################################################
                                               # PnP API calls - CONFIGURATION #
########################################################################################################################

    @staticmethod
    def api_get_pnp_configuration():
        """ Method gets all PnP configurations """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/file/namespace/config', headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to APIC-EM is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_upload_pnp_configuration(configuration_path, configuration_file, number):
        """ Method uploads all PnP configurations from the local folder into the APIC-EM """
        try:
            # Define maximum attempts for the request
            counter = 3
            try:
                # File parameters from the local folder are saved into the object
                configuration_filename = open(configuration_path, "r")
                # Create a payload for POST method
                payload = {'fileUpload': configuration_filename}
            except:
                print("  File does not exist!")
                pass
            # Create a header with instruction
            header = {"X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
            try:
                # API call
                response = requests.post(ApiAPICEM.__urlControllerAPI + 'api/v1/file/config', files=payload, headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # If the response code is 200
                if response.status_code == 200:
                    print("  Configuration " + configuration_file + " was successfully uploaded!")
                    number += 1
            except requests.exceptions.RequestException as e:
                print("  ERROR! Connection to APIC-EM is not working! Enter correct IP address!")
                return False
            # Transform a response to JSON format
            r_json = response.json()
            # Save an error code into a variable
            a = r_json['response'].get('errorCode')
            try:
                # If file has already been uploaded
                if a == "FILE_ALREADY_EXISTS":
                    print("  Configuration " + configuration_file + " has already been uploaded in the past!")
                # If the request call returns "RBAC"
                elif (isinstance(r_json['response'], dict)) and (a == "RBAC"):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    pass
                # Return the number variable which counts successfully uploaded configurations
                return number
            except Exception as e:
                print("  Something's wrong: " + str(e))
        except Exception as e:
            print("  Something's wrong: " + str(e))

    @staticmethod
    def api_delete_pnp_configuration(configurationID, printResp=True, printResp2=True, printResp3=True):
        """ Method deletes a PnP configuration """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.delete(ApiAPICEM.__urlControllerAPI + 'api/v1/file/' + configurationID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else None
                # If the response code is 200 and printResp is True
                if response.status_code == 200 and printResp:
                    print("   Configuration was successfully deleted!")
                    pass
                # If the response code is 200 and printResp2 is True
                if response.status_code == 200 and printResp2:
                    print("     Configuration was successfully deleted!")
                    pass
                # Transform a response to JSON format
                r_json = response.json()
                # If the response code is 404 and printResp is True
                if response.status_code == 404 and printResp:
                    print("   Configuration has already been deleted!")
                    pass
                # If the response code is 404 and printResp2 is True
                elif response.status_code == 404 and printResp2:
                    print("     Configuration has already been deleted!")
                    pass
                # If the response code is 404 and printResp3 is True
                elif response.status_code == 404 and printResp3:
                    pass
                # If the request call returns an error code
                elif isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))

########################################################################################################################
                                                 # PnP API calls - DEVICE #
########################################################################################################################

    @staticmethod
    def api_get_pnp_project_devices(projectID, printResp=True):
        """ Method gets all devices of the selected PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else None
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_get_pnp_devices(printResp=True):
        """ Method gets all PnP devices in the APIC-EM """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-device', headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else None
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_delete_pnp_devices(deviceID, printResp=True):
        """ Method deletes a PnP device from the APIC-EM """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.delete(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-device/' + deviceID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("    " + str(response)) if printResp else None
                # If the response code is 202 and printResp is True
                if response.status_code == 202 and printResp:
                    print("    Device was successfully deleted!")
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("    Something's wrong: " + str(e))

    @staticmethod
    def api_delete_pnp_project_devices(projectID, deviceID, printResp=True):
        """ Method deletes a device from the selected PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.delete(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device/' + deviceID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("     " + str(response)) if printResp else None
                # Transform a response to JSON format
                r_json = response.json()
                # Use the API call method with taskID parameter to get information about a completed API call
                result = ApiAPICEM.api_get_task_info(r_json["response"]["taskId"])
                # If the request call doesn't return an error
                if result["response"].get("isError") == False and printResp:
                    print("     Device was successfully deleted!")
                    pass
                # If the request call returns an error
                if result["response"].get("isError") == True and printResp:
                    print("     Device has already been deleted!")
                    pass
                # If the request call returns an error code
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("    Something's wrong: " + str(e))

    @staticmethod
    def api_get_pnp_files_for_post_project_devices(namespace):
        """ Method gets all configurations or all images uploaded in the APIC-EM """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/file/namespace/' + namespace, headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # Gets all configurations
                if namespace == "config":
                    # Save the response into the list
                    configurationList = r_json['response']
                    #print("File list " + json.dumps(configurationList, indent=2))
                    # Create tuple in format [("configName", "configId"),...]
                    configurationTuple = [(configuration['name'], configuration['id']) for configuration in configurationList]
                    #print("File tuple " + json.dumps(configurationTuple, indent=2))
                    # Return created tuple
                    return configurationTuple
                # Get all images
                elif namespace == "image":
                    # Save the response into the list
                    imageList = r_json['response']
                    #print("File list " + json.dumps(imageList, indent=2))
                    # Create tuple in format [("imageName", "imageId"),...]
                    imageTuple = [(image['name'], image['id']) for image in imageList]
                    #print("File tuple " + json.dumps(imageTuple, indent=2))
                    # Return created tuple
                    return imageTuple
                # If the request call returns an error code
                elif isinstance(r_json['response'], dict) and r_json['response'].get('errorCode'):
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                else:
                    print("  ERROR! Used namespace is wrong!")
                    break
        except Exception as e:
            print("  Something's wrong: " + str(e))

    @staticmethod
    def api_post_pnp_project_devices(projectID, data_set):
        """ Method posts devices into the selected PnP project """
        try:
            # Variables for final stats
            cycle = 0
            number = 0
            num_conf = 0
            num_im = 0
            # Use the API call method with "config" parameter to get all configurations in the APIC-EM
            configurationTuple = ApiAPICEM.api_get_pnp_files_for_post_project_devices("config")
            # Use the API call method with "image" parameter to get all images in the APIC-EM
            imageTuple = ApiAPICEM.api_get_pnp_files_for_post_project_devices("image")
            # Run the cycle for posting devices according to rows in XLS table ("data_set" is the list of dictionaries)
            for i in data_set:
                cycle += 1
                # Find the configId based on a configuration name by comparing the "i" dictionary and the tuple
                try:
                    configurationName = i["hostName"] + "_configuration"
                    configId = [id for cn, id in configurationTuple if cn == configurationName][0]
                except Exception as e:
                    # If no match was found
                    configId = None
                # Find the imageId based on a image name by comparing the "i" dictionary and the tuple
                try:
                    imageName = i["image"]
                    imageId = [id for imn, id in imageTuple if imn == imageName][0]
                except Exception as e:
                    # If no match was found
                    imageId = None
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # Create a payload for POST method
                payload = [{
                    "hostName": i["hostName"],
                    "serialNumber": i["serialNumber"],
                    "platformId": i["platformId"],
                    }]
                #print("Payload " + str(counter) + json.dumps(payload, indent=2))

                # Adds a devCert parameter to the created payload
                if i["devCert"] == "yes":
                    payload[0]["pkiEnabled"] = True
                else:
                    payload[0]["pkiEnabled"] = False
                # If a match was found adds the appropriate configId to the created payload
                if configId is not None:
                    payload[0]["configId"] = configId
                    print("\n" + "   Configuration " + configurationName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_conf += 1
                # Otherwise print a question
                else:
                    cmd = input("\n" + "   Do you want to upload device " + i["hostName"] + " without configuration? (y/n/q for quit upload) ")
                    if cmd == "q" or cmd == "Q":
                        print("\n" + "    INFO! Upload was stopped! Please make configuration for device " + i["hostName"] +"!")
                        break
                    if cmd == "n" or cmd == "N":
                        print("\n" + "    <Response [202]>")
                        print("    ERROR! Device " + i["hostName"] + " was not created in selected PnP project!")
                        continue
                    if cmd == "y" or cmd == "Y":
                        print("\n" + "   WARNING! There is no configuration " + configurationName + " for the device " + i["hostName"] + " in the APIC-EM!")
                        pass
                # If a match was found adds the appropriate imageId to the created payload
                if imageId is not None:
                    payload[0]["imageId"] = imageId
                    print("   Image " + imageName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_im += 1
                # Otherwise print warning notification
                else:
                    print("   WARNING! There is no image " + imageName + " for the device " + i["hostName"] + " in the xlsx or in the APIC-EM!")
                    pass
                try:
                    # API call
                    response = requests.post(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', data=json.dumps(payload), headers=header, verify=False)
                    # Print the response code
                    print("    " + str(response))
                    # Transform a response to JSON format
                    r_json = response.json()
                    # Use the API call method with taskID parameter to get information about a completed API call
                    result = ApiAPICEM.api_get_task_info(r_json["response"]["taskId"])
                    try:
                        # If the request call doesn't return an error
                        if result["response"].get("isError") == False:
                            print("    Device " + i["hostName"] + " was successfully created in selected PnP project!")
                            number += 1
                        # If the request call returns an error
                        if result["response"].get("isError") == True:
                            # And the failure reason starts with the letter P
                            if result["response"]["failureReason"][0] == "P":
                                print("    ERROR! Device " + i["hostName"] + " has been already created in selected PnP project!")
                            else:
                                print("    ERROR! Device " + i["hostName"] + " is assigned to other PnP project!")
                    except Exception as e:
                        print("    Something's wrong: " + str(e))
                except Exception as e:
                    print("    Something's wrong: " + str(e))
            # Print the stats about posting devices into the selected PnP project
            print("\n" + "     STATS!"
                  "\n" + "     Devices with configuration:               " + str(num_conf) + " / " + str(cycle) + ""
                  "\n" + "     Devices with image:                       " + str(num_im) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to APIC-EM: " + str(number) + " / " + str(cycle))
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_get_task_info(taskID):
        """ Method gets information about a completed API call"""
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # API call
                response = requests.get(ApiAPICEM.__urlControllerAPI + 'api/v1/task/' + taskID, headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns an error code "RBAC"
                if isinstance(r_json['response'], dict) and r_json['response'].get('errorCode')=="RBAC":
                    # Call the method for creating new ticket
                    ApiAPICEM.__ticket.get_new_ticket()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_post_pnp_project_devices_toISE(projectID, data_set, ise_credentials_b64, ise_url):
        """ Method posts devices into the selected PnP project and creates devices in Cisco ISE"""
        try:
            # Variables for final stats
            cycle = 0
            number = 0
            num_conf = 0
            num_im = 0
            num_ise = 0
            # Use the API call method with "config" parameter to get all configurations in the APIC-EM
            configurationTuple = ApiAPICEM.api_get_pnp_files_for_post_project_devices("config")
            # Use the API call method with "image" parameter to get all images in the APIC-EM
            imageTuple = ApiAPICEM.api_get_pnp_files_for_post_project_devices("image")
            # Run the cycle for posting devices according to rows in XLS table ("data_set" is the list of dictionaries)
            for i in data_set:
                # Part for the APIC-EM
                cycle += 1
                # Find the configId based on a configuration name by comparing the "i" dictionary and the tuple
                try:
                    configurationName = i["hostName"] + "_configuration"
                    configId = [id for cn, id in configurationTuple if cn == configurationName][0]
                except Exception as e:
                    # If no match was found
                    configId = None
                # Find the imageId based on a image name by comparing the "i" dictionary and the tuple
                try:
                    imageName = i["image"]
                    imageId = [id for imn, id in imageTuple if imn == imageName][0]
                except Exception as e:
                    # If no match was found
                    imageId = None
                # Create a header with instruction for the APIC-EM
                header = {"content-type": "application/json", "X-Auth-Token": ApiAPICEM.__ticket.get_ticket()}
                # Create a payload for POST method into the APIC-EM
                payload = [{
                    "hostName": i["hostName"],
                    "serialNumber": i["serialNumber"],
                    "platformId": i["platformId"],
                    }]
                #print("Payload " + str(counter) + json.dumps(payload, indent=2))

                # Adds a devCert parameter to the created payload
                if i["devCert"] == "yes":
                    payload[0]["pkiEnabled"] = True
                else:
                    payload[0]["pkiEnabled"] = False
                # If a match was found adds the appropriate configId to the created payload
                if configId is not None:
                    payload[0]["configId"] = configId
                    print("\n" + "   Configuration " + configurationName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_conf += 1
                # Otherwise print a question
                else:
                    cmd = input("\n" + "   Do you want to upload device " + i["hostName"] + " without configuration? (y/n/q for quit upload) ")
                    if cmd == "q" or cmd == "Q":
                        print("\n" + "    INFO! Upload was stopped! Please make configuration for device " + i["hostName"] + "!")
                        break
                    if cmd == "n" or cmd == "N":
                        print("\n" + "    <Response [202]>")
                        print("    ERROR! Device " + i["hostName"] + " was not created in selected PnP project!")
                        print("    ERROR! Device " + i["hostName"] + " was not created in ISE!")
                        continue
                    if cmd == "y" or cmd == "Y":
                        print("\n" + "   WARNING! There is no configuration " + configurationName + " for the device " + i["hostName"] + " in the APIC-EM!")
                        pass
                # If a match was found adds the appropriate imageId to the created payload
                if imageId is not None:
                    payload[0]["imageId"] = imageId
                    print("   Image " + imageName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_im += 1
                # Otherwise print warning notification
                else:
                    print("   WARNING! There is no image " + imageName + " for the device " + i["hostName"] + " in the xlsx or in the APIC-EM!")
                    pass
                try:
                    # API call into the APIC-EM
                    response = requests.post(ApiAPICEM.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', data=json.dumps(payload), headers=header, verify=False)
                    # Print the response code
                    print("    " + str(response))
                    # Transform a response to JSON format
                    r_json = response.json()
                    # Use the API call method with taskID parameter to get information about a completed API call
                    result = ApiAPICEM.api_get_task_info(r_json["response"]["taskId"])
                    try:
                        # If the request call doesn't return an error
                        if result["response"].get("isError") == False:
                            print("    Device " + i["hostName"] + " was successfully created in selected PnP project!")
                            number += 1
                        # If the request call returns an error
                        if result["response"].get("isError") == True:
                            # And the failure reason starts with the letter P
                            if result["response"]["failureReason"][0] == "P":
                                print("    ERROR! Device " + i["hostName"] + " has been already created in selected PnP project!")
                            else:
                                print("    ERROR! Device " + i["hostName"] + " is assigned to other PnP project!")
                    except Exception as e:
                        print("    Something's wrong: " + str(e))
                except Exception as e:
                    print("    Something's wrong with upload to APIC-EM: " + str(e))
                # Part for the Cisco ISE
                try:
                    # Create a header with instruction for the Cisco ISE
                    header_ise = {"content-type": "application/json", "authorization": "Basic " + ise_credentials_b64, "accept": "application/json", "cache-control": "no-cache"}
                    # Create a payload for POST method into the Cisco ISE
                    payload_ise = {
                        "NetworkDevice" : {
                        #"id" : "223456789",
                        "name" : i["hostName"],
                        "description" : i["site"],
                        "authenticationSettings" : {
                        #        "radiusSharedSecret" : "aaa",
                        #        "enableKeyWrap" : True,
                        #        #"dtlsRequired" : True,
                        #        "keyEncryptionKey" : "1234567890123456",
                        #        "messageAuthenticatorCodeKey" : "12345678901234567890",
                        #        "keyInputFormat" : "ASCII"
                        },
                        #"snmpsettings" : {                                      #WHEN THIS
                        #          "version" : "ONE",                            #REGUIRED
                        #          "roCommunity" : "aaa",                        #REQUIRED
                        #         "username" : "user"                           #REQUIRED FOR VERSION THREE
                        #         "securityLevel" : "Auth"                      #REQUIRED FOR VERSION THREE
                        #         "pollingInterval" : 3600,
                        #         "linkTrapQuery" : True,
                        #         "macTrapQuery" : True,
                        #         "originatingPolicyServicesNode" : "Auto"
                        #},
                        #"trustsecsettings" : {                                 #WHEN THIS
                        #        "deviceAuthenticationSettings" : {             #REQUIRED
                        #                "sgaDeviceId" : i["hostName"],         #REQUIRED
                        #                "sgaDevicePassword" : "aaa"            #REQUIRED
                        #                },
                        #        "deviceConfigurationDeployment" : {
                        #                "includeWhenDeployingSGTUpdates" : True,
                        #                "enableModePassword" : "aaa",
                        #                "execModePassword" : "aaa",
                        #                "execModeUsername" : "aaa"
                        #                }
                        #},
                        #"tacacsSettings" : {                                   #WHEN THIS
                        #        "sharedSecret" : "aaa",
                        #        "connectModeOptions" : "ON_LEGACY"             #REQUIRED
                        #},
                        "profileName" : "Cisco",
                        #"coaPort" : 1700,
                        #"dtlsDnsName" : "ISE213.il.com",
                        "NetworkDeviceIPList" : [ {
                                "ipaddress" : i["ipAddress"],
                                "mask" : 32
                        } ],
                        "NetworkDeviceGroupList" : [ "Location#All Locations", "Device Type#All Device Types" ]
                        #"NetworkDeviceGroupList" : [ "Location#Dejvice", "Device Type#switch#Catalyst 3560-CX" ]
                        #"NetworkDeviceGroupList": ["Location#"+i["location"], "Device Type#"+i["type"]]
                        }
                    }
                    # If all conditions are met, then adds a RADIUS parameter to the created payload
                    try:
                        if i["radius"] == "yes":
                            if i["radiusSecret"] == "":
                                print('     ERROR! Item "radiusSecret" is not defined in the xls table!')
                                raise RuntimeError
                            else:
                                payload_ise["NetworkDevice"]["authenticationSettings"] = {"radiusSharedSecret" : i["radiusSecret"]}
                    except RuntimeError:
                        print("     INFO! Upload was stopped! Please edit the xls table correctly!")
                        break
                    # If all conditions are met, then adds a TACACS parameter to the created payload
                    try:
                        if i["tacacs"] == "yes":
                            if i["tacacsSecret"] == "":
                                print('     ERROR! Item "tacacsSecret" is not defined in the xls table!')
                                raise RuntimeError
                            else:
                                payload_ise["NetworkDevice"].setdefault("tacacsSettings")
                                payload_ise["NetworkDevice"]["tacacsSettings"] = {"sharedSecret" : i["tacacsSecret"], "connectModeOptions" : "ON_LEGACY"}
                    except RuntimeError:
                        print("     INFO! Upload was stopped! Please edit the xls table correctly!")
                        break
                    # API call into the Cisco ISE
                    response_ise = requests.request("POST", ise_url, data=json.dumps(payload_ise), headers=header_ise, verify=False)
                    # Print the response code
                    print("    " + str(response_ise))
                    # If the response code is 201
                    if response_ise.status_code == 201:
                        print("    Device " + i["hostName"] + " was successfully created in ISE!")
                        num_ise += 1
                    # If the response code is 400
                    elif response_ise.status_code == 400:
                        print("    ERROR! Device " + i["hostName"] + " already exists in ISE!")
                    # If the response code is 401
                    elif response_ise.status_code == 401:
                        print("    ERROR! Device " + i["hostName"] + " was not created in ISE! User does not have permission! Enter correct credentials!")
                        break
                    else:
                        print("    ERROR! Device " + i["hostName"] + " was not created in ISE! Something is wrong, try again!")
                        break
                except Exception:
                    print("    ERROR! Device " + i["hostName"] + " was not created in ISE! Connection is not working! Enter correct IP address!")
                    break
            # Print the stats about posting devices into the selected PnP project
            print("\n" + "     STATS!"
                  "\n" + "     Devices with configuration:               " + str(num_conf) + " / " + str(cycle) + ""
                  "\n" + "     Devices with image:                       " + str(num_im) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to APIC-EM: " + str(number) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to ISE:     " + str(num_ise) + " / " + str(cycle))
        except Exception as e:
            print("   Something's wrong: " + str(e))
