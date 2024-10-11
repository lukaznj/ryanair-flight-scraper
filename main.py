import os
from dataclasses import asdict

from dotenv import load_dotenv

from mongo_service import MongoService, serialize_new_flight_route, serialize_new_price_record
from scrape_engine import scrape_flight_list, format_new_flight_route, format_new_price_records

load_dotenv()

if __name__ == "__main__":
    mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))
    collection = mongo_service.get_collection("flight_routes")

    scrape_result = scrape_flight_list(
        "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-11-01&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=EIN&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-11-01&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=EIN&tpDestinationIata=STN")
    # formated_data = (format_new_flight_route(scrape_result))
    # collection.insert_one(serialize_new_flight_route(formated_data))

    price_records_updates = (format_new_price_records(scrape_result))

    for price_record_update in price_records_updates:
        collection.update_one({"flights.flight_number": price_record_update.flight_number},
                              {"$push": {"flights.$.price_record": serialize_new_price_record(
                                  price_record_update.price_record)}})
