import os
import time
import random
import logging

import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType

load_dotenv()

logging.basicConfig(level=logging.INFO)


class Automation:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = None
        self.api_keys = [os.getenv("APIKEY_1"), os.getenv("APIKEY_2")]

    def start_driver(self):

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 '
            'Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/87.0.4280.141 Safari/537.36'
        ]

        # Proxy rotation occurs because api keys are being rotated randomly at the time of proxy url configuration
        api_key = random.choice(self.api_keys)

        # Proxy url configuration
        proxy = f"http://scraperapi:{api_key}@proxy-server.scraperapi.com:8001"
        selenium_proxy = Proxy()
        selenium_proxy.proxy_type = ProxyType.MANUAL
        selenium_proxy.http_proxy = proxy
        selenium_proxy.ssl_proxy = proxy

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        chrome_options.add_argument("--enable-javascript")

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # When the Chrome driver instance is created, the configured proxy is automatically used for all requests
        # made by the browser, resulting in IP rotation
        chrome_options.proxy = selenium_proxy

        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Information about the ip used
        logging.info(f"Proxy used: {proxy}")

        proxies = {
            "http": proxy,
            "https": proxy,
        }
        response = requests.get("http://httpbin.org/ip", proxies=proxies)
        ip_used = response.json()['origin']

        logging.info(f"IP used: {ip_used}")

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def access_site(self):
        self.start_driver()

        try:
            self.driver.get("https://www.ikesaki.com.br/")

            time.sleep(random.uniform(8, 10))

            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            title = soup.find("h2")
            if title:
                print(title.text)

        finally:
            self.stop_driver()


if __name__ == "__main__":
    automation = Automation()
    automation.access_site()
