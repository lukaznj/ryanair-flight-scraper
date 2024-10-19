import os

import requests
from bson import ObjectId

from backend import mongo_service
from backend.custom_types import PriceRecord, PriceChange


def send_price_change_emails(price_changes: [PriceChange]):
    for price_change in price_changes:
        requests.post(
            "https://api.mailgun.net/v3/notif.datadreamgroup.tech/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={"from": "Flight Scraper <price.change@notif.datadreamgroup.tech>",
                  "to": price_change.user_email,
                  "subject": f"The price for {price_change.flight_number} has changed!",
                  "text": f"Hi! \n\nThe price for the flight {price_change.flight_number} has changed "
                          f"from {price_change.old_price} to {price_change.new_price}. \n\nKind regards, \nDataDream Flight Scraper"})


def check_for_price_change(old_price_record: dict, new_price_record: PriceRecord) -> bool:
    if old_price_record["price"] != new_price_record.price:
        return True
    return False


def prepare_price_changes(old_price_record: PriceRecord, new_price_record: PriceRecord, flight_id: ObjectId) -> [
    PriceChange]:
    price_changes = []
    flight_route = mongo_service.get_flight_route_by_flight_id(flight_id)
    users = mongo_service.find_users_by_tracked_flight_route_id(flight_route["_id"])

    for user in users:
        price_change = PriceChange(user_email=user["email"],
                                   flight_number=mongo_service.get_flight(flight_id)["flight_number"],
                                   old_price=old_price_record.price,
                                   new_price=new_price_record.price,
                                   currency=new_price_record.currency,
                                   origin_code=flight_route["origin"],
                                   destination_code=flight_route["destination"],
                                   departure_time=mongo_service.get_flight(flight_id)["departure_time"],
                                   arrival_time=mongo_service.get_flight(flight_id)["arrival_time"])
        price_changes.append(price_change)
    return price_changes
