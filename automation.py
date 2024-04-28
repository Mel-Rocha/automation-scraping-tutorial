import time
import random
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import NoSuchElementException, TimeoutException

logging.basicConfig(level=logging.INFO)


class Automation:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())  # Automatically downloads the version of WebDriver
        # compatible with the version of Chrome
        self.driver = None  # Browser instance that we will control

    def start_driver(self):
        """
        launch the browser
        """

        # What are user_agents: They contain information about the user's browser
        # and operating system, they serve the server to provide content compatible with the user
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        ]

        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
        chrome_options.add_argument(
            f'user-agent={random.choice(user_agents)}')  # Simulate different types of devices and browsers
        chrome_options.add_argument('start-maximized')  # Maximizes the screen to simulate human behavior
        chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        chrome_options.add_argument("--enable-javascript")  # Enables the application to interact with dynamic elements

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)  # Initialization of the browser
        # driver with the service that is responsible for downloading the version of the WebDriver compatible with my
        # browser and with the configuration defined in Options

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  #
        # Removes the indication that the browser is being controlled by automation

    def stop_driver(self):
        """
        The browser/driver instance is terminated when it is no longer needed by the following
        reasons: release of resources, avoid conflicts, because if you want to start a new
        instance and still have the old one running, this can lead to conflicts and cleanup
        session.
        """
        if self.driver:
            self.driver.quit()

    def access_site(self):
        self.start_driver()

        try:
            self.driver.get("https://www.ikesaki.com.br/")

            time.sleep(random.uniform(8, 10))  # Random time.sleeps to simulate real user behavior

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

            def static_page():
                """
                for the static pages prefer bs4
                """
                html_content = self.driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')

                title = soup.find("h2")
                if title:
                    print(title.text)

            static_page()
            dynamic_page()

        finally:
            self.stop_driver()


if __name__ == "__main__":
    automation = Automation()
    automation.access_site()
