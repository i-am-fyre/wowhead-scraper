#!/usr/bin/env python3.7

########## TO-DO ###########
    #formatting to MaNGOS database style
    # -- Will need to format the quotation marks properly so that they don't break something.

import re
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv

category = ["quest"]
language = ["en", "de","es","fr","it","pt","ru","ko","cn"]
id_start = 1
id_end = 1000

for c in category:
    for i in range (id_start,id_end+1):
        # first, check if id exists
        test_url="https://classic.wowhead.com/"+c+"="+str(i)
        test_page = requests.get(test_url)
        test_soup = BeautifulSoup(test_page.content, 'html.parser')

        if test_soup.find("h1", {"class": "heading-size-1"}).text not in ["Quests", "<UNUSED>"]:
            print("URL: https://classic.wowhead.com/"+c+"="+str(i))
            #second, pull translations
            for li, l in enumerate(language):
                gender_phrases = ["succubus/infernal", "he/she", "priest/priestess", "boy/girl", "lad/lass", "son/daughter", "brother/sister", "brudda/sista", "poppy/mama", "himself/herself", "man/lady", "him/her", "his/her", "sons/daughters", "boys/girls", "brothers/sisters","handsome/pretty", "good sir/my lady", "male/female", "sir/madam", "buddy/lady", "man/woman", "men/women", "sir/miss", "fella/lady", "sir/ma'am", "himself/herself", "dad/mom", "father/mother", "laddy/lassy", "lad/missy", "king/queen", "Mr./Ms.", "fellow/sister", "mister/missy", "mister/miss", "hero/heroine", "grizzled/tough", "sonny/missy", "Mr./Miss", "hot stuff/girly", "boyo/girly", "man/sweetheart", "lord/lady", "my son/my daughter", "man/strong", "buddy/lassy", "guy/lady", "tough-guy/hotshot", "good lad/doll", "pal/lass", "brother/miss", "friend/missy", "daddy/mama", "sonny/lass", "prince/princess", "boy/beautiful flower", "hunter/huntress", "big arms/funny hair", "Hey there, handsome! I've had my eye on those big, beefy biceps ever since you stepped into town./What're you looking at, ugly? I've seen you walking around Razor Hill, trying to steal MY men from me!", "Thanks sweetie!: Don't ask why, just get to it!", "Hey handsome, welcome back! You wouldn't mind running another errand, would you? I'd be EVER so grateful.../You! Stop right there, you tramp! I'm not finished with you yet.", "See you soon, beefcake!/Get cracking, missy!", "Oh, sweetie, I just remembered!/Sorry if I've been mean to you. Sometimes I get a little jealous when other women come into town, as I'm a little insecure about my appearance.", "What, we can't see other people?/Thanks.", "buddy/gorgeous","he's/she's", "SWASHBUCKLING HERO/BREATHTAKING HEROINE", "gentleman/lady", "friend/young lady", "Mr./Miss", "boys/three", "Drinkin' ale/Holdin' hands", "Sumi and Tumi missed you, you should say hi after your lesson/I have heard tales of your adventures, sounds like you have been busy", "Jackson/Princess", "waiter/watress", "boyo/girlie", "mon/sis", "Hey there cutie, you looking for a ride to Grom'gol? I hear it gets mighty steamy down in those jungles, maybe I could join you for a short vacation, show you a real jungle cat./Come, take a trip to the wonderful, gorgeous, tropical jungles of Stranglethorn. That's right, you too can be spending your time sunbathing by the crystal blue waters while I stand here in this unbearable heat with nothing to look at but my brother Frezza all day! Enjoy your trip!", "noble sir/gentle lady", "fella/lady", "Good job!/We should get t ogether for drinks sometime, what do you say?", "man!/gorgeous!", "see you around./Ihope we get to continue to do so.", "boy/lovely", "son/young lady", "boyo/girly", "go out some place for dinnger?/get together for a girl's night?", "man/chicky", "dude/dudette", "sir/madame", "pal/sugar", "buddy/ma'am", "sir/dame", "bug guy/bunny", "champ/lady", "man/kitten", "master/mistress", "bud/lady", "bud/girlie", "dude/toots", "babe/hon", "Candy/Chip", "man/babe", "skilled/lovely", "brave/fair", "handsome/gorgeous", "sugar/scumbag", "scrub/trash", "patriarch: matriarch", "Mortal/mortal", "sweetie/girl", "iskal/searched", "master/madam", "I see that look in your eyes, do not think I will tolerate any insolence. Thrall himself has declared the Hordes females to be on equal footing with you men. Disrespect me in the slightest, and you will know true pain./I'm happy to have met you. Thrall will be glad to know that more females like you and I are taking the initiative to push forward in the Barrens.", "hot stuff/girly", "to leave/set off", "ot it/found it", "sam/yourself", "guy/damsel", "Heard/Heard", "ser/ma'am", "mother/damsel", "friend/girlfriend", "sudar/ma'am", "yunosh/damsel", "Hi, handsome! Want to ride in Grom'gol? Down there, in the jungle, they say it's hot ... But I’d even make you company, I showed you a real reed cat .../Hey, beauty, do you want to visit the wonderful, luxurious tropical jungle of Stranglethorn Valley? Sunbathe on the shores of crystal clear lakes while I'm soaring in the heat in the company of my brother Freza? In general, have a nice flight !", "moy/mine", "b/sister", "Sumi and Tumi miss you, stop by after the lesson: I heard something about your adventures, it looks like you haven’t wasted your time./Well, let's see what you managed to learn during this time.", "gone/gone", "such a hero/such a heroine", "uncle/aunt", "sam/itself", "yuny/young", "sam/yourself", "dear young man/dear girl", "parent/girl", "ranhen/wounded", "too/noticed", "healthy/wide in the bone", "my friend/dear", "sam/myself", "kind lord/kind lady", "brave guy", "Mr. Lord/Madam", "yunosh/girl", "my friend/wanderer", "investigated/examined", "master/mistress", "messed up/a bunch of bombers", "trade magnate/trade mogul", "trading prince/trading princess", "so experienced/so cute", "fella/lady", "soldier/hon", "man/honey", "man/sweetheart", "ya/yer", "fellow/gal", "Milord/Milady", "da-da/ma-ma", "flyboy/flygirl", "magister/magistrix", "how's it hangin?/you look pretty", "manly/womanly", "dearest/dear", "pal/gal", "bub/lady", "Right away", "sir/Right away ma'am", "Sir, yes sir", "Ma'am, yes ma'am", "sea giant/harpy", "you/a pretty little thing like you", "bub/toots", "sweet-thing/lady", "sister/brother", "mister/sister", "handsome/lady", "boyfriend's/girlfriend's", "daddy/pie", "mish/mishter", "fisherman/fisherwoman", "chief/sweetie", "Hey there, handsome. You want to go somewhere after this?  Just you and me?/Back off, skank. I'm trying to put out a vibe here, and you're ruining it.", "Hey there, stranger. I'd brawl with you any day of the week. And I promise you, it'll last longer than 2 minutes. <Helga winks disarmingly.>;I saw you making eyes at Harr back there. That tauren is MINE. Why don't you drag your ugly, gold-digging face to another blimp?"]
                for gp in gender_phrases:
                    if gp.lower() in test_soup.text.lower():
                        # because of the numerous possibilities of gender phrasing, for now we will put all of the quests with any of these tags into a csv for manual review.
                        filename = c + '_manual_checks_required_' + l + '_test.csv'
                        break
                    else:
                        filename = c + '_output_' + l + '_test.csv'

                with open(filename, mode='a') as csv_output:
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
                    try:
                        title = soup.find("h1", {"class": "heading-size-1"}).text.strip()
                    except:
                        title = ""
                    print("[" + l + "] title: " + title)

                    # get id details
                    try:
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
                                    if nextNode.name == "h2" or nextNode.name == "table":
                                        break
                                    details += nextNode.get_text(strip=True).strip()
                    except:
                        details = ""
                    details = re.sub(r'([.?!])([a-zA-Z])', r'\1$B$B\2', details)
                    print("[" + l + "] details: " + details)

                    # get id objectives
                    try:
                        objectives = soup.find("div", {"class": "block-block-bg is-btf"}).next_sibling.strip()
                    except:
                        objectives = ""
                    objectives = re.sub(r'([.?!])([a-zA-Z])', r'\1$B$B\2', objectives)
                    print("[" + l + "] objectives: " + objectives)

                    # get id offer reward text
                    try:
                        offerRewardText = soup.find("div", {"id": "lknlksndgg-completion"}).text.strip()
                    except:
                        offerRewardText = ""
                    offerRewardText = re.sub(r'([.?!])([a-zA-Z])', r'\1$B$B\2', offerRewardText)
                    print("[" + l + "] offerRewardText: " + offerRewardText)

                    # get id requestItemsText
                    try:
                        requestItemsText = soup.find("div", {"id": "lknlksndgg-progress"}).text.strip()
                    except:
                        requestItemsText = ""
                    print("[" + l + "] requestItemsText: " + requestItemsText)

                    # get id end text  --   NOT IMPLEMENTED
                    try:
                        endText = "NOT IMPLEMENTED"
                    except:
                        endText = "NOT IMPLEMENTED"
                    print("[" + l + "] endText: " + endText)

                    # get id objectiveText1
                    try:
                        objectiveText1 = soup.find("table", {"class": "iconlist"}).select("tr")[0].text.strip()
                    except:
                        objectiveText1 = ""
                    print("[" + l + "] objectiveText1: " + str(objectiveText1))

                    # get id objectiveText2
                    try:
                        objectiveText2 = soup.find("table", {"class": "iconlist"}).select("tr")[1].text.strip()
                    except:
                        objectiveText2 = ""
                    print("[" + l + "] objectiveText2: " + str(objectiveText2))

                    # get id objectiveText3
                    try:
                        objectiveText3 = soup.find("table", {"class": "iconlist"}).select("tr")[2].text.strip()
                    except:
                        objectiveText3 = ""
                    print("[" + l + "] objectiveText3: " + str(objectiveText3))

                    # get id objectiveText4
                    try:
                        objectiveText4 = soup.find("table", {"class": "iconlist"}).select("tr")[3].text.strip()
                    except:
                        objectiveText4 = ""
                    print("[" + l + "] objectiveText4: " + str(objectiveText4))

                                    # English, German, Spanish, French, Italian, Portuquese, Russian, Korean, Chinese
                    wowhead_format = [["<name>", "<Name>", "<nombre>", "<nom>", "<name_it>", "<name_pt>", "<name_ru>", "<name_ko>", "<name_cn>"], 
                                      ["<class>", "<Klasse>", "<clase>", "<classe>", "<class_it>", "<class_pt>", "<class_ru>", "<class_ko>", "<class_cn>"],
                                      ["<race>", "<Volk>", "<raza>", "<race>", "<race>", "<race>", "<race>", "<race>", "<race>"]]
                    mangos_format = ["$N", "$C", "$R"]
                    for index, item in enumerate(wowhead_format):
                        title = title.replace(item[li],mangos_format[index])
                        details = details.replace(item[li],mangos_format[index])
                        objectives = details.replace(item[li],mangos_format[index])
                        offerRewardText = offerRewardText.replace(item[li],mangos_format[index])
                        requestItemsText = requestItemsText.replace(item[li],mangos_format[index])

                    #write to csv
                    csv_writer.writerow([i, title, details, objectives, offerRewardText, requestItemsText, endText, objectiveText1, objectiveText2, objectiveText3, objectiveText4])
                    csv_output.close()

                    print(soup.find("div", {"id": "lknlksndgg-completion"}).text)
            print("=========")
print("DONE")
