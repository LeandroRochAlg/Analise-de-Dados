import pandas as pd
import numpy as np
import datetime

def load_data():
    user_data = pd.read_csv('Dados Tratados/USD-BRL-Tratado.csv')
    user_data['Date'] = pd.to_datetime(user_data['Date'])
    user_data.sort_values('Date', inplace=True)
    user_data['Log_Returns'] = np.log(user_data['MediaValue'] / user_data['MediaValue'].shift(1))
    user_data['Volatility'] = user_data['Log_Returns'].rolling(window=30).std() * np.sqrt(252)

    usd_eur_data = pd.read_csv('Dados Tratados/USD-EUR-TRATADO.csv')
    usd_eur_data['Date'] = pd.to_datetime(usd_eur_data['Date'])
    usd_eur_data.sort_values('Date', inplace=True)
    usd_eur_data['Log_Returns'] = np.log(usd_eur_data['MediaValue'] / usd_eur_data['MediaValue'].shift(1))
    usd_eur_data['Volatility'] = usd_eur_data['Log_Returns'].rolling(window=30).std() * np.sqrt(252)

    dx_y_data = pd.read_csv('Dados Tratados/DX-Y.NYB-TRATADO.csv')
    dx_y_data['Date'] = pd.to_datetime(dx_y_data['Date'])
    dx_y_data.sort_values('Date', inplace=True)
    dx_y_data['Log_Returns'] = np.log(dx_y_data['MediaValue'] / dx_y_data['MediaValue'].shift(1))
    dx_y_data['Volatility'] = dx_y_data['Log_Returns'].rolling(window=30).std() * np.sqrt(252)

    start_date = datetime.datetime(2019, 6, 3)

    export_data = pd.read_csv('Dados Tratados/Exportação-TRATADO.csv')
    import_data = pd.read_csv('Dados Tratados/Importação-TRATADO.csv')

    export_data = export_data[export_data['Ano'] >= 2018]
    import_data = import_data[import_data['Ano'] >= 2018]

    export_data_brazil = export_data[export_data['Países'] == 'Brasil']
    import_data_brazil = import_data[import_data['Países'] == 'Brasil']

    export_data_grouped = export_data_brazil.groupby('Ano')['Valor US$ FOB'].sum().reset_index()
    import_data_grouped = import_data_brazil.groupby('Ano')['Valor US$ FOB'].sum().reset_index()

    unemployment_data = pd.read_csv('Dados Tratados/Desemprego-TRATADO.csv')
    month_map = {
        'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
        'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
    }
    unemployment_data['Mes'] = unemployment_data['Mes'].map(month_map)
    unemployment_data['Date'] = pd.to_datetime(unemployment_data['Ano'].astype(str) + '-' + unemployment_data['Mes'] + '-01')
    unemployment_data_filtered = unemployment_data[unemployment_data['Date'] >= start_date]

    ipca_data = pd.read_csv('Dados Tratados/IPCA-TRATADO.csv')
    ipca_data['data'] = pd.to_datetime(ipca_data['data'], format='%d/%m/%Y')
    ipca_data.sort_values('data', inplace=True)
    ipca_filtered_data = ipca_data[ipca_data['data'] >= start_date]

    return user_data, export_data, import_data, export_data_grouped, import_data_grouped, unemployment_data_filtered, ipca_filtered_data, usd_eur_data, dx_y_data

user_data, export_data, import_data, export_data_grouped, import_data_grouped, unemployment_data_filtered, ipca_filtered_data, usd_eur_data, dx_y_data = load_data()
pandemic_start = datetime.datetime(2020, 3, 1)
war_start = datetime.datetime(2022, 2, 24)