from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data_processing import user_data, unemployment_data_filtered, ipca_filtered_data, pandemic_start, war_start, usd_eur_data, dx_y_data

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

    @app.callback(
        Output('exchange-volatility-graph', 'figure'),
        [Input('exchange-dropdown', 'value')]
    )
    def update_exchange_volatility_graph(selected_exchange):
        if selected_exchange == 'BRL/USD':
            data = user_data
            name = 'BRL/USD'
        elif selected_exchange == 'USD/EUR':
            data = usd_eur_data
            name = 'USD/EUR'
        elif selected_exchange == 'DX-Y.NYB':
            data = dx_y_data
            name = 'DX-Y.NYB'

        figure = {
            'data': [
                go.Scatter(
                    x=data['Date'],
                    y=data['MediaValue'],
                    mode='lines',
                    name=name,
                    line=dict(color='blue')
                ),
                go.Scatter(
                    x=data['Date'],
                    y=data['Volatility'],
                    mode='lines',
                    name='Volatility',
                    line=dict(color='red'),
                    yaxis='y2'
                ),
                go.Scatter(
                    x=[pandemic_start, pandemic_start],
                    y=[data['MediaValue'].min(), data['MediaValue'].max()],
                    mode='lines',
                    name='Início da Pandemia',
                    line=dict(color='black', dash='dash')
                ),
                go.Scatter(
                    x=[war_start, war_start],
                    y=[data['MediaValue'].min(), data['MediaValue'].max()],
                    mode='lines',
                    name='Início da Guerra na Ucrânia',
                    line=dict(color='grey', dash='dash')
                )
            ],
            'layout': go.Layout(
                title=f'{name}',
                xaxis=dict(title='Date'),
                yaxis=dict(title=name, titlefont=dict(color='blue'), tickfont=dict(color='blue')),
                yaxis2=dict(title='Volatility', titlefont=dict(color='red'), tickfont=dict(color='red'), overlaying='y', side='right'),
                legend=dict(x=0, y=1.2),
                margin=dict(l=50, r=50, t=50, b=50)
            )
        }
        return figure