import pandas as pd
import streamlit as st
from pathlib import Path
from events.plots import plot_users_per_period
from events.create_data import create_dummy_data

def display_customer_acquisition():
    st.header("Customer Acquisition Details")
    st.write("Customer acquisition is the process of bringing new customers or clients to your business."
             "The goal of this process is to create a systematic, sustainable acquisition strategy that"
             "can evolve with new trends and changes.")

    st.subheader("You can see: ")
    st.text("1. New acquired users per period")
    st.text("2. Number of acquired users who are active per period")
    st.text("3. Number of returning users per period \n(i.e. active users who were acquired during a previous period)")
    st.text("4. W/W Growth: week-on-week percentage growth. \nIdeally, you want this to be always in the positives and increasing with time.")
    st.text("5. N/R Ratio: new-to-returning users ratio. \n Indicative of how the period activity is shared between new and returning customers.")
    
    # dummy data
    events = create_dummy_data()
    fig = plot_users_per_period(events=events, acquisition_event_name='Cart Created',
                                user_source_col='user_source', period='m')
    st.plotly_chart(fig)