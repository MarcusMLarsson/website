from flask import Blueprint, render_template, session, abort
import plotly.io as pio
import plotly.express as px
from arctic import Arctic
from pymongo import MongoClient
import pymongo
from matplotlib import pyplot as plt
import plotly.figure_factory as ff
import plotly.tools as tls
import statsmodels.formula.api as smapi
import time
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import seaborn as sns
from dateutil import parser
from datetime import timezone
import pytz
import re
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from dateutil import parser
from datetime import timezone
from datetime import datetime
import pytz

sns.set()
pio.templates.default = 'plotly_white'

start_time = time.time()


url = 'https://www.eia.gov/petroleum/supply/weekly/'
req = Request(url, headers={
    'User-Agent': 'Mozilla/5.0'
})


webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")

rdates = page_soup.find_all("span", class_="date")
rdates = re.sub('<[^>]*>', '', str(rdates))
rdates = rdates.replace("[", "")
rdates = rdates.replace("]", "")
rdates = rdates.replace(" ", "")
rdates = rdates.split(',', 2)[2:3]
utc = pytz.timezone('utc')

EIAdate = parser.parse(rdates[0])
EIAdate = EIAdate.replace(hour=14, minute=30)
EIAdate = EIAdate.replace(tzinfo=utc)

EIA_release_date = EIAdate.strftime('%b. %d, %Y')
EIA_release_time = EIAdate.strftime('%H:' '%M UTC')

timenow = datetime.utcnow()
timenow = timenow.replace(tzinfo=utc)
EIA_time_left = EIAdate - timenow
days, seconds = EIA_time_left.days, EIA_time_left.seconds
EIAhours = seconds // 3600
EIAminutes = (seconds % 3600) // 60
EIAseconds = seconds % 60

EIA_time_left = str(days) + " days, " + str(EIAhours) + \
    " hours, " + str(EIAminutes) + " minutes"


url = 'https://www.eia.gov/totalenergy/data/monthly/'
req = Request(url, headers={
    'User-Agent': 'Mozilla/5.0'
})

webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")

rdates = page_soup.find_all("span", class_="date")
rdates = re.sub('<[^>]*>', '', str(rdates))
rdates = rdates.replace("[", "")
rdates = rdates.replace("]", "")
rdates = rdates.replace(" ", "")
rdates = rdates.split(',', 2)[2:3]
utc = pytz.timezone('utc')

OECDdate = parser.parse(rdates[0])
OECDdate = OECDdate.replace(hour=18, minute=0)
OECDdate = OECDdate.replace(tzinfo=utc)

OECD_release_date = OECDdate.strftime('%b. %d, %Y')
OECD_release_time = OECDdate.strftime('%H:' '%M UTC')

timenow = datetime.utcnow()
timenow = timenow.replace(tzinfo=utc)
OECD_time_left = OECDdate - timenow
days, seconds = OECD_time_left.days, OECD_time_left.seconds
OECDhours = seconds // 3600
OECDminutes = (seconds % 3600) // 60
OECDseconds = seconds % 60

OECD_time_left = str(days) + " days, " + str(OECDhours) + \
    " hours, " + str(OECDminutes) + " minutes"
    


#store = Arctic('mongodb+srv://MarcusMLarsson:Britney1234@mongodb-0ydzb.azure.mongodb.net/test?retryWrites=true&w=majority')
store = Arctic('mongodb://MarcusMLarsson:Britney1234@mongodb-shard-00-00-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-01-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-02-0ydzb.azure.mongodb.net:27017/test?ssl=true&replicaSet=MongoDB-shard-0&authSource=admin&retryWrites=true&w=majority')

library = store['OIL']


# Reading the data
item = library.read('dfUS')
item1 = library.read('dfOECD')
item2 = library.read('dfUStable')
item3 = library.read('dfOECDtable')
item4 = library.read('Water_data1_crude')
item5 = library.read('Water_data1_products')
item6 = library.read('statsUS')
item7 = library.read('statsOECD')
item8 = library.read('crude_change_magnitude')
item9 = library.read('products_change_magnitude')
dfUS = item.data
dfOECD = item1.data
dfUStable = item2.data
dfOECDtable = item3.data
Water_data1_crude = item4.data
Water_data1_products = item5.data
statsUS = item6.data
statsOECD = item7.data
crude_change_magnitude = item8.data
products_change_magnitude = item9.data




