from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from plotly import graph_objs as go
from online_metrics.customer_metrics import dataframe_min_purchase
# https://towardsdatascience.com/data-driven-growth-with-python-part-1-know-your-metrics-812781e66a5b


def retention_table(df):
    #df = dataframe_min_purchase(df)
    # Monthly Retention Rate = Retained Customers From Prev. Month/Active Customers Total (using crosstab)

    # identifying active users are active by looking at their revenue per month
    #df_user_purchase = df.groupby(['customer_unique_id','month_y'])['payment_value'].sum().reset_index()

    # identifying active users are active by looking at their order count per month
    df_user_purchase = df.groupby(['customer_unique_id', 'month_y'])[
        'payment_value'].count().reset_index()
    # create retention matrix with crosstab using purchase
    df_retention = pd.crosstab(
        df_user_purchase['customer_unique_id'], df_user_purchase['month_y']).reset_index()

    # creating an array of dictionary which keeps Retained & Total User count for each month
    months = df_retention.columns[2:]
    retention_array = []
    for i in range(len(months)-1):
        retention_data = {}
        selected_month = months[i+1]
        prev_month = months[i]
        retention_data['month_y'] = int(selected_month)
        retention_data['TotalUserCount'] = df_retention[selected_month].sum()
        retention_data['RetainedUserCount'] = df_retention[(df_retention[selected_month] > 0) & (
            df_retention[prev_month] > 0)][selected_month].sum()
        retention_array.append(retention_data)

    # convert the array to dataframe and calculate Retention Rate
    df_retention = pd.DataFrame(retention_array)
    df_retention['RetentionRate'] = df_retention['RetainedUserCount'] / \
        df_retention['TotalUserCount']
    df_retention['ChurnRate'] = 1 - df_retention['RetentionRate']
    return df_retention


@st.cache
def plot_bar(df, col1, col2, name, color, y_range, title, xaxis_title, yaxis_title):
    plot_data = [
        go.Bar(
            x=df[col1],
            y=df[col2],
            textposition='outside',
            name=name,
            marker_color=color
        )
    ]

    plot_layout = go.Layout(
        xaxis=dict(
            type="category",
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            tickangle=90,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            range=y_range,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)'
            ),
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white',
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title)

    return go.Figure(data=plot_data, layout=plot_layout)


def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.

    Example
    -------
    Say you want to get the 3rd month for every user:
        df.sort(['UserId', 'OrderTime', inplace=True)
        df = df.groupby('UserId').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df['cohort_period'] = np.arange(len(df)) + 1
    return df


def cohort_based_retention_rate(df):
    dfr = df[['order_id', 'order_purchase_timestamp', 'customer_unique_id',
              'payment_value', 'product_id', 'delivery_against_estimated']]
    # Create a period column based on the OrderDate Since we're doing monthly cohorts, we'll be looking at the total monthly behavior of our users. Therefore, we don't want granular OrderDate data (right now).
    dfr['order_period'] = dfr['order_purchase_timestamp'].apply(
        lambda x: x.strftime('%Y-%m'))
    # Determine the user's cohort group (based on their first order)
    dfr.set_index('customer_unique_id', inplace=True)

    dfr['cohort_group'] = dfr.groupby(
        level=0)['order_purchase_timestamp'].min().apply(lambda x: x.strftime('%Y-%m'))
    dfr.reset_index(inplace=True)

    # Rollup data by CohortGroup & OrderPeriod Since we're looking at monthly cohorts, we need to aggregate users, orders, and amount spent by the CohortGroup within the month (OrderPeriod).

    grouped = dfr.groupby(['cohort_group', 'order_period'])

    # count the unique users, orders, and total revenue per Group + Period
    cohorts = grouped.agg({'customer_unique_id': pd.Series.nunique,
                           'order_id': pd.Series.nunique,
                           'payment_value': np.sum})

    # make the column names more meaningful
    cohorts.rename(columns={'customer_unique_id': 'total_users',
                            'order_id': 'total_orders'}, inplace=True)

    cohorts = cohorts.groupby(level=0).apply(cohort_period)

    # reindex the DataFrame
    cohorts.reset_index(inplace=True)
    cohorts.set_index(['cohort_group', 'cohort_period'], inplace=True)

    # create a Series holding the total size of each CohortGroup
    cohort_group_size = cohorts['total_users'].groupby(level=0).first()
    user_retention = cohorts['total_users'].unstack(
        0).divide(cohort_group_size, axis=1)

    return user_retention

# def cohort_based_churn_rate(df):
#     user_churn = np.round((1 - df), 3)
#     return user_churn


def plot_heatmap_log(df, colorscale, title):
    # Log: https://www.mathsisfun.com/algebra/logarithms.html
    plot_data = [
        go.Heatmap(
            z=np.round(np.log(df.values), 2),
            x=df.columns,
            y=df.index,
            colorscale = colorscale
        )
    ]

    axis_template = dict(autorange=True, type='category',
                        showgrid=False, zeroline=False,
                        linecolor='black', showticklabels=True,
                        ticks='')

    plot_layout = go.Layout(
        xaxis=axis_template,
        yaxis=axis_template,
        showlegend=False,
        autosize=True,
        xaxis_title="Cohort Period",
        yaxis_title="Cohort",
        font_family="Courier New",
        font_color="blue",
        title_font_family="Times New Roman",
        title_font_color="black",
        title_font_size=30,
        title=title,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Arial"))

    return go.Figure(data=plot_data, layout=plot_layout)

def plot_heatmap(df, colorscale, title):
    # Log: https://www.mathsisfun.com/algebra/logarithms.html
    plot_data = [
        go.Heatmap(
            z=np.round(df.values, 2),
            x=df.columns,
            y=df.index,
            colorscale = colorscale
        )
    ]

    axis_template = dict(autorange=True, type='category',
                        showgrid=False, zeroline=False,
                        linecolor='black', showticklabels=True,
                        ticks='')

    plot_layout = go.Layout(
        xaxis=axis_template,
        yaxis=axis_template,
        showlegend=False,
        autosize=True,
        xaxis_title="Cohort Period",
        yaxis_title="Cohort",
        font_family="Courier New",
        font_color="blue",
        title_font_family="Times New Roman",
        title_font_color="black",
        title_font_size=30,
        title=title,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Arial"))

    return go.Figure(data=plot_data, layout=plot_layout)
    