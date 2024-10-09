import string

import requests


def fetch_raw_webpage(url: str) -> str:
    response = requests.get(url)
    return response.text


print(fetch_raw_webpage(
    "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-10-31&dateIn=2024-11-03&isConnectedFlight=false&discount=0&promoCode=&isReturn=true&originIata=ZAG&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-10-31&tpEndDate=2024-11-03&tpDiscount=0&tpPromoCode=&tpOriginIata=ZAG&tpDestinationIata=STN")
)
