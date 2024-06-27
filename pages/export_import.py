from dash import dcc, html
import plotly.graph_objs as go
from data_processing import export_data_grouped, import_data_grouped

export_import_figure = {
    'data': [
        go.Bar(
            x=export_data_grouped['Ano'],
            y=export_data_grouped['Valor US$ FOB'],
            name='Exportação',
            marker=dict(color='green')
        ),
        go.Bar(
            x=import_data_grouped['Ano'],
            y=import_data_grouped['Valor US$ FOB'],
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

layout = html.Div([
    html.H2("Exportação e Importação do Brasil (2020-2024)", className='text-center my-4'),
    dcc.Graph(
        id='export-importacao-por-ano',
        figure=export_import_figure
    ),
])