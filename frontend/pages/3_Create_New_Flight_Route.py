import re

import streamlit as st

from backend.users_service import user_create_flight_route

st.set_page_config(page_title="Track New Flight", page_icon="🌍")


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)


def handle_create_button_click(url):
    user_create_flight_route(url, st.session_state.user_id)


st.title("Track New Flight")
scrape_url = st.text_input("Enter the URL to the Ryanair website for the route you want to track",
                           placeholder="Enter URL here")
# TODO: Add URL validation
if st.button("Start Tracking"):
    if st.session_state.user_id is None:
        st.error("Please log in to start tracking a flight.")
    else:
        handle_create_button_click(scrape_url)
