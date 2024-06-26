import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
import numpy as np
import plotly.express as px

# Carregar os dados
user_data = pd.read_csv('Dados Tratados/USD-BRL-Tratado.csv')
user_data['Date'] = pd.to_datetime(user_data['Date'])
user_data.sort_values('Date', inplace=True)

# Calcular a variação diária (log returns)
user_data['Log_Returns'] = np.log(user_data['MediaValue'] / user_data['MediaValue'].shift(1))

# Calcular a volatilidade usando uma janela móvel de 30 dias (aproximadamente um mês)
user_data['Volatility'] = user_data['Log_Returns'].rolling(window=30).std() * np.sqrt(252)  # Anualizando a volatilidade

# Filtrar o período de interesse (dois anos antes da guerra até o presente)
start_date = datetime.datetime(2020, 2, 1)
filtered_data = user_data[user_data['Date'] >= start_date]

# Carregar os dados de exportação e importação
export_data = pd.read_csv('Dados Tratados/Exportação-TRATADO.csv')
import_data = pd.read_csv('Dados Tratados/Importação-TRATADO.csv')
# Filtrar dados apenas do Brasil
export_data_brazil = export_data[export_data['Países'] == 'Brasil']
import_data_brazil = import_data[import_data['Países'] == 'Brasil']

# Filtrar dados para os anos de 2020 a 2024
export_data_brazil = export_data_brazil[(export_data_brazil['Ano'] >= 2020) & (export_data_brazil['Ano'] <= 2024)]
import_data_brazil = import_data_brazil[(import_data_brazil['Ano'] >= 2020) & (import_data_brazil['Ano'] <= 2024)]

# Agrupar dados por ano
export_data_grouped = export_data_brazil.groupby('Ano')['Valor US$ FOB'].sum().reset_index()
import_data_grouped = import_data_brazil.groupby('Ano')['Valor US$ FOB'].sum().reset_index()

# Carregar os dados de desemprego
unemployment_data = pd.read_csv('Dados Tratados/Desemprego-TRATADO.csv')

# Mapear os meses para valores numéricos
month_map = {
    'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
    'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
}
unemployment_data['Mes'] = unemployment_data['Mes'].map(month_map)
unemployment_data['Date'] = pd.to_datetime(unemployment_data['Ano'].astype(str) + '-' + unemployment_data['Mes'] + '-01')

# Filtrar dados de desemprego para os anos de 2020 a 2024
unemployment_data_filtered = unemployment_data[(unemployment_data['Ano'] >= 2020) & (unemployment_data['Ano'] <= 2024)]

# Inicializar o Dash app
app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div(children=[
    html.H1(children='Painel de Análises Econômicas do Brasil', className='text-center my-4'),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2020, 2025)],
        value=[2020],
        multi=True,
        placeholder='Selecione o ano'
    ),

    dcc.Graph(
        id='taxaCambio-volatilidade-BRL-USD'
    ),
    
    html.H2(children='Exportação e Importação do Brasil (2020-2024)', className='text-center my-4'),

    dcc.Graph(
        id='export-importacao-por-ano'
    ),

    html.H2(children='Taxa de Desemprego no Brasil (2020-2024)', className='text-center my-4'),

    dcc.Graph(
        id='taxa-desemprego-brasil'
    )
])

# Callback para atualizar os gráficos com base na seleção do dropdown
@app.callback(
    [Output('taxaCambio-volatilidade-BRL-USD', 'figure'),
     Output('export-importacao-por-ano', 'figure'),
     Output('taxa-desemprego-brasil', 'figure')],
    [Input('year-dropdown', 'value')]
)
def update_graphs(selected_years):
    if not isinstance(selected_years, list):
        selected_years = [selected_years]

    if not selected_years:
        selected_years = list(range(2020, 2025))

    # Atualizar gráfico de câmbio e volatilidade
    filtered_exchange_data = user_data[user_data['Date'].dt.year.isin(selected_years)]

    exchange_figure = {
        'data': [
            go.Scatter(
                x=filtered_exchange_data['Date'],
                y=filtered_exchange_data['MediaValue'],
                mode='lines',
                name='BRL/USD',
                line=dict(color='blue')
            ),
            go.Scatter(
                x=filtered_exchange_data['Date'],
                y=filtered_exchange_data['Volatility'],
                mode='lines',
                name='Volatility',
                line=dict(color='red'),
                yaxis='y2'
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

    # Atualizar gráfico de exportação/importação
    export_data_filtered = export_data_brazil[export_data_brazil['Ano'].isin(selected_years)]
    import_data_filtered = import_data_brazil[import_data_brazil['Ano'].isin(selected_years)]
    export_data_grouped_filtered = export_data_filtered.groupby('Ano')['Valor US$ FOB'].sum().reset_index()
    import_data_grouped_filtered = import_data_filtered.groupby('Ano')['Valor US$ FOB'].sum().reset_index()

    export_import_figure = {
        'data': [
            go.Bar(
                x=export_data_grouped_filtered['Ano'],
                y=export_data_grouped_filtered['Valor US$ FOB'],
                name='Exportação',
                marker=dict(color='green')
            ),
            go.Bar(
                x=import_data_grouped_filtered['Ano'],
                y=import_data_grouped_filtered['Valor US$ FOB'],
                name='Importação',
                marker=dict(color='red')
            )
        ],
        'layout': go.Layout(
            title='Exportação e Importação do Brasil (2020-2024)',
            xaxis=dict(title='Ano', type='category'),  # Definindo o tipo do eixo x como categoria
            yaxis=dict(title='Valor US$ FOB'),
            barmode='stack',
            margin=dict(l=50, r=50, t=50, b=100)
        )
    }

    # Atualizar gráfico de desemprego
    filtered_unemployment_data = unemployment_data_filtered[unemployment_data_filtered['Ano'].isin(selected_years)]

    unemployment_figure = {
        'data': [
            go.Scatter(
                x=filtered_unemployment_data['Date'],
                y=filtered_unemployment_data['Taxa'],
                mode='lines+markers',
                name='Taxa de Desemprego',
                line=dict(color='orange')
            )
        ],
        'layout': go.Layout(
            title='Taxa de Desemprego no Brasil (2020-2024)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Taxa de Desemprego (%)'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
    }

    return exchange_figure, export_import_figure, unemployment_figure

if __name__ == '__main__':
    app.run_server(debug=True)