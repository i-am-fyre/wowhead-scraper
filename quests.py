#!/usr/bin/env python3.7

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

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
                with open(c + '_output_' + l + '.csv', mode='a') as csv_output:
                    csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n',)

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

                    # get id title
                    title = soup.find("h1", {"class": "heading-size-1"}).text
                    print("[" + l + "] title: " + title)

                    # get id details
                    details = ""
                    for d in soup.select('h2.heading-size-3')[0]:
                        nextNode = d
                        while True:
                            nextNode = nextNode.next
                            if nextNode is None:
                                break
                            if isinstance(nextNode, NavigableString):
                                details += nextNode.strip()
                            if isinstance(nextNode, Tag):
                                if nextNode.name == "h2":
                                    break
                                details += nextNode.get_text(strip=True).strip()
                    print("[" + l + "] details: " + details)

                    # get id objectives
                    objectives = soup.find("div", {"class": "block-block-bg is-btf"}).next_sibling.strip()
                    print("[" + l + "] objectives: " + objectives)

                    # get id offer reward text
                    offerRewardText = soup.find("div", {"id": "lknlksndgg-completion"}).text.strip()
                    print("[" + l + "] offerRewardText: " + offerRewardText)

                    # get id requestItemsText
                    try:
                        requestItemsText = soup.find("div", {"id": "lknlksndgg-progress"}).text.strip()
                    except:
                        requestItemsText = ""
                    print("[" + l + "] requestItemsText: " + requestItemsText)

                    # get id end text ---- NOT IMPLEMENTED YET
                    endText = ""
                    print("[" + l + "] endText: " + endText)

                    # get id objectiveText1 ---- NOT IMPLEMENTED YET
                    objectiveText1 = ""
                    print("[" + l + "] objectiveText1: " + objectiveText1)

                    # get id objectiveText2 ---- NOT IMPLEMENTED YET
                    objectiveText2 = ""
                    print("[" + l + "] objectiveText2: " + objectiveText2)

                    # get id objectiveText3 ---- NOT IMPLEMENTED YET
                    objectiveText3 = ""
                    print("[" + l + "] objectiveText3: " + objectiveText3)

                    # get id objectiveText4 ---- NOT IMPLEMENTED YET
                    objectiveText4 = ""
                    print("[" + l + "] objectiveText4: " + objectiveText4)

                    #write to csv
                    csv_writer.writerow([i, title, details, objectives, offerRewardText, requestItemsText, endText, objectiveText1, objectiveText2, objectiveText3, objectiveText4])
            print("=========")

print("DONE"),
