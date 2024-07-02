from dash import dcc, html
import plotly.graph_objs as go
from data_processing import unemployment_data_filtered, ipca_filtered_data, pandemic_start, war_start

unemployment_ipca_figure = {
    'data': [
        go.Scatter(
            x=unemployment_data_filtered['Date'],
            y=unemployment_data_filtered['Taxa'],
            mode='lines',
            name='Taxa de Desemprego',
            line=dict(color='purple')
        ),
        go.Scatter(
            x=ipca_filtered_data['data'],
            y=ipca_filtered_data['valor'],
            mode='lines',
            name='IPCA',
            line=dict(color='orange'),
            yaxis='y2'
        ),
        go.Scatter(
            x=[pandemic_start, pandemic_start],
            y=[unemployment_data_filtered['Taxa'].min(), unemployment_data_filtered['Taxa'].max()],
            mode='lines',
            name='Início da Pandemia',
            line=dict(color='black', dash='dash')
        ),
        go.Scatter(
            x=[war_start, war_start],
            y=[unemployment_data_filtered['Taxa'].min(), unemployment_data_filtered['Taxa'].max()],
            mode='lines',
            name='Início da Guerra na Ucrânia',
            line=dict(color='grey', dash='dash')
        )
    ],
    'layout': go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Taxa de Desemprego', titlefont=dict(color='purple'), tickfont=dict(color='purple')),
        yaxis2=dict(title='IPCA', titlefont=dict(color='orange'), tickfont=dict(color='orange'), overlaying='y', side='right'),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50)
    )
}

layout = html.Div([
    html.H2("Taxa de Desemprego e IPCA de bens não-duráveis", className='text-center my-4'),
    dcc.Graph(
        id='unemployment-ipca',
        figure=unemployment_ipca_figure
    ),
    html.P("Aqui você pode visualizar a evolução da taxa de desemprego e do IPCA de bens não-duráveis ao longo do tempo."),
    html.P(["O ", html.Strong("IPCA"), " é o índice oficial de inflação do Brasil, calculado pelo IBGE. Ele mede a variação de preços de um conjunto de produtos e serviços consumidos pelas famílias brasileiras com rendimentos de 1 a 40 salários mínimos."]),
    html.P(["A ", html.Strong("Taxa de Desemprego"), " é a proporção da força de trabalho que está desempregada e procura ativamente por um emprego remunerado."]),
])