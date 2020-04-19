"""
Samaritan Security Web Scrapper Script

SDMay20-45
Dept. of Electrical and Computer Engineering
Iowa State University
Author(s): Ryan Goluch, Ann Gould
"""

import urllib.parse
from time import sleep

from bs4 import BeautifulSoup
import requests
import re
from requests import Response

# for debugging
import os

def init_search(terms: str) -> list:
    url = "https://google.com/search?q=" + urllib.parse.quote(terms)
    # print(url)
    resp = get_website_data(url)
    soup = BeautifulSoup(resp, 'html.parser')
    total = []
    for i in soup.findAll('a'):
        print(i.get('href'))
        total.append(i.get('href'))
    return total
    # write_to_file("output_a.txt", str(total))


def get_website_data(website: str) -> Response:
    try:
        r = requests.get(website, timeout=2)
        sleep(0.2)
        r.encoding = 'utf-8'
        print(r.status_code, r.url)
        return r.text
    except:
        # TODO: make this better... maybe mock at some point
        r = requests.get("https://gould-ann.github.io/redirect.html")
        return r.text
