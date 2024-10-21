import logging
import os
import re
from datetime import datetime, time
from urllib.parse import urlparse, parse_qs

from bson import ObjectId
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from backend import mongo_service
from backend.custom_types import FlightRoute, Flight, PriceRecord

FLIGHT_LIST_XPATH = ("/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/"
                     "flights-summary/div/div[1]/journey-container/journey/flight-list/ry-spinner/div/flight-card-new")


def scrape_flights(scrape_urls: [str]) -> [[str]]:
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    scraped_flights = []

    for scrape_url in scrape_urls:
        try:
            driver.get(scrape_url)

            elements = WebDriverWait(driver, float(os.getenv("WEBDRIVER_TIMEOUT"))).until(
                ec.presence_of_all_elements_located((By.XPATH, FLIGHT_LIST_XPATH))
            )

            scraped_flights.append([remove_unnecessary_data(element.text.split("\n")) for element in elements])

        except TimeoutException as exception:
            logging.error(
                "Could not find the specified element with XPath.\nDeleting the probably no longer existent flight route.\nLink: %s",
                scrape_url, exc_info=exception)
            # handle_flight_not_found(scrape_url) FIXME: Implement this so it takes admin input

    driver.quit()
    return scraped_flights


def handle_flight_not_found(scrape_url: str):
    flight_route_id = mongo_service.find_flight_route_by_scrape_url(scrape_url)
    mongo_service.delete_flight_route(flight_route_id)


def get_scraped_flight_number(scraped_flight_lines: [str]):
    return scraped_flight_lines[2]


def parse_flight_route(scrape_url: str) -> FlightRoute:
    parsed_url = urlparse(scrape_url)
    query_params = parse_qs(parsed_url.query)

    origin_code = query_params.get("originIata", [None])[0]
    destination_code = query_params.get("destinationIata", [None])[0]
    date = query_params.get("dateOut", [None])[0]

    return FlightRoute(
        origin_code=origin_code,
        destination_code=destination_code,
        date=datetime.strptime(date, "%Y-%m-%d").date(),
        scrape_url=scrape_url
    )


def parse_flight(scraped_flight_lines: [str], price_record_ids: [ObjectId]) -> Flight:
    return Flight(
        flight_number=scraped_flight_lines[2],
        departure_time=datetime.strptime(scraped_flight_lines[0], "%H:%M").time(),
        arrival_time=datetime.strptime(scraped_flight_lines[4], "%H:%M").time(),
        price_record_ids=price_record_ids
    )


def parse_price_record(scraped_flight_lines: [str]) -> PriceRecord:
    price_line = scraped_flight_lines[6]
    match = re.match(r"([^\d]+)([\d,]+\.\d+)", price_line)
    if match:
        currency = match.group(1)
        price = float(match.group(2).replace(",", ""))
    else:
        raise ValueError(f"Price line format is incorrect: {price_line}")
    return PriceRecord(
        price=price,
        currency=currency,
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
