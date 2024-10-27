import os
from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

from backend.custom_types import PriceRecord, Flight, FlightRoute, User


class MongoService:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def get_tracked_flight_routes(self) -> [ObjectId]:
        collection = self.get_collection("system_data")
        tracked_flight_routes_ids = \
            collection.find_one({"_id": ObjectId(os.getenv("MONGO_TRACKED_FLIGHT_ROUTES_DOC_ID"))})[
                "tracked_flight_routes"]
        return [ObjectId(tracked_flight_route_id) for tracked_flight_route_id in tracked_flight_routes_ids]

    def get_user_tracked_flight_routes(self, user_id: ObjectId) -> [ObjectId]:
        collection = self.get_collection("users")
        user = collection.find_one({"_id": user_id})
        return user["followed_flight_route_ids"]

    def get_flight_price_records(self, flight_id: ObjectId) -> [dict]:
        collection = self.get_collection("flights")
        flight = collection.find_one({"_id": flight_id})
        price_records = self.get_collection("price_records").find({"_id": {"$in": flight["price_record_ids"]}})
        return price_records.to_list()

    def get_flight_route_flights(self, flight_route_id: ObjectId) -> [dict]:
        collection = self.get_collection("flight_routes")
        flight_route = collection.find_one({"_id": flight_route_id})
        flights = self.get_collection("flights").find({"_id": {"$in": flight_route["flight_ids"]}})
        return flights.to_list()

    def find_by_id(self, collection_name: str, object_id: ObjectId) -> dict:
        collection = self.get_collection(collection_name)
        return collection.find_one({"_id": object_id})

    def find_user_by_email(self, email: str) -> ObjectId | None:
        collection = self.get_collection("users")
        user = collection.find_one({"email": email})
        if user:
            return user["_id"]
        return None

    def find_flight_route_by_scrape_url(self, scrape_url: str) -> ObjectId:
        collection = self.get_collection("flight_routes")
        flight_route = collection.find_one({"scrape_url": scrape_url})
        if flight_route:
            return flight_route["_id"]

    def find_users_by_tracked_flight_route_id(self, flight_route_id: ObjectId) -> [ObjectId]:
        collection = self.get_collection("users")
        return collection.find({"followed_flight_route_ids": str(flight_route_id)}).to_list()

    def get_flight_by_flight_number(self, flight_number: str) -> ObjectId:
        collection = self.get_collection("flights")
        return collection.find_one({"flight_number": flight_number})["_id"]

    def get_flight_route(self, flight_route_id: ObjectId) -> dict:
        collection = self.get_collection("flight_routes")
        return collection.find_one({"_id": flight_route_id})

    def get_flight_routes(self, flight_route_ids: [ObjectId]) -> [dict]:
        collection = self.get_collection("flight_routes")
        return collection.find({"_id": {"$in": flight_route_ids}}).to_list()

    def get_flight_route_by_flight_id(self, flight_id: ObjectId) -> dict:
        collection = self.get_collection("flight_routes")
        return collection.find_one({"flight_ids": flight_id})

    def get_flight(self, flight_id: ObjectId) -> dict:
        collection = self.get_collection("flights")
        return collection.find_one({"_id": flight_id})

    def get_user(self, user_id: ObjectId) -> dict:
        collection = self.get_collection("users")
        return collection.find_one({"_id": user_id})

    def close_connection(self):
        self.client.close()

    def save_price_record(self, price_record: PriceRecord) -> ObjectId:
        collection = self.get_collection("price_records")
        result = collection.insert_one(serialize_price_record(price_record))
        return result.inserted_id

    def save_flight(self, flight: Flight) -> ObjectId:
        collection = self.get_collection("flights")
        result = collection.insert_one(serialize_flight(flight))
        return result.inserted_id

    def save_flight_route(self, flight_route: FlightRoute) -> ObjectId:
        collection = self.get_collection("flight_routes")
        result = collection.insert_one(serialize_flight_route(flight_route))
        return result.inserted_id

    def save_user(self, user: User) -> ObjectId:
        collection = self.get_collection("users")
        result = collection.insert_one(serialize_user(user))
        return result.inserted_id

    def add_flight_route_to_user(self, user_id: ObjectId, flight_route_id: ObjectId):
        collection = self.get_collection("users")
        collection.update_one({"_id": user_id}, {"$push": {"followed_flight_route_ids": flight_route_id}})

    def remove_flight_route_from_user(self, user_id: ObjectId, flight_route_id: ObjectId):
        collection = self.get_collection("users")
        collection.update_one({"_id": user_id}, {"$pull": {"followed_flight_route_ids": flight_route_id}})

    def add_flight_route_to_tracking(self, flight_route_id: ObjectId):
        collection = self.get_collection("system_data")
        collection.update_one({"_id": ObjectId(os.getenv("MONGO_TRACKED_FLIGHT_ROUTES_DOC_ID"))},
                              {"$push": {"tracked_flight_routes": flight_route_id}})

    def delete_flight_route(self, flight_route_id: ObjectId):
        collection = self.get_collection("flight_routes")
        flight_route = self.get_flight_route(flight_route_id)
        for flight_id in flight_route["flight_ids"]:
            self.delete_flight(flight_id)
        collection.delete_one({"_id": flight_route_id})

    def delete_flight(self, flight_id: ObjectId):
        collection = self.get_collection("flights")
        flight = self.get_flight(flight_id)
        for price_record_id in flight["price_record_ids"]:
            self.delete_price_record(price_record_id)
        collection.delete_one({"_id": flight_id})

    def delete_price_record(self, price_record_id: ObjectId):
        collection = self.get_collection("price_records")
        collection.delete_one({"_id": price_record_id})


