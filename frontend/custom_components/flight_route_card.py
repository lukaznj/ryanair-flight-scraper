from backend import mongo_service
from backend.airport_search import get_airport_by_code
from backend.custom_types import FlightRoute
import streamlit as st

from backend.mongo_service import deserialize_flight
from frontend.custom_components.price_graphs_dialog import price_graphs_dialog

ICON_PLANE_PATH = "../resources/images/icon_plane.svg"

HIDE_IMG_FS = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        .stMarkdown a {
            display: none;}
        </style>
        '''


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
            if st.button("View Graphs", key=flight_route.scrape_url):
                flights = mongo_service.get_flight_route_flights(flight_route._id)
                price_graphs_dialog([deserialize_flight(flight) for flight in flights])
            st.write("📅 " + date)
