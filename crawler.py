"""
A program that get datas from website.

Crawling directories:
    1. Directories inside the web root
    2. Can contain files or other directories

"""
import optparse
import requests


def get_arguments():
    """
    Get the url of a target website.

    :return: the url of a website
    :rtype: str
    """
    parser = optparse.OptionParser()

    # Get the name of intergace from user input
    parser.add_option("-u", "--url", dest="url",
                      help="URL of website")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.url:
        parser.error(
            "[-] Please specify an url, use --help for more info.")

    return options.url


def request(url):
    """
    Reqeust from url. 
    :param url: url of website
    :type url: str
    :return: result of request
    :rtype: obj
    """
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


def find_subdomain(url):
    """
    Find and print all submains of the web server specified in url.
    :param url: URL of a website
    :type url: str
    """
    with open("./subdomains-wodlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered subdomian --> " + test_url)


def find_directories(url):
    """
    Find all directories inside the target web server.
    :param url: URL of a website
    :type url: str
    """
    with open("./files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered URL --> " + test_url)

if __name__ == "__main__":
    target_url = get_arguments()
    # test
    target_url = "10.0.2.7/mutillidae/"
    find_directories(target_url)
