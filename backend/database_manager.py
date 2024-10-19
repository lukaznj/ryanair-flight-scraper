from bson import ObjectId

from backend import mongo_service
from backend.custom_types import PriceRecord, User, FlightRouteCreationRequest
from backend.mailgun_service import check_for_price_change, send_price_change_emails, prepare_price_changes
from backend.mongo_service import deserialize_price_record
from backend.scrape_engine import scrape_flights, parse_price_record, parse_flight, \
    parse_flight_route, get_scraped_flight_number


def ryanair_url_maker(flight_route_creation_request: FlightRouteCreationRequest) -> str:
    return flight_route_creation_request.url


def create_flight_route(flight_route_creation_request: FlightRouteCreationRequest):
    url = ryanair_url_maker(flight_route_creation_request)
    scraped_flights = scrape_flights([url])[0]

    flight_route = parse_flight_route(url)

    for scraped_flight_lines in scraped_flights:
        price_record = parse_price_record(scraped_flight_lines)
        price_record_id = mongo_service.save_price_record(price_record)

        flight = parse_flight(scraped_flight_lines, [price_record_id])
        flight_id = mongo_service.save_flight(flight)

        flight_route.flight_ids.append(flight_id)

    mongo_service.save_flight_route(flight_route)


def add_price_record(flight_id: ObjectId, price_record: PriceRecord) -> ObjectId:
    if mongo_service.find_by_id("flights", flight_id):
        price_record_id = mongo_service.save_price_record(price_record)
        mongo_service.get_collection("flights").update_one({"_id": ObjectId(flight_id)},
                                                           {"$push": {"price_record_ids": price_record_id}})
        return price_record_id


def update_flight(scraped_flight_lines: [str]) -> ObjectId:
    new_price_record = parse_price_record(scraped_flight_lines)
    flight_number = get_scraped_flight_number(scraped_flight_lines)
    flight_id = mongo_service.get_flight_by_flight_number(flight_number)

    old_price_record_id = mongo_service.get_flight(flight_id)["price_record_ids"][-1]
    old_price_record = mongo_service.find_by_id("price_records", old_price_record_id)

    if not check_for_price_change(old_price_record, new_price_record):  # Fixme: CHANGE THIS TO TRUE
        price_changes = prepare_price_changes(deserialize_price_record(old_price_record), new_price_record,
                                              flight_id)

        send_price_change_emails(price_changes)

    add_price_record(flight_id, new_price_record)
    return flight_id


def create_user(username: str, email: str):
    user = User(username, email)
    user_id = mongo_service.save_user(user)
    return user_id
