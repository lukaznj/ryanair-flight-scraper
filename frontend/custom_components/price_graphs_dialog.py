from datetime import datetime

import pandas as pd
import streamlit as st

from backend import mongo_service
from backend.custom_types import Flight, PriceRecord
from backend.mongo_service import deserialize_price_record


def create_chart_data(price_records: [PriceRecord]) -> pd.DataFrame:
    data = {
        "Date": [price_record.date_time for price_record in price_records],
        f"Price ({price_records[0].currency})": [price_record.price for price_record in price_records]
    }
    print(data)
    return pd.DataFrame(data)


@st.dialog("Price Graphs")
def price_graphs_dialog(flights: [Flight]):
    tabs = st.tabs([flight.flight_number for flight in flights])

    for i, tab in enumerate(tabs):
        with tab:
            col1, col2 = st.columns(2)
            with col1:
                st.caption(
                    f"<div style='text-align: left;'>Departure</div>",
                    unsafe_allow_html=True)
                st.caption(
                    f"<div style='text-align: left;'>{datetime.strftime(flights[i].departure_time, "%H:%M")}</div>",
                    unsafe_allow_html=True)
            with col2:
                st.caption(
                    f"<div style='text-align: right;'>Arrival</div>",
                    unsafe_allow_html=True)
                st.caption(
                    f"<div style='text-align: right;'>{datetime.strftime(flights[i].arrival_time, '%H:%M')}</div>",
                    unsafe_allow_html=True)

            st.header("")
            price_records = mongo_service.get_flight_price_records(flights[i]._id)
            st.line_chart(create_chart_data([deserialize_price_record(price_record) for price_record in price_records]),
                          x="Date", y=f"Price ({deserialize_price_record(price_records[0]).currency})")
