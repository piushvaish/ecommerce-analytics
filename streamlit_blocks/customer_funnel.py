import pandas as pd
import streamlit as st
from pathlib import Path
from events.plots import  plot_stacked_funnel
from events.create_data import create_dummy_data

def display_customer_funnel():
    st.header("Customer Funnel Analysis")
    st.write("Funnel analysis is critical in identifying bottlenecks at any point in the user journey."
             " Usually, there is a key event which generates revenue for the business."
             "Maximising the number of people performing this action is thus to our best interest.")

    st.subheader("You can see: ")
    st.text("1. Number of customers that perform each step")
    st.text("2. Percentage of customers that perform each step")

    steps = ['Cart Created', 'Add Payment',
             'Order Created', 'Order Processed', 'Shipment Released', 'Order Completed']
    # dummy data
    events = create_dummy_data()
    fig = plot_stacked_funnel(events, steps, col='user_source')
    st.plotly_chart(fig)