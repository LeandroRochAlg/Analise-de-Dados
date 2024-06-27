from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data_processing import user_data, unemployment_data_filtered, ipca_filtered_data, pandemic_start, war_start

def register_callbacks(app):
    @app.callback(
        Output('dynamic-graph', 'figure'),
        [Input('interval-component', 'n_intervals'),
         Input('variable-dropdown', 'value')]
    )
    def update_dynamic_graph(n_intervals, selected_vars):
        dynamic_data = []
        for var in selected_vars:
            if var in user_data.columns:
                dynamic_data.append(go.Scatter(
                    x=user_data['Date'],
                    y=user_data[var],
                    mode='lines',
                    name=var
                ))
            elif var in unemployment_data_filtered.columns:
                dynamic_data.append(go.Scatter(
                    x=unemployment_data_filtered['Date'],
                    y=unemployment_data_filtered[var],
                    mode='lines',
                    name=var
                ))
            elif var in ipca_filtered_data.columns:
                dynamic_data.append(go.Scatter(
                    x=ipca_filtered_data['data'],
                    y=ipca_filtered_data[var],
                    mode='lines',
                    name=var
                ))

        dynamic_figure = {
            'data': dynamic_data + [
                go.Scatter(
                    x=[pandemic_start, pandemic_start],
                    y=[min([data['y'].min() for data in dynamic_data]), max([data['y'].max() for data in dynamic_data])],
                    mode='lines',
                    name='Início da Pandemia',
                    line=dict(color='black', dash='dash')
                ),
                go.Scatter(
                    x=[war_start, war_start],
                    y=[min([data['y'].min() for data in dynamic_data]), max([data['y'].max() for data in dynamic_data])],
                    mode='lines',
                    name='Início da Guerra na Ucrânia',
                    line=dict(color='grey', dash='dash')
                )
            ],
            'layout': go.Layout(
                title='Painel Dinâmico de Indicadores Econômicos',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Valor'),
                legend=dict(x=0, y=1.2),
                margin=dict(l=50, r=50, t=50, b=50)
            )
        }
        return dynamic_figure