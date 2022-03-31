import pandas as pd
import streamlit as st 
import numpy as np
import plotly.graph_objs as go
import streamlit as st
from online_metrics.create_data import create_dataframe


def display_bubble_plot():
    st.header("Animated Bubble Plot")

    data = create_dataframe()
    data = data.sample(n=2000, random_state=1)

    # Define figure
    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }

    dataset = data
    dataset['month_year'] = pd.to_datetime(dataset['month_year']).dt.strftime('%Y-%m')
    years = list(dataset['month_year'].sort_values().unique())

    weekdays = list(dataset['order_purchase_day'].sort_values().unique())
    N = len(weekdays) 
    data = []

    year = years[0]

    for day in weekdays:

        df = dataset[(dataset['order_purchase_day'] == day) & (dataset['month_year'] == year)]

        data.append(go.Scatter(x=df['freight_value'],
                            y=df['payment_value'],
                            text=df['order_purchase_day'],
                                mode='markers',
                            marker=dict(
                                size= df['price'],
                                sizemode = "area",
                                color= np.random.rand(N), #set color equal to a variable
                                colorscale=  'rdylgn', # one of plotly colorscales
                                showscale=False
                            ),
                            name=day))
    
    layout = {
        'xaxis': {
            'title': 'Freight Value',
            #'tickformat' : '%B <br>%Y',
            'type' :'linear',
            #'autorange': True,
            'range' : [0, 110],
            'showline' : True,
            'showticklabels' : True,
            'linecolor' : 'rgb(204, 204, 204)',
            'linewidth' : 2,
            'ticks': 'outside',
            'tickfont' : dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )
            
        },

        'yaxis': {
            'title': 'Payment Value',
            #'autorange': True,
            'range' : [0 , 2500],
            'showline' : True,
            'showticklabels' : True,
            'linecolor' : 'rgb(204, 204, 204)',
            'linewidth' : 2,
            'ticks': 'outside',
            'tickfont' : dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )
        },
        'hovermode': 'closest',
        'showlegend': True,
        'title_text' : "Freight vs Payment Value per Weekday",
        'title_font' : dict(family='Arial',
                size=20,
                color='rgb(82, 82, 82)'),
        'legend_title' : "Weekday",
        'legend_traceorder': "grouped",
        'legend_title_font_color' : "green",
        'legend_title_font': dict(family='Arial',
                size=15,
                color='rgb(82, 82, 82)'),
        'plot_bgcolor' : 'rgb(223, 232, 243)',
        'updatemenus': [{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 1200, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 100, 'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 80},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }],

        'sliders': [{
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 14},
                'prefix': 'Month-Year:',
                'visible': True,
                'xanchor': 'right'},
            'transition': {'duration': 500, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': []
        }]

    }

    frames = []

    for year in years[1:]:

        frame = {'data': [], 'name': year}

        for day in weekdays:

            df = dataset[(dataset['order_purchase_day'] == day) & (dataset['month_year'] == year)]

            frame['data'].append(go.Scatter(x=df['freight_value'],
                            y=df['payment_value'],
                            text=df['order_purchase_day'],
                                        mode='markers',
                                        marker=dict(
                                            size= df['price'],
                                            sizemode =  "area",
                                            color= np.random.rand(N), #set color equal to a variable
                                            colorscale=  'rdylgn', # one of plotly colorscales
                                            showscale=False
                                        ),
                                        name=day))


        frames.append(go.Frame(data=frame['data'], name=frame['name']))

        slider_step = {
            'args': [
                [year],
                {'frame': {'duration': 1200, 'redraw': True},
                'mode': 'immediate',
                'transition': {'duration': 500}}
            ],
            'label': year,
            'method': 'animate'
        }

        layout['sliders'][0]['steps'].append(slider_step)

    fig = go.Figure(data=data, layout=layout, frames=frames)
    return st.plotly_chart(fig)



