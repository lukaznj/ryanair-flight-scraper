import os
import sys
import streamlit as st
from streamlit import session_state as ss, switch_page

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Welcome", page_icon="✈️")

LOGO_CIRCLE_PATH = "../resources/images/logo_circle.png"
LOGO_FULL_PATH = "../resources/images/logo_full.png"

st.logo(image=LOGO_FULL_PATH, icon_image=LOGO_CIRCLE_PATH, size="large")

st.markdown(
    " <style> div[class^='stMainBlockContainer block-container'] { padding-top: 1rem; } [data-testid='stHeaderActionElements'] {display: none;} </style> ",
    unsafe_allow_html=True)

if "authentication_status" not in ss:
    switch_page("pages/2_🔐_Account.py")

elif not ss["authentication_status"]:
    st.title("Flight Scraper")
    st.caption("By DataDream Group")
    st.divider()
    st.subheader("To view your tracked flights, or start tracking new ones, please login or create an account.")
    if st.button("Login or Create Account"):
        st.switch_page("pages/2_🔐_Account.py")

elif ss["authentication_status"]:
    st.title(f"Welcome back {ss['name']}!")

    st.write("You can view your tracked flights or start tracking new ones.")
    if st.button("Go to Flight Tracking"):
        st.switch_page("pages/1_🛫_Flight_Tracking.py")

ss.authenticator.login(location="unrendered")
