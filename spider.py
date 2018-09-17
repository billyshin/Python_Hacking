import optparse

import requests
import re

import requests
import re
import urlparse

target_links = []


def get_arguments():
    """
    Get the url of a target website.

    :return: the url of a website
    :rtype: str
    """
    parser = optparse.OptionParser()

    # Get the url
    parser.add_option("-u", "--url", dest="url",
                      help="URL of website")

    (options, arguments) = parser.parse_args()

    # Code to handle error
    if not options.url:
        parser.error(
            "[-] Please specify an url, use --help for more info.")

    return options.url


def extract_links_from(url):
    """
    Get request from url and return all of its links.
    :param url: url of a website/web server
    :type url: str
    :return: list of href
    :rtype: list
    """
    response = requests.get(url)

    return re.findall('(?:href=")(.*?)"', response.content)


def craw(url):
    """ 
    Recrusively find all ahref links and print them.
    
    :param url: url 
    :type url: str
    """
    href_links = extract_links_from(url)

    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            craw(link)


if __name__ == "__main__":
    target_url =get_arguments()

    craw(target_url)
