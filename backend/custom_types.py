from dataclasses import dataclass, field
from datetime import time, date, datetime

from bson import ObjectId


@dataclass
class PriceRecord:
    price: float
    currency: str
    date_time: datetime
    _id: ObjectId = None


@dataclass
class Flight:
    flight_number: str
    departure_time: time
    arrival_time: time
    price_record_ids: [ObjectId]
    _id: ObjectId = None


@dataclass
class FlightRoute:
    origin_code: str
    destination_code: str
    date: date
    scrape_url: str
    flight_ids: list[ObjectId] = field(default_factory=list)
    _id: ObjectId = None


@dataclass
class FlightRouteCreationRequest:
    url: str
    origin_code: str = None
    destination_code: str = None
    date: date = None


@dataclass
class User:
    name: str
    email: str
    followed_flight_route_ids: list[ObjectId] = field(default_factory=list)
    _id: ObjectId = None


@dataclass
class PriceChange:
    user_email: str
    flight_number: str
    old_price: float
    new_price: float
    currency: str
    origin_code: str
    destination_code: str
    departure_time: time
    arrival_time: time
