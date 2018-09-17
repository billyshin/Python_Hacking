import requests
import re

import requests
import re


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

if __name__ == "__main__":
    target_url = "10.0.2.7"

    response = request(target_url)

    href_links = re.findall('(?:href=")(.*?)"', response.content)

    for link in href_links:
        print(link)
