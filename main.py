import asyncio
import threading

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import functools
import typing
import random
import EmailSender
import ProxyChecker
import Kamernet
import Pararius
import Ikwilhuren

errored_proxies = []
valid_proxies = []


es = EmailSender.EmailSender()
pc = ProxyChecker.ProxyChecker()
kn = Kamernet.kamernet_scraper()
pa = Pararius.pararius_scraper()
iw = Ikwilhuren.ikwilhuren_scraper()

def sleepFunct(lower, upper):
    duration = random.randint(lower, upper)
    time.sleep(duration)

def checkWebsite():
    print("Checking")
    proxy = pc.getValidProxy()
    print(proxy)
    if proxy is not None:
        try:
            iw_res = iw.check_website(proxy)
            kn_res = kn.check_website(proxy)
            pa_res = pa.check_website(proxy)
            if (pa_res or kn_res or iw_res):
                pc.invalidateProxy(proxy)
            sleepFunct(30,60)
        except Exception as e:
            print("Error in checking!")
            print(e.__str__())
            pc.invalidateProxy(proxy)
    checkWebsite()

if __name__ == "__main__":
    es.send_email("test", "test")
    checkWebsite()

    # page = get_driver(proxy.split(":")[0], proxy.split(":")[1])
    # source = ""
    # error = False
    # try:
    #
    #     check_ikwilhuren(page)
    # except Exception as e:
    #     print(e)
    #     error = True
    #     errored_proxies.append(proxy)
    #     if proxy in valid_proxies:
    #         valid_proxies.remove(proxy)
    # finally:
    #     page.close()
    #     page.quit()
    #     if not error:
    #         sleepFunct()

#
# def check_pararius(proxy):
#     # page.get("https://www.pararius.com/apartments/delft")
#     # myElem = WebDriverWait(page, 100).until(
#     #     EC.presence_of_element_located((By.CLASS_NAME, 'listing-search-item__title')))
#
#     proxies = {"https": proxy}
#     session = requests.Session()
#     session.proxies.update(proxies);
#
#     while True:
#         session.get("https://www.pararius.com/english")
#
#         sleepFunct(5, 10)
#
#         source = session.get("https://www.pararius.com/apartments/delft").text
#
#         soup = BeautifulSoup(source, "html.parser")
#
#         #check if it got flagged
#         if len(soup.findAll('body', {"id":"fl-captcha"})) != 0:
#             print("Got flagged")
#             raise RuntimeError("Got flagged")
#
#
#         h2s = soup.find_all("h2")
#         linkFile = open('pararius.txt', 'a')
#         print("Found " + str(len(h2s)) + " links")
#         for h2 in h2s:
#             if not (h2.a is None):
#                 link = h2.a['href']
#                 if not (link in parariusLinks) and not link is None:
#                     parariusLinks.append(link)
#                     linkFile.write(link + "\n")
#                     msg = 'https://www.pararius.com' + link
#                     print("Message to send: " + msg)
#                     es.send_email("New listing", msg)
#         linkFile.close()
#
#
#
#
# def check_ikwilhuren(driver):
#     driver.get("https://ikwilhuren.nu/aanbod/")
#     selection = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-selection')))
#     selection.send_keys(Keys.ENTER)
#     textbox = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field')))
#     textbox.send_keys('Delft')
#     WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-results__option--highlighted')))
#     textbox.send_keys(Keys.ENTER)
#     WebDriverWait(driver, 100).until(EC.staleness_of(textbox))
#     time.sleep(10)
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     cards = soup.findAll("span", {"class": "card-title h5 text-secondary mb-0"})
#     linkFile = open('ikwilhuren.txt', 'a')
#     print("Found " + str(len(cards)) + " links in ikwilhuren")
#     for card in cards:
#         if (card is not None and card.a is not None):
#             link = card.a['href']
#             msg = 'https://ikwilhuren.nu' + link
#             print("Found: " + msg)
#             if link not in ikwilhurenLinks:
#                 linkFile.write(link + "\n")
#
#                 es.send_email("New listing in ikwilhuren!", msg)
#     linkFile.close()

# def getProxies():
#     r = requests.get(
#         "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all")
#     text = r.text
#     proxies = text.split("\r\n")
#     return proxies
#
# def findValidProxy():
#     if len(valid_proxies) > 0:
#         return valid_proxies[0]
#
#     proxies = getProxies()
#     currentProxyIndex = 0
#     while currentProxyIndex < len(proxies):
#         currentProxy = proxies[currentProxyIndex]
#         res = validate_proxy(currentProxy)
#         if res:
#             print("Valid Proxy Found!")
#             valid_proxies.append(currentProxy)
#             return currentProxy
#         else:
#             print("Invalid Proxy")
#             print(currentProxy)
#             currentProxyIndex += 1
#     return None
#
#
# def get_driver(proxy_host, proxy_port):
#     # Set up Firefox options with proxy settings
#     proxy_settings = Proxy({
#         'proxyType': ProxyType.MANUAL,
#         'socksProxy': f"{proxy_host}:{proxy_port}",
#         'sslProxy': f"{proxy_host}:{proxy_port}",
#         'httpProxy': f"{proxy_host}:{proxy_port}",
#         'socksVersion': 5  # This specifies that the proxy is SOCKS5
#     })
#
#     options = Options()
#     options.proxy = proxy_settings
#     options.add_argument('--headless')
#
#     # Create a Firefox WebDriver instance with the specified options
#     driver = webdriver.Firefox(options=options)
#
#     return driver
#
#
#
# def validate_proxy(proxy):
#     if proxy in errored_proxies:
#         return False
#     print("Checking proxy: " + proxy)
#     proxies = {"https": proxy}
#     try:
#         r = requests.get("https://www.duckduckgo.com/", proxies=proxies)
#         if (r.status_code == 200):
#
#             print("Valid")
#             return True
#         print("Invalid " + r.status_code)
#         return False
#     except Exception as e:
#         print("Invalid  " + e.__str__())
#         return False



