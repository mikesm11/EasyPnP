# EasyPnP/easypnp_networksys_cz/model
This is the `model` part of the EasyPnP tool.

  - [isecredentials.py, sshcredentials.py, usercredentials.py](#setcredentialspy)
  - [credentials.py](#credentialspy)
  - [client.py](#clientpy)
  - [directory.py](#directorypy)
  - [cache.py](#cachepy)
  - [url.py](#urlpy)
  
# isecredentials.py, sshcredentials.py, usercredentials.py 
:page_facing_up:
The methods contained in these files serve to display a dialog box (using the `Tkinter` library) for setting user credentials to the controller (usercredentials.py), to the particular device (sshcredentials.py) or to the Cisco ISE (isecredentials.py). The contents of these files are almost identical — differ only in the number of variables.

# credentials.py
:page_facing_up:
This file serve to store user credentials to the controller, to the particular device and to the Cisco ISE. The content is a `Credentials` class with 8 global variables that are accessible to other parts. The user credentials are stored only when the program runs into these variables. If the program is restarted, the credentials are not stored anywhere.

# client.py 
:page_facing_up:
This file serve to automatically delete and restart the particular network devices. A `paramiko` library is used to establish an SSH connection. With this feature, you can remotely clean the selected device and then upload a new system configuration (using EasyPnP and the selected controller). This ensures very simple changes in the configurations of multiple devices without manual control.

# directory.py 
:page_facing_up:
There are 2 methods that allow you to select a XLS table and a configuration template in this file. The `Tkinter` library (its `filedialog` module) is used to display a dialog box which serves for interactive selection of these files from the internal repository. The selection of files is limited by the parameter — the table with defined devices must be in **XLS** format (extension xlsx), the configuration template must be in **Jinja2** format (extension jnj). The table is copied into the `devices` folder and the configuration template into the `template` folder (of the EasyPnP tool) to keep this file after the EasyPnP ends and to keep the stability of file path.

# cache.py 
:page_facing_up:
The methods of this file serve to store the selected data on a local disk, specifically in the `cache_config` text file. The content of this text file is the **URL address** of the controller and the appropriate **authentication string**. The text file has a dictionary data structure. Text file is located as the same as the `main.py` initialization file, but it does not exist before the first run of EasyPnP tool. This text file is created after entering the IP or DNS address of the selected controller. Subsequent by entering the user credentials the authentication string is stored (after successful authentication). This string is used for all other API calls to the particular controller. These data (URL address and authentication string) are automatically refreshed with the currently valid values.    

# url.py 
:page_facing_up:
This file includes 4 methods for working with the URL address of the selected controller. The URL address is stored in the local variable `__url` and in the variable `__urlController` (inside the class from the `module` part) so that the URL address does not have to be read from the `cache_config` text file for each API call. If EasyPnP is ended, the address is stored only in the `cache_config` text file.


