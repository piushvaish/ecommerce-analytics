import pandas as pd
import streamlit as st
from scipy import stats
from online_metrics.create_data import create_dataframe
from segmentation.customer_segmentation import create_rfm, remove_outliers, create_groups, normalize_data, scaled_data, create_clusters
from segmentation.segmentation_plots import plot_parallel_coordinate, plot_snake, plot_bar


def display_segmentation():
    st.header("Customer Segmentation")

    st.markdown("""
    <h4 style="color:#26608e;">Using RFM (Recency - Frequency - Monetary Value) Clustering</h2>
    <ul>
    <li>Low Value: Customers who are less active than others, not very frequent buyer/visitor and generates very low - zero - maybe negative revenue.</li>
    <li>Mid Value: Using platform fairly frequent and generates moderate revenue.</li>
    <li>High Value: High Revenue, Frequency and low Inactivity.</li>
    </ul>

    """, unsafe_allow_html=True)

    df = create_dataframe()
    rfm = create_rfm(df)

    rfm = remove_outliers(rfm)

    rfm = create_groups(rfm)
    rfm_log = normalize_data(rfm)
    rfm_scaled = scaled_data(rfm_log, rfm)

    rfm_scaled = create_clusters(rfm_scaled, rfm)

    fig = plot_parallel_coordinate(rfm_scaled)

    st.plotly_chart(fig)

    rfm_melted = pd.melt(frame=rfm_scaled, id_vars=['customer_unique_id', 'RFM_Level', 'K_Cluster'],
                         var_name='Metrics', value_name='Value')
    fig = plot_snake(rfm_melted)
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.write("""
        Low (1 & 0): The frequency is not too high compared to the nominal transaction, but the last time he was trading was fast
        Medium (2): The frequency is quite high and the transaction nominal is quite high, but the last time he was trading was quite long
        High (3): The frequency for spending is high and the nominal spent is also a lot, but the last transaction time is long
        """)

    # How many customers are there by category?
    rfm_cus_level = rfm_scaled.groupby(
        'RFM_Level')['customer_unique_id'].nunique().reset_index()
    fig = plot_bar(rfm_cus_level, 'RFM_Level', 'customer_unique_id', 'customer_unique_id',
                   'crimson', 'Customer Based on RFM Level', 'RFMLevel', 'Amount of Customer')
    st.plotly_chart(fig)
    with st.beta_expander("See explanation"):
        st.markdown("""
        <ul>
        <li>Low: A customer who doesn't make frequent purchases and the transaction nominal is low but the last time he made transactions was fast. There are 36,000 customers of this type.</li>
        <ul>
        <li>
        Action: You can try giving discounts or offers at an affordable nominal so that the conversion rate increases because there are quite a lot of customers in the Bronze category
        </li>
        </ul>
        </ul>
        <ul>
        <li>Medium: A customer who makes purchases quite often and the transaction nominal is quite high, but the last transaction time was quite long. There are 42,000 customers of this type.</li>
        <ul>
        <li>
        Action: Given a combination of discounts and post-transaction campaigns to increase purchases by using a personnelized email that can give a personal touch.</li>
        </ul>
        </ul>
        <ul>
        <li>High: Customers who frequently shop and have a lot of nominal transactions, but the last transaction took a long time. There are 15,000 customers of this type.
        </li>
        <ul>
        <li>
        Action: More often given the campaign after making transactions to make purchases again. You can also give rewards because they are more likely to make transactions and the nominal is high.</li>
        </ul>
        </ul> """, unsafe_allow_html=True)
