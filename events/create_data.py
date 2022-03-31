import pandas as pd
import numpy as np
import random
import streamlit as st


@st.cache  # 👈 This function will be cached
def create_dummy_data():
    # Generate dummy data
    # instantiate a dataframe with 100,000 rows
    events = pd.DataFrame({'distinct_id': 0,
                           'name': None,
                           'time': pd.NaT,
                           'user_source': None},
                          index=list(range(100000)))

    # define lists to choose randomly from to populate all the rows
    distinct_id_list = np.arange(5000)+1  # 5,000 distinct users with ids starting from 1
    name_list = ['Cart Created', 'Add Payment',
                 'Order Created', 'Order Processed', 'Shipment Released', 'Order Completed', 'Return & Exchanges']
    date_list = pd.date_range(start='2020-01-01', end='2020-09-01', freq='H')
    user_source_list = ['Organic', 'Non-organic']

    # generate distinct_id, name and time columns
    events['distinct_id'] = events['distinct_id'].apply(lambda x: random.choice(distinct_id_list))
    events['name'] = events['name'].apply(lambda x: random.choice(name_list))
    events['time'] = events['time'].apply(lambda x: random.choice(date_list)).dt.tz_localize('UTC')

    # generate user_source column which is based on distinct_id column
    user_source_dict = {uid: random.choice(user_source_list) for uid in events['distinct_id'].unique()}
    events['user_source'] = events['distinct_id'].map(user_source_dict)
    return events
