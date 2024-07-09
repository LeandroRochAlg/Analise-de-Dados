import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from data_processing import user_data, export_data, import_data, export_data_grouped, import_data_grouped, unemployment_data_filtered, ipca_filtered_data, pandemic_start, war_start
from layout import navbar, content
from pages.export_import import register_export_import_callbacks
from pages.commodities import register_commodities_callbacks
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([dcc.Location(id='url', refresh=False), navbar, content])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/exchange-volatility':
        from pages.exchange_volatility import layout as ev_layout
        return ev_layout
    elif pathname == '/export-import':
        from pages.export_import import layout as ei_layout
        return ei_layout
    elif pathname == '/unemployment-ipca':
        from pages.unemployment_ipca import layout as ui_layout
        return ui_layout
    elif pathname == '/commodities':
        from pages.commodities import layout as commodities_layout
        return commodities_layout
    else:
        from pages.home import layout as home_layout
        return home_layout

# Registrar callbacks específicos da página de exportação/importação
register_export_import_callbacks(app)

# Registrar callbacks específicos da página de commodities
register_commodities_callbacks(app)

# Registrar callbacks gerais
register_callbacks(app)

server = app.server
if __name__ == '__main__':
    app.run_server(debug=False)