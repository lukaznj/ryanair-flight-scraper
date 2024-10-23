from streamlit import session_state as ss
import streamlit as st

from backend.users_service import user_create_flight_route, user_already_tracking_flight


def handle_create_button_click(url):
    user_create_flight_route(url, st.session_state.user_id)


def track_new_flight():
    scrape_url = st.text_input("Enter the URL to the Ryanair website for the flight you want to track",
                               placeholder="Enter URL here")

    # TODO: Add URL validation
    if st.button("Start Tracking"):
        if user_already_tracking_flight(scrape_url, st.session_state.user_id):
            st.error("You are already tracking this flight.")
        else:
            handle_create_button_click(scrape_url)


def view_tracked_flights():
    st.write("LIST OF YOUR TRACKED FLIGHTS")


st.set_page_config(page_title="Flight Tracking", page_icon="✈️")

LOGO_CIRCLE_PATH = "../resources/images/logo_circle.png"
LOGO_FULL_PATH = "../resources/images/logo_full.png"

st.logo(image=LOGO_FULL_PATH, icon_image=LOGO_CIRCLE_PATH, size="large")

st.markdown(
    " <style> div[class^='stMainBlockContainer block-container'] { padding-top: 1rem; } </style> ",
    unsafe_allow_html=True)

st.title("Flight Tracking")

if "authentication_status" not in ss:
    st.switch_page("pages/2_🔐_Account.py")
elif not ss["authentication_status"]:
    st.subheader("You need to be logged in to use Flight Tracking.", divider=True)
    button = st.button("Go to Login and Registration Page")
    if button:
        st.switch_page("pages/2_🔐_Account.py")

elif ss["authentication_status"]:

    track_new_tab, view_tracked_tab = st.tabs(["Track New Flight", "View Tracked Flights"])

    with track_new_tab:
        track_new_flight()

    with view_tracked_tab:
        view_tracked_flights()

ss.authenticator.login(location="unrendered")
