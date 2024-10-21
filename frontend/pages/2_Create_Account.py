import streamlit as st
import re

from backend.database_manager import create_user
from backend.users_service import user_exists


def is_valid_email(email_input):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email_input)


st.set_page_config(page_title="Register", page_icon="🔒")

st.title("Create an Account")

name = st.text_input("Name", placeholder="Enter your name")

email = st.text_input("Email", placeholder="Enter your email")

register_button = st.button("Register")

if register_button:
    if not is_valid_email(email):
        st.error("Please enter a valid email address.")
    elif user_exists(email):
        st.error("User with this email already exists.")
    else:
        st.session_state.user_id = create_user(name, email)
        st.switch_page("pages/3_Track_New_Flight_Route.py")
