# EasyPnP/easypnp_networksys_cz/pnp_dnac
This is the `module` part for **Cisco DNA-C** controller of the EasyPnP tool.

  - [token.py](#tokenpy)
  - [pnp_dnac.py](#pnp_dnacpy)
  - [apidnac.py](#apidnacpy)
  - [devices](#devices)
  - [template](#template)
  - [configurations](#configurations)
  
# token.py 
:page_facing_up:
This file manages the appropriate **authentication string** (token in the **Cisco DNA-C**) which is used for all API calls (except it where this string is obtained) to the selected controller. The authentication string and the URL address of the controller are stored on the local disk in the `cache_config` text file.

# pnp_dnac.py 
:page_facing_up:
This file manages the **Cisco DNA-C** controller module and all its features. The file contains the `PnP_DNAC` class which is divided into 4 logical code blocks, i.e. `Menu`, `Project`, `Configuration` and `Device`. There are methods that perform tasks according to their name in each code block. The methods use the `model` part functions and call the `ApiDNAC` class functions (which perform the specific API calls) to work with the selected controller. 

# apidnac.py 
:page_facing_up:
This file contains methods which perform all **API calls** to the **Cisco DNA-C** controller. These methods return the responses to the `module` part methods and `program` part methods. The `ApiDNAC` class is divided into 4 logical code blocks according to their purpose, i.e. `System`, `Project`, `Configuration` and `Device`. There are only two methods outside these blocks. Both methods work with local variables, so that the URL address of the selected controller does not have to be read from the `cache_config` text file for each API call.

# devices 
:file_folder:
The uploaded **XLS table** with defined devices is copied to this folder to keep this file after the EasyPnP ends and to keep the stability of file path.

# template 
:file_folder:
The uploaded **configuration template** is copied to this folder to keep this file after the EasyPnP ends and to keep the stability of file path.

# configurations
:file_folder:
All **generated configurations** are stored in this folder. EasyPnP can be used independently of the controller to create configurations, so local access to these files is required.






