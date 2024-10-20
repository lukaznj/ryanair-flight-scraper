from bson import ObjectId

from backend import mongo_service
from backend.custom_types import FlightRouteCreationRequest
from backend.database_manager import create_flight_route


def user_exists(email: str) -> bool:
    if mongo_service.find_user_by_email(email) is None:
        return False
    return True


def user_create_flight_route(scrape_url: str, user_id: ObjectId) -> bool:
    if mongo_service.find_flight_route_by_scrape_url(scrape_url):
        flight_route_id = mongo_service.find_flight_route_by_scrape_url(scrape_url)
        mongo_service.add_flight_route_to_user(user_id, flight_route_id)
        return True
    flight_route_id = create_flight_route(FlightRouteCreationRequest(scrape_url))
    mongo_service.add_flight_route_to_user(user_id, flight_route_id)


def user_already_tracking_flight(scrape_url: str, user_id: ObjectId) -> bool:
    flight_route_id = mongo_service.find_flight_route_by_scrape_url(scrape_url)
    user = mongo_service.get_user(user_id)
    if flight_route_id in user["followed_flight_route_ids"]:
        return True
