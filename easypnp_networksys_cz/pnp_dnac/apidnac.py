from easypnp_networksys_cz import program
from easypnp_networksys_cz.pnp_dnac import token
import json
import requests
import base64


class ApiDNAC:
    __token = token.Token()
    __urlController = ''
    __urlControllerAPI = ''

    @staticmethod
    def set_url(new_url):
        ApiDNAC.__urlController = new_url
        ApiDNAC.__urlControllerAPI = "https://" + new_url + "/"

    @staticmethod
    def get_url():
        return ApiDNAC.__urlController

########################################################################################################################
                                                    # PnP API calls - SYSTEM #
########################################################################################################################

    @staticmethod
    def api_connection(first_url):
        """ Tries connection to DNA-C and asks for credentials """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                payload_string = (program.Program.get_credentials(c_user=True, c_pass=False) + ":" + program.Program.get_credentials(c_user=False, c_pass=True)).encode('utf-8')
                payload_b64 = (base64.b64encode(payload_string)).decode('utf-8')
                header = {"content-type": "application/json", "authorization": "Basic " + payload_b64}
                response = requests.request("POST", 'https://' + first_url + '/api/system/v1/auth/token', headers=header, verify=False)
                # If program request call returned error code
                if response.status_code != 200:
                    return True
        except Exception:
            print("   ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_get_host():
        """ Gets a user basic info """
        try:
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/host', headers=header, verify=False)
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    return False
                else:
                    print("  " + str(response))
                    print("  Token is still valid!")
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")

    @staticmethod
    def api_get_token():
        """ Gets a new valid token and asks for possible credentials """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                payload_string = (program.Program.get_credentials(c_user=True, c_pass=False) + ":" + program.Program.get_credentials(c_user=False, c_pass=True)).encode('utf-8')
                payload_b64 = (base64.b64encode(payload_string)).decode('utf-8')
                header = {"content-type": "application/json", "authorization": "Basic " + payload_b64}
                response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/system/v1/auth/token', headers=header, verify=False)
                print("  " + str(response))
                # If program request call returned error code
                if response.status_code != 200:
                    if response.status_code == 403:
                        print("  Response status code 403 = access is denied by controller!")
                        pass
                    # Call main program controller for valid credentials
                    state = program.Program.update_credentials()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    elif state == False:
                        raise RuntimeError()
                    continue
                r_json = response.json()
                if not r_json.get("Token"):
                    program.Program.update_credentials()
                    continue
                else:
                    print("  Token was successfully created!")
                return r_json["Token"]
        except Exception:
            print("  ERROR! Token was not created!")

    @staticmethod
    def api_get_network_devices():
        """ Gets all network devices """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/network-device', headers=header, verify=False)
                #print("   " + str(response))
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_get_device_interface(deviceID):
        """ Gets all interfaces of selected device """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/interface/network-device/' + deviceID, headers=header, verify=False)
                #print("   " + str(response))
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

########################################################################################################################
                                                # PnP API calls - PROJECT#
########################################################################################################################

    @staticmethod
    def api_get_pnp_project():
        """ Gets all PnP projects """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project', headers=header, verify=False)
                print("  " + str(response))
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_create_pnp_project(project_name):
        """ Create PnP project """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                payload = "[{\"siteName\": \"" + project_name + "\"}]"
                response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project', data=payload, headers=header, verify=False)
                print("  " + str(response))
                if response.status_code == 202:
                    print("   New project " + project_name + " was successfully created!")
                    pass
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_delete_pnp_project(projectID, printResp=True):
        """ Delete PnP project """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID, headers=header, verify=False)
                print("   " + str(response)) if printResp else print("    " + str(response))
                if response.status_code == 202 and printResp:
                    print("   Project was successfully deleted!")
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))

########################################################################################################################
                                            # PnP API calls - CONFIGURATION#
