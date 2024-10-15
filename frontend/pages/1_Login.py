import streamlit as st

from backend.custom_types import User

st.set_page_config(page_title="Login", page_icon="🔑")

st.title("Login")

email = st.text_input("Email", placeholder="Enter your email")

login_button = st.button("Login")

if login_button:
    st.session_state['email'] = email
    user = User(email)
