import logging
import os
from datetime import datetime

from bson import ObjectId
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from custom_types import FlightRoute, Flight, PriceRecord

FLIGHT_LIST_XPATH = "/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/flight-list/ry-spinner/div/flight-card-new"


def scrape_flights(url: str) -> [[str]]:
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    # Add Chrome option --headless to run Chrome in headless mode
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)

        elements = WebDriverWait(driver, float(os.getenv("WEBDRIVER_TIMEOUT"))).until(
            ec.presence_of_all_elements_located((By.XPATH, FLIGHT_LIST_XPATH))
        )
        return [remove_unnecessary_data(element.text.split("\n")) for element in elements]

    except TimeoutException as exception:
        logging.error("Could not find the specified element with XPath: %s", FLIGHT_LIST_XPATH, exc_info=exception)

    finally:
        driver.quit()


def format_flight_route(scraped_flight_lines: [str], flight_ids: [ObjectId]) -> FlightRoute:
    return FlightRoute(
        origin=scraped_flight_lines[1],
        destination=scraped_flight_lines[5],
        flight_ids=flight_ids
    )


def format_flight(scraped_flight_lines: [str], price_record_ids: [ObjectId]) -> Flight:
    return Flight(
        flight_number=scraped_flight_lines[2],
        departure_time=datetime.strptime(scraped_flight_lines[0], "%H:%M").time(),
        arrival_time=datetime.strptime(scraped_flight_lines[4], "%H:%M").time(),
        price_record_ids=price_record_ids
    )


def format_price_record(scraped_flight_lines: [str]) -> PriceRecord:
    return PriceRecord(
        price=float(scraped_flight_lines[6][1:]),
        currency=scraped_flight_lines[6][0],
        date_time=datetime.now()
    )


def remove_unnecessary_data(scraped_flight_lines: [str]) -> [str]:
    return list(filter(
        lambda
            line: line != "Select" and line != "Ryanair" and "Fare" not in line and "Plus" not in line and "left at this price" not in line,
        scraped_flight_lines))
