import plotly
import plotly.graph_objs as go
import pandas as pd
import json
import pyxlsb
import pymongo
from pymongo import MongoClient
from arctic import Arctic
import numpy as np
import plotly.io as pio
pio.templates.default = 'plotly_white'
import time
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from dateutil import parser
from datetime import timezone
from datetime import datetime
import pytz
import re


start_time = time.time()

url = 'https://uk.investing.com/economic-calendar/baker-hughes-u.s.-rig-count-1652'
req = Request(url, headers={
    'User-Agent': 'Mozilla/5.0'
})

webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")

rdates = page_soup.find_all("td", class_="left")

utc = pytz.timezone('utc')

dateNextRelease = rdates[0]
dateNextRelease = re.sub('<[^>]*>', '', str(dateNextRelease))
timeNextRelease = rdates[1]
timeNextRelease = re.sub('<[^>]*>', '', str(timeNextRelease))

dateTimeNextRelease = parser.parse(dateNextRelease + timeNextRelease)
dateTimeNextRelease = dateTimeNextRelease.replace(tzinfo=utc)

time_now = datetime.utcnow()
time_now = time_now.replace(tzinfo=utc)


time_left = dateTimeNextRelease - time_now
daysLeft, secondsLeft = time_left.days, time_left.seconds
hoursLeft = secondsLeft // 3600
minutesLeft = (secondsLeft % 3600) // 60
secondsLeft = secondsLeft % 60

time_left = str(daysLeft) + " days, " + str(hoursLeft) + \
    " hours, " + str(minutesLeft) + " minutes"

#store = Arctic('mongodb+srv://MarcusMLarsson:Britney1234@mongodb-0ydzb.azure.mongodb.net/test?retryWrites=true&w=majority')
store = Arctic('mongodb://MarcusMLarsson:Britney1234@mongodb-shard-00-00-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-01-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-02-0ydzb.azure.mongodb.net:27017/test?ssl=true&replicaSet=MongoDB-shard-0&authSource=admin&retryWrites=true&w=majority')

library = store['RIGCOUNT']


# Reading the data
item = library.read('df')
item1 = library.read('df1')
item2 = library.read('Production')
item3 = library.read('df4')
item4 = library.read('df2')
item5 = library.read('df3')
item6 = library.read('CL1')

df = item.data
df1 = item1.data
Production = item2.data
df4 = item3.data
df2 = item4.data
df3 = item5.data
CL1 = item6.data

################################################################################################################################

from flask import Blueprint, render_template, session,abort

app_file3 = Blueprint('app_file3',__name__)

@app_file3.route("/rigcount")
def function():
    plot = create_plot()
    plot1 = create_plot1()
    plot2 = create_plot2()

    table = df1[["ShiftCL1", "OilRigs"]]
    table = pd.DataFrame(table)
    table["Error"] = np.exp(df1["Forecast"]).values - np.exp(df1["OilRigs"]).values
    table["Rig count"] = np.exp(df1["OilRigs"])
    table["Forecast"] = np.exp(df1["Forecast"])
    table["Forecast"] = table["Forecast"].astype(int)
    table["Rig count"] = table["Rig count"].astype(int)
    table["Error"] = table["Error"].astype(int)
    table.reset_index(inplace=True)
    table = table[["Date", "Rig count", "Forecast", "Error"]].tail(21)

    tablerigcount = [table.iloc[::-1].to_html(
        classes='mystyle', header="true", index=False)]

    corr = round(df1["Forecast"].corr(df1["OilRigs"]),3)
    rmse= ((np.exp(df1["Forecast"]).values - np.exp(df1["OilRigs"]).values) **2).mean() ** 0.5


    return render_template('rigcount.html', plot=plot, plot1=plot1, plot2=plot2, tablerigcount=tablerigcount, corr=corr, rmse=rmse,
    dateNextRelease=dateNextRelease, timeNextRelease=timeNextRelease, time_left=time_left)

