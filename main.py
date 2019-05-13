# This is the main initialization file
from easypnp_networksys_cz import program

# Variable for menu name
MENU_NAME = "MENU"

# Start of the EasyPnP application
while True:
    try:
        # Main menu
        print("\n" + MENU_NAME + ":")
        command = input(" 1 - APIC-EM\n 2 - DNA-C\n 3 - END\n Your choice (enter a number or q)? ")
        if command == "1":
            # Entry to the Cisco APIC-EM controller
            program.Program.run_program_APICEM(MENU_NAME)
        elif command == "2":
            # Entry to the Cisco DNA-C controller
            program.Program.run_program_DNAC(MENU_NAME)
        elif command == "3" or command == "q" or command == "Q":
            # End of the EasyPnP application
            break
    except RuntimeError:
        continue
