import os

import requests
from dotenv import load_dotenv

from custom_types import PriceRecord

load_dotenv()


def send_price_change_email(old_price_record: dict, new_price_record: PriceRecord):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Excited User <mailgun@sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org>",
              "to": ["razemluka@gmail.com", "YOU@sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org"],
              "subject": "A price change has occurred!",
              "text": f"The price has changed from {old_price_record["price"]} to {new_price_record.price}!"})


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Excited User <mailgun@sandbox5acfc6fda2ec459ea2996f5682df99ed.mailgun.org>",
              "to": "razemluka@gmail.com",
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!"})


print(send_simple_message())
