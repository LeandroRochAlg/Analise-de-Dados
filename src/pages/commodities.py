from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
from data_processing import filtered_commodities_data, pandemic_start, war_start
import pandas as pd

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
                text='<a href="https://www.worldbank.org/en/research/commodity-markets" target="_blank">Fonte: Banco Mundial</a>',
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
                text='<a href="https://www.worldbank.org/en/research/commodity-markets" target="_blank">Fonte: Banco Mundial</a>',
                font=dict(size=12),
            )
        ]
    )
}

export_data = {
    'Commodities': ['Complexo soja', 'Carnes', 'Complexo sucroalcooleiro', 'Cereais, farinhas e preparações', 'Produtos Florestais'],
    'Percentual': [40.4, 14.1, 10.4, 9.3, 8.6],
    'Color': ['#0f5132', '#d9534f', '#ffd700', '#5bc0de', '#5cb85c']
}

import_data = {
    'Commodities': ['Adubos e fertilizantes', 'Óleos combustíveis de petróleo', 'Óleos brutos de petróleo'],
    'Percentual': [9.7, 8.5, 3.4],
    'Color': ['#ff7f0e', '#1f77b4', '#2ca02c']
}

exportDf = pd.DataFrame(export_data)
importDf = pd.DataFrame(import_data)

export_fig = px.pie(
    exportDf,
    values='Percentual',
    names='Commodities',
    color='Commodities',
    color_discrete_map={row['Commodities']: row['Color'] for index, row in exportDf.iterrows()}
)
import_fig = px.pie(
    importDf,
    values='Percentual',
    names='Commodities',
    color='Commodities',
    color_discrete_map={row['Commodities']: row['Color'] for index, row in importDf.iterrows()}
)

classification = {
    'Complexo soja': ['Soybeans ($/mt)', 'Soybean oil ($/mt)', 'Soybean meal ($/mt)'],
    'Carnes': ['Beef ** ($/kg)', 'Chicken ** ($/kg)', 'Lamb ** ($/kg)'],
    'Complexo sucroalcooleiro': ['Sugar, EU ($/kg)', 'Sugar, US ($/kg)', 'Sugar, world ($/kg)'],
    'Cereais, farinhas e preparações': ['Barley ($/mt)', 'Maize ($/mt)', 'Sorghum ($/mt)', 'Rice, Thai 5%  ($/mt)', 'Rice, Thai 25%  ($/mt)', 'Rice, Thai A.1 ($/mt)', 'Rice, Viet Namese 5% ($/mt)', 'Wheat, US SRW ($/mt)', 'Wheat, US HRW ($/mt)'],
    'Produtos Florestais': ['Logs, Cameroon ($/cubic meter)', 'Logs, Malaysian ($/cubic meter)', 'Sawnwood, Cameroon ($/cubic meter)', 'Sawnwood, Malaysian ($/cubic meter)', 'Plywood (cents/sheet)'],
    'Adubos e fertilizantes': ['Phosphate rock ($/mt)', 'DAP ($/mt)', 'TSP ($/mt)', 'Urea  ($/mt)', 'Potassium chloride ** ($/mt)'],
    'Óleos combustíveis de petróleo': ['Crude oil, average ($/bbl)', 'Crude oil, Brent ($/bbl)', 'Crude oil, Dubai ($/bbl)', 'Crude oil, WTI ($/bbl)', 'Natural gas, US ($/mmbtu)', 'Natural gas, Europe ($/mmbtu)', 'Liquefied natural gas, Japan ($/mmbtu)'],
    'Óleos brutos de petróleo': ['Crude oil, average ($/bbl)', 'Crude oil, Brent ($/bbl)', 'Crude oil, Dubai ($/bbl)', 'Crude oil, WTI ($/bbl)'],
}

commoditiesList = [commodity for key, value in classification.items() for commodity in value]

