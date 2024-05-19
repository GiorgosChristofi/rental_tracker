import random
import time

import requests
from bs4 import BeautifulSoup
from EmailSender import EmailSender


class pararius_scraper:

    def __init__(self):
        self.es = EmailSender()
        self.url = "https://kamernet.nl/services/api/listing/findlistings"
        self.payload = payload = {
            "pageNo": 1,
            "variant": None,
            "location": {
                "cityName": "Delft",
                "name": "Delft"
            },
            "radiusId": 1,
            "listingTypeIds": [2, 4],
            "maxRentalPriceId": 0,
            "surfaceMinimumId": 2,
            "listingSortOptionId": 1,
            "suitableForGenderIds": [],
            "furnishings": [],
            "availabilityPeriods": [],
            "availableFromDate": None,
            "isBathroomPrivate": None,
            "isToiletPrivate": None,
            "isKitchenPrivate": None,
            "hasInternet": None,
            "suitableForNumberOfPersonsId": None,
            "candidateAge": None,
            "suitableForStatusIds": [],
            "isSmokingInsideAllowed": None,
            "isPetsInsideAllowed": None,
            "roommateMaxNumberId": None,
            "roommateGenderIds": [],
            "ownerTypeIds": [],
            "searchview": 1,
            "rowsPerPage": 18,
            "OpResponse": {
                "Code": 1000,
                "Message": "Operation successful.",
                "HttpStatusCode": 200
            },
            "LogEntryId": None,
            "citySlug": "delft"
        }
        self.headers = {
            "Content-Type": "application/json"
        }
        self.prevLinks = []
        self.read_previous_links()

    def read_previous_links(self):
        with open("pararius.txt", "r") as reader:
            for line in reader:
                self.prevLinks.append(line.strip())

    def check_website(self, proxy):
        proxies = {"https": proxy}
        session = requests.Session()
        session.proxies.update(proxies);

        try:
            session.get("https://www.pararius.com/english")

            time.sleep(random.randint(5, 10))

            source = session.get("https://www.pararius.com/apartments/delft").text

            soup = BeautifulSoup(source, "html.parser")

            #check if it got flagged
            if len(soup.findAll('body', {"id": "fl-captcha"})) != 0:
                print("Got flagged")
                raise RuntimeError("Got flagged")

            h2s = soup.find_all("h2")
            with open('pararius.txt', 'a') as linkFile:
                print("Found " + str(len(h2s)) + " links")
                for h2 in h2s:
                    if not (h2.a is None):
                        link = h2.a['href']
                        if not (link in self.prevLinks) and not link is None:
                            self.prevLinks.append(link)
                            linkFile.write(link + "\n")
                            msg = 'https://www.pararius.com' + link
                            print("Message to send: " + msg)
                            self.es.send_email("New listing", msg)
            session.close()
            return True
        except Exception as e:
            print("Error in pararius")
            print(e)
            session.close()
            return False