########################################################################################################################

    @staticmethod
    def api_get_pnp_configuration():
        """ Gets all PnP configurations """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/file/namespace/config', headers=header, verify=False)
                print("  " + str(response))
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
            return False

    @staticmethod
    def api_upload_pnp_configuration(configuration_path, configuration_file, number):
        """ Upload all PnP configurations """
        try:
            # Defines maximum attempts for request
            counter = 3
            try:
                configuration_filename = open(configuration_path, "r")
                payload = {'fileUpload': configuration_filename}
            except:
                print("  File does not exist!")
                pass
            header = {"X-Auth-Token": ApiDNAC.__token.get_token()}
            try:
                response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/file/config', files=payload, headers=header, verify=False)
                print("  " + str(response))
                if response.status_code == 200:
                    print("  Configuration " + configuration_file + " was successfully uploaded!")
                    number += 1
            except requests.exceptions.RequestException as e:
                print("  ERROR! Connection to DNA-C is not working! Enter correct IP address!")
                return False
            r_json = response.json()
            a = r_json['response'].get('errorCode')
            try:
                if a == "FILE_ALREADY_EXISTS":
                    print("  Configuration " + configuration_file + " has already been uploaded in the past!")
                elif r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    pass
                return number
            except Exception as e:
                print("  Something's wrong: " + str(e))
        except Exception as e:
            print("  Something's wrong: " + str(e))

    @staticmethod
    def api_delete_pnp_configuration(configurationID, printResp=True, printResp2=True, printResp3=True):
        """ Delete PnP configuration """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/file/' + configurationID, headers=header, verify=False)
                print("   " + str(response)) if printResp else None
                if response.status_code == 200 and printResp:
                    print("   Configuration was successfully deleted!")
                    pass
                if response.status_code == 200 and printResp2:
                    print("     Configuration was successfully deleted!")
                    pass
                r_json = response.json()
                if response.status_code == 404 and printResp:
                    print("   Configuration has already been deleted!")
                    pass
                elif response.status_code == 404 and printResp2:
                    print("     Configuration has already been deleted!")
                    pass
                elif response.status_code == 404 and printResp3:
                    pass
                if r_json.get("message") or r_json.get("exp"): #or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e)) if printResp else print("    Something's wrong: " + str(e))

########################################################################################################################
                                             # PnP API calls - DEVICE#
