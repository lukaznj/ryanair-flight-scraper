import logging
import os
from datetime import datetime, time

from bson import ObjectId
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from backend.custom_types import FlightRoute, Flight, PriceRecord

FLIGHT_LIST_XPATH = "/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/flight-list/ry-spinner/div/flight-card-new"


def scrape_flights(urls: [str]) -> [[str]]:
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    to_return = []

    try:
        for url in urls:
            driver.get(url)

            elements = WebDriverWait(driver, float(os.getenv("WEBDRIVER_TIMEOUT"))).until(
                ec.presence_of_all_elements_located((By.XPATH, FLIGHT_LIST_XPATH))
            )

            to_return.append([remove_unnecessary_data(element.text.split("\n")) for element in elements])

        return to_return

    except TimeoutException as exception:
        logging.error("Could not find the specified element with XPath: %s", FLIGHT_LIST_XPATH, exc_info=exception)

    finally:
        driver.quit()


def get_scraped_flight_number(scraped_flight_lines: [str]):
    return scraped_flight_lines[2]


def parse_flight_route(scraped_flight_lines: [str], flight_ids: [ObjectId]) -> FlightRoute:
    return FlightRoute(
        origin=scraped_flight_lines[1],
        destination=scraped_flight_lines[5],
        flight_time=parse_flight_time(scraped_flight_lines[3]),
        flight_ids=flight_ids
    )


def parse_flight(scraped_flight_lines: [str], price_record_ids: [ObjectId]) -> Flight:
    return Flight(
        flight_number=scraped_flight_lines[2],
        departure_time=datetime.strptime(scraped_flight_lines[0], "%H:%M").time(),
        arrival_time=datetime.strptime(scraped_flight_lines[4], "%H:%M").time(),
        price_record_ids=price_record_ids
    )


def parse_price_record(scraped_flight_lines: [str]) -> PriceRecord:
    return PriceRecord(
        price=float(scraped_flight_lines[6][1:]),
        currency=scraped_flight_lines[6][0],
        date_time=datetime.now()
    )


def remove_unnecessary_data(scraped_flight_lines: [str]) -> [str]:
    return list(filter(
        lambda
            line: line != "Select" and line != "Ryanair" and "Operated" not in line and "Fare" not in line and "Plus" not in line and "left at this price" not in line,
        scraped_flight_lines))


def parse_flight_time(flight_time_str: str) -> time:
    hours, minutes = 0, 0
    if 'h' in flight_time_str:
        hours = int(flight_time_str.split('h')[0].strip())
        flight_time_str = flight_time_str.split('h')[1].strip()
    if 'm' in flight_time_str:
        minutes = int(flight_time_str.split('m')[0].strip())
    return time(hour=hours, minute=minutes)
