import os

import streamlit as st
import re

from backend.database_manager import create_flight_route
from backend.mongo_service import MongoService

st.set_page_config(page_title="Track New Flight", page_icon="🌍")


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)


def handle_create_button_click(url):
    mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))
    create_flight_route(url, mongo_service)


st.title("Track New Flight")
url_to_scrape = st.text_input("Enter the URL to the Ryanair website for the route you want to track",
                              placeholder="Enter URL here")

if st.button("Start Tracking"):
    handle_create_button_click(url_to_scrape)
