from dotenv import load_dotenv

from scrape_engine import scrape_flight_list, format_scraped_flights_data

load_dotenv()

if __name__ == "__main__":
    result = scrape_flight_list(
        "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-11-03&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=ZAG&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-11-03&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=ZAG&tpDestinationIata=STN")
    print(format_scraped_flights_data(result))
