import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc

# Importar layouts e callbacks
from layout import navbar, content
from pages.export_import import register_export_import_callbacks
from pages.commodities import register_commodities_callbacks
from callbacks import register_callbacks

# Inicializar o app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir o layout principal
app.layout = html.Div([dcc.Location(id='url', refresh=False), navbar, html.Div(id='page-content')])

# Callback para mudar a página
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

# Registrar callbacks específicos das páginas
register_export_import_callbacks(app)
register_commodities_callbacks(app)

# Registrar callbacks gerais
register_callbacks(app)

# Inicializar o servidor
server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)