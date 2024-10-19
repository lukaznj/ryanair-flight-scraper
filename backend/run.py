from backend import mongo_service
from database_manager import update_flight
from scrape_engine import scrape_flights


def run():
    print("Scraping flights...")
    flight_route_urls = []
    flight_routes_collection = mongo_service.get_collection("flight_routes")

    for flight_route in flight_routes_collection.find():
        flight_route_urls.append(flight_route["scrape_url"])

    scraped_flights = scrape_flights(flight_route_urls)
    
    for scraped_flight in scraped_flights:
        for scraped_flight_lines in scraped_flight:
            update_flight(scraped_flight_lines)
