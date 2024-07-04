from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
from data_processing import filtered_commodities_data, pandemic_start, war_start

# Gráfico de preços de commodities ao longo do tempo
commodity_figure = {
    'data': [
        go.Scatter(
            x=filtered_commodities_data['Date'],
            y=filtered_commodities_data['Crude oil, average ($/bbl)'],
            mode='lines',
            name='Petróleo ($/bbl)',
            line=dict(color='#0f5132')
        ),
        go.Scatter(
            x=filtered_commodities_data['Date'],
            y=filtered_commodities_data['Soybeans ($/mt)'],
            mode='lines',
            name='Soja ($/mt)',
            line=dict(color='#d9534f')
        ),
        go.Scatter(
            x=filtered_commodities_data['Date'],
            y=filtered_commodities_data['Iron ore, cfr spot ($/dmtu)'],
            mode='lines',
            name='Ferro ($/dmtu)',
            line=dict(color='#ffd700')
        ),
        go.Scatter(
            x=[pandemic_start, pandemic_start],
            y=[min(filtered_commodities_data['Crude oil, average ($/bbl)'].min(), filtered_commodities_data['Soybeans ($/mt)'].min(), filtered_commodities_data['Iron ore, cfr spot ($/dmtu)'].min()), max(filtered_commodities_data['Crude oil, average ($/bbl)'].max(), filtered_commodities_data['Soybeans ($/mt)'].max(), filtered_commodities_data['Iron ore, cfr spot ($/dmtu)'].max())],
            mode='lines',
            name='Início da Pandemia',
            line=dict(color='black', dash='dash')
        ),
        go.Scatter(
            x=[war_start, war_start],
            y=[min(filtered_commodities_data['Crude oil, average ($/bbl)'].min(), filtered_commodities_data['Soybeans ($/mt)'].min(), filtered_commodities_data['Iron ore, cfr spot ($/dmtu)'].min()), max(filtered_commodities_data['Crude oil, average ($/bbl)'].max(), filtered_commodities_data['Soybeans ($/mt)'].max(), filtered_commodities_data['Iron ore, cfr spot ($/dmtu)'].max())],
            mode='lines',
            name='Início da Guerra na Ucrânia',
            line=dict(color='grey', dash='dot')
        ),
    ],
    'layout': go.Layout(
        xaxis=dict(title='Data', showgrid=False),
        yaxis=dict(title='Preço ($/mmbtu)'),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50),
        annotations=[
            dict(
                x=0,
                y=-0.11,
                xref='paper',
                yref='paper',
                showarrow=False,
                text='Fonte: Banco Mundial',
                font=dict(size=12),
            )
        ]
    )
}

natural_gas_figure = {
    'data': [
        go.Scatter(
            x=filtered_commodities_data['Date'],
            y=filtered_commodities_data['Natural gas, US ($/mmbtu)'],
            mode='lines',
            name='Preço do Gás Natural nos EUA',
            line=dict(color='#0f5132')
        ),
        go.Scatter(
            x=filtered_commodities_data['Date'],
            y=filtered_commodities_data["Natural gas, Europe ($/mmbtu)"],
            mode='lines',
            name='Preço do Gás Natural na Europa',
            line=dict(color='#d9534f')
        ),
        go.Scatter(
            x=[pandemic_start, pandemic_start],
            y=[min(filtered_commodities_data['Natural gas, US ($/mmbtu)'].min(), filtered_commodities_data['Natural gas, Europe ($/mmbtu)'].min()), max(filtered_commodities_data['Natural gas, US ($/mmbtu)'].max(), filtered_commodities_data['Natural gas, Europe ($/mmbtu)'].max())],
            mode='lines',
            name='Início da Pandemia',
            line=dict(color='black', dash='dash')
        ),
        go.Scatter(
            x=[war_start, war_start],
            y=[min(filtered_commodities_data['Natural gas, US ($/mmbtu)'].min(), filtered_commodities_data['Natural gas, Europe ($/mmbtu)'].min()), max(filtered_commodities_data['Natural gas, US ($/mmbtu)'].max(), filtered_commodities_data['Natural gas, Europe ($/mmbtu)'].max())],
            mode='lines',
            name='Início da Guerra na Ucrânia',
            line=dict(color='grey', dash='dot')
        ),
    ],
    'layout': go.Layout(
        xaxis=dict(title='Data', showgrid=False),
        yaxis=dict(title='Preço (USD)'),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50),
        annotations=[
            dict(
                x=0,
                y=-0.11,
                xref='paper',
                yref='paper',
                showarrow=False,
                text='Fonte: Banco Mundial',
                font=dict(size=12),
            )
        ]
    )
}

layout = html.Div([
    html.H2("Análise de Commodities", className='text-center my-4'),
    html.H3("Preços de Commodities", className='text-center'),
    dcc.Graph(
        id='commodity-prices',
        figure=commodity_figure
    ),
    html.P("Aqui você pode visualizar a evolução dos preços das principais commodities ao longo do tempo."),
    html.H3("Preço do Gás Natural", className='text-center my-4'),
    dcc.Graph(
        id='natural-gas-prices',
        figure=natural_gas_figure
    ),
    html.P("No gráfico acima, você pode comparar a evolução dos preços do gás natural nos EUA e na Europa ao longo do tempo."),
    html.P("Os dados são provenientes do Banco Mundial e refletem os preços de mercado das commodities.", className='data-details'),
])