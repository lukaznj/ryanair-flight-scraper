import streamlit as st

import os
import streamlit_authenticator as stauth
from streamlit import session_state as ss
from streamlit_authenticator import RegisterError, LoginError

from backend.database_manager import create_user

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/config.yaml'))


st.set_page_config(page_title="Account", page_icon="🔐")

LOGO_CIRCLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/images/logo_circle.png'))
LOGO_FULL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/images/logo_full.png'))

st.logo(image=LOGO_FULL_PATH, icon_image=LOGO_CIRCLE_PATH, size="large")

st.markdown(
    " <style> div[class^='stMainBlockContainer block-container'] { padding-top: 1rem; } [data-testid='stHeaderActionElements'] {display: none;}</style> ",
    unsafe_allow_html=True)


def handle_register_user(user):
    create_user(user["new_name"], user["new_email"])
    st.switch_page("🏠_Home.py")


st.title("Account")
st.session_state.authenticator = stauth.Authenticate(CONFIG_PATH)

if st.session_state["authentication_status"]:
    st.subheader("You are logged in.")
    ss.authenticator.logout(callback=lambda _: st.rerun())

else:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        try:
            ss.authenticator.login(location="main")

            if st.session_state["authentication_status"] is False:
                st.error("Username/password is incorrect")

            elif st.session_state["authentication_status"] is None:
                st.warning('Please enter your username and password')

        except LoginError as e:
            st.error(e)

    with register_tab:
        try:
            ss.authenticator.register_user(location="main", merge_username_email=True,
                                           callback=handle_register_user)
        except RegisterError as e:
            st.error(e)
