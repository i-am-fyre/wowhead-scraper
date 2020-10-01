#!/usr/bin/env python3.7

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

category = ["quest"]
language = ["en", "de","es","fr","it","pt","ru","ko","cn"]
id_start = 1
id_end = 100

for c in category:
    for i in range (id_start,id_end+1):
        # first, check if id exists
        test_url="https://classic.wowhead.com/"+c+"="+str(i)
        test_page = requests.get(test_url)
        test_soup = BeautifulSoup(test_page.content, 'html.parser')

        if test_soup.find("h1", {"class": "heading-size-1"}).text != "Quests":
            print("URL: https://classic.wowhead.com/"+c+"="+str(i))
            #second, pull translations
            for l in language:
                if l == "en":
                    l = ""
                else:
                    l = l + "."

                url = "https://"+l+"classic.wowhead.com/"+c+"="+str(i)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                if l == "":
                    l = "en"
                else:
                    l = l[:-1]

                # get id name
                name = soup.find("h1", {"class": "heading-size-1"}).text
                print("[" + l + "] name: " + name)

                # get id details
                details = soup.find("div", {"class": "block-block-bg is-btf"}).next_sibling.strip()
                print("[" + l + "] details: " + details)

                # get id description
                description = ""
                for d in soup.select('h2.heading-size-3')[0]:
                    nextNode = d
                    while True:
                        nextNode = nextNode.next
                        if nextNode is None:
                            break
                        if isinstance(nextNode, NavigableString):
                            description += nextNode.strip()
                        if isinstance(nextNode, Tag):
                            if nextNode.name == "h2":
                                break
                            description += nextNode.get_text(strip=True).strip()
                print("[" + l + "] description: " + description)

                # get id progress
                progress = soup.find("div", {"id": "lknlksndgg-progress"}).text.strip()
                print("[" + l + "] progress: " + progress)

                # get id completion
                completion = soup.find("div", {"id": "lknlksndgg-completion"}).text.strip()
                print("[" + l + "] completion: " + completion)

                #get id rewards ---- NOT IMPLEMENTED YET
                # rewards
                # print("[" + l + "] rewards: " + rewards)


            print("=========")

print("DONE")
