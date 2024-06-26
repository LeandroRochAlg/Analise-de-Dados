from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
import numpy as np

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

# Carregar os dados do IPCA
ipca_data = pd.read_csv('Dados Tratados/IPCA-TRATADO.csv')
ipca_data['data'] = pd.to_datetime(ipca_data['data'], format='%d/%m/%Y')
ipca_data.sort_values('data', inplace=True)

# Filtrar o período de interesse (dois anos antes da guerra até o presente)
start_date = datetime.datetime(2020, 2, 1)
ipca_filtered_data = ipca_data[ipca_data['data'] >= start_date]

# Datas importantes
pandemic_start = datetime.datetime(2020, 3, 1)
war_start = datetime.datetime(2022, 2, 24)

def register_callbacks(app):
    @app.callback(
        [Output('taxaCambio-volatilidade-BRL-USD', 'figure'),
         Output('export-importacao-por-ano', 'figure'),
         Output('unemployment-ipca', 'figure')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_graphs(n_intervals):
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
                ),
                go.Scatter(
                    x=[pandemic_start, pandemic_start],
                    y=[filtered_exchange_data['MediaValue'].min(), filtered_exchange_data['MediaValue'].max()],
                    mode='lines',
                    name='Início da Pandemia',
                    line=dict(color='black', dash='dash')
                ),
                go.Scatter(
                    x=[war_start, war_start],
                    y=[filtered_exchange_data['MediaValue'].min(), filtered_exchange_data['MediaValue'].max()],
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

        # Atualizar gráfico de desemprego e IPCA
        filtered_unemployment_data = unemployment_data[unemployment_data['Date'].dt.year.isin(selected_years)]
        filtered_ipca_data = ipca_data[ipca_data['data'].dt.year.isin(selected_years)]

        unemployment_ipca_figure = {
            'data': [
                go.Scatter(
                    x=filtered_unemployment_data['Date'],
                    y=filtered_unemployment_data['Taxa'],
                    mode='lines',
                    name='Taxa de Desemprego',
                    line=dict(color='purple')
                ),
                go.Scatter(
                    x=filtered_ipca_data['data'],
                    y=filtered_ipca_data['valor'],
                    mode='lines',
                    name='IPCA',
                    line=dict(color='orange'),
                    yaxis='y2'
                ),
                go.Scatter(
                    x=[pandemic_start, pandemic_start],
                    y=[filtered_unemployment_data['Taxa'].min(), filtered_unemployment_data['Taxa'].max()],
                    mode='lines',
                    name='Início da Pandemia',
                    line=dict(color='black', dash='dash')
                ),
                go.Scatter(
                    x=[war_start, war_start],
                    y=[filtered_unemployment_data['Taxa'].min(), filtered_unemployment_data['Taxa'].max()],
                    mode='lines',
                    name='Início da Guerra na Ucrânia',
                    line=dict(color='grey', dash='dash')
                )
            ],
            'layout': go.Layout(
                title='Taxa de Desemprego e IPCA',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Taxa de Desemprego', titlefont=dict(color='purple'), tickfont=dict(color='purple')),
                yaxis2=dict(title='IPCA', titlefont=dict(color='orange'), tickfont=dict(color='orange'), overlaying='y', side='right'),
                legend=dict(x=0, y=1.2),
                margin=dict(l=50, r=50, t=50, b=50)
            )
        }

        return exchange_figure, export_import_figure, unemployment_ipca_figure