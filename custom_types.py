from dataclasses import dataclass
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
    origin: str
    destination: str
    flight_time: time
    flight_ids: [ObjectId]
    scrape_url: str = None
    _id: ObjectId = None


@dataclass
class CreateFlightRouteRequest:
    origin: str
    destination: str
    date: date
