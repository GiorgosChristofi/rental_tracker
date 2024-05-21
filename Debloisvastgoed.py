from bs4 import BeautifulSoup

from EmailSender import EmailSender
import requests


class deblois_scraper:
    def __init__(self):
        self.es = EmailSender()
        self.prevLinks = []
        self.read_previous_links()
        self.url = "https://www.deblooisvastgoed.nl/huuraanbod/"
        self.querystring = {"filter_city": "Delft", "filter_min_price": "", "filter_max_price": "",
                            "filter_interior": "", "filter_surface": ""}

    def read_previous_links(self):
        with open("deblois.txt", "r") as reader:
            for line in reader:
                self.prevLinks.append(line.strip())

    def check_website(self, proxy):
        try:
            print("Checking deblois")
            proxies = {
                "https": proxy,
                "http": proxy,
                "socksProxy": proxy
            }
            r = requests.request("POST", self.url, params=self.querystring, proxies=proxies)
            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", {"class": "residence"})
            print("Found " + str(len(divs)) + " links in deblois")
            for div in divs:
                if div is not None:
                    link = div.a['href']
                    if link not in self.prevLinks:
                        self.es.send_email("New listing in debloisvastgoed!", link)
                        self.prevLinks.append(link)
                        with open('deblois.txt', 'a') as linkFile:
                            linkFile.write(link + "\n")
            return True
        except Exception as e:
            print("Error in deblois")
            print(e)
            return False
