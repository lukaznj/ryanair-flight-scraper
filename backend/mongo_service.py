from typing import Any

from bson import ObjectId
from pymongo import MongoClient

from backend.custom_types import PriceRecord, Flight, FlightRoute, User


class MongoService:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def find_by_id(self, collection_name: str, object_id: ObjectId) -> dict:
        collection = self.get_collection(collection_name)
        return collection.find_one({"_id": ObjectId(object_id)})

    def find_user_by_email(self, email: str) -> ObjectId | None:
        collection = self.get_collection("users")
        user = collection.find_one({"email": email})
        if user:
            return user["_id"]
        return None

    def get_flight_by_flight_number(self, flight_number: str) -> ObjectId:
        collection = self.get_collection("flights")
        return collection.find_one({"flight_number": flight_number})["_id"]

    def get_flight(self, flight_id: ObjectId) -> dict:
        collection = self.get_collection("flights")
        return collection.find_one({"_id": ObjectId(flight_id)})

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


def serialize_price_record(price_record: PriceRecord) -> dict:
    return {
        "price": price_record.price,
        "currency": price_record.currency,
        "date_time": price_record.date_time.strftime("%Y-%m-%d %H:%M:%S")
    }


def serialize_flight(flight: Flight) -> dict:
    return {
        "flight_number": flight.flight_number,
        "departure_time": flight.departure_time.strftime("%H:%M"),
        "arrival_time": flight.arrival_time.strftime("%H:%M"),
        "price_record_ids": flight.price_record_ids
    }


def serialize_flight_route(flight_route: FlightRoute) -> dict:
    return {
        "origin": flight_route.origin,
        "destination": flight_route.destination,
        "flight_time": flight_route.flight_time.strftime("%Hh %Mm"),
        "flight_ids": flight_route.flight_ids,
        "scrape_url": flight_route.scrape_url
    }


def serialize_user(user: User) -> dict:
    return {
        "email": user.email,
        "tracked_flight_route_ids": user.tracked_flight_route_ids
    }
