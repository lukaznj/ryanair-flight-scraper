import os
from datetime import datetime

from dotenv import load_dotenv

from custom_types import CreateFlightRouteRequest, PriceRecord
from flight_route_manager import create_flight_route, add_price_record
from mongo_service import MongoService
from scrape_engine import scrape_flights

load_dotenv()

if __name__ == "__main__":
    mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))

    flight_route_request = CreateFlightRouteRequest(
        origin="EIN",
        destination="STN",
        date=datetime.strptime("2024-11-01", "%Y-%m-%d")
    )

    # print(scrape_flights(
    #     "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-11-01&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=EIN&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-11-01&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=EIN&tpDestinationIata=STN"))

    add_price_record("6709aeeb69acc732ae1a7d1a", PriceRecord(price=100, currency="€", date_time=datetime.now()),
                     mongo_service)

    # create_flight_route(flight_route_request, mongo_service)
