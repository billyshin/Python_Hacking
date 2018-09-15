import requests
import subprocess
import optparse


def get_arguments():
    # Get command line arguments
    """
    Get the url of file and destination of downloaded file.

    :return: the url of file, destination of downloaded file.
    :rtype: str, str
    """
    parser = optparse.OptionParser()

    # Get the name of intergace from user input
    parser.add_option("-u", "--url", dest="url",
                      help="URL of file")
    # Get the new MAC Address
    parser.add_option("-d", "--destination", dest="destination",
                      help="Destination of downloaded file")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.url:
        parser.error(
            "[-] Please specify an url, use --help for more info.")
    elif not options.destination:
        parser.error(
            "[-] Please specify a destination, use --help for more info.")
    return options.url, options.destination


def download_file(url, destination):
    """
    Download a file from url and store in destination.
    
    :param url: url of file that we want to download
    :type url: str
    :param destination: destination of downloaded file
    :type destination: str
    """
    resp = requests.get(url)
    with open(destination, "wb") as output:
        output.write(resp.content)


if __name__ == "__main__":
    input_url, input_destination = get_arguments()
    download_file(input_url, input_destination)
    subprocess.Popen(input_destination, shell=True)
