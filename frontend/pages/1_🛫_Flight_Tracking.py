from streamlit import session_state as ss
import streamlit as st

from backend import mongo_service
from backend.custom_types import FlightRoute
from backend.mongo_service import deserialize_flight_route
from backend.users_service import user_create_flight_route, user_already_tracking_flight
from frontend.custom_components.flight_route_card import flight_route_card

st.set_page_config(page_title="Flight Tracking", page_icon="✈️")

LOGO_CIRCLE_PATH = "../resources/images/logo_circle.png"
LOGO_FULL_PATH = "../resources/images/logo_full.png"

st.logo(image=LOGO_FULL_PATH, icon_image=LOGO_CIRCLE_PATH, size="large")

st.markdown(
    " <style> div[class^='stMainBlockContainer block-container'] { padding-top: 1rem; } .stMarkdown a { display: none; } [data-testid='stHeaderActionElements'] {display: none;}</style> ",
    unsafe_allow_html=True)


def track_new_flight():
    scrape_url = st.text_input("Enter the URL to the Ryanair website for the flight you want to track",
                               placeholder="Enter URL here")

    # TODO: Add URL validation
    if st.button("Start Tracking"):
        if user_already_tracking_flight(scrape_url, st.session_state.email):
            st.error("You are already tracking this flight.")
        else:
            user_create_flight_route(scrape_url, st.session_state.email)
            st.success("Flight successfully added to tracking! To view it, go to the Tracked Flights tab.")


def get_tracked_flight_routes_for_user(email: str) -> [FlightRoute]:
    user_id = mongo_service.find_user_by_email(email)
    followed_flight_route_ids = mongo_service.get_user(user_id)["followed_flight_route_ids"]
    if followed_flight_route_ids:
        flight_routes = mongo_service.get_flight_routes(followed_flight_route_ids)
        return [deserialize_flight_route(flight_route) for flight_route in flight_routes]


def view_tracked_flights():
    if get_tracked_flight_routes_for_user(st.session_state.email):
        for flight_route in get_tracked_flight_routes_for_user(st.session_state.email):
            flight_route_card(flight_route)
    else:
        st.warning("You are not tracking any flights. To start tracking a flight, go to the Track New Flight tab.")


st.title("Flight Tracking")

if "authentication_status" not in ss:
    st.switch_page("pages/2_🔐_Account.py")
elif not ss["authentication_status"]:
    st.subheader("You need to be logged in to use Flight Tracking.", divider=True)
    button = st.button("Go to Login and Registration Page")
    if button:
        st.switch_page("pages/2_🔐_Account.py")

elif ss["authentication_status"]:

    track_new_tab, view_tracked_tab = st.tabs(["Track New Flight", "Tracked Flights"])

    with track_new_tab:
        track_new_flight()

    with view_tracked_tab:
        view_tracked_flights()

ss.authenticator.login(location="unrendered")
