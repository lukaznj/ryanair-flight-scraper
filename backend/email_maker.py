from datetime import datetime

from bson import ObjectId

from backend import mongo_service
from backend.airport_search import get_airport_by_code
from backend.custom_types import PriceChange, PriceRecord


def create_pure_text_email(price_change: PriceChange) -> str:
    origin = get_airport_by_code(price_change.origin_code)
    destination = get_airport_by_code(price_change.destination_code)
    percent_change = (price_change.new_price - price_change.old_price) / price_change.old_price * 100
    return f"Hello {price_change.user_name}! \n\n" \
           f"Flight ({price_change.flight_number}) from {origin} to {destination} on " \
           f"{price_change.departure_date.strftime(f"%A, %B %d,")} departing at " \
           f"{price_change.departure_time.strftime("%H:%M")} and arriving at " \
           f"{price_change.arrival_time.strftime("%H:%M")} has recently " \
           f"had a price change!\n\n" \
           f"Price change: {price_change.currency}{price_change.old_price} -> " \
           f"{price_change.currency}{price_change.new_price}" \
           f"{'+' if percent_change > 0 else '-'}{percent_change}%\n\n" \
           f"\n\nKind regards, \nYour DataDream Flight Scraper Team"


def create_html_email(price_change: PriceChange) -> str:
    origin = get_airport_by_code(price_change.origin_code).upper()
    destination = get_airport_by_code(price_change.destination_code).upper()

    with open("../resources/email_templates/price_change_email.html", "r") as file:
        html = file.read()

    html = html.replace("{flight_number}", price_change.flight_number)
    html = html.replace("{user_name}", price_change.user_name)
    html = html.replace("{old_price}", str(price_change.old_price))
    html = html.replace("{new_price}", str(price_change.new_price))
    html = html.replace("{currency}", price_change.currency)
    html = html.replace("{origin}", origin)
    html = html.replace("{destination}", destination)
    html = html.replace("{departure_date}", price_change.departure_date.strftime("%a, %d %b %Y"))
    html = html.replace("{departure_time}", price_change.departure_time.strftime("%H:%M"))
    html = html.replace("{arrival_time}", price_change.arrival_time.strftime("%H:%M"))

    return html


# noinspection PyTypeChecker
def prepare_price_changes(old_price_record: PriceRecord, new_price_record: PriceRecord, flight_id: ObjectId) -> [
    PriceChange]:
    price_changes = []
    flight_route = mongo_service.get_flight_route_by_flight_id(flight_id)
    users = mongo_service.find_users_by_tracked_flight_route_id(flight_route["_id"])

    for user in users:
        str_departure_time = mongo_service.get_flight(flight_id)["departure_time"]
        str_arrival_time = mongo_service.get_flight(flight_id)["arrival_time"]
        price_change = PriceChange(user_email=user["email"],
                                   user_name=user["name"],
                                   flight_number=mongo_service.get_flight(flight_id)["flight_number"],
                                   old_price=old_price_record.price,
                                   new_price=new_price_record.price,
                                   currency=new_price_record.currency,
                                   origin_code=flight_route["origin_code"],
                                   destination_code=flight_route["destination_code"],
                                   departure_date=datetime.strptime(flight_route["date"], "%Y-%m-%d"),
                                   departure_time=datetime.strptime(str_departure_time, "%H:%M"),
                                   arrival_time=datetime.strptime(str_arrival_time, "%H:%M"))
        price_changes.append(price_change)
    return price_changes
