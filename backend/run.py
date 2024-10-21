from backend import mongo_service
from backend.system_service import check_flight_route_deprecated
from database_manager import update_flight
from scrape_engine import scrape_flights


def run():
    print("Scraping flights...")
    urls_to_scrape = []
    tracked_flight_routes_ids = mongo_service.get_tracked_flight_routes()
    
    for flight_route_id in tracked_flight_routes_ids:
        if not check_flight_route_deprecated(flight_route_id):
            scrape_url = mongo_service.find_by_id("flight_routes", flight_route_id)["scrape_url"]
            urls_to_scrape.append(scrape_url)

    scraped_flights = scrape_flights(urls_to_scrape)

    for scraped_flight in scraped_flights:
        for scraped_flight_lines in scraped_flight:
            update_flight(scraped_flight_lines)
