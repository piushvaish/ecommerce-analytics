import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from online_metrics.create_data import create_dataframe
from online_metrics.monthly_retention_rate import retention_table, plot_bar, cohort_based_retention_rate, plot_heatmap_log, plot_heatmap
#from online_metrics.customer_metrics_plot import plot_scatter, plot_bar
from events.plots import retention_heatmap


def display_retention():
    st.header("Customer Retention")
    st.write("Retention analysis is key to understanding if customers come back to your buy your product"
             " and at what frequency. Inevitably, the percentage of customers coming back will decrease"
             " with time after their acquisition as some users fail to see the value"
             "or maybe they just don’t need it or did not like it.")

    st.subheader("Monthly Retention Rate")
    st.markdown("""<h4 style="color:#26608e;">Monthly Retention Rate = Retained Customers From Prev. Month/Active Customers Total</h2>""", unsafe_allow_html=True)

    # data
    df = create_dataframe()

    df_retention = retention_table(df)

    fig = plot_bar(df_retention, 'month_y', 'RetentionRate',
                   'RetentionRate', 'indianred', [0, .008], 'Monthly Retention Rate', 'Month - Year', 'Rate')
    st.plotly_chart(fig)

    with st.beta_expander("See explanation"):
        st.write("""
        Monthly Retention Rate is significantly lower over time.
        """)

    fig = plot_bar(df_retention, 'month_y', 'ChurnRate',
                   'ChurnRate', 'crimson', [0.97, 1], 'Monthly Churn Rate', 'Month - Year', 'Rate')
    st.plotly_chart(fig)

    with st.beta_expander("See explanation"):
        st.write("""
        Monthly Churn Rate is significantly high with the maximum rate at January '18.
        """)

    st.subheader("Cohort Based Retention Rate")
    st.write("Cohorts are determined as first purchase year-month of the customers."
             "You will be measuring what percentage of the customers retained after their"
             "first purchase in each month. This view will helps to see how recent and old cohorts"
             "differ regarding retention rate and if recent changes in customer experience affected"
             "new customer’s retention or not.")

    st.subheader("You can see: ")
    st.write("1. Size of each user cohort (new users per period)")
    #st.text("2. Number of returning users per subsequent period for each cohort")
    st.write("2. Percentage of returning users per subsequent period for each cohort")

    user_retention = cohort_based_retention_rate(df)
    if st.checkbox('Show Retention Table'):
        st.dataframe(user_retention.style.highlight_max(axis=0))
    fig = plot_heatmap_log(user_retention, 'bluyl', "Cohort Based Retention Rate")
    st.plotly_chart(fig)

    with st.beta_expander("See explanation"):
        st.write("""
        First month natural log of retention rate is better with rate decreasing over time.
        """)

    user_churn = 1 - user_retention

    if st.checkbox('Show Churn Table'):
        st.dataframe(user_churn.style.highlight_max(axis=0))
    # fig = plot_heatmap_log(user_churn,  'ylgnbu', "Cohort Based Churn Rate")
    # st.plotly_chart(fig)

    # with st.beta_expander("See explanation"):
    #     st.write("""
    #     First month natural log of churn rate is better with rate decreasing over time.
    #     """)
