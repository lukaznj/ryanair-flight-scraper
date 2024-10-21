import os
from datetime import datetime, timedelta

from bson import ObjectId

from backend import mongo_service
from backend.custom_types import PriceRecord


def stop_tracking_flight_route(flight_route_id: ObjectId):
    collection = mongo_service.get_collection("system_data")
    return collection.find_one_and_update({"_id": ObjectId(os.getenv("MONGO_TRACKED_FLIGHT_ROUTES_DOC_ID"))},
                                          {"$pull": {"tracked_flight_routes": str(flight_route_id)}})


def check_flight_route_deprecated(flight_route_id: ObjectId) -> bool:
    flight_route = mongo_service.find_by_id("flight_routes", flight_route_id)
    date = datetime.strptime(flight_route["date"], "%Y-%m-%d").date()

    if date <= (datetime.now().date() - timedelta(days=1)):
        stop_tracking_flight_route(flight_route_id)
        return True


def check_for_price_change(old_price_record: dict, new_price_record: PriceRecord) -> bool:
    if old_price_record["price"] != new_price_record.price:
        return True
    return False
