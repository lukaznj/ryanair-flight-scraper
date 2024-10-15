import streamlit as st

st.set_page_config(page_title="Welcome", page_icon="✈️")

st.title("Welcome to the Ryanair Flight Price Tracker!")

col1, col2 = st.columns(2)

with col1:
    register_button = st.button("Register")

with col2:
    login_button = st.button("Login")
if register_button:
    st.switch_page("pages/2_Create_Account.py")

if login_button:
    st.switch_page("pages/1_Login.py")
