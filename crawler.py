"""
A program that get datas from website.

Crawling directories:
    1. Directories inside the web root
    2. Can contain files or other directories
    
Discover hidden paths that admin does not want us to know
Analyse discovered paths to discover more paths

"""
import optparse
import requests


def get_arguments():
    """
    Get the url of a target website and the method that we want to use.

    :return: the url of a website, the method that we want to use
    :rtype: str, str
    """
    parser = optparse.OptionParser()

    # Get the url
    parser.add_option("-u", "--url", dest="url",
                      help="URL of website")

    # Get method
    parser.add_option("-m", "--method", dest="method",
                      help="Method")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.url:
        parser.error(
            "[-] Please specify an url, use --help for more info.")

    if not options.method:
        parser.error(
            "[-] Please specify a method, use --help for more info.")

    return options.url, options.method


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
            test_url = word + "." + url
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
            test_url = url + "/" + word
            response = request(test_url)
            if response:
                print("[+] Discovered URL --> " + test_url)

if __name__ == "__main__":
    target_url, method = get_arguments()
    if method:
        if method == "subdomain":
            find_subdomain(target_url)
        if method == "directory":
            find_directories(target_url)
