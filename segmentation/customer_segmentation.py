import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
# Fetaure Selection
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import streamlit as st


def create_rfm(df):
    pin_date = max(df.order_purchase_timestamp) + dt.timedelta(1)
    # Membuat dataframe RFM
    rfm = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (pin_date - x.max()).days,
        'order_item_id': 'count',
        'payment_value': 'sum'})

    # Merubah nama kolom
    rfm.rename(columns={'order_purchase_timestamp': 'Recency',
                        'order_item_id': 'Frequency',
                        'payment_value': 'Monetary'}, inplace=True)
    return rfm


def remove_outliers(df):
    outliers1_drop = df[(df['Monetary'] > 1500)].index
    df.drop(outliers1_drop, inplace=True)
    return df

@st.cache
def create_groups(df):
    # Create customer groups based on Recency, Frequency, and Monetary
    # Because Recency if the fewer days the better, it will make the order in reverse

    r_labels = range(3, 0, -1)
    r_groups = pd.qcut(df.Recency, q=3, labels=r_labels).astype('int')

    # Because the Frequency is very much at the value of 1, you cannot use qcut,
    # because the value will be skewed to the most

    f_groups = pd.qcut(df.Frequency.rank(method='first'), 3).astype('str')
    #df['F'] = np.where((df['Frequency'] != 1) & (df['Frequency'] != 2), 3, df.Frequency)

    m_labels = range(1, 4)
    m_groups = pd.qcut(df.Monetary, q=3, labels=m_labels).astype('int')

    # Create a column based on the group that has been created

    df['R'] = r_groups.values
    df['F'] = f_groups.values
    df['M'] = m_groups.values

    # Change the input column F to categorical

    df['F'] = df['F'].replace({'(0.999, 30650.0]': 1,
                               '(30650.0, 61299.0]': 2,
                               '(61299.0, 91948.0]': 3}).astype('int')

    # Combine these three columns
    df['RFM_Segment'] = df.apply(lambda x: str(
        x['R']) + str(x['F']) + str(x['M']), axis=1)
    df['RFM_Score'] = df[['R', 'F', 'M']].sum(axis=1)

    # Create labels based on RFM_Score
    score_labels = ['Low', 'Medium', 'High']
    score_groups = pd.qcut(
        df.RFM_Score, q=3, labels=score_labels).astype('object')

    df['RFM_Level'] = score_groups.values
    return df

@st.cache
def normalize_data(df):

    df_log = df[['Recency', 'Monetary']].apply(np.log, axis=1).round(3)
    df_log['Frequency'] = stats.boxcox(df['Frequency'])[0]
    return df_log

def scaled_data(df_log, df):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_log)
    # Create a new dataframe after scaling
    df_scaled = pd.DataFrame(df_scaled, index = df.index, columns = df_log.columns)
    return df_scaled
    
@st.cache
def create_clusters(df, rfm):
    #Choose n_clusters = 4 according to the elbow method
    clus = KMeans(n_clusters= 4, n_init=10, init= 'k-means++', max_iter= 300)
    clus.fit(df)
    # Enter everything into the scaling data
    df['K_Cluster'] = clus.labels_
    df['RFM_Level'] = rfm.RFM_Level
    df.reset_index(inplace = True)
    return df
