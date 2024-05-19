import random
import time

import EmailSender
import Ikwilhuren
import Kamernet
import Pararius
import ProxyChecker

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
            if pa_res or kn_res or iw_res:
                pc.invalidateProxy(proxy)
            sleepFunct(30, 60)
        except Exception as e:
            print("Error in checking!")
            print(e.__str__())
            pc.invalidateProxy(proxy)
    checkWebsite()


if __name__ == "__main__":
    checkWebsite()
