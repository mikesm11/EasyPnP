import time
import paramiko


class Client:
    """ Class responsible for connecting to the device """
    @staticmethod
    def ssh_access(ssh_address, ssh_username, ssh_password, printResp=True):
        try:
            # Create a new instance of an SSH client
            client = paramiko.SSHClient()
            # Set the missing host key policy to auto add the certificate
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=ssh_address, username=ssh_username, password=ssh_password)
            remote_conn = client.invoke_shell()
            if printResp:
                print("     Interactive session established with {0}".format(ssh_address))
            remote_conn.send('\n')
            time.sleep(1)
            remote_conn.send("erase /all nvram:\n")
            time.sleep(3)
            remote_conn.send("\n")
            remote_conn.send("\n")
            time.sleep(1)
            remote_conn.send("reload\n")
            time.sleep(3)
            remote_conn.send("no\n")
            remote_conn.send("\n")
            time.sleep(3)
            remote_conn.send("reload\n")
            time.sleep(3)
            remote_conn.send("\n")
            remote_conn.send("\n")
            #client.close()
            #print("     Device was successfully cleaned and reloaded!")
            return True
        except Exception as e:
            #print("     Something's wrong with connection to device: " + str(e))
            return False