def create_plot():
    trace1 = go.Scatter(
    x=df1.index,
    y=round(np.exp(df1["Lower"]),0),
    name='',
    yaxis='y1',
    #fill='tonextx',
    fillcolor='rgba(0,176,246,0.8)',
    line=dict(color='rgba(255,255,255,0)'),
    visible=True,
    showlegend=False,

    )
    trace2 = go.Scatter(
            x=df1.index,
            y=round(np.exp(df1["Upper"]),0),
            name='',
            yaxis='y1',
            fill='tonexty',
            fillcolor='rgb(220,220,220, 0.5)',
            line=dict(color='rgba(255,255,255,0)'),
            visible=True,
            showlegend=False,

        )
    trace3 = go.Scatter(
            x=df1.index,
            y=round(np.exp(df1["Forecast"]),0),
            name='Forecast',
            yaxis='y1',
            line=dict(color='#17becf'),
            visible=True,

        )
    trace4 = go.Scatter(
            x=df.index,
            y=np.exp(df["OilRigs"].iloc[0:-11]),
            name='Rig Count',
            yaxis='y1',
            line=dict(color='#F06A6A'),
            visible=True,

        )


    data = [trace1, trace2, trace3, trace4]


    layout = go.Layout(
        autosize=True,
        height=700,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),
            #displayModeBar=False,
            #paper_bgcolor='rgb(255,255,255)',
            #plot_bgcolor='rgb(229,229,229)',
            legend=dict(orientation="h"),
            #font=dict(family='Helvetica', size=12),
            
            
            
            xaxis=dict(
                showgrid=True,
                showline=False,
                zeroline=False,
                showticklabels=True
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=False,
                #gridcolor='rgb(255,255,255)',
                title='# of Active Drilling Rigs (log)',
                type = 'log',
                
                titlefont=dict(
                    #color = ('#00C094')
                ),
                tickfont=dict(
                    #color = ('#00C094')
                ),       
            ),
        shapes=[
                    
                                # 1st highlight during Feb 4 - Feb 6
                    dict(
                    type="rect",
                        # x-reference is assigned to the x-values
                        xref="x",
                        # y-reference is assigned to the plot paper [0,1]
                        yref="paper",
                        x0=str(df1.iloc[-12:-11, 0].index.values[0]),
                        y0=0,
                        x1=str(df1.iloc[-1:, 0].index.values[0]),
                        y1=1,
                        fillcolor="rgba(255, 65, 54, 0.6)",
                        opacity=0.15,
                        layer="above",
                        line_width=0,
                    )
            ]
            
        )

    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