#dfOECD[["Date","Brent", "Forecast", "Error", "Inventory", "Crude", "Products"]]


################################################################################################################################


app_file2 = Blueprint('app_file2', __name__)


@app_file2.route("/oil")
def function():
    plot1 = create_plot1()
    plot2 = create_plot2()
    plot3 = create_plot3()
    plot4 = create_plot4()
    plot5 = create_plot5()
    plot6 = create_plot6()
    plot7 = create_plot7()
    plot8 = create_plot8()
    plot9 = create_plot9()
    plot10 = create_plot10()
    plot11 = create_plot11()

    tableUSInventory = dfUStable[[
        "Date", "WTI", "Forecast_inventory", "Error_inventory", "Inventory"]].tail(21)
    tableUSInventory.columns = [
        "Date", "WTI", "Forecast", "Error", "Inventory"]
    tableUSInventory = [tableUSInventory.to_html(
        classes='mystyle', header="true", index=False)]

    tableOECDInventory = dfOECDtable[[
        "Date", "Brent", "Forecast_inventory", "Error_inventory", "Inventory"]].tail(21)
    tableOECDInventory.columns = [
        "Date", "Brent", "Forecast", "Error", "Inventory"]
    tableOECDInventory = [tableOECDInventory.to_html(
        classes='mystyle', header="true", index=False)]

    tableUSCrude = dfUStable[["Date", "WTI",
                              "Forecast_crude", "Error_crude", "Crude"]].tail(21)
    tableUSCrude.columns = ["Date", "WTI", "Forecast", "Error", "Inventory"]
    tableUSCrude = [tableUSCrude.to_html(
        classes='mystyle', header="true", index=False)]

    tableOECDCrude = dfOECDtable[[
        "Date", "Brent", "Forecast_crude", "Error_crude", "Crude"]].tail(21)
    tableOECDCrude.columns = ["Date", "Brent",
                              "Forecast", "Error", "Inventory"]
    tableOECDCrude = [tableOECDCrude.to_html(
        classes='mystyle', header="true", index=False)]

    tableUSInventory_no_spr = dfUStable[[
        "Date", "WTI", "Forecast_inventory_no_spr", "Error_inventory_no_spr", "Inventory_no_spr"]].tail(21)
    tableUSInventory_no_spr.columns = [
        "Date", "WTI", "Forecast", "Error", "Inventory"]
    tableUSInventory_no_spr = [tableUSInventory_no_spr.to_html(
        classes='mystyle', header="true", index=False)]

    tableOECDInventory_no_spr = dfOECDtable[[
        "Date", "Brent", "Forecast_inventory_no_spr", "Error_inventory_no_spr", "Inventory_no_spr"]].tail(21)
    tableOECDInventory_no_spr.columns = [
        "Date", "Brent", "Forecast", "Error", "Inventory"]
    tableOECDInventory_no_spr = [tableOECDInventory_no_spr.to_html(
        classes='mystyle', header="true", index=False)]

    tableUSCrude_no_spr = dfUStable[[
        "Date", "WTI", "Forecast_crude_no_spr", "Error_crude_no_spr", "Crude_no_spr"]].tail(21)
    tableUSCrude_no_spr.columns = [
        "Date", "WTI", "Forecast", "Error", "Inventory"]
    tableUSCrude_no_spr = [tableUSCrude_no_spr.to_html(
        classes='mystyle', header="true", index=False)]

    tableOECDCrude_no_spr = dfOECDtable[[
        "Date", "Brent", "Forecast_crude_no_spr", "Error_crude_no_spr", "Crude_no_spr"]].tail(21)
    tableOECDCrude_no_spr.columns = [
        "Date", "Brent", "Forecast", "Error", "Inventory"]
    tableOECDCrude_no_spr = [tableOECDCrude_no_spr.to_html(
        classes='mystyle', header="true", index=False)]

    USForecast_crude_corr = round(statsUS.iloc[0, 0:1], 3).values[0]
    USForecast_crude_no_spr_corr = round(statsUS.iloc[0, 1:2], 3).values[0]
    USForecast_inventory_corr = round(statsUS.iloc[0, 2:3], 3).values[0]
    USForecast_inventory_no_spr_corr = round(statsUS.iloc[0, 3:4], 3).values[0]

    OECDForecast_crude_corr = round(statsOECD.iloc[0, 0:1], 3).values[0]
    OECDForecast_crude_no_spr_corr = round(statsOECD.iloc[0, 1:2], 3).values[0]
    OECDForecast_inventory_corr = round(statsOECD.iloc[0, 2:3], 3).values[0]
    OECDForecast_inventory_no_spr_corr = round(
        statsOECD.iloc[0, 3:4], 3).values[0]

    RMSE_UScrude = (dfUS["Error_crude"] ** 2).mean()
    RMSE_UScrude_no_spr = (dfUS["Error_crude_no_spr"] ** 2).mean()
    RMSE_USInventory = (dfUS["Error_inventory"] ** 2).mean()
    RMSE_USInventory_no_spr = (dfUS["Error_inventory_no_spr"] ** 2).mean()

    RMSE_OECDcrude = (dfOECD["Error_crude"] ** 2).mean()
    RMSE_OECDcrude_no_spr = (dfOECD["Error_crude_no_spr"] ** 2).mean()
    RMSE_OECDInventory = (dfOECD["Error_inventory"] ** 2).mean()
    RMSE_OECDInventory_no_spr = (dfOECD["Error_inventory_no_spr"] ** 2).mean()

    return render_template('oil.html', plot1=plot1, plot2=plot2, plot3=plot3, plot4=plot4, plot5=plot5, plot6=plot6, plot7=plot7, plot8=plot8, plot9=plot9,
                           plot10=plot10, plot11=plot11, tableUSInventory=tableUSInventory, tableOECDInventory=tableOECDInventory, tableUSCrude=tableUSCrude,
                           tableOECDCrude=tableOECDCrude, tableUSInventory_no_spr=tableUSInventory_no_spr, tableOECDInventory_no_spr=tableOECDInventory_no_spr,
                           tableUSCrude_no_spr=tableUSCrude_no_spr, tableOECDCrude_no_spr=tableOECDCrude_no_spr,

                           USForecast_crude_corr=USForecast_crude_corr,
                           USForecast_crude_no_spr_corr=USForecast_crude_no_spr_corr, USForecast_inventory_corr=USForecast_inventory_corr,
                           USForecast_inventory_no_spr_corr=USForecast_inventory_no_spr_corr,

                           OECDForecast_crude_corr=OECDForecast_crude_corr,
                           OECDForecast_crude_no_spr_corr=OECDForecast_crude_no_spr_corr, OECDForecast_inventory_corr=OECDForecast_inventory_corr,
                           OECDForecast_inventory_no_spr_corr=OECDForecast_inventory_no_spr_corr,

                           RMSE_UScrude=RMSE_UScrude, RMSE_UScrude_no_spr=RMSE_UScrude_no_spr, RMSE_USInventory=RMSE_USInventory, RMSE_USInventory_no_spr=RMSE_USInventory_no_spr,
                           RMSE_OECDcrude=RMSE_OECDcrude, RMSE_OECDcrude_no_spr=RMSE_OECDcrude_no_spr, RMSE_OECDInventory=RMSE_OECDInventory, RMSE_OECDInventory_no_spr=RMSE_OECDInventory_no_spr,
                           EIA_release_date=EIA_release_date, EIA_release_time=EIA_release_time, EIA_time_left=EIA_time_left,
                           OECD_release_date=OECD_release_date, OECD_release_time=OECD_release_time, OECD_time_left=OECD_time_left,
                           products_change_magnitude=products_change_magnitude, crude_change_magnitude=crude_change_magnitude,
                           products_change=Water_data1_products["Products Change"][0], crude_change=Water_data1_crude["Crude Change"][0])


