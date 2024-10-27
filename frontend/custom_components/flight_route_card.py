from backend import mongo_service
from backend.airport_search import get_airport_by_code
from backend.custom_types import FlightRoute
import streamlit as st
import os

from backend.mongo_service import deserialize_flight
from frontend.custom_components.price_graphs_dialog import price_graphs_dialog

ICON_PLANE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/images/icon_plane.svg"))

HIDE_IMG_FS = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        .stMarkdown a {
            display: none;}
        </style>
        '''
@st.dialog("Delete Tracked Flight")
def delete_flight_route_dialog(flight_route: FlightRoute):
    st.subheader("Are you sure you want to delete this tracked flight?")
    st.caption("You can always add it back later.")
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel"):
            st.rerun()
    with col2:
        if st.button("I am sure"):
            user_id = mongo_service.find_user_by_email(st.session_state.email)
            mongo_service.remove_flight_route_from_user(user_id, flight_route._id)
            st.switch_page("🏠_Home.py")


def flight_route_card(flight_route: FlightRoute):
    st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)
    origin = get_airport_by_code(flight_route.origin_code)
    destination = get_airport_by_code(flight_route.destination_code)
    date = flight_route.date.strftime("%d %b, %Y")

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([0.35, 0.1, 0.35, 0.2], vertical_alignment="center")

        with col1:
            st.markdown(f"<h2 style='text-align: center;'>{origin}</h2>", unsafe_allow_html=True)
            st.write("")
        with col2:
            st.image(ICON_PLANE_PATH, use_column_width=True)

        with col3:
            st.markdown(f"<h2 style='text-align: center;'>{destination}</h2>", unsafe_allow_html=True)
            st.write("")
        with col4:
            col5, col6 = st.columns([1, 0.3])
            with col5:
                if st.button("View Graphs", key=flight_route.scrape_url + "_view"):
                    flights = mongo_service.get_flight_route_flights(flight_route._id)
                    price_graphs_dialog([deserialize_flight(flight) for flight in flights])
            with col6:
                if st.button("", icon=":material/delete:", key=flight_route.scrape_url + "_delete"):
                    delete_flight_route_dialog(flight_route)
            st.write("📅 " + date)
