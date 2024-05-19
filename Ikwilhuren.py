import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from EmailSender import EmailSender


class ikwilhuren_scraper:

    def __init__(self):
        self.es = EmailSender()
        self.prevLinks = []
        self.read_previous_links()

    def read_previous_links(self):
        with open("ikwilhuren.txt", "r") as reader:
            for line in reader:
                self.prevLinks.append(line.strip())

    def check_website(self, proxy):
        try:
            driver = self.get_driver(proxy.split(":")[0], proxy.split(":")[1])

            driver.get("https://ikwilhuren.nu/aanbod/")
            selection = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'select2-selection')))
            selection.send_keys(Keys.ENTER)
            textbox = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
            textbox.send_keys('Delft')
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'select2-results__option--highlighted')))
            textbox.send_keys(Keys.ENTER)
            WebDriverWait(driver, 100).until(EC.staleness_of(textbox))
            time.sleep(10)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()
            cards = soup.findAll("span", {"class": "card-title h5 text-secondary mb-0"})
            with open('ikwilhuren.txt', 'a') as linkFile:
                print("Found " + str(len(cards)) + " links in ikwilhuren")

                for card in cards:
                    if card is not None and card.a is not None:
                        link = card.a['href']
                        msg = 'https://ikwilhuren.nu' + link
                        print("Found: " + msg)
                        if link not in self.prevLinks and 'delft' in link:
                            linkFile.write(link + "\n")
                            self.es.send_email("New listing in ikwilhuren!", msg)
                            self.prevLinks.append(link)
                    return True
        except Exception as e:
            print("Error in ikwilhuren")
            print(e.__str__())
            return False

    def get_driver(self, proxy_host, proxy_port):
        # Set up Firefox options with proxy settings
        proxy_settings = Proxy({
            'proxyType': ProxyType.MANUAL,
            'socksProxy': f"{proxy_host}:{proxy_port}",
            'sslProxy': f"{proxy_host}:{proxy_port}",
            'httpProxy': f"{proxy_host}:{proxy_port}",
            'socksVersion': 5  # This specifies that the proxy is SOCKS5
        })

        options = Options()
        options.proxy = proxy_settings
        options.add_argument('--headless')

        # Create a Firefox WebDriver instance with the specified options
        driver = webdriver.Firefox(options=options)

        return driver
