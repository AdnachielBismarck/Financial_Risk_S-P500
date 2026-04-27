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
# PRECOMPUTE REGIME SEGMENTS (OPTIMIZACIÓN CLAVE)
def compute_regime_segments(df):
    segments = []

    current_regime = df['Regime'].iloc[0]
    start_date = df.index[0]

    for i in range(1, len(df)):
        if df['Regime'].iloc[i] != current_regime:
            segments.append((start_date, df.index[i], current_regime))
            current_regime = df['Regime'].iloc[i]
            start_date = df.index[i]

    segments.append((start_date, df.index[-1], current_regime))
    return segments

regime_segments = compute_regime_segments(df)

#===================================================================================
# APP
app = dash.Dash(__name__)
server = app.server

#===================================================================================
# KPI CARD
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
        "width": "18%",
        "textAlign": "center"
    })

#===================================================================================
# LAYOUT
app.layout = html.Div([

    html.H1("Market Risk Monitoring Dashboard", style={"textAlign": "center"}),

    html.P(
        "Risk regimes emerge from volatility dynamics and event intensity λ(t).",
        style={"textAlign": "center", "color": "gray"}
    ),

    dcc.DatePickerRange(
        id='date-picker',
        start_date=df.index.min(),
        end_date=df.index.max(),
        display_format='YYYY-MM-DD',
        style={'margin': '20px'}
    ),

    html.Div(id='kpi-container', style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginBottom': '30px'
    }),

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
    current_regime = dff['Regime'].iloc[-1]

    kpis = [
        create_kpi_card("Current Risk", f"{current_lambda:.4f}"),
        create_kpi_card("Volatility", f"{current_vol:.4f}"),
        create_kpi_card("Recent Return", f"{recent_return:.4f}"),
        create_kpi_card("Extreme Events (30d)", f"{int(extreme_events)}"),
        create_kpi_card("Current Regime", current_regime)
    ]

    #================ CONFIG BASE =================
    common_layout = dict(
        template='plotly_white',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='x unified',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    )

    #================ PRICE =================
    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['Close'],
        mode='lines',
        line=dict(color='#2c3e50', width=2)
    ))
    price_fig.update_layout(title='Market Trend (S&P 500)', **common_layout)

    #================ RETURNS =================
    returns_fig = go.Figure()
    returns_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['Log_Return'],
        mode='lines',
        line=dict(color='#7f8c8d', width=2)
    ))

    returns_fig.add_trace(go.Scatter(
        x=dff[dff['Extreme_Event'] == 1].index,
        y=dff[dff['Extreme_Event'] == 1]['Log_Return'],
        mode='markers',
        marker=dict(color='red', size=6)
    ))

    returns_fig.update_layout(
        title='Extreme Negative Events Detection',
        **common_layout
    )

    #================ VOLATILITY =================
    vol_fig = go.Figure()
    vol_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['GARCH_Volatility'],
        mode='lines',
        line=dict(color='#ff7f50', width=2)
    ))

    vol_fig.update_layout(
        title='Volatility Dynamics (GARCH Model)',
        **common_layout
    )

    #================ LAMBDA =================
    lambda_fig = go.Figure()

    # REGIME BACKGROUND OPTIMIZADO
    regime_colors = {
        "Stable": "rgba(0,200,0,0.08)",
        "Moderate": "rgba(255,165,0,0.08)",
        "High Risk": "rgba(255,0,0,0.08)"
    }

    for start, end, regime in regime_segments:

        if end >= dff.index.min() and start <= dff.index.max():

            lambda_fig.add_vrect(
                x0=max(start, dff.index.min()),
                x1=min(end, dff.index.max()),
                fillcolor=regime_colors.get(regime),
                opacity=0.5,
                layer="below",
                line_width=0
            )

    # Línea principal
    lambda_fig.add_trace(go.Scatter(
        x=dff.index,
        y=dff['Lambda'],
        mode='lines',
        line=dict(color='#ff4d00', width=3),
        fill='tozeroy',
        fillcolor='rgba(255,77,0,0.15)'
    ))

    # Eventos extremos
    extreme_points = dff[dff['Extreme_Event'] == 1]

    lambda_fig.add_trace(go.Scatter(
        x=extreme_points.index,
        y=extreme_points['Lambda'],
        mode='markers',
        marker=dict(color='red', size=5)
    ))

    # Eventos históricos (ligeros)
    key_events = [
        {"date": "2020-03-11", "label": "COVID"},
        {"date": "2022-02-24", "label": "War"},
        {"date": "2023-03-10", "label": "Bank"}
    ]

    max_lambda = dff['Lambda'].max()

    for i, event in enumerate(key_events):
        event_date = pd.to_datetime(event["date"])

        if dff.index.min() <= event_date <= dff.index.max():

            lambda_fig.add_vline(
                x=event_date,
                line_width=1,
                line_dash="dot",
                line_color="black"
            )

            lambda_fig.add_annotation(
                x=event_date,
                y=max_lambda * (1 if i % 2 == 0 else 0.85),
                text=event["label"],
                showarrow=False,
                textangle=-45,
                font=dict(size=10)
            )

    lambda_fig.update_layout(
        title='Estimated Risk Intensity λ(t)',
        **common_layout
    )

    return kpis, price_fig, returns_fig, vol_fig, lambda_fig

#===================================================================================
# RUN
if __name__ == '__main__':
    app.run(debug=True)