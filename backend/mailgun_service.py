import os

import requests

from backend.custom_types import PriceRecord


def send_price_change_email(old_price_record: dict, new_price_record: PriceRecord, user_email: str):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Ryanair Flight Scraper <price.change@notif.datadreamgroup.tech>",
              "to": user_email,
              "subject": "A price change has occurred!",
              "text": f"The price has changed from {old_price_record["price"]} to {new_price_record.price}!"})
