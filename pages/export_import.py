from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
from data_processing import export_data, import_data
from utils import country_translation as ct

# Adicionar coluna com códigos ISO-3166
export_data['country_code'] = export_data['Países'].apply(ct.translate_country)
import_data['country_code'] = import_data['Países'].apply(ct.translate_country)

# Obter a lista de países únicos
countries = sorted(export_data['Países'].unique())

# Obter a lista de anos únicos
years = export_data['Ano'].unique()

# Layout da página com o dropdown
layout = html.Div([
    html.H2("Exportação e importação ao longo dos anos", className='text-center my-4'),
    html.Label("Selecione os países para visualizar a exportação e importação por ano:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value=['Brasil'],
        multi=True
    ),
    dcc.Graph(id='export-importacao-por-ano'),
    html.P("Acima, você pode visualizar a evolução da exportação e importação de produtos entre 2018 e 2024."),
    html.Hr(),
    html.H2(f"Exportação e importação por país", className='text-center my-4'),
    html.Label("Selecione o ano para visualizar a exportação e importação por país:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in years],
        value=years[0],  # Valor inicial como o primeiro ano disponível
        clearable=False
    ),
    html.H3(f"Exportação", className='text-center my-4'),
    dcc.Graph(id='export-map'),
    html.H3(f"Importação", className='text-center my-4'),
    dcc.Graph(id='import-map'),
    html.P(["Os mapas acima mostram a distribuição geográfica das exportações e importações do Brasil para os países exibidos."]),
    html.Hr(),
    html.P(["Os dados são referentes ao valor FOB (Free on Board), que é o valor total das mercadorias exportadas/importadas, incluindo o custo de transporte e seguro até o porto de destino."], className='data-details'),
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
                margin=dict(l=50, r=50, t=50, b=100),
                annotations=[
                    dict(
                        x=0,
                        y=-0.11,
                        xref='paper',
                        yref='paper',
                        showarrow=False,
                        text=f'<a href="https://comexstat.mdic.gov.br/pt/geral" target="_blank">Fonte: Comex Stat</a>',
                        font=dict(size=12),
                    )
                ]
            )
        }
        return figure

    @app.callback(
        [Output('export-map', 'figure'),
         Output('import-map', 'figure')],
        [Input('year-dropdown', 'value')]
    )
    def update_maps(selected_year):
        # Filtrar dados pelo ano selecionado
        export_data_year = export_data[export_data['Ano'] == selected_year]
        import_data_year = import_data[import_data['Ano'] == selected_year]

        # Filtrar apenas os países com código válido
        export_data_year = export_data_year[export_data_year['country_code'].notna()]
        import_data_year = import_data_year[import_data_year['country_code'].notna()]

        # Dados para exportação
        export_fig = px.choropleth(
            export_data_year,
            locations="country_code",
            locationmode="ISO-3",
            color="Valor US$ FOB",
            hover_name="Países",
            color_continuous_scale=px.colors.sequential.Greens,
        )

        # Dados para importação
        import_fig = px.choropleth(
            import_data_year,
            locations="country_code",
            locationmode="ISO-3",
            color="Valor US$ FOB",
            hover_name="Países",
            color_continuous_scale=px.colors.sequential.Greens,
        )

        # Atualizar layout dos gráficos
        export_fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
        import_fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))

        return export_fig, import_fig