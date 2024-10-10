import logging
import os

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape_webpage(url: str, xpath: str) -> None:
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))

    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)

        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            xpath))
        )
        print(price.text)

    except TimeoutException as exception:
        logging.error("Could not find the element with XPath: %s", xpath, exc_info=exception)

    finally:
        driver.quit()