def serialize_price_record(price_record: PriceRecord) -> dict:
    return {
        "price": price_record.price,
        "currency": price_record.currency,
        "date_time": price_record.date_time.strftime("%Y-%m-%d %H:%M:%S")
    }


def deserialize_price_record(price_record: dict) -> [PriceRecord]:
    return PriceRecord(
        _id=price_record["_id"],
        price=price_record["price"],
        currency=price_record["currency"],
        date_time=datetime.strptime(price_record["date_time"], "%Y-%m-%d %H:%M:%S")
    )


# noinspection PyTypeChecker
def deserialize_flight(flight: dict) -> [Flight]:
    return Flight(
        _id=flight["_id"],
        flight_number=flight["flight_number"],
        departure_time=datetime.strptime(flight["departure_time"], "%H:%M"),
        arrival_time=datetime.strptime(flight["arrival_time"], "%H:%M"),
        price_record_ids=flight["price_record_ids"]
    )


def deserialize_flight_route(flight_route: dict) -> [FlightRoute]:
    return FlightRoute(
        _id=flight_route["_id"],
        origin_code=flight_route["origin_code"],
        destination_code=flight_route["destination_code"],
        date=datetime.strptime(flight_route["date"], "%Y-%m-%d"),
        scrape_url=flight_route["scrape_url"],
        flight_ids=flight_route["flight_ids"]
    )


def serialize_flight(flight: Flight) -> dict:
    return {
        "flight_number": flight.flight_number,
        "departure_time": flight.departure_time.strftime("%H:%M"),
        "arrival_time": flight.arrival_time.strftime("%H:%M"),
        "price_record_ids": flight.price_record_ids
    }


def serialize_flight_route(flight_route: FlightRoute) -> dict:
    return {
        "origin_code": flight_route.origin_code,
        "destination_code": flight_route.destination_code,
        "date": flight_route.date.strftime("%Y-%m-%d"),
        "scrape_url": flight_route.scrape_url,
        "flight_ids": flight_route.flight_ids
    }


def serialize_user(user: User) -> dict:
    return {
        "name": user.name,
        "email": user.email,
        "followed_flight_route_ids": user.followed_flight_route_ids
    }
