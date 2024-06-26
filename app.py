import dash
from dash import dcc, html
from callbacks import register_callbacks
from layout import app_layout

# Inicializar o Dash app
app = dash.Dash(__name__)
app.layout = app_layout

# Registrar os callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)