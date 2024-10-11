import logging
import os
from datetime import datetime

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from custom_types import FlightRoute, Flight, PriceRecord, PriceRecordUpdate

FLIGHT_LIST_XPATH = "/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/flight-list/ry-spinner/div/flight-card-new"


def scrape_flight_list(url: str) -> [str]:
    """
    Scrapes the flight list from the given URL.

    Args:
        url (str): The URL to scrape the flight list from.

    Returns:
        list of str: A list of strings, each representing a flight's details.
    """
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    # Add Chrome option --headless to run Chrome in headless mode
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)

        elements = WebDriverWait(driver, float(os.getenv("WEBDRIVER_TIMEOUT"))).until(
            ec.presence_of_all_elements_located((By.XPATH, FLIGHT_LIST_XPATH))
        )
        return [element.text for element in elements]

    except TimeoutException as exception:
        logging.error("Could not find the specified element with XPath: %s", FLIGHT_LIST_XPATH, exc_info=exception)

    finally:
        driver.quit()


def format_new_flight_route(flights_data: [str]) -> FlightRoute:
    lines = flights_data[0].split("\n")
    formated_flight_route = FlightRoute(
        origin=lines[2],
        destination=lines[6],
        flights=[]
    )

    for flight_data in flights_data:
        lines = flight_data.split("\n")
        flight = Flight(
            flight_number=lines[3],
            departure_time=datetime.strptime(lines[1], "%H:%M").time(),
            arrival_time=datetime.strptime(lines[5], "%H:%M").time(),
            price_record=[PriceRecord(
                price=float(lines[9][1:]),
                currency=lines[9][0],
                date_time=datetime.now()
            )]
        )
        formated_flight_route.flights.append(flight)

    return formated_flight_route


def format_new_price_records(flights_data: [str]) -> [PriceRecordUpdate]:
    price_records_updates = []
    for flight_data in flights_data:
        lines = flight_data.split("\n")
        price_record_update = PriceRecordUpdate(
            flight_number=lines[3],
            price_record=PriceRecord(
                price=float(lines[9][1:]),
                currency=lines[9][0],
                date_time=datetime.now()
            )
        )
        price_records_updates.append(price_record_update)

    return price_records_updates
