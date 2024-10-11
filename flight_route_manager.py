from custom_types import CreateFlightRouteRequest
from mongo_service import MongoService
from scrape_engine import scrape_flights, format_price_record, format_flight, \
    format_flight_route


def ryanair_url_maker(flight_route_request: CreateFlightRouteRequest) -> str:
    # Add logic that uses flight_route_request to create a URL to the Ryanair website to scrape flight data
    return "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-11-01&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=EIN&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-11-01&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=EIN&tpDestinationIata=STN"


def create_flight_route(flight_route_request: CreateFlightRouteRequest, mongo_service: MongoService):
    url = ryanair_url_maker(flight_route_request)
    scraped_flights = scrape_flights(url)

    flight_route = format_flight_route(scraped_flights[0], [])

    for scraped_flight_lines in scraped_flights:
        price_record = format_price_record(scraped_flight_lines)
        price_record_id = mongo_service.save_price_record(price_record)

        flight = format_flight(scraped_flight_lines, [price_record_id])
        flight_id = mongo_service.save_flight(flight)

        flight_route.flight_ids.append(flight_id)

    mongo_service.save_flight_route(flight_route)
