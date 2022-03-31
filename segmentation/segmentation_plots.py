from plotly import graph_objs as go
import streamlit as st


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

@st.cache
def plot_parallel_coordinate(df):
    sample = df.sample(frac=0.1, replace=True, random_state=1)
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=sample['K_Cluster'],
                   colorscale=[[0, 'purple'], [
                       0.5, 'lightseagreen'], [1, 'gold']],
                   showscale=True,
                   cmin=-5.5,
                   cmax=3),
        dimensions=list([
            dict(range=[0, 3],
                constraintrange=[0, 3],
                label='Cluster', values=sample['K_Cluster']),
            dict(range=[-5.5, 1.5],
                constraintrange=[-5.5, 1.5],
                label='Recency', values=sample['Recency']),
            dict(range=[-.5, 2.5],
                 constraintrange=[-.5, 2.5],
                label='Frequency', values=sample['Frequency']),
            dict(range=[-3, 3],
                 constraintrange=[-3, 3],
                label='Monetary', values=sample['Monetary'])
        ])
        )
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig


@st.cache
def plot_snake(df):
    traces=[]

    for x, cluster in df.groupby('K_Cluster'):

        traces.append(go.Scatter(x=cluster.Metrics, y=cluster.Value, name=x, mode='lines'))
        
        plot_layout = go.Layout(
        xaxis=dict(
            type="category",
            showline=False,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            tickangle=0,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)'
            ),
        ),
        # autosize=True,
        # showlegend=True,
        margin=dict(
            autoexpand=False,
            # l=100,
            # r=20,
            # t=110,
        ),
        plot_bgcolor='white',
        title='Snake Plot for Cluster',
        xaxis_title='Metrics',
        yaxis_title='Value')

    return go.Figure(data=traces, layout=plot_layout)
