from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Taxa de Câmbio e Volatilidade", href="/exchange-volatility")),
        dbc.NavItem(dbc.NavLink("Exportação e Importação", href="/export-import")),
        dbc.NavItem(dbc.NavLink("Desemprego e IPCA", href="/unemployment-ipca")),
    ],
    brand="Painel de Indicadores Econômicos",
    brand_href="/",
    color="primary",
    dark=True,
)

content = html.Div(id="page-content", children=[])