########################################################################################################################

    @staticmethod
    def api_get_pnp_project_devices(projectID, printResp=True):
        """ Gets all devices of PnP project """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', headers=header, verify=False)
                print("   " + str(response)) if printResp else None
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_get_pnp_devices(printResp=True):
        """ Gets all devices """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-device', headers=header, verify=False)
                print("   " + str(response)) if printResp else None
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_delete_pnp_devices(deviceID, printResp=True):
        """ Delete devices """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-device/' + deviceID, headers=header, verify=False)
                print("    " + str(response)) if printResp else None
                if response.status_code == 202 and printResp:
                    print("    Device was successfully deleted!")
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("    Something's wrong: " + str(e))

    @staticmethod
    def api_delete_pnp_project_devices(projectID, deviceID, printResp=True):
        """ Delete device from PnP project """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("DELETE", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device/' + deviceID, headers=header, verify=False)
                print("     " + str(response)) if printResp else None
                r_json = response.json()
                result = ApiDNAC.api_get_task_info(r_json["response"]["taskId"])
                if result["response"].get("isError") == False and printResp:
                    print("     Device was successfully deleted!")
                    pass
                if result["response"].get("isError") == True and printResp:
                    print("     Device has already been deleted!")
                    pass
                if r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("    Something's wrong: " + str(e))

    @staticmethod
    def api_get_pnp_files_for_post_project_devices(namespace):
        """ Gets all PnP configurations """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/file/namespace/' + namespace, headers=header, verify=False)
                r_json = response.json()
                if namespace == "config":
                    configurationList = r_json['response']
                    #print("File list " + json.dumps(configurationList, indent=2))
                    configurationTuple = [(configuration['name'], configuration['id']) for configuration in configurationList]
                    #print("File tuple " + json.dumps(configurationTuple, indent=2))
                    return configurationTuple
                elif namespace == "image":
                    imageList = r_json['response']
                    #print("File list " + json.dumps(imageList, indent=2))
                    imageTuple = [(image['name'], image['id']) for image in imageList]
                    #print("File tuple " + json.dumps(imageTuple, indent=2))
                    return imageTuple
                elif r_json.get("message") or r_json.get("exp") or response.status_code != 202:
                    ApiDNAC.__token.get_new_token()
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
        """ Post devices to PnP project """
        try:
            cycle = 0
            number = 0
            num_conf = 0
            num_im = 0
            configurationTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("config")
            imageTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("image")
            for i in data_set:
                cycle += 1
                try:
                    configurationName = i["hostName"] + "_configuration"
                    configId = [id for cn, id in configurationTuple if cn == configurationName][0]
                except Exception as e:
                    configId = None
                try:
                    imageName = i["image"]
                    imageId = [id for imn, id in imageTuple if imn == imageName][0]
                except Exception as e:
                    imageId = None

                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                payload = [{
                    "hostName": i["hostName"],
                    "serialNumber": i["serialNumber"],
                    "platformId": i["platformId"],
                    "site": i["site"],
                    }]
                #print("Payload " + str(counter) + json.dumps(payload, indent=2))
                if i["devCert"] == "yes":
                    payload[0]["pkiEnabled"] = True
                else:
                    payload[0]["pkiEnabled"] = False
                #print("Payload " + str(counter) + json.dumps(payload, indent=2))
                if configId is not None:
                    payload[0]["configId"] = configId
                    print("\n" + "   Configuration " + configurationName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_conf += 1
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
                #print("Payload " + str(counter) + json.dumps(payload, indent=2))
                if imageId is not None:
                    payload[0]["imageId"] = imageId
                    print("   Image " + imageName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_im += 1
                else:
                    print("   WARNING! There is no image " + imageName + " for the device " + i["hostName"] + " in the xlsx or in the DNA-C!")
                    pass
                #print("Payload " + str(counter) + json.dumps(payload, indent=2))
                try:
                    response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', data=json.dumps(payload), headers=header, verify=False)
                    print("    " + str(response))
                    r_json = response.json()
                    result = ApiDNAC.api_get_task_info(r_json["response"]["taskId"])
                    try:
                        if result["response"].get("isError") == False:
                            print("    Device " + i["hostName"] + " was successfully created in selected PnP project!")
                            number += 1
                        if result["response"].get("isError") == True:
                            if result["response"]["failureReason"][0] == "P":
                                print("    ERROR! Device " + i["hostName"] + " has been already created in selected PnP project!")
                            else:
                                print("    ERROR! Device " + i["hostName"] + " is assigned to other PnP project!")
                    except Exception as e:
                        print("    Something's wrong: " + str(e))
                except Exception as e:
                    print("    Something's wrong: " + str(e))
            print("\n" + "     STATS!"
                  "\n" + "     Devices with configuration:               " + str(num_conf) + " / " + str(cycle) + ""
                  "\n" + "     Devices with image:                       " + str(num_im) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to DNA-C:   " + str(number) + " / " + str(cycle))
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_get_task_info(taskID):
        """ Gets information from completed task """
        try:
            # Defines maximum attempts for request
            counter = 3
            while True:
                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                response = requests.request("GET", ApiDNAC.__urlControllerAPI + 'api/v1/task/' + taskID, headers=header, verify=False)
                r_json = response.json()
                if r_json.get("message") or r_json.get("exp") or response.status_code != 200:
                    ApiDNAC.__token.get_new_token()
                    counter -= 1
                    if counter < 0:
                        raise RuntimeError()
                    continue
                return r_json
        except Exception as e:
            print("   Something's wrong: " + str(e))

    @staticmethod
    def api_post_pnp_project_devices_toISE(projectID, data_set, ise_credentials_b64, ise_url):
        """ Post devices to PnP project and ISE """
        try:
            cycle = 0
            number = 0
            num_conf = 0
            num_im = 0
            num_ise = 0
            configurationTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("config")
            imageTuple = ApiDNAC.api_get_pnp_files_for_post_project_devices("image")
            for i in data_set:
                cycle += 1
                try:
                    configurationName = i["hostName"] + "_configuration"
                    configId = [id for cn, id in configurationTuple if cn == configurationName][0]
                except Exception as e:
                    configId = None
                try:
                    imageName = i["image"]
                    imageId = [id for imn, id in imageTuple if imn == imageName][0]
                except Exception as e:
                    imageId = None

                header = {"content-type": "application/json", "X-Auth-Token": ApiDNAC.__token.get_token()}
                payload = [{
                    "hostName": i["hostName"],
                    "serialNumber": i["serialNumber"],
                    "platformId": i["platformId"],
                    "site": i["site"],
                    }]
                if i["devCert"] == "yes":
                    payload[0]["pkiEnabled"] = True
                else:
                    payload[0]["pkiEnabled"] = False
                if configId is not None:
                    payload[0]["configId"] = configId
                    print("\n" + "   Configuration " + configurationName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_conf += 1
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
                if imageId is not None:
                    payload[0]["imageId"] = imageId
                    print("   Image " + imageName + " was added to device " + i["hostName"] + " for upload to the PnP project!")
                    num_im += 1
                else:
                    print("   WARNING! There is no image " + imageName + " for the device " + i["hostName"] + " in the xlsx or in the DNA-C!")
                    pass
                try:
                    response = requests.request("POST", ApiDNAC.__urlControllerAPI + 'api/v1/pnp-project/' + projectID + '/device', data=json.dumps(payload), headers=header, verify=False)
                    print("    " + str(response))
                    r_json = response.json()
                    result = ApiDNAC.api_get_task_info(r_json["response"]["taskId"])
                    try:
                        if result["response"].get("isError") == False:
                            print("    Device " + i["hostName"] + " was successfully created in selected PnP project!")
                            number += 1
                        if result["response"].get("isError") == True:
                            if result["response"]["failureReason"][0] == "P":
                                print("    ERROR! Device " + i["hostName"] + " has been already created in selected PnP project!")
                            else:
                                print("    ERROR! Device " + i["hostName"] + " is assigned to other PnP project!")
                    except Exception as e:
                        print("    Something's wrong: " + str(e))
                except Exception as e:
                    print("    Something's wrong with upload to DNA-C: " + str(e))

                try:
                    header_ise = {"content-type": "application/json", "authorization": "Basic " + ise_credentials_b64, "accept": "application/json", "cache-control": "no-cache"}
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
                    response_ise = requests.request("POST", ise_url, data=json.dumps(payload_ise), headers=header_ise, verify=False)
                    print("    " + str(response_ise))
                    if response_ise.status_code == 201:
                        print("    Device " + i["hostName"] + " was successfully created in ISE!")
                        num_ise += 1
                    elif response_ise.status_code == 400:
                        print("    ERROR! Device " + i["hostName"] + " already exists in ISE!")
                    elif response_ise.status_code == 401:
                        print("    ERROR! Device " + i["hostName"] + " was not created in ISE! User does not have permission! Enter correct credentials!")
                        break
                    else:
                        print("    ERROR! Device " + i["hostName"] + " was not created in ISE! Something is wrong, try again!")
                        break
                except Exception:
                    print("    ERROR! Device " + i["hostName"] + " was not created in ISE! Connection is not working! Enter correct IP address!")
                    break
            print("\n" + "     STATS!"
                  "\n" + "     Devices with configuration:               " + str(num_conf) + " / " + str(cycle) + ""
                  "\n" + "     Devices with image:                       " + str(num_im) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to DNA-C:   " + str(number) + " / " + str(cycle) + ""
                  "\n" + "     Successfully uploaded devices to ISE:     " + str(num_ise) + " / " + str(cycle))
        except Exception as e:
            print("   Something's wrong: " + str(e))
