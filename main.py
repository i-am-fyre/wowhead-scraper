#!/usr/bin/env python3.7

import requests
from bs4 import BeautifulSoup

language = ["en", "de","es","fr","it","pt","ru","ko","cn"]
item_id_start = 1
item_id_end = 100

for i in range (item_id_start,item_id_end):
    # first, check if item exists
    test_url="https://en.classic.wowhead.com/item="+str(i)
    test_page = requests.get(test_url)
    test_soup = BeautifulSoup(test_page.content, 'html.parser')

    if test_soup.find("h1", {"class": "heading-size-1"}).text != "Items":
        print("URL: https://en.classic.wowhead.com/item="+str(i))
        #second, pull translations
        for l in language:
            url = "https://"+l+".classic.wowhead.com/item="+str(i)
            
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # get item name
            print(l + ": " + soup.find("h1", {"class": "heading-size-1"}).text)
        print("=========")

print("DONE")
