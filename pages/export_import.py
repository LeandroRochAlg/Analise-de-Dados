from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from data_processing import export_data, import_data

# Obter a lista de países únicos
countries = export_data['Países'].unique()

# Layout da página com o dropdown
layout = html.Div([
    html.H2("Exportação e Importação (2020-2024)", className='text-center my-4'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value=['Brasil'],
        multi=True
    ),
    dcc.Graph(id='export-importacao-por-ano'),
])

def register_export_import_callbacks(app):
    @app.callback(
        Output('export-importacao-por-ano', 'figure'),
        [Input('country-dropdown', 'value')]
    )
    def update_export_import_graph(selected_countries):
        data = []
        colors = ['green', 'red', 'blue', 'orange', 'purple', 'brown']  # Lista de cores para distinguir os países
        for i, country in enumerate(selected_countries):
            country_export_data = export_data[export_data['Países'] == country]
            country_import_data = import_data[import_data['Países'] == country]
            
            country_export_data_grouped = country_export_data.groupby('Ano')['Valor US$ FOB'].sum().reset_index()
            country_import_data_grouped = country_import_data.groupby('Ano')['Valor US$ FOB'].sum().reset_index()
            
            data.append(go.Bar(
                x=country_export_data_grouped['Ano'],
                y=country_export_data_grouped['Valor US$ FOB'],
                name=f'Exportação {country}',
                marker=dict(color=colors[i % len(colors)])
            ))
            data.append(go.Bar(
                x=country_import_data_grouped['Ano'],
                y=country_import_data_grouped['Valor US$ FOB'],
                name=f'Importação {country}',
                marker=dict(color=colors[i % len(colors)]),
                marker_pattern_shape='/'
            ))
        
        figure = {
            'data': data,
            'layout': go.Layout(
                xaxis=dict(title='Ano', type='category'),
                yaxis=dict(title='Valor US$ FOB'),
                barmode='group',  # Modo de barras agrupadas
                margin=dict(l=50, r=50, t=50, b=100)
            )
        }
        return figure