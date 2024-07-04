from dash import dcc, html
import plotly.graph_objs as go
from data_processing import unemployment_data_filtered, ipca_filtered_data, pandemic_start, war_start

unemployment_figure = {
    'data': [
        go.Scatter(
            x=unemployment_data_filtered['Date'],
            y=unemployment_data_filtered['Taxa'],
            mode='lines',
            name='Taxa de Desemprego',
            line=dict(color='#0f5132')
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
            line=dict(color='grey', dash='dot')
        )
    ],
    'layout': go.Layout(
        xaxis=dict(title='Data', showgrid=False),
        yaxis=dict(title='Taxa de Desemprego'),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50),
        annotations=[
            dict(
                x=0,
                y=-0.11,
                xref='paper',
                yref='paper',
                showarrow=False,
                text=f'<a href="https://www.ibge.gov.br/estatisticas/sociais/trabalho/9173-pesquisa-nacional-por-amostra-de-domicilios-continua-trimestral.html?=&t=series-historicas&utm_source=landing&utm_medium=explica&utm_campaign=desemprego" target="_blank">Fonte: IBGE</a>',
                font=dict(size=12),
            )
        ]
    )
}

ipca_figure = {
    'data': [
        go.Scatter(
            x=ipca_filtered_data['data'],
            y=ipca_filtered_data['valor'],
            mode='lines',
            name='IPCA',
            line=dict(color='#5cb85c')
        ),
            go.Scatter(
            x=[pandemic_start, pandemic_start],
            y=[ipca_filtered_data['valor'].min(), ipca_filtered_data['valor'].max()],
            mode='lines',
            name='Início da Pandemia',
            line=dict(color='black', dash='dash')
        ),
        go.Scatter(
            x=[war_start, war_start],
            y=[ipca_filtered_data['valor'].min(), ipca_filtered_data['valor'].max()],
            mode='lines',
            name='Início da Guerra na Ucrânia',
            line=dict(color='grey', dash='dot')
        )
    ],
    'layout': go.Layout(
        xaxis=dict(title='Data', showgrid=False),
        yaxis=dict(title='IPCA'),
        legend=dict(x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50),
        annotations=[
            dict(
                x=0,
                y=-0.11,
                xref='paper',
                yref='paper',
                showarrow=False,
                text=f'<a href="https://dadosabertos.bcb.gov.br/dataset/10841-indice-de-precos-ao-consumidor-amplo-ipca---bens-nao-duraveis" target="_blank">Fonte: Dados Abertos</a>',
                font=dict(size=12),
            )
        ]
    )
}

layout = html.Div([
    html.H2("Desemprego e IPCA", className='text-center my-4'),
    html.H3("Taxa de Desemprego", className='text-center my-4'),
    dcc.Graph(
        id='unemployment',
        figure=unemployment_figure
    ),
    html.P("Aqui você pode visualizar a evolução da taxa de desemprego no Brasil ao longo do tempo."),
    html.Hr(),
    html.H3("IPCA de Bens Não-Duráveis", className='text-center my-4'),
    dcc.Graph(
        id='ipca',
        figure=ipca_figure
    ),
    html.P("Aqui você pode visualizar a evolução do IPCA de bens não-duráveis ao longo do tempo."),
    html.Hr(),
    html.P(["O ", html.Strong("IPCA"), " é o índice oficial de inflação do Brasil, calculado pelo IBGE. Ele mede a variação de preços de um conjunto de produtos e serviços consumidos pelas famílias brasileiras com rendimentos de 1 a 40 salários mínimos."], className='data-details'),
    html.P(["A ", html.Strong("Taxa de Desemprego"), " é a proporção da força de trabalho que está desempregada e procura ativamente por um emprego remunerado."], className='data-details'),
])