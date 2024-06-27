from dash import dcc, html
import plotly.graph_objs as go
from data_processing import user_data, pandemic_start, war_start

dynamic_figure = {
    'data': [
        go.Scatter(
            x=user_data['Date'],
            y=user_data['MediaValue'],
            mode='lines',
            name='BRL/USD',
            line=dict(color='blue')
        ),
        go.Scatter(
            x=user_data['Date'],
            y=user_data['Volatility'],
            mode='lines',
            name='Volatility',
            line=dict(color='red'),
            yaxis='y2'
        ),
        go.Scatter(
            x=[pandemic_start, pandemic_start],
            y=[user_data['MediaValue'].min(), user_data['MediaValue'].max()],
            mode='lines',
            name='Início da Pandemia',
            line=dict(color='black', dash='dash')
        ),
        go.Scatter(
            x=[war_start, war_start],
            y=[user_data['MediaValue'].min(), user_data['MediaValue'].max()],
            mode='lines',
            name='Início da Guerra na Ucrânia',
            line=dict(color='grey', dash='dash')
        )
    ],
    'layout': go.Layout(
        title='Painel de Taxa de Câmbio e Volatilidade BRL/USD',
        xaxis=dict(title='Date'),
        yaxis=dict(title='BRL/USD', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
        yaxis2=dict(title='Volatility', titlefont=dict(color='red'), tickfont=dict(color='red'), overlaying='y', side='right'),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50)
    )
}

layout = html.Div([
    html.H2("Taxa de Câmbio e Volatilidade BRL/USD", className='text-center my-4'),
    dcc.Graph(
        id='taxaCambio-volatilidade-BRL-USD',
        figure=dynamic_figure
    ),
])