# Python_Hacking

Programs and Tools written in Python that are useful in hacking in Kali Linux.

Required: Kali Linux, Python2, scapy package, netfilterqueue

          pip install scapy
          
          pip install scapy-http
          
          pip install netfilterqueue

Contents:
   1. mac_changer.py - A program that is used to change the MAC Address to ensure anonymity.
      
          Usage: python mac_changer.py -i [Interface] -m [new MAC Address]
      
   2. network_scanner.py - A program that uses target IP Address to get the target MAC Address under same network.
      
          Usage: python network_scanner.py -t [Taget IP Address]
      
   3. arp_spoof.py - A program that functions exactly the same as arpspoof command in Kali Linux. It takes target ip address and gateway ip address as command line arguments.
      
          Usage: python arp_spoof.py -t [Target IP Address] -g [Gateway]
     
   4. packet_sniffer.py - A program that acts as MITM (Man In The Middle) to sniff/capture data through http layer such as url, username, password, etc. It must run with arp_spoof.py simultaneously.
      
          Usage: python arp_spoof.py -t [Target IP Address] -g [Gateway]
                 python packet_sniffer.py -i [Interface]
