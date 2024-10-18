import os

import requests

from backend.custom_types import PriceRecord, PriceChangeRecord


def send_price_change_email(price_change_records: [PriceChangeRecord]):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Ryanair Flight Scraper <price.change@notif.datadreamgroup.tech>",
              "to": user_email,
              "subject": "A price change has occurred!",
              "text": f"The price has changed from {old_price_record["price"]} to {new_price_record.price}!"})


def check_for_price_change(old_price_record: dict, new_price_record: PriceRecord) -> bool:
    if old_price_record["price"] == new_price_record.price:
        send_price_change_email(old_price_record, new_price_record)
        return True
    return False
