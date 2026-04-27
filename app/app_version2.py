#===================================================================================
# LIBRERÍAS
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
from pathlib import Path

#===================================================================================
# CARGA DE DATOS
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DATA_PATH = PROJECT_DIR / 'data' / 'processed' / 'sp500_model_results.csv'
df = pd.read_csv(DATA_PATH, parse_dates=['Date'], index_col='Date')

#===================================================================================
# APP
app = dash.Dash(__name__)
server = app.server

#===================================================================================
# KPI CARD (FUNCIÓN AUXILIAR)
def create_kpi_card(title, value):
    return html.Div([
        html.H4(title, style={"marginBottom": "5px", "color": "#333"}),
        html.H2(value, style={"marginTop": "0px"})
    ],
    style={
        "backgroundColor": "#f9f9f9",
        "padding": "15px",
        "borderRadius": "10px",
        "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)",
        "width": "22%",
        "textAlign": "center"
    })

#===================================================================================
# LAYOUT
app.layout = html.Div([

    # TÍTULO
    html.H1(
        "Market Risk Monitoring Dashboard",
        style={"textAlign": "center"}
    ),

    # SUBTEXTO (storytelling)
    html.P(
        "Risk increases during periods of high volatility, reflected in the event intensity λ(t).",
        style={"textAlign": "center", "color": "gray"}
    ),

    # DATE PICKER
    dcc.DatePickerRange(
        id='date-picker',
        start_date=df.index.min(),
        end_date=df.index.max(),
        display_format='YYYY-MM-DD',
        style={'margin': '20px'}
    ),

    # KPI CARDS
    html.Div(id='kpi-container', style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginBottom': '30px'
    }),

    # GRÁFICAS
    dcc.Graph(id='price-chart'),
    dcc.Graph(id='returns-chart'),
    dcc.Graph(id='volatility-chart'),
    dcc.Graph(id='lambda-chart')

])

#===================================================================================
# CALLBACK
@app.callback(
    [
        Output('kpi-container', 'children'),
        Output('price-chart', 'figure'),
        Output('returns-chart', 'figure'),
        Output('volatility-chart', 'figure'),
        Output('lambda-chart', 'figure')
    ],
    [
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ]
)
def update_dashboard(start_date, end_date):

    dff = df.loc[start_date:end_date]

    #================ KPIs =================
    current_lambda = dff['Lambda'].iloc[-1]
    current_vol = dff['GARCH_Volatility'].iloc[-1]
    recent_return = dff['Log_Return'].iloc[-1]
    extreme_events = dff['Extreme_Event'].tail(30).sum()

    kpis = [
        create_kpi_card("Current Risk", f"{current_lambda:.4f}"),
        create_kpi_card("Volatility", f"{current_vol:.4f}"),
        create_kpi_card("Recent Return", f"{recent_return:.4f}"),
        create_kpi_card("Extreme Events (30d)", f"{int(extreme_events)}")
    ]

    #================ PRICE =================
    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['Close'],
        mode='lines'
    ))
    price_fig.update_layout(
        title='Market Trend (S&P 500)',
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    #================ RETURNS =================
    returns_fig = go.Figure()
    returns_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['Log_Return'],
        mode='lines',
        name='Returns'
    ))

    returns_fig.add_trace(go.Scatter(
        x=dff[dff['Extreme_Event'] == 1].index,
        y=dff[dff['Extreme_Event'] == 1]['Log_Return'],
        mode='markers',
        marker=dict(color='red', size=6),
        name='Extreme Events'
    ))

    returns_fig.update_layout(
        title='Extreme Negative Events Detection',
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    #================ VOLATILITY =================
    vol_fig = go.Figure()
    vol_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['GARCH_Volatility'],
        mode='lines'
    ))

    vol_fig.update_layout(
        title='Volatility Dynamics (GARCH Model)',
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    #================ LAMBDA =================
    lambda_fig = go.Figure()
    lambda_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['Lambda'],
        mode='lines'
    ))

    lambda_fig.update_layout(
        title='Estimated Risk Intensity λ(t)',
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return kpis, price_fig, returns_fig, vol_fig, lambda_fig

#===================================================================================
# RUN
if __name__ == '__main__':
    app.run(debug=True)