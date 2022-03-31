import pandas as pd
import numpy as np
import streamlit as st


@st.cache
def create_dataframe():
    # loading data
    customers_ = pd.read_csv("Data/olist_customers_dataset.csv")
    order_items_ = pd.read_csv("Data/olist_order_items_dataset.csv")
    order_payments_ = pd.read_csv("Data/olist_order_payments_dataset.csv")
    orders_ = pd.read_csv("Data/olist_orders_dataset.csv")
    products_ = pd.read_csv("Data/olist_products_dataset.csv")

    # dataframe
    df1 = order_payments_.merge(order_items_, on='order_id')
    df2 = df1.merge(orders_, on='order_id')
    df = df2.merge(customers_, on='customer_id')

    # converting date columns to datetime
    date_columns = ['shipping_limit_date', 'order_purchase_timestamp', 'order_approved_at',
                    'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S')

    # cleaning up name columns
    df['customer_city'] = df['customer_city'].str.title()
    df['payment_type'] = df['payment_type'].str.replace('_', ' ').str.title()
    # engineering new/essential columns
    df['delivery_against_estimated'] = (
        df['order_estimated_delivery_date'] - df['order_delivered_customer_date']).dt.days
    df['order_purchase_year'] = df.order_purchase_timestamp.apply(
        lambda x: x.year)
    df['order_purchase_month'] = df.order_purchase_timestamp.apply(
        lambda x: x.month)
    df['order_purchase_dayofweek'] = df.order_purchase_timestamp.apply(
        lambda x: x.dayofweek)
    df['order_purchase_hour'] = df.order_purchase_timestamp.apply(
        lambda x: x.hour)
    df['order_purchase_day'] = df['order_purchase_dayofweek'].map(
        {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'})
    df['order_purchase_mon'] = df.order_purchase_timestamp.apply(lambda x: x.month).map(
        {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
    # Changing the month attribute for correct ordenation
    df['month_year'] = df['order_purchase_month'].astype(
        str).apply(lambda x: '0' + x if len(x) == 1 else x)
    df['month_year'] = df['order_purchase_year'].astype(
        str) + '-' + df['month_year'].astype(str)
    # creating year month column
    df['month_y'] = df['order_purchase_timestamp'].map(
        lambda date: 100*date.year + date.month)
    # dropping missing values
    df.dropna(inplace=True)
    df.isnull().values.any()

    # excluding incomplete 2012 data and displaying first 3 rows of master dataframe
    df = df.query("month_year != '2016-12' and month_year != '2016-10'")

    return df
