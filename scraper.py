import requests
import re


def get_links() -> list:
    """

    :return: zip object containing the url and title param of the json records
    """
    WOT_URL = "https://worldoftanks.eu/en/news/"

    outer_pattern = re.compile(r'NEWS_LIST =.*CATEGORIES', flags=re.MULTILINE | re.DOTALL)
    url_pattern = re.compile(r'"url": "(/[^"]*)"', flags=re.MULTILINE)
    title_pattern = re.compile(r"\"title\": \"([\w\W]*?)\"")

    response = requests.get(WOT_URL)

    subtext = re.findall(outer_pattern, response.text)[0]
    url_list = re.findall(url_pattern, subtext)
    title_list = re.findall(title_pattern, subtext)

    url_list = ['https://worldoftanks.eu' + url for url in url_list]

    return zip(url_list, title_list)
