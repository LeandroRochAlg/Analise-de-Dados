from dash import dcc, html
import plotly.graph_objs as go
from data_processing import user_data, usd_eur_data, dx_y_data, pandemic_start, war_start

dynamic_figure = {
    'data': [
        go.Scatter(
            x=user_data['Date'],
            y=user_data['MediaValue'],
            mode='lines',
            name='BRL/USD',
            line=dict(color='green')
        ),
        go.Scatter(
            x=usd_eur_data['Date'],
            y=usd_eur_data['MediaValue'],
            mode='lines',
            name='EUR/USD',
            line=dict(color='blue'),
            yaxis='y2'
        ),
        go.Scatter(
            x=[pandemic_start, pandemic_start],
            y=[min(user_data['MediaValue'].min(), usd_eur_data['MediaValue'].min(), dx_y_data['MediaValue'].min()),
               max(user_data['MediaValue'].max(), usd_eur_data['MediaValue'].max())],
            mode='lines',
            name='Início da Pandemia',
            line=dict(color='black', dash='dash')
        ),
        go.Scatter(
            x=[war_start, war_start],
            y=[min(user_data['MediaValue'].min(), usd_eur_data['MediaValue'].min(), dx_y_data['MediaValue'].min()),
               max(user_data['MediaValue'].max(), usd_eur_data['MediaValue'].max())],
            mode='lines',
            name='Início da Guerra na Ucrânia',
            line=dict(color='grey', dash='dash')
        )
    ],
    'layout': go.Layout(
        xaxis=dict(title='Date', showgrid=False),
        yaxis=dict(title='BRL-USD', showgrid=False, titlefont=dict(color='green'), tickfont=dict(color='green')),
        yaxis2=dict(title='EUR/USD', overlaying='y', side='right', showgrid=False, titlefont=dict(color='blue'), tickfont=dict(color='blue')),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50),
        annotations=[
            dict(
                x=0,
                y=-0.11,
                xref='paper',
                yref='paper',
                showarrow=False,
                text=f'Fonte: Yahoo Finance',
                font=dict(size=12),
            )
        ]
    )
}

layout = html.Div([
    html.H2("Taxa de Câmbio e Volatilidade", className='text-center my-4'),
    dcc.Dropdown(
        id='exchange-dropdown',
        options=[
            {'label': 'BRL/USD', 'value': 'BRL/USD'},
            {'label': 'USD/EUR', 'value': 'USD/EUR'},
            {'label': 'DX-Y.NYB', 'value': 'DX-Y.NYB'}
        ],
        value='BRL/USD'
    ),
    dcc.Graph(id='exchange-volatility-graph'),
    html.H2("Variação das moedas em relação ao dólar", className='text-center my-4'),
    dcc.Graph(figure=dynamic_figure),
    html.P("Aqui você pode visualizar a evolução da taxa de câmbio e da volatilidade ao longo do tempo."),
    html.P(["A ", html.Strong("Taxa de Câmbio"), " é o valor de uma moeda em relação a outra. Por exemplo, a taxa de câmbio BRL/USD indica quantos dólares americanos são necessários para comprar um real."]),
    html.P(["A ", html.Strong("Volatilidade"), " é uma medida estatística que indica a variação dos preços de um ativo financeiro ao longo do tempo. Quanto maior a volatilidade, maior a incerteza em relação ao valor do ativo."]),
    html.P(["O Índice do Dólar ", html.Strong("(DX-Y.NYB)"), " é um índice que mede o valor do dólar americano em relação a uma cesta de moedas estrangeiras."]),
])