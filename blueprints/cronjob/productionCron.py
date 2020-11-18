from statsmodels.sandbox.regression.predstd import wls_prediction_std
from arctic import Arctic
from pymongo import MongoClient
import quandl
import pymongo
import time
from matplotlib import pyplot as plt
import plotly.figure_factory as ff
import plotly.tools as tls
import statsmodels.formula.api as smf
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import seaborn as sns
import re
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import numpy as np
import os
from dateutil import parser
from datetime import timezone
import pytz
sns.set()


def main():
    # change streams MongoDB
    start_time = time.time()

    # Connect to Local MONGODB
    # store = Arctic('mongodb+srv://MarcusMLarsson:Britney1234@mongodb-0ydzb.azure.mongodb.net/test?retryWrites=true&w=majority')
    store = Arctic('mongodb://MarcusMLarsson:Britney1234@mongodb-shard-00-00-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-01-0ydzb.azure.mongodb.net:27017,mongodb-shard-00-02-0ydzb.azure.mongodb.net:27017/test?ssl=true&replicaSet=MongoDB-shard-0&authSource=admin&retryWrites=true&w=majority')

    # Create the library - defaults to VersionStore
    store.initialize_library('PRODUCTION')

    # Access the library
    library = store['PRODUCTION']

    Canada = quandl.get("JODI/OIL_CRPRKD_CAN", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Argentina = quandl.get("JODI/OIL_CRPRKD_ARG", authtoken="ExYhsQRV9jyhdRQWb_s8") # 0.5MMbbls/d
    Australia = quandl.get("JODI/OIL_CRPRKD_AUS", authtoken="ExYhsQRV9jyhdRQWb_s8")  # 0.5MMbbls/d
    Austria = quandl.get("JODI/OIL_CRPRKD_AUT", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Azerbaijan = quandl.get("JODI/OIL_CRPRKD_AZE", authtoken="ExYhsQRV9jyhdRQWb_s8")  # 1MMbbls/d

    Bahrain = quandl.get("JODI/OIL_CRPRKD_BHR", authtoken="ExYhsQRV9jyhdRQWb_s8") #0.2 MMbbls/d
    Brazil = quandl.get("JODI/OIL_CRPRKD_BRA", authtoken="ExYhsQRV9jyhdRQWb_s8") # 2.5MMbbls/d
    Brunei = quandl.get("JODI/OIL_CRPRKD_BDI", authtoken="ExYhsQRV9jyhdRQWb_s8") #0.2

    Canada = quandl.get("JODI/OIL_CRPRKD_CAN", authtoken="ExYhsQRV9jyhdRQWb_s8") #4 MMbbls/d
    China = quandl.get("JODI/OIL_CRPRKD_CHN", authtoken="ExYhsQRV9jyhdRQWb_s8")  #4 MMbbls/d
    Columbia = quandl.get("JODI/OIL_CRPRKD_COL", authtoken="ExYhsQRV9jyhdRQWb_s8") #0.5 MMbbls/d
    Croatia = quandl.get("JODI/OIL_CRPRKD_HRV", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Denmark = quandl.get("JODI/OIL_CRPRKD_DNK", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Ecuador= quandl.get("JODI/OIL_CRPRKD_ECU", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Egypt = quandl.get("JODI/OIL_CRPRKD_EGY", authtoken="ExYhsQRV9jyhdRQWb_s8")

    France = quandl.get("JODI/OIL_CRPRKD_FRA", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Germany = quandl.get("JODI/OIL_CRPRKD_DEU", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Hungary = quandl.get("JODI/OIL_CRPRKD_HUN", authtoken="ExYhsQRV9jyhdRQWb_s8")

    India = quandl.get("JODI/OIL_CRPRKD_IND", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Indonesia = quandl.get("JODI/OIL_CRPRKD_IDN", authtoken="ExYhsQRV9jyhdRQWb_s8") #0.8
    Italy = quandl.get("JODI/OIL_CRPRKD_ITA", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Kazakhstan= quandl.get("JODI/OIL_CRPRKD_KAZ", authtoken="ExYhsQRV9jyhdRQWb_s8") #1.5


    Malaysia= quandl.get("JODI/OIL_CRPRKD_MYS", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Mexicao= quandl.get("JODI/OIL_CRPRKD_MEX", authtoken="ExYhsQRV9jyhdRQWb_s8") #2

    Netherlands= quandl.get("JODI/OIL_CRPRKD_NLD", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Norway= quandl.get("JODI/OIL_CRPRKD_NOR", authtoken="ExYhsQRV9jyhdRQWb_s8")  #1.5
    NewZealand = quandl.get("JODI/OIL_CRPRKD_NZL", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Oman = quandl.get("JODI/OIL_CRPRKD_OMN", authtoken="ExYhsQRV9jyhdRQWb_s8") #1

    Peru= quandl.get("JODI/OIL_CRPRKD_PER", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Qatar = quandl.get("JODI/OIL_CRPRKD_QAT", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Romania = quandl.get("JODI/OIL_CRPRKD_ROU", authtoken="ExYhsQRV9jyhdRQWb_s8") #0.8
    Russia = quandl.get("JODI/OIL_CRPRKD_RUS", authtoken="ExYhsQRV9jyhdRQWb_s8") #10

    Thailand = quandl.get("JODI/OIL_CRPRKD_THA", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Trinidad = quandl.get("JODI/OIL_CRPRKD_TTO", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Turkey = quandl.get("JODI/OIL_CRPRKD_TUR", authtoken="ExYhsQRV9jyhdRQWb_s8")


    UK = quandl.get("JODI/OIL_CRPRKD_GBR", authtoken="ExYhsQRV9jyhdRQWb_s8") #1M
    USA = quandl.get("JODI/OIL_CRPRKD_USA", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Algeria = quandl.get("JODI/OIL_CRPRKD_DZA", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Angola = quandl.get("JODI/OIL_CRPRKD_AGO", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Equatorial_Guniea = quandl.get("JODI/OIL_CRPRKD_GNQ", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Gabon = quandl.get("JODI/OIL_CRPRKD_GAB", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Iran = quandl.get("JODI/OIL_CRPRKD_IRN", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Iraq = quandl.get("JODI/OIL_CRPRKD_IRQ", authtoken="ExYhsQRV9jyhdRQWb_s8")

    Kuwait= quandl.get("JODI/OIL_CRPRKD_KWT", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Libya= quandl.get("JODI/OIL_CRPRKD_LAJ", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Nigeria= quandl.get("JODI/OIL_CRPRKD_NGA", authtoken="ExYhsQRV9jyhdRQWb_s8")

    SaudiArabia = quandl.get("JODI/OIL_CRPRKD_SAU", authtoken="ExYhsQRV9jyhdRQWb_s8")
    UAE = quandl.get("JODI/OIL_CRPRKD_ARE", authtoken="ExYhsQRV9jyhdRQWb_s8")
    Venezuela = quandl.get("JODI/OIL_CRPRKD_VEN", authtoken="ExYhsQRV9jyhdRQWb_s8")


    df = pd.concat([Algeria,Angola,Argentina,Australia,Austria,Azerbaijan,Bahrain,Brazil,Brunei,Canada,China,Columbia,Croatia,Denmark,Ecuador,Equatorial_Guniea, Egypt,France,Gabon,Germany,Hungary,India,Indonesia,Iran,Iraq,Italy,Kazakhstan,Kuwait, Libya, Malaysia,Mexicao,Netherlands,Nigeria,Norway,NewZealand,Oman,Peru,Qatar,Romania,Russia,SaudiArabia,Thailand,Trinidad,Turkey,UAE, UK, USA,Venezuela], axis=1)
    df.drop(list(df.filter(regex = 'Notes')), axis = 1, inplace = True)

    df.columns = ["Algeria","Angola","Argentina","Australia","Austria","Azerbaijan","Bahrain","Brazil","Brunei","Canada","China","Columbia","Croatia","Denmark","Ecuador","Equatorial_Guniea","Egypt","France","Gabon","Germany","Hungary","India","Indonesia","Iran","Iraq","Italy","Kazakhstan","Kuwait", "Libya","Malaysia","Mexicao","Netherlands","Nigeria","Norway","NewZealand","Oman","Peru","Qatar","Romania","Russia","SaudiArabia","Thailand","Trinidad","Turkey","UAE", "UK","USA","Venezuela"]
    df.replace(0, np.nan, inplace=True)
    df.fillna(method="bfill", inplace=True)
    df.fillna(method="ffill", inplace=True)
    df = df/1000
    df["World"] = df.sum(axis=1, skipna= True)
    df["OPEC"] = df["Algeria"] + df["Angola"] + df["Equatorial_Guniea"] + df["Gabon"] + df["Iran"]+ df["Iraq"]+ df["Kuwait"]+ df["Libya"]+ df["Nigeria"]+ df["SaudiArabia"]+ df["UAE"]+ df["Venezuela"]
    df["WordLessUSA"] = df["World"] - df["USA"]
    df["NonOPEC"] = df["World"] - df["OPEC"]
    df["NonOPECLessUSA"] = df["NonOPEC"] - df["USA"]


    AlgeriaYoY = df["Algeria"]- df["Algeria"].shift(12)
    AngolaYoY = df["Angola"]- df["Angola"].shift(12)
    EcuadorYoY = df["Ecuador"]- df["Ecuador"].shift(12)
    GabonYoY = df["Gabon"]- df["Gabon"].shift(12)
    IranYoY = df["Iran"]- df["Iran"].shift(12)
    IraqYoY = df["Iraq"]- df["Iraq"].shift(12)
    KuwaitYoY = df["Kuwait"]- df["Kuwait"].shift(12)
    LibyaYoY = df["Libya"]- df["Libya"].shift(12)
    SaudiArabiaYoY = df["SaudiArabia"]- df["SaudiArabia"].shift(12)
    UAEYoY = df["UAE"]- df["UAE"].shift(12)
    VenezuelaYoY = df["Venezuela"]- df["Venezuela"].shift(12)

    wAlgeriaYoY = df["Algeria"]- df["Algeria"].shift(1)
    wAngolaYoY = df["Angola"]- df["Angola"].shift(1)
    wEcuadorYoY = df["Ecuador"]- df["Ecuador"].shift(1)
    wGabonYoY = df["Gabon"]- df["Gabon"].shift(1)
    wIranYoY = df["Iran"]- df["Iran"].shift(1)
    wIraqYoY = df["Iraq"]- df["Iraq"].shift(1)
    wKuwaitYoY = df["Kuwait"]- df["Kuwait"].shift(1)
    wLibyaYoY = df["Libya"]- df["Libya"].shift(1)
    wSaudiArabiaYoY = df["SaudiArabia"]- df["SaudiArabia"].shift(1)
    wUAEYoY = df["UAE"]- df["UAE"].shift(1)
    wVenezuelaYoY = df["Venezuela"]- df["Venezuela"].shift(1)

    dAlgeriaYoY = df["Algeria"]- df["Algeria"].shift(120)
    dAngolaYoY = df["Angola"]- df["Angola"].shift(120)
    dEcuadorYoY = df["Ecuador"]- df["Ecuador"].shift(120)
    dGabonYoY = df["Gabon"]- df["Gabon"].shift(120)
    dIranYoY = df["Iran"]- df["Iran"].shift(120)
    dIraqYoY = df["Iraq"]- df["Iraq"].shift(120)
    dKuwaitYoY = df["Kuwait"]- df["Kuwait"].shift(120)
    dLibyaYoY = df["Libya"]- df["Libya"].shift(120)
    dSaudiArabiaYoY = df["SaudiArabia"]- df["SaudiArabia"].shift(120)
    dUAEYoY = df["UAE"]- df["UAE"].shift(120)
    dVenezuelaYoY = df["Venezuela"]- df["Venezuela"].shift(120)


    Water_data = pd.concat([AlgeriaYoY, AngolaYoY, EcuadorYoY, GabonYoY, IranYoY, IraqYoY, KuwaitYoY, LibyaYoY, SaudiArabiaYoY, UAEYoY, VenezuelaYoY], axis=1)
    Water_data1 = Water_data.tail(1)
    Water_data1["YoY Change"] = Water_data1.sum(axis=1, skipna= True)

    Water_data2 = pd.concat([wAlgeriaYoY, wAngolaYoY, wEcuadorYoY, wGabonYoY, wIranYoY, wIraqYoY, wKuwaitYoY, wLibyaYoY, wSaudiArabiaYoY, wUAEYoY, wVenezuelaYoY], axis=1)
    Water_data3 = Water_data2.tail(1)
    Water_data3["YoY Change"] = Water_data3.sum(axis=1, skipna= True)

    Water_data6 = pd.concat([dAlgeriaYoY, dAngolaYoY, dEcuadorYoY, dGabonYoY, dIranYoY, dIraqYoY, dKuwaitYoY, dLibyaYoY, dSaudiArabiaYoY, dUAEYoY, dVenezuelaYoY], axis=1)
    Water_data7 = Water_data6.tail(1)
    Water_data7["YoY Change"] = Water_data7.sum(axis=1, skipna= True)



    # Store the data in the library
    library.write('df', df)
    library.write('Water_data1', Water_data1)
    library.write('Water_data3', Water_data3)
    library.write('Water_data7', Water_data7)
    #Water_data1
 


    print("--- %s seconds : productionAPI" % (time.time() - start_time))


if __name__ == '__main__':
    main()
