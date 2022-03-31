import streamlit as st
from pathlib import Path
from PIL import Image

image_folder = Path("olist_images/")

def display_home():
    st.header("Welcome to Analytics Dashboard")
    st.markdown("""
    This dashboard showcases what we can do for our clients using the data from:
    * <a href="https://www.olist.com/" target="_blank">Olist</a>, 
    the largest department store in Brazilian marketplaces. Olist connects small businesses from all over Brazil to channels without 
    hassle and with a single contract. 
    Those merchants are able to sell their products through the Olist Store 
    and ship them directly to the customers using Olist logistics partners.
    * Dummy Data. 
    """ , unsafe_allow_html=True)

    image = Image.open(image_folder / 'olist_webpage.PNG')
    st.image(image, caption='https://olist.com/', use_column_width=True)

    st.markdown(""" 
    After a customer purchases the product from Olist Store a seller gets 
    notified to fulfill that order. Once the customer receives the product, 
    or the estimated delivery date is due, the customer gets a satisfaction 
    survey by email where he can give a note for the purchase experience 
    and write down some comments. 
    """ , unsafe_allow_html=True)

    # landing page
    image = Image.open('olist_images/olist_landing_page.png')
    st.image(image, caption='Landing Page', use_column_width=True)

    st.title("Data Description")
    st.subheader("Orders")
    st.markdown("""
    The dataset has information of 100k orders from 2016 to 2018 made at multiple 
    marketplaces in Brazil. Its features allow viewing an order from multiple 
    dimensions: from order status, price, payment and freight performance to 
    customer location, geolocation, product attributes and finally reviews written 
    by customers.  
    """)

    # Order Data Schema
    image = Image.open('olist_images/olist_data_schema.png')
    st.image(image, caption='Orders Data Schema', use_column_width=True)

    st.subheader("Marketing")
    st.markdown(""" 
    Marketing funnel dataset from sellers that filled-in requests of contact to 
    sell their products on Olist Store. 
    The dataset has information of 8k Marketing Qualified Leads (MQLs) that 
    requested contact between Jun. 1st 2017 and Jun 1st 2018. 
    They were randomly sampled from the total of MQLs. 
    Its features allow viewing a sales process from multiple dimensions: 
    lead category, catalog size, behaviour profile, etc. 
    """)

    # Order Data Schema
    image = Image.open('olist_images/olist_marketing_dataset_schema.png')
    st.image(image, caption='Marketing Data Schema', use_column_width=True)

    