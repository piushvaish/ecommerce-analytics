import pandas as pd
import streamlit as st
from pathlib import Path
from events.plots import  plot_user_flow
from events.create_data import create_dummy_data

def display_customer_sankey():
    st.header("Visualizing Customer Journey using Sankey Diagram")
    st.write("Sankey diagram is a type of chart that displays flows and their quantities."
             " Arrows of various thickness are used to visualize the quantity in each flow as well"
             " as the direction or path in which they flow."
             " Mapping out journey flow diagrams helps in identifying and visualising the most dominant ones."
             " This helps in raising insights around customer's touchpoints, but also identifying which steps your customers use the most.")

    st.subheader("You can see: ")
    st.text(
        "1. Most dominant customer journey flows by first defining the starting point")
    events = create_dummy_data()
    fig = plot_user_flow(events, starting_step='Cart Created')
    st.plotly_chart(fig)