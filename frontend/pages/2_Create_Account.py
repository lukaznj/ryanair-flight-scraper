import streamlit as st
import sys
import os
import re


def is_valid_email(email_input):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email_input)


st.set_page_config(page_title="Register", page_icon="🔒")

st.title("Create an Account")

email = st.text_input("Email", placeholder="Enter your email")

button = st.button("Register")

if button:
    if is_valid_email(email):
        st.session_state['email'] = email

        # create_user(email)
    # mongo_service.find_by_id("flights", "670db49be901f7e808e2fbf2")

    else:
        st.error("Please enter a valid email address.")
