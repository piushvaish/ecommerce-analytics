import seaborn as sns
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import streamlit as st


@st.cache
def plot_scatter(df, col1, col2, color, title, xaxis_title, yaxis_title):
    plot_data = [
        go.Scatter(
            x=df[col1],
            y=df[col2],
            line=dict(color=color,
                      width=4,
                      dash='dash')
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
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
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


@st.cache
def plot_bar(df, col1, col2, name, color, title, xaxis_title, yaxis_title):
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


