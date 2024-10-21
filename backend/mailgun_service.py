import os

import requests

from backend.custom_types import PriceChange
from backend.email_maker import create_pure_text_email, create_html_email


def send_price_change_emails(price_changes: [PriceChange]):
    for price_change in price_changes:
        requests.post(
            "https://api.mailgun.net/v3/notif.datadreamgroup.tech/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={
                "from": "Flight Scraper <price.change@notif.datadreamgroup.tech>",
                "to": price_change.user_email,
                "subject": f"Price change for flight {price_change.flight_number}",
                "text": create_pure_text_email(price_change),
                "html": create_html_email(price_change)
            }
        )