##########################################################################################################################################


def create_plot1():

    fig = px.scatter(dfUS,
                     x="RIN_inventory", y="WTI", color="Year", size=round(dfUS["GPR"], 2), size_max=31, hover_name="Year",
                     color_discrete_sequence=px.colors.qualitative.D3, opacity=0.78)
    # title="<b> Non-linear Relationship Between the WTI Spot <br> Price and the Relative Inventory Level</b>")

    fig.add_trace(go.Scatter(x=dfUS["RIN_inventory"], y=round(dfUS['Forecast_inventory'], 2),
                             mode='lines',
                             line=dict(
        width=1.5,
    ),
        marker=go.Marker(color='lightgray', size=2),
        name='Fit'))

    fig.update_traces(marker=dict(opacity=0.8,
                                  line=dict(width=0.5,
                                            color='white')),
                      selector=dict(mode='markers'))

    fig.update_layout(
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=0,
            t=5,
            pad=4),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),
        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True,
            title='Billion Barrels (seasonally adjusted)',
        ),

    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot2():

    trace1 = go.Scatter(
        x=dfUS.index,
        y=dfUS["lower_inventory"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,
    )
    trace2 = go.Scatter(
        x=dfUS.index,
        y=dfUS["upper_inventory"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,

    )
    trace3 = go.Scatter(
        x=dfUS.index,
        y=round(dfUS.Forecast_inventory, 2),
        name='Forecast',
        line=dict(color='#1f77b4'),
        visible=True,

    )
    trace4 = go.Scatter(
        x=dfUS.index,
        y=dfUS["WTI"],
        name='WTI',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        visible=True,
    )

    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig2 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot3():

    trace5 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["lower_inventory"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,

    )
    trace6 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["upper_inventory"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,
    )
    trace7 = go.Scatter(
        x=dfOECD.index,
        y=round(dfOECD["Forecast_inventory"], 2),
        name='Forecast',
        yaxis='y1',
        line=dict(color='#1f77b4'),
        # visible=False
    )
    trace8 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["Brent"],
        name='Brent',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        # visible=False
    )

    data1 = [trace5, trace6, trace7, trace8]

    layout1 = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig3 = go.Figure(data=data1, layout=layout1)

    graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot4():

    trace1 = go.Scatter(
        x=dfUS.index,
        y=dfUS["lower_crude"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,
    )
    trace2 = go.Scatter(
        x=dfUS.index,
        y=dfUS["upper_crude"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,

    )
    trace3 = go.Scatter(
        x=dfUS.index,
        y=round(dfUS.Forecast_crude, 2),
        name='Forecast',
        line=dict(color='#1f77b4'),
        visible=True,

    )
    trace4 = go.Scatter(
        x=dfUS.index,
        y=dfUS["WTI"],
        name='WTI',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        visible=True,
    )

    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig4 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot5():

    trace5 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["lower_crude"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,

    )
    trace6 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["upper_crude"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,
    )
    trace7 = go.Scatter(
        x=dfOECD.index,
        y=round(dfOECD["Forecast_crude"], 2),
        name='Forecast',
        yaxis='y1',
        line=dict(color='#1f77b4'),
        # visible=False
    )
    trace8 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["Brent"],
        name='Brent',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        # visible=False
    )

    data1 = [trace5, trace6, trace7, trace8]

    layout1 = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig5 = go.Figure(data=data1, layout=layout1)

    graphJSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot6():

    trace1 = go.Scatter(
        x=dfUS.index,
        y=dfUS["lower_inventory_no_spr"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,
    )
    trace2 = go.Scatter(
        x=dfUS.index,
        y=dfUS["upper_inventory_no_spr"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,

    )
    trace3 = go.Scatter(
        x=dfUS.index,
        y=round(dfUS.Forecast_inventory, 2),
        name='Forecast',
        line=dict(color='#1f77b4'),
        visible=True,

    )
    trace4 = go.Scatter(
        x=dfUS.index,
        y=dfUS["WTI"],
        name='WTI',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        visible=True,
    )

    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig6 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot7():

    trace5 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["lower_inventory_no_spr"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,

    )
    trace6 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["upper_inventory_no_spr"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,
    )
    trace7 = go.Scatter(
        x=dfOECD.index,
        y=round(dfOECD["Forecast_inventory_no_spr"], 2),
        name='Forecast',
        yaxis='y1',
        line=dict(color='#1f77b4'),
        # visible=False
    )
    trace8 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["Brent"],
        name='Brent',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        # visible=False
    )

    data1 = [trace5, trace6, trace7, trace8]

    layout1 = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig7 = go.Figure(data=data1, layout=layout1)

    graphJSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot8():

    trace1 = go.Scatter(
        x=dfUS.index,
        y=dfUS["lower_crude_no_spr"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,
    )
    trace2 = go.Scatter(
        x=dfUS.index,
        y=dfUS["upper_crude_no_spr"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        visible=True,
        showlegend=False,

    )
    trace3 = go.Scatter(
        x=dfUS.index,
        y=round(dfUS.Forecast_crude_no_spr, 2),
        name='Forecast',
        line=dict(color='#1f77b4'),
        visible=True,

    )
    trace4 = go.Scatter(
        x=dfUS.index,
        y=dfUS["WTI"],
        name='WTI',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        visible=True,
    )

    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig8 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot9():

    trace5 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["lower_crude_no_spr"],
        name='',
        yaxis='y1',
        # fill='tonextx',
        fillcolor='rgba(0,176,246,0.8)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,

    )
    trace6 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["upper_crude_no_spr"],
        name='',
        yaxis='y1',
        fill='tonexty',
        fillcolor='rgb(220,220,220, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        # visible=False,
        # showlegend=False,
    )
    trace7 = go.Scatter(
        x=dfOECD.index,
        y=round(dfOECD["Forecast_crude_no_spr"], 2),
        name='Forecast',
        yaxis='y1',
        line=dict(color='#1f77b4'),
        # visible=False
    )
    trace8 = go.Scatter(
        x=dfOECD.index,
        y=dfOECD["Brent"],
        name='Brent',
        yaxis='y1',
        line=dict(color='#ff7f0e'),
        # visible=False
    )

    data1 = [trace5, trace6, trace7, trace8]

    layout1 = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='<b> Predicted WTI Price and Actual Spot Price </b>',
        # font=dict(family='Helvetica', size=12),
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Dollars per Barrel',
            tickformat='$',
            titlefont=dict(
                # color = ('#1f77b4')
            ),
            tickfont=dict(
                # color = ('#1f77b4')
            ),
        ),

    )
    fig9 = go.Figure(data=data1, layout=layout1)

    graphJSON = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot10():

    trace1 = go.Waterfall(
        name="20", orientation="v",
        measure=["relative", "relative", "relative",
                 "relative", "relative", "total"],
        x=['Crude Imports', 'Crude Exports', 'Production',
            'Refinery Input', 'Crude Unaccounted', 'Crude Change'],
        textposition="none",
        text=round(Water_data1_crude*7, 1).values.tolist()[0],
        y=Water_data1_crude.values.tolist()[0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "rgba(219, 64, 82, 0.7)", "line": {
            "color": "rgba(219, 64, 82, 1.0)", "width": 2}}},
        increasing={"marker": {"color": "rgba(50, 171, 96, 0.7)", "line": {
            "color": 'rgba(50, 171, 96, 0.7)', "width": 2}}},
        totals={"marker": {"color": "rgba(55, 128, 191, 0.7)", "line": {
            "color": 'rgba(55, 128, 191, 1.0)', "width": 2}}}
    )
    data = [trace1]

    layout = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='Week over Week Inventory Change',
        #font=dict(family='Helvetica', size=12),
        height=350,
        autosize=True,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=10,
            pad=4),
        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Thousand Barrels',
            # tickformat='$',

            # titlefont=dict(
            # color = ('#00C094')
            # ),
            # tickfont=dict(
            # color = ('#00C094')
            # ),
        ),

    )
    fig10 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig10, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot11():

    trace1 = go.Waterfall(
        name="20", orientation="v",
        measure=["relative", "relative", "relative",
                 "relative", "relative", "relative", "total"],
        x=['Product Imports', 'Product Exports', 'Refinery Output', 'Refinery Production', 'Product Supplied',
            'Product Unaccounted', 'Product Change'],
        textposition="none",
        text=round(Water_data1_products*7, 1).values.tolist()[0],
        y=Water_data1_products.values.tolist()[0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "rgba(219, 64, 82, 0.7)", "line": {
            "color": "rgba(219, 64, 82, 1.0)", "width": 2}}},
        increasing={"marker": {"color": "rgba(50, 171, 96, 0.7)", "line": {
            "color": 'rgba(50, 171, 96, 0.7)', "width": 2}}},
        totals={"marker": {"color": "rgba(55, 128, 191, 0.7)", "line": {
            "color": 'rgba(55, 128, 191, 1.0)', "width": 2}}}
    )
    data = [trace1]

    layout = go.Layout(
        # displayModeBar=False,
        # paper_bgcolor='rgb(255,255,255)',
        # plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        #title='Week over Week Inventory Change',
        #font=dict(family='Helvetica', size=12),
        height=350,
        autosize=True,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=10,
            pad=4),
        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            # gridcolor='rgb(255,255,255)',
            title='Thousand Barrels',
            # tickformat='$',

            # titlefont=dict(
            # color = ('#00C094')
            # ),
            # tickfont=dict(
            # color = ('#00C094')
            # ),
        ),

    )
    fig11 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig11, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


print("--- %s seconds : Oil" % (time.time() - start_time))
