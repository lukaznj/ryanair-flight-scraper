from bson import ObjectId

from custom_types import CreateFlightRouteRequest, PriceRecord, Flight, User
from mailgun_service import send_price_change_email
from mongo_service import MongoService
from scrape_engine import scrape_flights, parse_price_record, parse_flight, \
    parse_flight_route, get_scraped_flight_number


# def ryanair_url_maker(flight_route_request: CreateFlightRouteRequest) -> str:
#     # Add logic that uses flight_route_request to create a URL to the Ryanair website to scrape flight data
#     return "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-11-01&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=EIN&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-11-01&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=EIN&tpDestinationIata=STN"

def ryanair_url_maker(url: str) -> str:
    return url


def create_flight_route(flight_route_request: CreateFlightRouteRequest, mongo_service: MongoService):
    url = ryanair_url_maker(flight_route_request)
    scraped_flights = scrape_flights([url])[0]

    flight_route = parse_flight_route(scraped_flights[0], [])
    flight_route.scrape_url = url

    for scraped_flight_lines in scraped_flights:
        price_record = parse_price_record(scraped_flight_lines)
        price_record_id = mongo_service.save_price_record(price_record)

        flight = parse_flight(scraped_flight_lines, [price_record_id])
        flight_id = mongo_service.save_flight(flight)

        flight_route.flight_ids.append(flight_id)

    mongo_service.save_flight_route(flight_route)


def add_price_record(flight_id: ObjectId, price_record: PriceRecord, mongo_service: MongoService) -> ObjectId:
    if mongo_service.find_by_id("flights", flight_id):
        price_record_id = mongo_service.save_price_record(price_record)
        mongo_service.get_collection("flights").update_one({"_id": ObjectId(flight_id)},
                                                           {"$push": {"price_record_ids": price_record_id}})
        return price_record_id


def update_flight(scraped_flight_lines: [str], mongo_service: MongoService) -> ObjectId:
    new_price_record = parse_price_record(scraped_flight_lines)
    flight_number = get_scraped_flight_number(scraped_flight_lines)
    flight_id = mongo_service.get_flight_by_flight_number(flight_number)
    add_price_record(flight_id, new_price_record, mongo_service)

    dict_price_record = mongo_service.find_by_id("price_records",
                                                 mongo_service.get_flight(flight_id)["price_record_ids"][-1])
    check_for_price_change(dict_price_record, new_price_record)

    return flight_id

def create_user(email: str, mongo_service: MongoService):
    user = User(email)
    user_id = mongo_service.save_user(user)
    return user_id

def check_for_price_change(old_price_record: dict, new_price_record: PriceRecord) -> bool:
    if old_price_record["price"] == new_price_record.price:
        send_price_change_email(old_price_record, new_price_record)
        return True
    return False
