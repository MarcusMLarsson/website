import numpy as np
import pandas as pd
from datetime import datetime
import quandl
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import matplotlib

import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.tools as tls
py.init_notebook_mode(connected=True)
import cufflinks as cf
import seaborn as sns
import plotly.io as pio
import statsmodels.formula.api as smf
import plotly.io as pio
import time
from arctic import Arctic
from pymongo import MongoClient
from datetime import timezone
import pytz

utc = pytz.timezone('utc')

def main():
    # change streams MongoDB
    start_time = time.time()

    # Connect to Local MONGODB
    # store = Arctic('mongodb+srv://MarcusMLarsson:Britney1234@mongodb-0ydzb.azure.mongodb.net/test?retryWrites=true&w=majority')
    store = Arctic('mongodb://MarcusMLarsson:Britney1234@mongodb-shard-00-00-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-01-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-02-0ydzb.azure.mongodb.net:27017/test?ssl=true&replicaSet=MongoDB-shard-0&authSource=admin&retryWrites=true&w=majority')

    # Create the library - defaults to VersionStore
    store.initialize_library('RIGCOUNT')

    # Access the library
    library = store['RIGCOUNT']

    # Request o Baker Hughes webpage
    result = requests.get("https://rigcount.bakerhughes.com/na-rig-count", headers={
        'User-Agent': 'Mozilla/5.0'})

    # Obtain content of webpage
    src = result.content

    # Pass variable into BeautifulSoup class, creating an Soup object.
    # Object allows us to extract information
    soup = BeautifulSoup(src, 'lxml')
    # Find all links
    links = soup.find_all("a")


    # Extract link to excel file
    rig_link = []
    for i in links:
        if "North America Rotary Rig Count (Jan 2000 - Current)" in i.text:
            rig_link.append(i.attrs['href'])
            #print(i.attrs['href'])


    req = Request(
        str(rig_link[0]), 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    xld = urlopen(req).read()
    df = pd.read_excel(xld, "US Oil & Gas Split", engine='pyxlsb', skiprows=6)
    sr = pd.Series(pd.date_range('1987-07-17', periods = df.shape[0], freq = 'W'))
    df = pd.concat([df, sr], axis=1)
    df.columns = ["Date_Int", "OilRigs", "GasRigs", "Misc", "Total", "%OilRigs", "%GasRigs", "Date"]
    df.index = df["Date"]
    df.dropna(inplace=True)

    CL1 = quandl.get("CHRIS/CME_CL1", authtoken="ExYhsQRV9jyhdRQWb_s8", collapse="weekly")
    CL1 = CL1["Settle"]
    CL1 = CL1["1987-07-19":"2100"]
    CL1 = pd.DataFrame(CL1)

    df = pd.concat([df, CL1], axis=1)
    df.columns = ["Date_Int", "OilRigs", "GasRigs", "Misc", "Total", "%OilRigs", "%GasRigs", "Date", "CL1"]


    a = []
    b = []
    for i in range(31):
        corr = df["CL1"].shift(i).corr(df["OilRigs"])
        a.append(corr)
        b.append(i)
        
    dfcorr = pd.DataFrame(a,b)
    dfcorr.columns = ["correlation"]

    dfcorr = dfcorr.iloc[dfcorr['correlation'].abs().argsort()][::-1]

    OptimalLag = dfcorr.index[0]


    df1 = df

    for i in [1,1,1,1, 1,1,1,1,1,1,1]:
        df1.loc[max(df1.index)+pd.Timedelta(weeks=i), :] = None
            

    df1["ShiftCL1"] = df1['CL1'].shift(12)

    df1.fillna(method="ffill", inplace=True)
    df1.fillna(method="bfill", inplace=True)

    df1["OilRigs"] = np.log(df1["OilRigs"])            
    df1["ShiftCL1"] = np.log(df1["ShiftCL1"])

    df1 = df1[["OilRigs", "ShiftCL1"]]   


        # Count per Trajectory

    df2 = pd.read_excel(xld, "US Count by Trajectory", engine='pyxlsb', skiprows=5)
    sr = pd.Series(pd.date_range('1991-01-04', periods = df2.shape[0], freq = 'W'))
    df2 = pd.concat([df2, sr], axis=1)
    df2.columns = ["Date_Number","Directonal","Horizontal", "Vertical", "Total", "% DIR.","% HORIZ.", "% VERT.","Date"]
    df2.index = df2["Date"]


    # Count per MGulf of Mexico

    df3 = pd.read_excel(xld, "Gulf of Mexico Split", engine='pyxlsb', skiprows=7)
    sr = pd.Series(pd.date_range('2000-01-07', periods = df3.shape[0], freq = 'W'))
    df3 = pd.concat([df3, sr], axis=1)
    df3.columns = ["Date_Number","US_Offshore","Total_GoM", "Gas_GoM", "Oil_GoM","NaN", "Date"]
    df3.index = df3["Date"]
    df3["Other_Offshore"] = df3["US_Offshore"] - df3["Total_GoM"]
    df3 = df3[["US_Offshore", "Gas_GoM", "Oil_GoM", "Other_Offshore"]]
    df3.columns = ["Total", "Gas", "Oil", "Other"]
    df3.dropna(inplace=True)

    # Count per Basin

    df4 = pd.read_excel(xld, "US Count by Basin", engine='pyxlsb', skiprows=10)
    sr = pd.Series(pd.date_range('2011-02-04', periods = df4.shape[0], freq = 'W'))
    df4 = pd.concat([df4, sr], axis=1)
    df4.columns = ["Date_Number","Ardmore_Oil","Ardmore_Gas", "Ardmore_Misc","Ardmore_Total","Arkoma_Oil","Arkoma_Gas", "Arkoma_Misc","Arkoma_Total", "Barnett_Oil","Barnett_Gas", "Barnett_Misc","Barnett_Total","Cana_Woodford_Oil","Cana_Woodford_Gas", "Cana_Woodford_Misc","Cana_Woodford_Total", "DJ-Niobrara_Oil","DJ-Niobrara_Gas", "DJ-Niobrara_Misc","DJ-Niobrara_Total", "Eagle_Ford_Oil","Eagle_Ford_Gas", "Eagle_Ford_Misc","Eagle_Ford_Total", "Fayetteville_Oil","Fayetteville_Gas", "Fayetteville_Misc","Fayetteville_Total", "Granite_Wash_Oil","Granite_Wash_Gas", "Granite_Wash_Misc","Granite_Wash_Total", "Haynesville_Oil","Haynesville_Gas", "Haynesville_Misc","Haynesville_Total","Marcellus_Oil","Marcellus_Gas", "Marcellus_Misc","Marcellus_Total", "Mississippian_Oil","Mississippian_Gas", "Mississippian_Misc","Mississippian_Total", "Permian_Oil","Permian_Gas", "Permian_Misc","Permian_Total", "Utica_Oil","Utica_Gas", "Utica_Misc","Utica_Total", "Williston_Oil","Williston_Gas", "Williston_Misc","Williston_Total", "Others_Oil","Others_Gas", "Others_Misc","Others_Total", "Total_US_Oil","Total_US_Gas", "Total_US_Misc","Total_US_Total", "Nan", "Date"]
    df4.index = df4["Date"]
    df4 = df4[["Ardmore_Oil","Arkoma_Oil", "Barnett_Oil", "Cana_Woodford_Oil", "DJ-Niobrara_Oil", "Eagle_Ford_Oil", "Fayetteville_Oil", "Granite_Wash_Oil", "Haynesville_Oil", "Marcellus_Oil", "Mississippian_Oil", "Permian_Oil", "Utica_Oil", "Williston_Oil", "Others_Oil", "Total_US_Oil"]]
    df4.columns = ["Ardmore","Arkoma", "Barnett", "Cana", "DJ-Niobrara", "Eagle Ford", "Fayetteville", "Granite Wash", "Haynesville", "Marcellus", "Mississippian", "Permian", "Utica", "Williston", "Others", "Total"]
    df4.dropna(inplace=True)


        # U.S. weekly production data
    Production = pd.read_excel('http://ir.eia.gov/wpsr/psw01.xls', "Data 2", index_col="Date", parse_dates=["Date"], skiprows=2)

    Production_cols = ['US_production_crude','Alaska_production_crude','lower48_production_crude','crude_netImports','crude_Imports','imports_excSpr','importsby_spr', 'importsfor_spr','crude_exports','stock_change','SPR_change','change_excSPR', 'crude_unaccounted','refinery_input','refinery_production_netGas','gasLiquids_production','renewable_production','Oxygenate','Fuel-Oxygenates',' Processing_Gain', 'netImports_products','products_imports', 'products_exports', 'products_change', 'supply_adjustment_products', 'products_supplied', 'Motor_Gasoline','Jet_Fue','Distillate_Fuel ' ,' Residual_Fuel' ,' Propane_Propylene' ,'Other_Oils ' ,'netImports_petroleum_products']
    Production.columns = Production_cols

    # Subset
    Production= Production["1987-07-19":"2050"]
    #ProductionP1 = Production["2010-01-01":"2015-06-20"]
    Production["US_production_crude_Shift"] = Production['US_production_crude'].shift(-38)


    df["ShiftOilRigs"] = df['OilRigs'].shift(-12)
    df["OilRigsLog"] = np.log(df["ShiftOilRigs"])
    df["CL1Log"] = np.log(df["CL1"]) 
    


    a=[]
    b=[] 

    for i in list(set(df1.index.year)):
        m1 = smf.ols('df1[str(i):str(i+1)].iloc[:,0:1] ~ df1[str(i):str(i+1)].iloc[:,1:2]', df1[str(i):str(i+1)]).fit()
        a.append(m1.params[1])
        b.append(str(i))
    a
    b

    dflist = pd.DataFrame(a,b)
    dflist.columns = ["koefficient"]
    dflist["koefficientdelta"] = dflist["koefficient"].diff()
    dflist = dflist.fillna(0)
    dflist = dflist.iloc[dflist['koefficientdelta'].abs().argsort()][::-1]
    largest = dflist[:15]
    largest = largest.sort_index()


    a=[]
    b=[] 

    count = 1
    for i in list(largest.index.values):
        for j in [1,2,3,4,5,6,7,8,9,10,11,12]:
            m1 = smf.ols('OilRigs ~ ShiftCL1', df1[str(i)+"-01-" + str(j):str(i)]).fit()
            a.append(m1.params[1])
            b.append(str(i) +"-01-" + str(j))
            count+=1
    a
    b


    dflist = pd.DataFrame(a,b)
    dflist.columns = ["koefficient"]
    dflist["koefficientdelta"] = dflist["koefficient"].diff()
    dflist = dflist.fillna(0)
    dflist = dflist.iloc[dflist['koefficientdelta'].abs().argsort()][::-1]
    largest = dflist[:15]
    largest = largest.sort_index()

    largest.index = pd.to_datetime(largest.index)


    df1["Dummy_Last"] = 0
    df1.loc[(df1.index >=str(largest.index[-1])) & (df1.index <="2200"), 'Dummy_Last'] = 1

    df1["Dummy_0"] = 0
    df1.loc[(df1.index >=str(df1.index[0].strftime('%Y-%m-%d'))) & (df1.index <=largest.index[0]), 'Dummy_0'] = 1

    count = 0
    for i in largest.index:
        if count < len(largest.index[:-1]):
            dfDummies = pd.get_dummies((df1.index >= largest.index[count]) & (df1.index <largest.index[count+1]))
            dfDummies.index = df1.index
            df1 = pd.concat([df1, dfDummies], axis=1)
            count+=1



    cols = []
    count = 1
    for i in df1.columns:
        if i == True:
            cols.append(f'Dummy_{count}')
            count+=1
            continue
        cols.append(i)
    df1.columns = cols

    df1 = df1.drop(False, 1)


    m1 = smf.ols('df1.iloc[:,0:1]~ df1.iloc[:,1:]', df1).fit()

    #print(m1.summary())
    df1['Forecast'] = m1.fittedvalues

    from statsmodels.sandbox.regression.predstd import wls_prediction_std
    prstd, iv_l, iv_u = wls_prediction_std(m1)

    iv_l = pd.DataFrame(iv_l)
    iv_u = pd.DataFrame(iv_u)

    iv_l.columns=["Lower"]
    iv_u.columns=["Upper"]

    df1 = pd.concat([df1, iv_l, iv_u], axis=1)


    Production["US_production_crude_Shift"] = Production['US_production_crude'].shift(-38)

    df = df.drop('Date', 1)
    df2 = df2.drop('Date', 1)


    library.write('df', df)
    library.write('df1', df1)
    library.write('Production', Production)
    library.write('df4', df4)
    library.write('df2', df2)
    library.write('df3', df3)
    library.write('CL1', CL1)


    print("--- %s seconds : rigcountAPI" % (time.time() - start_time))


if __name__ == '__main__':
    main()
