import os
import time
import random
import logging

from dotenv import load_dotenv
from selenium import webdriver
from ratelimit import limits, sleep_and_retry
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType


load_dotenv()

logging.basicConfig(level=logging.INFO)


class Automation:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = None
        self.api_keys = [os.getenv("APIKEY_1"), os.getenv("APIKEY_2")]

    def get_driver_ip(self):
        self.driver.get('https://api.ipify.org')
        ip_element = self.driver.find_element(By.TAG_NAME, 'body')
        return ip_element.text

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

        user_data_path = 'C:\\Users\\Backup 01\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument(f'--user-data-dir={user_data_path}')

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        chrome_options.proxy = selenium_proxy

        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver_ip = self.get_driver_ip()
        logging.info(f'Proxy: {proxy}, WebDriver IP: {driver_ip}')

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    @sleep_and_retry
    @limits(calls=1, period=60)
    def login(self):
        self.start_driver()

        try:
            self.driver.get("https://www.webmotors.com.br/login")

            time.sleep(random.uniform(2, 4))

            login_with_chrome_xpath = '//*[@id="app"]/div/div[3]/div[1]/div/div[1]/section[1]/div/button[2]/p'

            login_with_chrome = self.driver.find_element(By.XPATH, login_with_chrome_xpath)
            login_with_chrome.click()
            logging.info("Login realizado com sucesso.")
            time.sleep(20)

        except Exception as e:
            logging.error(f"Erro durante o login: {e}")

        finally:
            self.stop_driver()


if __name__ == "__main__":
    automation = Automation()
    automation.login()
