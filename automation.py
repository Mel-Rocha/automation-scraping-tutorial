import os
import time
import random
import logging

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Keys
from ratelimit import limits, sleep_and_retry
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common import TimeoutException, NoSuchElementException


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

        api_key = random.choice(self.api_keys)

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

        chrome_options.proxy = selenium_proxy

        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    @sleep_and_retry
    @limits(calls=1, period=60)
    def access_site(self):
        self.start_driver()

        try:
            self.driver.get("https://www.ikesaki.com.br/")

            time.sleep(random.uniform(8, 10))

            def dynamic_page():
                """
                To interact with elements that are dynamically loaded or modified
                with JavaScript prefer to use selenium. Example of use:
                clicking buttons, filling out forms, waiting for JavaScript to load.
                """

                try:
                    search_box_xpath = '//*[@id="downshift-0-input"]'
                    search_box = self.driver.find_element('xpath', search_box_xpath)
                    search_box.send_keys("Pesquisa", Keys.ENTER)
                    time.sleep(5)

                except TimeoutException as e:
                    print(f"Erro ao clicar no elemento: Tempo de execução limite {e}")
                    logging.error("O elemento foi encontrado, mas não se tornou visivel dentro do tempo limite.")
                except NoSuchElementException as e:
                    print(f"Erro ao clicar no elemento: Elemento não encontrado {e}.")
                    logging.error("O elemento não foi encontrado.")

            dynamic_page()

        finally:
            self.stop_driver()


if __name__ == "__main__":
    automation = Automation()
    automation.access_site()
