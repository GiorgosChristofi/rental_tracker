import time

import requests
import threading

class ProxyChecker:
    errored_proxies = []
    valid_proxies = []
    currentlyChecking = False
    current_proxy_index = 0
    proxies = []

    def getProxies(self):
        r = requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=1000&country=all&ssl=all&anonymity=all")
        text = r.text
        proxies = text.split("\r\n")
        return proxies

    def getNextProxies(self, amount):
        if self.current_proxy_index >= len(self.proxies) or len(self.proxies) == 0:
            self.current_proxy_index = 0
            self.proxies = self.getProxies()
        count = 0
        return_proxies = []
        while (self.current_proxy_index < len(self.proxies) and count < amount):
            return_proxies.append(self.proxies[self.current_proxy_index])
            self.current_proxy_index += 1
            count+=1

        return return_proxies

    def getValidProxy(self):
        if len(self.valid_proxies) == 0:
            proxies = self.getProxies()
            self.checkProxyList(self.getNextProxies(20))
            time.sleep(5)
            return self.getValidProxy()
        else:
            return self.valid_proxies[0]

    def invalidateProxy(self, proxy):
        self.valid_proxies.remove(proxy)
        self.errored_proxies.append(proxy)

    def checkProxyList(self, proxies):
        for proxy in proxies:
            t1 = threading.Thread(target=self.validate_proxy, args=(proxy,))
            t1.start()

    def validate_proxy(self, proxy):
        if proxy in self.errored_proxies:
            return
        proxies = {
            "https": proxy,
            "http": proxy,
            "socksProxy": proxy
        }
        try:
            r = requests.get("https://www.duckduckgo.com/", proxies=proxies)
            if (r.status_code == 200):

                print("Valid")
                self.valid_proxies.append(proxy)
                return
            self.errored_proxies.append(proxy)
            return
        except Exception as e:
            self.errored_proxies.append(proxy)
            return