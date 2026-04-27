#===================================================================================
# CARGA DE LIBRERÍAS
import dash 
from dash import dcc,html
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path
#===================================================================================
# CARGA DE DATOS
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATA_PATH = PROJECT_DIR / 'data' / 'processed' / 'sp500_model_results.csv'
df = pd.read_csv(DATA_PATH,parse_dates=['Date'],index_col='Date')
#===================================================================================
# APP
app = dash.Dash(__name__)
server = app.server
#===================================================================================
# GRÁFICO DE PRECIO
price_fig = go.Figure()
price_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['Close'],
    mode='lines',
    name='S&P 500'
))
price_fig.update_layout(title='Market Price')

#GRÁFICO DE RETORNO + EVENTOS
returns_fig = go.Figure()
returns_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['Log_Return'],
    mode='lines',
    name='Returns'
))
returns_fig.add_trace(go.Scatter(
    x=df[df['Extreme_Event']==1].index,
    y=df[df['Extreme_Event']==1]['Log_Return'],
    mode='markers',
    marker=dict(color='red',size=6),
    name='Extreme Events'
))
returns_fig.update_layout(title='Return & Extreme Events')

# GRÁFICO DE VOLATILIDAD
vol_fig = go.Figure()
vol_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['GARCH_Volatility'],
    mode='lines',
    name='GARCH Volatility'
))
vol_fig.update_layout(title='Volatility (GARCH)')

# GRÁFICO DE INTENSIDAD LAMBDA(t)
lambda_fig = go.Figure()
lambda_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['Lambda'],
    mode='lines',
    name='Lambda (Risk)'
))
lambda_fig.update_layout(title='Event Intensity λ(t)')
#===================================================================================
# LAYOUT
app.layout = html.Div([
    html.H1('Financial Risk Dashboard',style={'textAlign':'center'}),
    dcc.Graph(figure=price_fig),
    dcc.Graph(figure=returns_fig),
    dcc.Graph(figure=vol_fig),
    dcc.Graph(figure=lambda_fig)
])
#===================================================================================
# EJECUCIÓN DE LA APP
if __name__ == '__main__':
    app.run(debug=True)