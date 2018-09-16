# Python_Hacking

Programs and Tools written in Python that are useful in hacking in Kali Linux.

Required: Kali Linux, Python2, scapy package, netfilterqueue

          pip install scapy
          
          pip install scapy-http
          
          pip install netfilterqueue

Contents:
   1. mac_changer.py - A program that is used to change the MAC Address to ensure anonymity.
      
          Usage: python mac_changer.py -i [Interface] -m [new MAC Address]
      
   2. network_scanner.py - A program that uses target IP Address to get the target MAC Address under the same network.
      
          Usage: python network_scanner.py -t [Taget IP Address]
      
   3. arp_spoof.py - A program that functions exactly the same as arpspoof command in Kali Linux. It takes target ip address and gateway ip address as command line arguments.
      
          Usage: python arp_spoof.py -t [Target IP Address] -g [Gateway]
     
   4. packet_sniffer.py - A program that acts as MITM (Man In The Middle) to sniff/capture data through http layer such as url, username, password, etc. It must run with arp_spoof.py simultaneously.
      
          Usage: python arp_spoof.py -t [Target IP Address] -g [Gateway]
                 python packet_sniffer.py -i [Interface]
                 
   5. dns_spoof.py - A program that acts as MITM (Man In The Middle) to intercept packets and store them in netfilterqueue and redirect target device to a certain IP Address.
   
          Usage: python dns_spoof.py -i [IP Address]
          
  6. file_interceptor.py - A program that hijacks target's HTTP request and modifies HTTP status code as well as HTTP response in order to redirect to user specified url.
  
          Usage: iptables -I FORWARD -j NFQUEUE --queue-num 0
                 python arp_spoof.py -t [Target IP Address] -g [Gateway]
                 python file_interceptor.py -r [Redirect URL]
       
  7. download.py - A program that download a file from input URL and save it to input destination location.
  
          Usage: python download.py -u [URL] -d [Destination loaction]
          
  8. reverse_backdoor.py - A backdoor program that allows hacker to execute simple commands on target device using reversed TCP. Need to change ip_address to your current IP Address in main code. It must be run in the target device locally, and thus social engineering or any other MITM attack should be used. It works in all environment that supports Python. listener.py only works when reverse_backdoor.py is running locally in target device.
          
  8. listener.py - A socket program that allows us to listen from the reverser_backdoor.py program.
        
           Usage: reverse_backdoor.py is running in target device
                  python listener.py -i [IP Address]
                  
     Available commands in hacker's machine:
          
     1. Disable backdoor connection
     
                    exit
     
     2. Change working directory

                    cd [Destination directory]
                   
     3. Download/Read file from target device
                    
                    download [File]
                    
     4. Upload/Write file to traget device
                    
                    upload [File]


code_injector.py, bypass_http.py, kelogger.py, malware_packing.py, web_hack.py, crawler.py, vulnerability_scanner.py comming soon...
