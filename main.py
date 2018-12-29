# This is main initialization file
from easypnp_networksys_cz import program

MENU_NAME = "MENU"

# Start of application
while True:
    try:
        print("\n" + MENU_NAME + ":")
        command = input(" 1 - APIC-EM\n 2 - DNA-C\n 3 - END\n Your choice (enter a number or q)? ")
        if command == "1":
            program.Program.run_program_APICEM(MENU_NAME)
        elif command == "2":
            program.Program.run_program_DNAC(MENU_NAME)
        elif command == "3" or command == "q" or command == "Q":
            break
    except RuntimeError:
        continue