layout = html.Div([
    html.H2("Análise de Commodities", className='text-center my-4'),
    html.H3("Preços de Commodities", className='text-center'),
    dcc.Graph(
        id='commodity-prices-specific',
        figure=commodity_figure
    ),
    html.P("Aqui você pode visualizar a evolução dos preços das principais commodities ao longo do tempo."),
    html.Hr(),
    html.H3("Preço do Gás Natural", className='text-center my-4'),
    dcc.Graph(
        id='natural-gas-prices',
        figure=natural_gas_figure
    ),
    html.P("No gráfico acima, você pode comparar a evolução dos preços do gás natural nos EUA e na Europa ao longo do tempo."),
    html.Hr(),
    html.H2("Commodities e seus tipos", className='text-center my-4'),
    html.Div(
        [
            html.Div(
                [
                    html.H3("Tipos de Commodities mais exportadas pelo Brasil", className='text-center my-4'),
                    dcc.Graph(
                        id='export-pie',
                        figure=export_fig
                    )
                ]
            ),
            html.Hr(),
            html.Div(
                [
                    html.H3("Tipos de Commodities mais importadas pelo Brasil", className='text-center my-4'),
                    dcc.Graph(
                        id='import-pie',
                        figure=import_fig
                    )
                ]
            )
        ], className='pie-charts'
    ),
    html.P(html.A("Dados de 2023. Fonte: agência gov", href='https://agenciagov.ebc.com.br/noticias/202401/exportacoes-do-agronegocio-fecham-2023-com-us-166-55-bilhoes-em-vendas#:~:text=Em%20rela%C3%A7%C3%A3o%20ao%20valor%20exportado,florestais%20(8%2C6%25).', target='_blank'), className='data-details'),
    html.Label("Selecione a commodity para visualizar o gráfico de preços:"),
    dcc.Dropdown(
        id='commodity-dropdown',
        options=[{'label': commodity, 'value': commodity} for commodity in commoditiesList],
        value='Crude oil, average ($/bbl)',
        clearable=False,
        className='dropdown'
    ),
    dcc.Graph(id='commodity-prices'),
    html.P("Aqui você pode visualizar a evolução dos preços de diferentes commodities ao longo do tempo. Os tipos de commodities são destacados por cores diferentes no gráfico."),
    html.Hr(),
    html.P("Os dados são provenientes do Banco Mundial e refletem os preços de mercado das commodities.", className='data-details'),
    html.P([html.Strong("Commodities"), " são produtos primários que podem ser comprados e vendidos, como petróleo, soja, minério de ferro, entre outros."], className='data-details'),
])

def register_commodities_callbacks(app):
    @app.callback(
        Output('commodity-prices', 'figure'),
        [Input('commodity-dropdown', 'value')]
    )
    def update_commodity_graph(selected_commodity):
        line_color = 'grey'
        for key, value in classification.items():
            if selected_commodity in value:
                line_color = export_data['Color'][export_data['Commodities'].index(key)] if key in export_data['Commodities'] else import_data['Color'][import_data['Commodities'].index(key)]
                break

        return {
            'data': [
                go.Scatter(
                    x=filtered_commodities_data['Date'],
                    y=filtered_commodities_data[selected_commodity],
                    mode='lines',
                    name=selected_commodity,
                    line=dict(color=line_color)
                ),
                go.Scatter(
                    x=[pandemic_start, pandemic_start],
                    y=[filtered_commodities_data[selected_commodity].min(), filtered_commodities_data[selected_commodity].max()],
                    mode='lines',
                    name='Início da Pandemia',
                    line=dict(color='black', dash='dash')
                ),
                go.Scatter(
                    x=[war_start, war_start],
                    y=[filtered_commodities_data[selected_commodity].min(), filtered_commodities_data[selected_commodity].max()],
                    mode='lines',
                    name='Início da Guerra na Ucrânia',
                    line=dict(color='grey', dash='dot')
                )
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
                        text='<a href="https://www.worldbank.org/en/research/commodity-markets" target="_blank">Fonte: Banco Mundial</a>',
                        font=dict(size=12),
                    )
                ]
            )
        }