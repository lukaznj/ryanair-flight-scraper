from database_manager import add_price_record, update_flight
from mongo_service import MongoService
from scrape_engine import scrape_flights, get_scraped_flight_number, parse_price_record


def run(mongo_service: MongoService):
    print("Scraping flights...")
    updated_flights = []
    flight_route_urls = []
    flight_routes_collection = mongo_service.get_collection("flight_routes")

    for flight_route in flight_routes_collection.find():
        flight_route_urls.append(flight_route["scrape_url"])

    scraped_flights = scrape_flights(flight_route_urls)
    for scraped_flight in scraped_flights:
        for scraped_flight_lines in scraped_flight:
            updated_flights.append(update_flight(scraped_flight_lines, mongo_service))

    print("Updated flights: " + str(updated_flights))
