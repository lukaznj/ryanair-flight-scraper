from attr import dataclass
from datetime import time, datetime


@dataclass
class PriceRecord:
    price: float
    currency: str
    date_time: datetime


@dataclass
class Flight:
    departure_time: time
    arrival_time: time
    price_record: [PriceRecord]


@dataclass
class FlightRoute:
    origin: str
    destination: str
    flights: [Flight]
