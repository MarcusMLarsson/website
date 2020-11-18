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


#store = Arctic('mongodb+srv://MarcusMLarsson:Britney1234@mongodb-0ydzb.azure.mongodb.net/test?retryWrites=true&w=majority')
store = Arctic('mongodb://MarcusMLarsson:Britney1234@mongodb-shard-00-00-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-01-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-02-0ydzb.azure.mongodb.net:27017/test?ssl=true&replicaSet=MongoDB-shard-0&authSource=admin&retryWrites=true&w=majority')

library = store['PRODUCTION']


# Reading the data
item = library.read('df')
item1 = library.read('Water_data1')
item2 = library.read('Water_data3')
item3 = library.read('Water_data7')

df = item.data
Water_data1 = item1.data
Water_data3 = item2.data
Water_data7 = item3.data



################################################################################################################################


app_file4 = Blueprint('app_file4', __name__)


@app_file4.route("/production")
def function():
    plot1 = create_plot1()
    plot2 = create_plot2()
    plot3 = create_plot3()

    
    

    return render_template('production.html', plot1=plot1, plot2=plot2, plot3=plot3)


##########################################################################################################################################


def create_plot1():
    trace_OPEC = go.Scatter(x=list(df.index),
                        y=list(df["OPEC"]),
                        mode = 'lines+markers',
                        name='OPEC',
                        line=dict(
                            color=('#F8766D'),
                            width=2))
                                

    trace_Algeria = go.Scatter(x=list(df.index),
                                y=list(df["Algeria"]),
                                mode = 'lines+markers',
                                name='Algeria',
                                visible=False,
                                line=dict(
                                    color=('#C49A00'),
                                    width=2))
                                #line=dict(color='#33CFA5', dash='dash'))

    trace_Angola = go.Scatter(x=list(df.index),
                                y=list(df["Angola"]),
                                mode = 'lines+markers',
                                name='Angola',
                                visible=False,
                                line=dict(
                                    color=('#53B400'),
                                    width=2))
                                #line=dict(color='#33CFA5', dash='dash'))

    trace_Ecuador = go.Scatter(x=list(df.index),
                        y=list(df["Equatorial_Guniea"]),
                        mode = 'lines+markers',
                        name='Equatorial Guniea',
                        visible=False,
                        line=dict(
                                color=('#00C094'),
                                width=2))
                
                        #line=dict(color='#F06A6A'))

    trace_Gabon = go.Scatter(x=list(df.index),
                            y=list(df["Gabon"]),
                            mode = 'lines+markers',
                            name='Gabon',
                            visible=False,
                            line=dict(
                                color=('#00B6EB'),
                                width=2))
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_Iran = go.Scatter(x=list(df.index),
                            y=list(df["Iran"]),
                            mode = 'lines+markers',
                            name='Iran',
                            visible=False,
                            line=dict(
                                color=('#A58AFF'),
                                width=2))
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_Iraq = go.Scatter(x=list(df.index),
                            y=list(df["Iraq"]),
                            mode = 'lines+markers',
                            name='Iraq',
                            visible=False,
                            line=dict(
                                color=('#FB61D7'),
                                width=2))
                            
                        
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_Kuwait = go.Scatter(x=list(df.index),
                            y=list(df["Kuwait"]),
                            name='Kuwait',
                            mode = 'lines+markers',
                            visible=False,
                            )

                            #line=dict(color='#F06A6A', dash='dash'))

    trace_Libya = go.Scatter(x=list(df.index),
                            y=list(df["Libya"]),
                            name='Libya',
                            mode = 'lines+markers',
                            visible=False
                            )
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_Nigeria = go.Scatter(x=list(df.index),
                            y=list(df["Nigeria"]),
                            name='Nigeria',
                            mode = 'lines+markers',
                            visible=False,
                            )
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_SA = go.Scatter(x=list(df.index),
                            y=list(df["SaudiArabia"]),
                            name='Saudi Arabia',
                            mode = 'lines+markers',
                            visible=False,
                        )
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_UAE = go.Scatter(x=list(df.index),
                            y=list(df["UAE"]),
                            name='UAE',
                            mode = 'lines+markers',
                            visible=False,)
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_Venezuela = go.Scatter(x=list(df.index),
                            y=list(df["Venezuela"]),
                            mode = 'lines+markers',
                            name='Venezula',
                            visible=False,)
                            #line=dict(color='#F06A6A', dash='dash'))



    data = [trace_OPEC, trace_Algeria, trace_Angola, trace_Ecuador, trace_Gabon, trace_Iran, trace_Iraq, trace_Kuwait, trace_Libya, trace_Nigeria, trace_SA, trace_UAE, trace_Venezuela]

    us_annotations=[dict(x=1,
                        y=-0.20,
                        showarrow=False,
                        xref='paper', 
                        yref='paper',
                        text='Data Source:<a href="https://www.eia.gov/petroleum/supply/weekly/"> EIA Weekly Petroleum Status Report</a>',
                        xanchor='right',
                        yanchor='auto',
                        xshift=0, 
                        yshift=0,
                        font = dict(size = 9)),
                    dict(
                x=1,
                y=-0.15,
                text='© 2019 A tail of the Curve, L.L.C. All Rights Reserved'  ,
                showarrow=False,
                xref='paper', 
                yref='paper',
                xanchor='right',
                yanchor='auto',
                xshift=0, 
                yshift=0,
                font = dict(size = 9),
                
        
            )]

    updatemenus = list([
        dict(active=-1,
            buttons=list([   
                dict(label = 'OPEC',
                    method = 'update',
                    args = [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False, False]},
                            {'title': 'OPEC Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Algeria',
                    method = 'update',
                    args = [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False, False]},
                            {'title': 'Algeria Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Angola',
                    method = 'update',
                    args = [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False, False]},
                            {'title': 'Angola Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Equatorial Guniea',
                    method = 'update',
                    args = [{'visible': [False, False, False, True, False, False, False, False, False, False, False, False, False]},
                            {'title': 'Equatorial Guniea Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Gabon',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False, False]},
                            {'title': 'Gabon Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Iran',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, True, False, False, False, False, False, False, False]},
                            {'title': 'Iran Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Iraq',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, True, False, False, False, False, False, False]},
                            {'title': 'Iraq Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Kuwait',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, True, False, False, False, False, False]},
                            {'title': 'Kuwait Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Libya',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, True, False, False, False, False]},
                            {'title': 'Libya Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Nigeria',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, False, True, False, False, False]},
                            {'title': 'Nigeria Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Saudi Arabia',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, False, False, True, False, False]},
                            {'title': 'Saudi Arabia Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'UAE',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, True, False]},
                            {'title': 'UAE Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'Venezuela',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, True]},
                            {'title': 'Venezuela Crude Production',
                            'annotations': []}])
            ]),
        )
    ])

    layout = go.Layout(
        #displayModeBar=False,
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        updatemenus=updatemenus,
        title='OPEC Crude Oil Production',
        #font=dict(family='Helvetica', size=12),
        
        
        
        xaxis=dict(
            gridcolor='rgb(255,255,255)',
            tickcolor='rgb(127,127,127)',
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True       
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            gridcolor='rgb(255,255,255)',
            tickcolor='rgb(127,127,127)',
            title='Million Barrels per Day',
            
            titlefont=dict(
            # color = ('#00C094')
            ),
            tickfont=dict(
            # color = ('#00C094')
            ),       
        ),

    )
    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot2():

    trace_1 = go.Scatter(x=list(df.index),
                        y=list(df["WordLessUSA"]),
                        mode = 'lines+markers',
                        name='World Less USA',
                        line=dict(
                            color=('#F8766D'),
                            width=2))
                                

    trace_2 = go.Scatter(x=list(df.index),
                                y=list(df["NonOPECLessUSA"]),
                                mode = 'lines+markers',
                                name='Non OPEC Less USA',
                                visible=False,
                                line=dict(
                                    color=('#C49A00'),
                                    width=2))
                                #line=dict(color='#33CFA5', dash='dash'))

    trace_3 = go.Scatter(x=list(df.index),
                                y=list(df["Brazil"]),
                                mode = 'lines+markers',
                                name='Brazil',
                                visible=False,
                                line=dict(
                                    color=('#53B400'),
                                    width=2))
                                #line=dict(color='#33CFA5', dash='dash'))

    trace_4 = go.Scatter(x=list(df.index),
                        y=list(df["Canada"]),
                        mode = 'lines+markers',
                        name='Canada',
                        visible=False,
                        line=dict(
                                color=('#00C094'),
                                width=2))
                
                        #line=dict(color='#F06A6A'))

    trace_5 = go.Scatter(x=list(df.index),
                            y=list(df["China"]),
                            mode = 'lines+markers',
                            name='China',
                            visible=False,
                            line=dict(
                                color=('#00B6EB'),
                                width=2))
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_6 = go.Scatter(x=list(df.index),
                            y=list(df["Mexicao"]),
                            mode = 'lines+markers',
                            name='Mexico',
                            visible=False,
                            line=dict(
                                color=('#A58AFF'),
                                width=2))
                            #line=dict(color='#F06A6A', dash='dash'))
        
    trace_7 = go.Scatter(x=list(df.index),
                            y=list(df["Norway"]),
                            mode = 'lines+markers',
                            name='Norway',
                            visible=False,
                            line=dict(
                                color=('#A58AFF'),
                                width=2))
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_8 = go.Scatter(x=list(df.index),
                            y=list(df["Kazakhstan"]),
                            mode = 'lines+markers',
                            name='Kazakhstan',
                            visible=False,
                            line=dict(
                                color=('#FB61D7'),
                                width=2))
                            
                        
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_9 = go.Scatter(x=list(df.index),
                            y=list(df["Russia"]),
                            name='Russia',
                            mode = 'lines+markers',
                            visible=False,
                            )

                            #line=dict(color='#F06A6A', dash='dash'))

    trace_10 = go.Scatter(x=list(df.index),
                            y=list(df["UK"]),
                            name='UK',
                            mode = 'lines+markers',
                            visible=False
                            )
                            #line=dict(color='#F06A6A', dash='dash'))

    trace_11 = go.Scatter(x=list(df.index),
                            y=list(df["USA"]),
                            name='USA',
                            mode = 'lines+markers',
                            visible=False,
                            )
                            #line=dict(color='#F06A6A', dash='dash'))



    data = [trace_1, trace_2, trace_3, trace_4, trace_5, trace_6, trace_7, trace_8, trace_9, trace_10, trace_11]

    us_annotations=[dict(x=1,
                        y=-0.20,
                        showarrow=False,
                        xref='paper', 
                        yref='paper',
                        text='Data Source:<a href="https://www.eia.gov/petroleum/supply/weekly/"> EIA Weekly Petroleum Status Report</a>',
                        xanchor='right',
                        yanchor='auto',
                        xshift=0, 
                        yshift=0,
                        font = dict(size = 9)),
                    dict(
                x=1,
                y=-0.15,
                text='© 2019 A head of the Curve, L.L.C. All Rights Reserved'  ,
                showarrow=False,
                xref='paper', 
                yref='paper',
                xanchor='right',
                yanchor='auto',
                xshift=0, 
                yshift=0,
                font = dict(size = 9),
                
        
            )]

    updatemenus = list([
        dict(active=-1,
            buttons=list([   
                dict(label = 'WorldLessUS',
                    method = 'update',
                    args = [{'visible': [True, False, False, False, False, False, False, False, False, False, False]},
                            {'title': 'World Less USA',
                            'annotations': us_annotations}]),
                dict(label = 'NonOPECLessUS',
                    method = 'update',
                    args = [{'visible': [False, True, False, False, False, False, False, False, False, False, False]},
                            {'title': 'Non-OPEC Less USA',
                            'annotations': us_annotations}]),
                dict(label = 'Brazil',
                    method = 'update',
                    args = [{'visible': [False, False, True, False, False, False, False, False, False, False, False]},
                            {'title': 'Brazil',
                            'annotations': us_annotations}]),
                dict(label = 'Canada',
                    method = 'update',
                    args = [{'visible': [False, False, False, True, False, False, False, False, False, False, False]},
                            {'title': 'Canada',
                            'annotations': us_annotations}]),
                dict(label = 'China',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, True, False, False, False, False, False, False]},
                            {'title': 'China',
                            'annotations': us_annotations}]),
                dict(label = 'Mexico',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, True, False, False, False, False, False]},
                            {'title': 'Mexico',
                            'annotations': us_annotations}]),
                dict(label = 'Norway',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, True, False, False, False, False]},
                            {'title': 'Norway',
                            'annotations': us_annotations}]),
                dict(label = 'Kazakhstan',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, True, False, False, False]},
                            {'title': 'Kazakhstan',
                            'annotations': us_annotations}]),
                dict(label = 'Russia',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, True, False, False]},
                            {'title': 'Russia',
                            'annotations': us_annotations}]),
                dict(label = 'UK',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, False, True, False]},
                            {'title': 'Nigeria Crude Production',
                            'annotations': us_annotations}]),
                dict(label = 'US',
                    method = 'update',
                    args = [{'visible': [False, False, False, False, False, False, False, False, False, False, True]},
                            {'title': 'US',
                            'annotations': us_annotations}])
                
            ]),
        )
    ])

    layout = go.Layout(
        #displayModeBar=False,
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        updatemenus=updatemenus,
        title='World Less US',
        #font=dict(family='Helvetica', size=12),
        
        
        
        xaxis=dict(
            gridcolor='rgb(255,255,255)',
            tickcolor='rgb(127,127,127)',
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True       
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            gridcolor='rgb(255,255,255)',
            tickcolor='rgb(127,127,127)',
            title='Million Barrels per Day',
            
            titlefont=dict(
            # color = ('#00C094')
            ),
            tickfont=dict(
            # color = ('#00C094')
            ),       
        ),

    )

    fig2 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot3():

    trace1 = go.Waterfall(
    name = "20", orientation = "v", 
    measure = ["relative", "relative", "relative", "relative", "relative", "Relative",  "Relative", "Relative", "Relative", "Relative", "Relative", "total"], 
    x = Water_data1.columns, 
    textposition = "outside", 
    text = round(Water_data1,2).values.tolist()[0], 
    y = Water_data1.values.tolist()[0], 
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
    decreasing = {"marker":{"color":"rgba(219, 64, 82, 0.7)", "line":{"color":"rgba(219, 64, 82, 1.0)", "width":2}}}, 
    increasing = {"marker":{"color":"rgba(50, 171, 96, 0.7)", "line":{"color":'rgba(50, 171, 96, 0.7)', "width":2}}}, 
    totals = {"marker":{"color":"rgba(55, 128, 191, 0.7)", "line":{"color":'rgba(55, 128, 191, 1.0)', "width":2}}}
    )
    trace2 = go.Waterfall(
        name = "20", orientation = "v", 
        measure = ["relative", "relative", "relative", "relative", "relative", "Relative",  "Relative", "Relative", "Relative", "Relative", "Relative", "total"], 
        x = Water_data3.columns, 
        textposition = "outside", 
        text = round(Water_data3,2).values.tolist()[0], 
        y = Water_data3.values.tolist()[0], 
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"rgba(219, 64, 82, 0.7)", "line":{"color":"rgba(219, 64, 82, 1.0)", "width":2}}}, 
        increasing = {"marker":{"color":"rgba(50, 171, 96, 0.7)", "line":{"color":'rgba(50, 171, 96, 0.7)', "width":2}}}, 
        totals = {"marker":{"color":"rgba(55, 128, 191, 0.7)", "line":{"color":'rgba(55, 128, 191, 1.0)', "width":2}}},
        visible=False
    )
    trace4 = go.Waterfall(
        name = "20", orientation = "v", 
        measure = ["relative", "relative", "relative", "relative", "relative", "Relative",  "Relative", "Relative", "Relative", "Relative", "Relative", "total"], 
        x = Water_data7.columns, 
        textposition = "outside", 
        text = round(Water_data7,2).values.tolist()[0], 
        y = Water_data7.values.tolist()[0], 
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"rgba(219, 64, 82, 0.7)", "line":{"color":"rgba(219, 64, 82, 1.0)", "width":2}}}, 
        increasing = {"marker":{"color":"rgba(50, 171, 96, 0.7)", "line":{"color":'rgba(50, 171, 96, 0.7)', "width":2}}}, 
        totals = {"marker":{"color":"rgba(55, 128, 191, 0.7)", "line":{"color":'rgba(55, 128, 191, 1.0)', "width":2}}},
        visible=False
    )


    data = [trace1, trace2, trace4]

    jodi_annotations=[dict(x=1,
                        y=-0.20,
                        showarrow=False,
                        xref='paper', 
                        yref='paper',
                        text='Data Source:<a href="https://www.jodidata.org/oil/"> JODI Oil</a>',
                        xanchor='right',
                        yanchor='auto',
                        xshift=0, 
                        yshift=0,
                        font = dict(size = 9)),
                    dict(
                x=1,
                y=-0.15,
                text='© 2019 A Head of the Curve, L.L.C. All Rights Reserved'  ,
                showarrow=False,
                xref='paper', 
                yref='paper',
                xanchor='right',
                yanchor='auto',
                xshift=0, 
                yshift=0,
                font = dict(size = 9),
                
        
            )]



    updatemenus = list([
        dict(type="buttons",
            active=-1,
            direction = 'left',
            pad = {'r': 10, 't': 10},
            showactive = True,
            x = -0.01,
            xanchor = 'left',
            y = 1.2,
            yanchor = 'top', 
            buttons=list([
                dict(label = 'MoM',
                    method = 'update',
                    args = [{'visible': [False, True, False]},
                            {'title': 'Month over Month Crude Oil Production',
                                    'annotations': jodi_annotations}]),
                dict(label = 'YoY',
                    method = 'update',
                    args = [{'visible': [True, False, False]},
                            {'title': 'Year over Year Crude Oil Production',
                            'annotations': jodi_annotations}]),
                
                dict(label = 'DoD',
                    method = 'update',
                    args = [{'visible': [False, False, True]},
                            {'title': 'Decade over Decade Crude Oil Production',
                            'annotations': jodi_annotations}]),

            ]),
        )
    ])


        

    layout = go.Layout(
        #displayModeBar=False,
        #paper_bgcolor='rgb(255,255,255)',
        #plot_bgcolor='rgb(229,229,229)',
        legend=dict(orientation="h"),
        updatemenus=updatemenus,
        title='Year over Year Crude Oil Production',
        #font=dict(family='Helvetica', size=12),
        

        
        xaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True       
        ),
        yaxis=dict(
            showgrid=True,
            #zeroline=False,
            #gridcolor='rgb(255,255,255)',
            title='Millon Barrels per Day',
            #tickformat='$',
            
            #titlefont=dict(
                #color = ('#00C094')
            #),
            #tickfont=dict(
                #color = ('#00C094')
            #),       
        ),

    )
    fig3 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



print("--- %s seconds : Production" % (time.time() - start_time))
