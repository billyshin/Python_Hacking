"""
MAC Address Changer by calling system commands using subprocess module.
"""
import subprocess
import optparse  # get arguments from user, parse and use them
import re


def get_arguments():
    # Get command line arguments
    """
    Get the name of interface and new MAC Address from user input.
    
    :return: options and arugments of command line arguments
    :rtype: (options, argument)
    """
    parser = optparse.OptionParser()

    # Get the name of intergace from user input
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC Address")
    # Get the new MAC Address
    parser.add_option("-m", "--mac", dest="new_mac_address",
                      help="New MAC Address")

    (options, arguments) = get_arguments()

    # Code to handle error
    if not options.interface:
        parser.error(
            "[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac_address:
        parser.error(
            "[-] Please specify a new MAC Address, use --help for more info.")
    return options


def change_mac(interface, new_mac_address):

    """
    Change the MAC Address of interface to new_mac_address.

    :param interface: The name of the interface
    :type interface: str
    :param new_mac_address: THe new address that we want to change to
    :type new_mac_address: str
    """
    # Disable the interface
    subprocess.call(["ifconfig", interface, "down"])
    # Change the MAC Address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
    # Enable the interface
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac_address(interface):
    # Check to see if command line argument is correcrt
    """
    Check if the interface is valid by checking its MAC Address

    :param interface: The name of the interface
    :type interface: str
    :return: current MAC Address
    :rtype: 
    
    """
    ifcofnig_result = subprocess.check_output(["inconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                                          ifcofnig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


if __name__ == "__main__":
    command_options = get_arguments()

    current_mac_address = get_current_mac_address(command_options.interface)
    print("Before MAC Address = ", str(current_mac_address))

    change_mac(command_options.interface, command_options.new_mac_address)

    current_mac_address = get_current_mac_address(command_options.interface)

    if current_mac_address == command_options.new_mac_address:
        print("[-] MAC Address was successfully changed to " +
              command_options.new_mac_address)
    else:
        print("[-] MAC Address did not get changed.")
