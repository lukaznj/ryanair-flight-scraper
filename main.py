from dotenv import load_dotenv

from scrape_engine import scrape_webpage

load_dotenv()

if __name__ == "__main__":
    scrape_webpage(
        "https://www.ryanair.com/hr/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-10-31&dateIn=2024-11-06&isConnectedFlight=false&discount=0&promoCode=&isReturn=true&originIata=ZAG&destinationIata=STN&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-10-31&tpEndDate=2024-11-06&tpDiscount=0&tpPromoCode=&tpOriginIata=ZAG&tpDestinationIata=STN",
        "/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/div/div[2]/div/carousel-container/carousel/div/ul/li[3]/carousel-item/button/div[2]/flights-price/ry-price/span[2]")
