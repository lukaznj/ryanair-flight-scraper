import streamlit as st
from dotenv import load_dotenv

load_dotenv()

create_page = st.Page("track_new_flight_page.py", title="Track new flight", icon=":material/add_circle:")
delete_page = st.Page("tracked_flights_page.py", title="Currently tracked flights",
                      icon=":material/flight_takeoff:")

pg = st.navigation([create_page, delete_page])
pg.run()
