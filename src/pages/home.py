from dash import html

layout = html.Div([
    html.H1("Bem-vindo ao Painel de Indicadores Econômicos do Brasil", className='text-center my-4'),
    html.P("Utilize o menu de navegação para explorar os diferentes indicadores econômicos.", className='text-center'),
], className='main-content')