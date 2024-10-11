from pymongo import MongoClient

from custom_types import FlightRoute


class MongoService:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close_connection(self):
        self.client.close()


def serialize_new_flight_route(flight_route: FlightRoute):
    return {
        "origin": flight_route.origin,
        "destination": flight_route.destination,
        "flights": [
            {
                "flight_number": flight.flight_number,
                "departure_time": flight.departure_time.strftime("%H:%M"),
                "arrival_time": flight.arrival_time.strftime("%H:%M"),
                "price_record": [
                    {
                        "price": price_record.price,
                        "currency": price_record.currency,
                        "date_time": price_record.date_time.strftime("%Y-%m-%d %H:%M:%S")
                    } for price_record in flight.price_record
                ]
            } for flight in flight_route.flights
        ]

    }


def serialize_new_price_record(price_record):
    return {
        "price": price_record.price,
        "currency": price_record.currency,
        "date_time": price_record.date_time.strftime("%Y-%m-%d %H:%M:%S")
    }
