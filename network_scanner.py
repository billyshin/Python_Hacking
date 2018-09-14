"""
Scan the current network and get the IP Address of target device.

Network Scanner Algorithm:
1. Create arp request directed to broadcast MAC asking for IP
    a) Use ARP to ask who has target IP
    b) Set destination MAC to broadcast MAC
2. Send packet and receive response
3. Parse the response
4. Print result

Need to install scapy:
    Python2: pip install scapy
    Python3: pip3 install scapy-python3
"""

import scapy.all as scapy
import optparse


def get_arguments():
    # Get command line arguments
    """
    Get the target IP address from command line argument.

    :return: IP Address of target device
    :rtype: str
    """
    parser = optparse.OptionParser()

    # Get the ip address
    parser.add_option("-t", "--target", dest="target_ip",
                      help="Target IP / IP range")

    options = parser.parse_args()

    return options.target_ip


def scan(ip_address):
    """
    Discover clients on the same network using ARP protocol.
    
    :param ip_address: ip address
    :type ip_address: str
    """
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # ethernet object
    # final packet
    arp_request_broadcast = broadcast/arp_request

    # use srp function to send arp_request_broadcast packet and receive response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]

    # get list of client(ip address, mac address)
    clients_list = []
    for elements in answered_list:
        client_dict = {"ip":elements[1].psrc, "mac": elements[1].hwrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(result_list):
    """
    Print out the information of all client that are connected in the same 
    network.
    
    :param result_list: list of clients
    :type result_list: list of dict
    """
    print("IP\t\t\t\tMAC Address\n--------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


if __name__ == "__main__":
    target_ip = get_arguments()
    scan_result = scan(target_ip)
    print_result(scan_result)
