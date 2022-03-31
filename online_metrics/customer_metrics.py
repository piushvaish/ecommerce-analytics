from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


def monthly_revenue(df):
    # calculate Revenue for each row and create a new dataframe with YearMonth - Revenue columns
    df_revenue = df.groupby(['month_year'])[
        'payment_value'].sum().reset_index()
    return df_revenue


def monthly_revenue_growth_rate(df):
    # calculate Revenue for each row and create a new dataframe with YearMonth - Revenue columns
    # calculating for monthly revenie growth rate
    # using pct_change() function to see monthly percentage change
    df_revenue = monthly_revenue(df)
    df_revenue['monthly_growth'] = df_revenue['payment_value'].pct_change()
    return df_revenue


def monthly_active_customers(df):
    # creating monthly active customers dataframe by counting unique Customer IDs
    df_monthly_active = df.groupby('month_year')[
        'customer_unique_id'].nunique().reset_index()
    return df_monthly_active


def monthly_order_count(df):
    # creating monthly active customers dataframe by counting unique Customer IDs
    df_monthly_sales = df.groupby('month_year')[
        'order_status'].count().reset_index()
    return df_monthly_sales


def average_revenue_per_order(df):
    # create a new dataframe for average revenue by taking the mean of it
    df_monthly_order_avg = df.groupby(
        'month_year')['payment_value'].mean().reset_index()
    return df_monthly_order_avg

def dataframe_min_purchase(df):
    #create a dataframe contaning CustomerID and first purchase date
    df_min_purchase = df.groupby('customer_unique_id').order_purchase_timestamp.min().reset_index()
    df_min_purchase.columns = ['customer_unique_id','minpurchasedate']
    df_min_purchase['minpurchasedate'] = df_min_purchase['minpurchasedate'].map(lambda date: 100*date.year + date.month)

    #merge first purchase date column to our main dataframe (tx_uk)
    df = pd.merge(df, df_min_purchase, on='customer_unique_id')
    return df

def dataframe_user_type_revenue(df):
    df = dataframe_min_purchase(df)

    #create a column called User Type and assign Existing 
    #if User's First Purchase Year Month before the selected Invoice Year Month
    df['usertype'] = 'New'
    df.loc[df['month_y']>df['minpurchasedate'],'usertype'] = 'Existing'

    #calculate the Revenue per month for each user type
    df_user_type_revenue = df.groupby(['month_y','usertype', 'month_year'])['payment_value'].sum().reset_index()

    return df_user_type_revenue

def dataframe_new_customer_ratio(df):
    df = dataframe_min_purchase(df)

    #create a column called User Type and assign Existing 
    #if User's First Purchase Year Month before the selected Invoice Year Month
    df['usertype'] = 'New'
    df.loc[df['month_y']>df['minpurchasedate'],'usertype'] = 'Existing'
    #create a dataframe that shows new user ratio - we also need to drop NA values (first month new user ratio is 0)
    df_user_ratio = df.query("usertype == 'New'").groupby(['month_year'])['customer_unique_id'].nunique()/df.query("usertype == 'Existing'").groupby(['month_year'])['customer_unique_id'].nunique() 
    df_user_ratio = df_user_ratio.reset_index()

    #dropping nan values that resulted from first and last month
    df_user_ratio = df_user_ratio.dropna()
    df_user_ratio.columns = ['month_year','NewCusRatio']

    #print the dafaframe
    return df_user_ratio

