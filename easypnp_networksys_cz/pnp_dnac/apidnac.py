from easypnp_networksys_cz import program
from easypnp_networksys_cz.pnp_dnac import token
import json
import requests
import base64

class ApiDNAC:
    # Local variables
    __token = token.Token()
    __urlController = ''
    __urlControllerAPI = ''

    @staticmethod
    def set_url(new_url):
        """ Method to set local variables related to URL address of the controller """
        ApiDNAC.__urlController = new_url
        ApiDNAC.__urlControllerAPI = "https://" + new_url + "/"

    @staticmethod
    def get_url():
        """ Method to return URL address of the controller """
        return ApiDNAC.__urlController

########################################################################################################################
                                                    # PnP API calls - SYSTEM #
########################################################################################################################

    @staticmethod
    def api_connection(first_url):
        """ Method tries connection to DNA-C """
        try:
            while True:
                # Create a payload for POST method
                payload_string = (program.Program.get_credentials(c_user=True, c_pass=False) + ":" + program.Program.get_credentials(c_user=False, c_pass=True)).encode('utf-8')
                # Transform payload by base64 encoding
                payload_b64 = (base64.b64encode(payload_string)).decode('utf-8')
                # Create a header with instruction
                header = {"content-type": "application/json", "authorization": "Basic " + payload_b64}
                # API call
                response = requests.request("POST", 'https://' + first_url + '/api/system/v1/auth/token', headers=header, verify=False)
                # If the request call returns a response code different from 200
                if response.status_code != 200:
                    return True
        except Exception:
            print("   ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_get_host():
        """ Method gets a user basic info """
        try:
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/host', headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
                    return False
                # Otherwise print a notification
                else:
                    print("  " + str(response))
                    print("  Token is still valid!")
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")

    @staticmethod
    def api_get_token():
        """ Method asks for possible credentials and gets a new valid token """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a payload for POST method
                payload_string = (program.Program.get_credentials(c_user=True, c_pass=False) + ":" + program.Program.get_credentials(c_user=False, c_pass=True)).encode('utf-8')
                # Transform payload by base64 encoding
                payload_b64 = (base64.b64encode(payload_string)).decode('utf-8')
                # Create a header with instruction
                header = {"content-type": "application/json", "authorization": "Basic " + payload_b64}
                # API call
                response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/system/v1/auth/token', headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # If the request call returns a response code different from 200
                if response.status_code != 200:
                    # And if the response code is 403
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
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call doesn't return a response
                if not r_json.get("Token"):
                    # Call the method for setting valid credentials
                    program.Program.update_credentials()
                    continue
                # Otherwise print a success notification
                else:
                    print("  Token was successfully created!")
                # Return a new valid token
                return r_json["Token"]
        except Exception:
            print("  ERROR! Token was not created!")

    @staticmethod
    def api_get_network_devices():
        """ Method gets all network devices """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/network-device', headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_get_device_interface(deviceID):
        """ Method gets all interfaces of selected device """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/interface/network-device/' + deviceID, headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
                                                # PnP API calls - PROJECT#
########################################################################################################################

    @staticmethod
    def api_get_pnp_project():
        """ Method gets all PnP projects """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project', headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_create_pnp_project(project_name):
        """ Method creates a PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # Create a payload for POST method
                payload = "[{\"siteName\": \"" + project_name + "\"}]"
                # API call
                response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project', data=payload, headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # If the response code is 202
                if response.status_code == 202:
                    print("   New project " + project_name + " was successfully created!")
                    pass
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("   ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_delete_pnp_project(projectID, printResp=True):
        """ Method deletes a PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else print("    " + str(response))
                # If the response code is 202 and printResp is True
                if response.status_code == 202 and printResp:
                    print("   Project was successfully deleted!")
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
                                            # PnP API calls - CONFIGURATION#
########################################################################################################################

    @staticmethod
    def api_get_pnp_configuration():
        """ Method gets all PnP configurations """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/file/namespace/config', headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
                    # Subtract the counter
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                # Return the response in JSON format
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_upload_pnp_configuration(configuration_path, configuration_file, number):
        """ Method uploads all PnP configurations from the local folder into the DNA-C """
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
            header = {"X-Auth-Token": ApiDNAC.__token.get_token()}
            try:
                # API call
                response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/file/config', files=payload, headers=header, verify=False)
                # Print the response code
                print("  " + str(response))
                # If the response code is 200
                if response.status_code == 200:
                    print("  Configuration " + configuration_file + " was successfully uploaded!")
                    number += 1
            except requests.exceptions.RequestException as e:
                print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
                return False
            # Transform a response to JSON format
            r_json = response.json()
            # Save an error code into a variable
            a = r_json['response'].get('errorCode')
            try:
                # If file has already been uploaded
                if a == "FILE_ALREADY_EXISTS":
                    print("  Configuration " + configuration_file + " has already been uploaded in the past!")
                # If the request call returns one of these conditions
                elif r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/file/' + configurationID, headers=header, verify=False)
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
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp"):
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
                                             # PnP API calls - DEVICE#
########################################################################################################################

    @staticmethod
    def api_get_pnp_project_devices(projectID, printResp=True):
        """ Method gets all devices of the selected PnP project """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else None
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
        """ Method gets all PnP devices in the DNA-C """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-device', headers=header, verify=False)
                # Print the response code if printResp is True
                print("   " + str(response)) if printResp else None
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
        """ Method deletes a PnP device from the DNA-C """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-device/' + deviceID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("    " + str(response)) if printResp else None
                # If the response code is 202 and printResp is True
                if response.status_code == 202 and printResp:
                    print("    Device was successfully deleted!")
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device/' + deviceID, headers=header, verify=False)
                # Print the response code if printResp is True
                print("     " + str(response)) if printResp else None
                # Transform a response to JSON format
                r_json = response.json()
                # Use the API call method with taskID parameter to get information about a completed API call
                result = ApiDNAC.api_get_task_info(r_json["response"]["taskId"])
                # If the request call doesn't return an error
                if result["response"].get("isError") == False and printResp:
                    print("     Device was successfully deleted!")
                    pass
                # If the request call returns an error
                if result["response"].get("isError") == True and printResp:
                    print("     Device has already been deleted!")
                    pass
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
        """ Method gets all configurations or all images uploaded in the DNA-C """
        try:
            # Define maximum attempts for the request
            counter = 3
            while True:
                # Create a header with instruction
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/file/namespace/' + namespace, headers=header, verify=False)
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
                # If the request call returns one of these conditions
                elif r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
            # Use the API call method with "config" parameter to get all configurations in the DNA-C
            configurationTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("config")
            # Use the API call method with "image" parameter to get all images in the DNA-C
            imageTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("image")
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
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # Create a payload for POST method
                payload = [{
                    "hostName": i["hostName"],
                    "serialNumber": i["serialNumber"],
                    "platformId": i["platformId"],
                    "site": i["site"],
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
                        continue
                    if cmd == "y" or cmd == "Y":
                        print("\n" + "   WARNING! There is no configuration " + configurationName + " for the device " + i["hostName"] + " in the DNA-C!")
                        pass
                # If a match was found adds the appropriate imageId to the created payload
                if imageId is not None:
                    payload[0]["imageId"] = imageId
                    print("   Image " + imageName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_im += 1
                # Otherwise print warning notification
                else:
                    print("   WARNING! There is no image " + imageName + " for the device " + i["hostName"] + " in the xlsx or in the DNA-C!")
                    pass
                try:
                    # API call
                    response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', data=json.dumps(payload), headers=header, verify=False)
                    # Print the response code
                    print("    " + str(response))
                    # Transform a response to JSON format
                    r_json = response.json()
                    # Use the API call method with taskID parameter to get information about a completed API call
                    result = ApiDNAC.api_get_task_info(r_json["response"]["taskId"])
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
                  "\n" + "     Successfully uploaded devices to DNA-C:   " + str(number) + " / " + str(cycle))
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
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # API call
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/task/' + taskID, headers=header, verify=False)
                # Transform a response to JSON format
                r_json = response.json()
                # If the request call returns one of these conditions
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    # Call the method for creating new token
                    ApiDNAC.__token.get_new_token()
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
            # Use the API call method with "config" parameter to get all configurations in the DNA-C
            configurationTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("config")
            # Use the API call method with "image" parameter to get all images in the DNA-C
            imageTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("image")
            # Run the cycle for posting devices according to rows in XLS table ("data_set" is the list of dictionaries)
            for i in data_set:
                # Part for the DNA-C
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
                # Create a header with instruction for the DNA-C
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                # Create a payload for POST method into the DNA-C
                payload = [{
                    "hostName": i["hostName"],
                    "serialNumber": i["serialNumber"],
                    "platformId": i["platformId"],
                    "site": i["site"],
                    }]
                # print("Payload " + str(counter) + json.dumps(payload, indent=2))
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
                        print("\n" + "   WARNING! There is no configuration " + configurationName + " for the device " + i["hostName"] + " in the DNA-C!")
                        pass
                # If a match was found adds the appropriate imageId to the created payload
                if imageId is not None:
                    payload[0]["imageId"] = imageId
                    print("   Image " + imageName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_im += 1
                # Otherwise print warning notification
                else:
                    print("   WARNING! There is no image " + imageName + " for the device " + i["hostName"] + " in the xlsx or in the DNA-C!")
                    pass
                try:
                    # API call into the DNA-C
                    response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', data=json.dumps(payload), headers=header, verify=False)
                    # Print the response code
                    print("    " + str(response))
                    # Transform a response to JSON format
                    r_json = response.json()
                    # Use the API call method with taskID parameter to get information about a completed API call
                    result = ApiDNAC.api_get_task_info(r_json["response"]["taskId"])
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
                    print("    Something's wrong with upload to DNA-C: " + str(e))
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
                        "NetworkDeviceGroupList": ["Location#All Locations", "Device Type#All Device Types"]
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
                  "\n" + "     Successfully uploaded devices to DNA-C:   " + str(number) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to ISE:     " + str(num_ise) + " / " + str(cycle))
        except Exception as e:
            print("   Something's wrong: " + str(e))
