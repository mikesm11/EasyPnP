# EasyPnP
- [EasyPnP](#easypnp)
  - [Introduction](#introduction)
  - [Application Principles](#application-principles)
  - [Instruction Manual](#instruction-manual)
  - [Launch](#launch)
  - [Verified Environment](#verified-environment)
  - [main.py](#main.py)

# Introduction
Network administrators often deal with a problem how to deploy a lot of network devices in a short period of time, especially LAN infrastructure in campus networks. It is necessary to unbox each new device, upgrade it to a particular IOS version and upload the right configuration. In case we have to deploy several devices it might be an easy task, but what if there are hundreds? It may become a tough task with a big chance to make a mistake. The goal of **EasyPnP** solution is to simplify the **PnP** (Plug and Play) process as much as possible to deploy new or existing devices easy and intuitive, without the need to use **Cisco PI** (Prime Infrastracture). The only prerequisites for successful implementation are a filled in **XLS spreadsheet** with required devices details and a **configuration template**. Another use may be to mass-unify configurations of large number of devices, where some changes are needed. Simply erase the devices and re-provision them. My **EasyPnP** solution together with **Cisco APIC-EM** (Application Policy Infrastructure Controller - Enterprise Module) or **Cisco DNA-C** (Digital Network Architecture - Center) is able to effectively deal with a problem of preparation complex configuration template and it can make mass deployment of network devices fault proof, simple and quick. And it can add these devices to **Cisco ISE** (Identity Services Engine) as well. It is suitable for customers who want to profit from simplified network devices workflow with less effort.

# Application Principles
The entire PnP process can be managed using the EasyPnP tool without using a controller GUI. Based on upload XLS spreadsheet and configuration template the EasyPnP generates configurations for each device included in the spreadsheet. The configurations are then pushed to the APIC-EM or DNA-C controller through API. In the last step the devices are added into already created PnP project. There is also an option to create network devices in Cisco ISE. When the controller sees a device with a known serial number, it is claimed and provisioned. After the PnP process is complete, the device is ready for common use.

# Instruction Manual
  - English instruction [videomanual](https://youtu.be/Kxbin1WrpYY)
  - Czech instruction [videomanual](https://youtu.be/GOxJ5qpehj4)

# Launch
### MacOS/Linux
Open the operating system CLI and follow the instructions:
1. Create a virtual environment
  - `> cd .../EasyPnP`
  - `> python3.6 -m venv venv`
2. Run the virtual environment
  - `> source venv/bin/activate`
3. Install the necessary packages and libraries (see [requirements.txt](requirements.txt))
  - `> (venv) pip install -r requirements.txt`
4. Launch the EasyPnP tool
  - `> (venv) py main.py`
### Windows
Open the operating system CLI and follow the instructions:
1. Create a virtual environment
  - `> cd .../EasyPnP`
  - `> py -3 -m venv venv`
2. Run the virtual environment
  - `> source venv/Scripts/activate`
3. Install the necessary packages and libraries (see [reguirements.txt](requirements.txt))
  - `> (venv) pip install -r requirements.txt`
4. Launch the EasyPnP tool
  - `> (venv) py main.py`

# Verified Environment
  - Python 3.6
  - Cisco APIC-EM 1.6.2
  - Cisco DNA-C 1.1.7
  - Cisco ISE 2.3
  
# main.py
> Notice the UML [architecture](UML_architecture.pdf) of Easypnp.
EasyPnP is designed for modular use. For this reason, its structure is divided into three logical blocks - model, program and module part. Apart from these blocks, only the main.py file is included. This is the main initialization file and is used to launch the EasyPnP tool.


   