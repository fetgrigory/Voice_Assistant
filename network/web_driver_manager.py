'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
# Installing the necessary libraries
import logging
import fake_useragent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class WebDriverManager:
    """AI is creating summary for
    """

    def setup_driver(self):
        """AI is creating summary for setup_driver

        Returns:
            [type]: [description]
        """
        # Set up Selenium WebDriver with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument(f'--user-agent={fake_useragent.UserAgent().random}')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        return driver
