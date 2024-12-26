# Importing necessary libraries

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from dash import Dash, Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc

# loading files

with open("../europe_new.json") as f:
    jl = json.load(f)


df_init = pd.read_csv("../df_WSDI.csv", header=[0, 1, 2], index_col=0)
df0 = df_init["WSDI_events"]
df00 = df_init["WSDI_days"]
time_list = df0.index.to_list()
pre_df0 = {year: df_init["WSDI_events"].loc[year].reset_index() for year in time_list}
zmin=round(np.nanmin(df0.values))
zmax=round(np.nanmax(df0.values))
df0min=df0.min().min()
df0max=df0.max().max()
df00min=df00.min().min()
df00max=df00.max().max()
########### Dash App part

# MAIN APP CODE

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app_header = html.Div(
    [
        html.H1(
            children="Europe Climate Extremes",
            style={"textAlign": "center", "color": "white"},
        ),
        html.H2(
            "Warm Spell Duration Index [1991-2023]",
            style={"margin-bottom": "0px", "color": "white", "textAlign": "center"},
        ),
        # html.H3('1991 - 2023',
        # style = {"margin-top": "0px", 'color': 'white','textAlign':'center'})
    ],
    style={"backgroundColor": "black", "padding-bottom": "2%"},
)

app_slider = html.Div(
    dcc.Slider(
        id="year-slider",
        updatemode="mouseup",
        vertical=True,
        min=time_list[0],
        max=time_list[len(time_list) - 1],
        step=1,
        value=time_list[0],
        marks={
            i: "{}".format(i)
            for i in range(time_list[0], time_list[len(time_list) - 1] + 1, 1)
        },
    ),
    style={
        "width": "0%",
        "display": "inline-block",
        "height": "480px",
        "transform": "scale(1.4)",
        "padding-left": "01%",
    },
)

app_graph = html.Div(
    dcc.Graph(id="graph_fig", hoverData={"points": [{"location": "ITA"}]}),
    style={
        "width": "0%",
        "display": "inline-block",
        "padding-bottom": "2%",
        "padding-left": "7%",
    },
)


app_time_series = html.Div(
    dcc.Graph(id="time-series"),
    style={
        "display": "inline-block",
        "width": "0%",
        "padding-bottom": "19%",
        "padding-left": "0%",
    },
)

app_time_series2 = html.Div(
    dcc.Graph(id="time-series2"),
    style={
        "display": "inline-block",
        "width": "10%",
        "padding-left": "44%",
        "padding-bottom": "01%",
    },
)


app.layout = html.Div(
    [app_header, app_slider, app_graph, app_time_series2, app_time_series],
    style={
        "widh": "100vw",
        "height": "100vh",
        "border": "10px solid rgb(0, 0, 0)",
        "outline": "10px solid rgb(0, 0, 0)",
        "outlineOffset": "0px",
        "margin": "0px 0px 0px 0px",
        "padding": "0px 0px 0px 0px",
        "backgroundColor": "black",
        "backgroundSize": "auto",
    },
)


@app.callback(Output("graph_fig", "figure"), Input("year-slider", "value"))
def update_graph(sel_year):
    dfw = pre_df0[sel_year]
    mapping = {dfw.columns[2]: "Extreme Events"}
    dfw = dfw.rename(columns=mapping)
    dfw["id"] = np.arange(1, len(dfw["Extreme Events"]) + 1)
    fig0 = go.Figure(
        go.Choroplethmapbox(
            geojson=jl,
            locations=dfw["Abr"],
            z=dfw["Extreme Events"],
            colorscale=px.colors.sequential.OrRd,
            zmin=zmin,
            zmax=zmax,
            marker_opacity=0.5,
        )
    )
    fig0.update_layout(
        height=500,
        width=600,
        coloraxis_showscale=False,
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family="Courier New, monospace", size=18, color="white"),
        mapbox_zoom=2.3,
        mapbox_center={"lat": 57, "lon": 16},
        transition_duration=500,
    )
    return fig0


def create_time_series(data_df, country_value):
    fig = px.scatter(
        x=data_df.Year.values,
        y=data_df.iloc[:, 1],
        labels={"x": " ", "y": "WDSI Index Events"},
        title=data_df.columns.values[1],
    )

    fig.update_traces(
        mode="lines+markers", line=dict(color="red"), marker=dict(color="red")
    )

    fig.update_xaxes(showgrid=False, color="white")

    fig.update_yaxes(type="linear", color="white")

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        height=250,
        yaxis_range=[df0.min().min(), df0.max().max()],
        margin={"l": 0, "b": 0, "r": 0, "t": 30},
        title_font_color="white",
        font=dict(family="Courier New, monospace", size=18, color="white"),
    )
    return fig


def create_time_series2(data_df, country_value):
    fig2 = px.scatter(
        x=data_df.Year.values,
        y=data_df.iloc[:, 1],
        labels={"x": " ", "y": "WDSI Index Days"},
        title=data_df.columns.values[1],
    )

    fig2.update_traces(
        mode="lines+markers", line=dict(color="red"), marker=dict(color="red")
    )

    fig2.update_xaxes(showgrid=False, color="white")

    fig2.update_yaxes(type="linear", color="white")

    fig2.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        height=250,
        yaxis_range=[df00.min().min(), df00.max().max()],
        margin={"l": 0, "b": 0, "r": 0, "t": 30},
        title_font_color="white",
        font=dict(family="Courier New, monospace", size=18, color="white"),
    )
    return fig2


@callback(
    Output("time-series", "figure"),
    Input("graph_fig", "hoverData"),
)
def update_timeseries(hoverData):
    country_name = hoverData["points"][0]["location"]
    dff = df0[country_name].reset_index()

    # title = '<b>{}</b><br>{}'.format(country_name)
    return create_time_series(dff, country_name)


@callback(
    Output("time-series2", "figure"),
    Input("graph_fig", "hoverData"),
)
def update_timeseries2(hoverData):
    country_name = hoverData["points"][0]["location"]
    dff2 = df00[country_name].reset_index()
    return create_time_series2(dff2, country_name)


# run the app
if __name__ == "__main__":
    app.run(debug=True)
