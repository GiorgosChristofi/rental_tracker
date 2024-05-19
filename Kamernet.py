import random
import time

import requests
from EmailSender import EmailSender


class kamernet_scraper:

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
        self.prevIds = []
        self.read_prev_ids()

    def read_prev_ids(self):
        with open("kamernet.txt", "r") as reader:
            for line in reader:
                self.prevIds.append(line.strip())

    def check_website(self, proxy):
        print("Checking...")
        try:
            proxies = {
                "https": proxy,
                "http": proxy,
                "socksProxy": proxy
            }
            response = requests.request("POST", self.url, json=self.payload, headers=self.headers, proxies=proxies)
            data = response.json()
            print("Found " + str(len(data["listings"])) + " listings")
            for listing in data["listings"]:
                if str(listing["listingId"]) not in self.prevIds:
                    self.prevIds.append(str(listing["listingId"]))
                    self.es.send_email("New listing",
                                       "NEW LISTING https://kamernet.nl/en/for-rent/studio-delft/c.-fockstraat/studio-" + str(
                                           listing["listingId"]))
                    with open("kamernet.txt", "a") as writer:
                        writer.write(str(listing["listingId"]) + "\n")
            return True
        except Exception as e:
            print("Error in response")
            print(e)
            return False
