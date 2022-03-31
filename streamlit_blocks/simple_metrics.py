import pandas as pd
import streamlit as st
from pathlib import Path
from online_metrics.create_data import create_dataframe
from online_metrics.customer_metrics import monthly_revenue, monthly_revenue_growth_rate, monthly_active_customers, monthly_order_count, average_revenue_per_order, dataframe_user_type_revenue, dataframe_new_customer_ratio
from online_metrics.customer_metrics_plot import plot_scatter, plot_bar


def display_metrics():
    st.header("Key Performance Indicators (KPIs)")

    st.markdown("""
    KPIs are the critical (key) indicators of progress toward an 
    intended result. 
    KPIs provides a focus for strategic and operational improvement, 
    create an analytical basis for decision making and help focus attention on what matters most. 
    As Peter Drucker famously said,
    <blockquote>
    <b>What gets measured gets done. </b>
    </blockquote>
    Managing with the use of KPIs includes setting targets (the desired level of performance) and tracking progress against that target. 
    Managing with KPIs often means working to improve leading indicators that 
    will later drive lagging benefits. 
    Leading indicators are precursors of future success; 
    lagging indicators show how successful the organization was at achieving results in the past. 
    """, unsafe_allow_html=True)

    # data
    df = create_dataframe()
    st.markdown(
        "Sample data of [Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce")
    if st.checkbox('Show Online Data'):
        st.dataframe(df.head(10))

    #st.subheader("Monthly Revenue")
    st.markdown("""<h4 style="color:#26608e;"> Revenue = Active Customer Count * Order Count * Average Revenue per Order</h4>""", unsafe_allow_html=True)
    df_revenue = monthly_revenue(df)
    fig = plot_scatter(df_revenue, 'month_year', 'payment_value',
                       'firebrick', 'Monthly Revenue', 'Month - Year', 'R$')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Revenue is growing steadily with the maximum revenue around November '17.
        """)

    df_revenue = monthly_revenue_growth_rate(df)
    fig = plot_scatter(df_revenue, 'month_year',
                       'monthly_growth', 'royalblue', 'Monthly Revenue Growth Rate', 'Month - Year', '%')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        The growth rate has not been steady with it decreasing over time.
        """)

    df_monthly_active = monthly_active_customers(df)
    fig = plot_bar(df_monthly_active, 'month_year', 'customer_unique_id',
                   'customer_unique_id', 'crimson', 'Monthly Active Users', 'Month - Year', 'Number')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        The number of monthly active users has been increasing steadily with Nov '17 showing the highest number.
        """)

    df_monthly_sales = monthly_order_count(df)
    fig = plot_bar(df_monthly_sales, 'month_year', 'order_status',
                   'Monthly Order Count', 'indianred', 'Monthly Total # of Order', 'Month - Year', 'Number')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        The number of monthly active users has been increasing steadily with Nov '17 showing the highest number.
        """)

    df_monthly_order_avg = average_revenue_per_order(df)
    # st.dataframe(tx_monthly_active)
    fig = plot_bar(df_monthly_order_avg, 'month_year', 'payment_value',
                   'Monthly Order Average', 'lightslategray', 'Monthly Average # of Order', 'Month - Year', 'Number')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        However, the average has almost stayed the same over the month.
        """)

    df_user_type_revenue = dataframe_user_type_revenue(df)
    if st.checkbox('Show Revenue Data'):
        st.dataframe(df_user_type_revenue)

    fig = plot_scatter(df_user_type_revenue.query("usertype == 'Existing'"), 
    'month_year', 'payment_value',
    'firebrick', 'Monthly Revenue (Existing Customers)', 'Month - Year', 'R$')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Revenue is growing steadily with the maximum revenue between April '18 to May '18.
        """)

    fig = plot_scatter(df_user_type_revenue.query("usertype == 'New'"), 
    'month_year', 'payment_value',
    'royalblue', 'Monthly Revenue (New Customers)', 'Month - Year', 'R$')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Revenue is growing steadily with the maximum revenue around November '17. 
        However, the revenue from new customers is much higher than existing customers
        """)

    df_user_ratio = dataframe_new_customer_ratio(df)
    if st.checkbox('Show Ratio Data'):
        st.dataframe(df_user_ratio)

    fig = plot_bar(df_user_ratio, 'month_year', 'NewCusRatio',
                   'Monthly New Customer Ratio', 'crimson', 'Monthly New Customer Ratio', 'Month - Year', '%')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        New Customer ratio has been decreasing over the months.
        """)
