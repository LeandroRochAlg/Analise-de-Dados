from dash import dcc, html

app_layout = html.Div(children=[
    html.H1(children='Painel de Indicadores Econômicos do Brasil', className='text-center my-4'),

    dcc.Interval(
        id='interval-component',
        interval=1*60*1000,  # Atualiza a cada minuto
        n_intervals=0
    ),

    html.Div([
        dcc.Dropdown(
            id='variable-dropdown',
            options=[
                {'label': 'Dólar (BRL/USD)', 'value': 'MediaValue'},
                {'label': 'Volatilidade', 'value': 'Volatility'},
                {'label': 'Taxa de Desemprego', 'value': 'Taxa'},
                {'label': 'IPCA', 'value': 'valor'}
            ],
            value=['MediaValue', 'Volatility'],
            multi=True,
            placeholder='Selecione as variáveis'
        ),
    ], style={'width': '50%', 'margin': '0 auto'}),

    dcc.Graph(
        id='dynamic-graph',
    ),
    
    html.H2(children='Exportação e Importação do Brasil (2020-2024)', className='text-center my-4'),

    dcc.Graph(
        id='export-importacao-por-ano',
    ),

    html.H2(children='Taxa de Desemprego e IPCA', className='text-center my-4'),

    dcc.Graph(
        id='unemployment-ipca',
    )
])