def create_plot1():
    trace1 = go.Scatter(
        x=Production['US_production_crude'].index,
        y=Production['US_production_crude'],
        name='Production',
        line=dict(color='#17becf')
    )
    trace2 = go.Scatter(
            x=df.index,
            y=df['OilRigs'].iloc[0:-11],
            name='Rig Count',
            yaxis='y2',
            line=dict(color='#33CFA5'),
        )
    trace3 = go.Scatter(
            x=df.index,
            y=df["CL1"].iloc[0:-11],
            name='WTI',
            yaxis='y3',
            line=dict(color='#F06A6A'),

        )
    trace4 = go.Scatter(
            x=Production['US_production_crude_Shift'].index,
            y=Production['US_production_crude_Shift'],
            name='Production',
            line=dict(color='#17becf'),
            visible=False
        )
    trace5 = go.Scatter(
            x=df.index,
            y=df['ShiftOilRigs'].iloc[0:-23],
            name='Rig Count',
            yaxis='y2',
            line=dict(color='#33CFA5'),
            visible=False
        )
    trace6 = go.Scatter(
            x=df.index,
            y=df["CL1"].iloc[0:-11],
            name='WTI',
            yaxis='y3',
            line=dict(color='#F06A6A'),
            visible=False

        )




    data = [trace1, trace2, trace3, trace4, trace5, trace6]

    updatemenus = list([
            dict(type="buttons",
                active=-1,
                direction='left',
                pad={'r': 10, 't': 10},
                showactive=True,
                x=-0.04,
                xanchor='left',
                y=1.1,
                yanchor='top',
                buttons=list([
                    dict(label='Primary Data',
                        method='update',
                        args=[{'visible': [True, True, True, False, False, False]}]),
                    dict(label='Shifted Data',
                        method='update',
                        args=[{'visible': [False, False, False, True, True, True]}]),
                
                ]),
                )
        ])

    layout = go.Layout(
            autosize=True,
            height=700,
            margin=go.layout.Margin(
            l=50,
            r=50,
            b=5,
            t=0,
            pad=4),

            # paper_bgcolor='rgb(255,255,255)',
            # plot_bgcolor='rgb(229,229,229)',
            updatemenus=updatemenus,
            legend=dict(orientation="h"),
            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                showticklabels=True,
                domain=[0, 0.93]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                gridcolor='rgb(255,255,255)',
                title='MMbbls/d',
                titlefont=dict(
                    color=('#17becf')
                ),
                tickfont=dict(
                    color=('#17becf')
                )
            ),
            yaxis2=dict(
                showgrid=False,
                zeroline=False,
                gridcolor='rgb(255,255,255)',
                titlefont=dict(
                    color=('#33CFA5')
                ),
                tickfont=dict(
                    color='#33CFA5'
                ),
                overlaying='y',
                side='right',
                position=1,
                title="# of Rotary Rigs"
            ),
            yaxis3=dict(
                # gridcolor='rgb(255,255,255)',
                title='Dollar per Barrel',
                tickformat='$',
                titlefont=dict(
                    color='#F06A6A'
                ),
                tickfont=dict(
                    color='#F06A6A'
                ),
                anchor='x',
                overlaying='y',
                side='right',
                position=1.0
            ),

        )
    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def create_plot2():
    trace1 = dict(
        x=df4.index,
        y=df4["Ardmore"],
        #hoverinfo='x+y',
        mode='lines',
        visible=True,
        line=dict(width=0.5),
        stackgroup='one',
        name='Ardmore'
        )
    trace2 = dict(
            x=df4.index,
            y=df4["Arkoma"],
            #hoverinfo='x+y',
            mode='lines',
            visible=True,
            line=dict(width=0.5),
            stackgroup='one',
            name='Arkoma'
        )
    trace3 = go.Scatter(
            x=df4.index,
            #hoverinfo='x+y',
            mode='lines',
            y=df4['Barnett'],
            visible=True,
            name='Barnett',
            stackgroup='one',
            #line=dict(color='#bcbd22')
        )
    trace4 = go.Scatter(
            x=df4.index,
            y=df4['Cana'],
            #hoverinfo='x+y',
            mode='lines',
            visible=True,
            name='Cana',
            stackgroup='one',
            #line=dict(color='#7f7f7f')
        )
    trace5 = dict(
            x=df4.index,
            y=df4['DJ-Niobrara'],
            visible=True,
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='DJ-Niobrara'
        )
    trace6 = dict(
            x=df4.index,
            y=df4['Eagle Ford'],
            visible=True,
            #hoverinfo='x+y',
            #mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Eagle Ford'
        )
    trace7 = go.Scatter(
            x=df4.index,
            y=df4['Fayetteville'],
            #line=dict(color='#bcbd22'),
            visible=True,
            #hoverinfo='x+y',
            stackgroup='one',
            name='Fayetteville_Oil'

        )
    trace8 = go.Scatter(
            x=df4.index,
            y=df4['Granite Wash'],
            visible=True,
            #hoverinfo='x+y',
            name='Granite Wash',
            yaxis='y1',
            stackgroup='one',
            #line=dict(color='#7f7f7f')
        )
    trace9 = dict(
            x=df4.index,
            y=df4['Haynesville'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Haynesville',
            visible=True,
        )
    trace10 = dict(
            x=df4.index,
            y=df4['Marcellus'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Marcellus',
            visible=True,
        )
    trace11 = dict(
            x=df4.index,
            y=df4['Mississippian'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Mississippian',
            visible=True,
                
        )
    trace12 = dict(
            x=df4.index,
            y=df4['Permian'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Permian',
            visible=True,
        )
    trace13 = dict(
            x=df4.index,
            y=df4['Utica'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Utica',
            visible=True,
        )
    trace14 = dict(
            x=df4.index,
            y=df4['Williston'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Williston',
            visible=True,
        )
    trace15 = dict(
            x=df4.index,
            y=df4['Others'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Others',
            visible=True,
        )
    trace16 = dict(
            x=df4.index,
            y=df4['Total'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.1),
            #stackgroup='one',
            name='Total',
            visible=True,
        )
    trace17 = dict(
            x=df2.index,
            y=df2['Directonal'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Directional',
            visible=False,
        )
    trace18 = dict(
            x=df2.index,
            y=df2['Horizontal'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Horizontal',
            visible=False,
        )
    trace19 = dict(
            x=df2.index,
            y=df2['Vertical'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Vertical',
            visible=False,
        )
    trace20 = dict(
            x=df3.index,
            y=df3['Gas'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Gas',
            visible=False,
        )
    trace21 = dict(
            x=df3.index,
            y=df3['Oil'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Oil',
            visible=False,
        )
    trace22 = dict(
            x=df3.index,
            y=df3['Other'],
            #hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name='Other',
            visible=False,
        )
    trace23 = go.Scatter(
            x=CL1["2011-02-06":"2100"].index,
            y=CL1["Settle"]["2011-02-06":"2100"],
            visible=True,
            name='WTI',
            yaxis='y2',
            line=dict(width=2, color='#17becf'),
            #line=dict(color='#7f7f7f')
        )
    trace24 = go.Scatter(
            x=CL1["1991-01-06":"2100"].index,
            y=CL1["Settle"]["1991-01-06":"2100"],
            visible=False,
            name='WTI',
            yaxis='y2',
            line=dict(width=2, color='#17becf'),
            #line=dict(color='#7f7f7f')
        )
    trace25 = go.Scatter(
            x=CL1["2000-01-09":"2100"].index,
            y=CL1["Settle"]["2000-01-09":"2100"],
            visible=False,
            name='WTI',
            yaxis='y2',
            line=dict(width=2, color='#17becf'),
            #line=dict(color='#7f7f7f')
        )


    data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12, trace13,
                trace14, trace15, trace16, trace17, trace18, trace19, trace20, trace21, trace22, trace23, trace24, trace25]

    updatemenus = list([
            dict(type="buttons",
                active=-1,
                direction='left',
                pad={'r': 10, 't': 10},
                showactive=True,
                x=-0.04,
                xanchor='left',
                y=1.1,
                yanchor='top',
                buttons=list([
                    dict(label='By Basin',
                        method='update',
                        args=[{'visible': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False, False]}]),
                    dict(label='By Trajectory',
                        method='update',
                        args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, True, False]}]),
                    dict(label='Gulf of Mexico',
                        method='update',
                        args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, True]}]),

                ]),
                )
        ])

    layout = go.Layout(
            autosize=True,
            height=700,
            margin=go.layout.Margin(
                l=50,
                r=50,
                b=5,
                t=0,
                pad=4),
            # displayModeBar=False,
            # paper_bgcolor='rgb(255,255,255)',
            # plot_bgcolor='rgb(229,229,229)',
            legend=dict(orientation="h"),
            updatemenus=updatemenus,
            # font=dict(family='Helvetica', size=12),
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
                title='# of Active Drilling Rigs',

                titlefont=dict(
                    # color = ('#00C094')
                ),
                tickfont=dict(
                    # color = ('#00C094')
                ),
            ),
            yaxis2=dict(
                showgrid=False,
                zeroline=False,
                # autorange = "reversed",
                tickformat='$',
                # gridcolor='rgb(255,255,255)',
                title='Dollars per Barrel',
                # type='log',
                tickfont=dict(
                    color='#17becf'
                ),
                overlaying='y',
                side='right',
            )
        )
    fig3 = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON






##########################################################################################################################################
print("--- %s seconds : Rigcount" % (time.time() - start_time))
