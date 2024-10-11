from dataclasses import dataclass
from datetime import time, datetime


@dataclass
class PriceRecord:
    price: float
    currency: str
    date_time: datetime


@dataclass
class Flight:
    flight_number: str
    departure_time: time
    arrival_time: time
    price_record: [PriceRecord]


@dataclass
class FlightRoute:
    origin: str
    destination: str
    flights: [Flight]


@dataclass
class PriceRecordUpdate:
    flight_number: str
    price_record: PriceRecord
