# EasyPnP/easypnp_networksys_cz/pnp_apicem
This is the `module` part for **Cisco APIC-EM** controller of the EasyPnP tool.

  - [ticket.py](#ticketpy)
  - [pnp_apicem.py](#pnp_apicempy)
  - [apiapicem.py](#apiapicempy)
  - [devices](#devices)
  - [template](#template)
  - [configurations](#configurations)  
  
# ticket.py 
:page_facing_up:
This file manages the appropriate **authentication string** (ticket in the **Cisco APIC-EM**) which is used for all API calls (except it where this string is obtained) to the selected controller. The authentication string and the URL address of the controller are stored on the local disk in the `cache_config` text file.

# pnp_apicem.py 
:page_facing_up: 
This file manages the **Cisco APIC-EM** controller module and all its features. The file contains the `PnP_APICEM` class which is divided into 4 logical code blocks, i.e. `Menu`, `Project`, `Configuration` and `Device`. There are methods that perform tasks according to their name in each code block. The methods use the `model` part functions and call the `ApiAPICEM` class functions (which perform the specific API calls) to work with the selected controller. 

# apiapicem.py 
:page_facing_up:
This file contains methods which perform all **API calls** to the **Cisco APIC-EM** controller. These methods return the responses to the `module` part methods and `program` part methods. The `ApiAPICEM` class is divided into 4 logical code blocks according to their purpose, i.e. `System`, `Project`, `Configuration` and `Device`. There are only two methods outside these blocks. Both methods work with local variables, so that the URL address of the selected controller does not have to be read from the `cache_config` text file for each API call.
  
# devices 
:file_folder:
The uploaded **XLS table** with defined devices is copied to this folder to keep this file after the EasyPnP ends and to keep the stability of file path.

# template 
:file_folder:
The uploaded **configuration template** is copied to this folder to keep this file after the EasyPnP ends and to keep the stability of file path.

# configurations 
:file_folder:
All **generated configurations** are stored in this folder. EasyPnP can be used independently of the controller to create configurations, so local access to these files is required.









