from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from data import getDataframe

app = Dash(__name__)

df = getDataframe()

ratios = df.columns[2:]

app.layout = html.Div([
    html.H1('Stock Ratio Visualizer', style={"text-align": "center"}),

    html.Div([
        html.Div([
            dcc.Graph(id="time-series-chart", figure={"layout": {"height": 750}}),
        ], style={"width": "80%", "margin-top": "10px", "margin-bottom": "10px"}),
        html.Div([
            html.P("Select Ratio:"),
            dcc.Dropdown(
                id="ratio",
                options=ratios,
                value=ratios[0],
                clearable=False,
            ),
        ], style={"width": "10%", "margin-top": "10px", "margin-bottom": "10px", "margin-right" : "75px", "padding": "10px", "border": "1px solid black", "border-radius": "5px"})
        
    ], style={"display": "flex", "flex-direction": "row", "justify-content": "space-between", "align-items": "center", "width": "100%"})

], style={"font-family": "sans-serif"})


@app.callback(
    Output("time-series-chart", "figure"),
    Input("ratio", "value"))
def display_time_series(ratio):
    fig = px.line(df, x='date', y=ratio, markers=True,
                  color='symbol', template="plotly_dark")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
