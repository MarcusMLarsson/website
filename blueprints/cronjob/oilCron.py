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
    store.initialize_library('OIL')

    # Access the library
    library = store['OIL']

    dfUS = pd.read_excel('http://ir.eia.gov/wpsr/psw01.xls', "Data 1", usecols="A:C, S:T", index_col="Date", parse_dates=["Date"],
                         skiprows=2)
    # Historical Spot Price
    dfSpot = pd.read_excel('https://www.eia.gov/dnav/pet/xls/PET_PRI_SPT_S1_W.xls', "Data 1", parse_dates=["Date"],
                           index_col="Date", skiprows=[0, 1])
    # Intrada Spot Price
    dfIntraSpotWTI = quandl.get(
        "CHRIS/CME_CL1", authtoken="ExYhsQRV9jyhdRQWb_s8", index_col="Date", parse_dates=["Date"])
    dfIntraSpotWTI = dfIntraSpotWTI["2010":"2050"]

    dfIntraSpotBRENT = quandl.get(
        "CHRIS/CME_UB1", authtoken="ExYhsQRV9jyhdRQWb_s8", index_col="Date", parse_dates=["Date"])
    dfIntraSpotBRENT = dfIntraSpotBRENT["2010":"2050"]

    # Subset
    dfUS = dfUS["2010":"2050"]*1000
    dfSpot = dfSpot["2010":"2050"]

    Geo = pd.read_excel('https://www.matteoiacoviello.com/gpr_files/gpr_daily_latest.xlsx',
                        "Sheet1", parse_dates=["DATE"], index_col="DATE")
    Geo = Geo["GPRD*"]["2010-01-01":"2100"]

    ntrain = dfUS.shape[0]

    Geo = Geo[:ntrain]
    Geo.index = dfUS.index

    dfUS = pd.concat([dfUS, Geo], axis=1)

    # Create seasonal dummies
    dfDummies = pd.get_dummies(dfUS.index.week)
    dfDummies.index = dfUS.index
    dfUS = pd.concat([dfUS, dfDummies], axis=1)

    # Rename cols
    dfUS_cols = ['crude_oil', 'crude_no_spr', 'inventory', 'inventory_no_spr', 'GPR', 'W1', 'W2', 'W3', 'W4', 'W5',
                 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W20',
                 'W21', 'W22', 'W23', 'W24', 'W25', 'W26', 'W27', 'W28', 'W29', 'W30', 'W31', 'W32', 'W33', 'W34',
                 'W35', 'W36', 'W37', 'W38', 'W39', 'W40', 'W41', 'W42', 'W43', 'W44', 'W45', 'W46', 'W47', 'W48',
                 'W49', 'W50', 'W51', 'W52', 'W53']
    dfUS.columns = dfUS_cols

    dfSpot_cols = ['WTI', 'Brent']
    dfSpot.columns = dfSpot_cols

    # IEA MONTHLY INVENTORY REPORT
    dfOECD = pd.read_excel('https://www.eia.gov/totalenergy/data/browser/xls.php?tbl=T03.04&freq=m',
                           "Monthly Data", index_col="Month", parse_dates=["Month"], skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11])

    # Subset
    dfOECD = dfOECD["2010":"2030"]

    # Create dummies
    dfdummy = pd.get_dummies(dfOECD.index.month)
    dfdummy.index = dfOECD.index
    dfOECD = pd.concat([dfdummy, dfOECD], axis=1)

    # Rename cols
    dfOECD_cols = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'CrudeSPR', 'CrudeNonSpr', 'CrudeTot',
                   'Distillate', 'Propane', 'Propylene', 'Propane&Propylene', 'GasLiquids', 'JetFuel', 'MotorGasoline', 'Residual', 'Other', 'stocks_oecd']
    dfOECD.columns = dfOECD_cols

    # Spot Prices for Crude Oil and Petroleum Products - EIA
    dfBrent = pd.read_excel('https://www.eia.gov/dnav/pet/xls/PET_PRI_SPT_S1_M.xls',
                            "Data 1", parse_dates=["Date"], index_col="Date", skiprows=[0, 1])

    # Rename cols
    dfBrent_cols = ['WTI', 'Brent']
    dfBrent.columns = dfBrent_cols

    dfBrent.reset_index(inplace=True)
    dfBrent['Date'] = dfBrent['Date'].values.astype('datetime64[M]')
    dfBrent.set_index('Date', inplace=True)

    dfBrent = dfBrent["2010":"2030"]
    dfOECD = pd.concat([dfOECD, dfBrent], axis=1)

    # Create Year variable
    dfOECD.reset_index(inplace=True)
    dfOECD['Year'] = dfOECD['index'].dt.year
    dfOECD.set_index('index', inplace=True)

    # Log Transformation
    dfUS['crude_log'] = np.log(dfUS.crude_oil)
    dfUS['crude_no_spr_log'] = np.log(dfUS.crude_no_spr)
    dfUS['inventory_log'] = np.log(dfUS.inventory)
    dfUS['inventory_no_spr_log'] = np.log(dfUS.inventory_no_spr)

    # Linear Regression
    m1 = smf.ols('crude_log ~ W1 +W2+ W3+ W4+ W5+ W6+ W7+ W8+ W9+ W10+ W11+ W12+ W13+ W14+ W15+ W16+ W17+ W18+ W19+ W20+ W21+ W22+ W23+ W24+ W25+ W26+ W27+ W28+ W29+ W30+ W31+ W32+ W33+ W34+ W35+ W36+ W37+ W38+ W39+ W40+ W41+ W42+ W43+ W44+ W45+ W46+ W47+ W48+ W49+ W50+ W51+ W52+ W53 -1', dfUS).fit()
    m2 = smf.ols('crude_no_spr_log ~ W1 +W2+ W3+ W4+ W5+ W6+ W7+ W8+ W9+ W10+ W11+ W12+ W13+ W14+ W15+ W16+ W17+ W18+ W19+ W20+ W21+ W22+ W23+ W24+ W25+ W26+ W27+ W28+ W29+ W30+ W31+ W32+ W33+ W34+ W35+ W36+ W37+ W38+ W39+ W40+ W41+ W42+ W43+ W44+ W45+ W46+ W47+ W48+ W49+ W50+ W51+ W52+ W53 -1', dfUS).fit()
    m3 = smf.ols('inventory_log ~ W1 +W2+ W3+ W4+ W5+ W6+ W7+ W8+ W9+ W10+ W11+ W12+ W13+ W14+ W15+ W16+ W17+ W18+ W19+ W20+ W21+ W22+ W23+ W24+ W25+ W26+ W27+ W28+ W29+ W30+ W31+ W32+ W33+ W34+ W35+ W36+ W37+ W38+ W39+ W40+ W41+ W42+ W43+ W44+ W45+ W46+ W47+ W48+ W49+ W50+ W51+ W52+ W53 -1', dfUS).fit()
    m4 = smf.ols('inventory_no_spr_log ~ W1 +W2+ W3+ W4+ W5+ W6+ W7+ W8+ W9+ W10+ W11+ W12+ W13+ W14+ W15+ W16+ W17+ W18+ W19+ W20+ W21+ W22+ W23+ W24+ W25+ W26+ W27+ W28+ W29+ W30+ W31+ W32+ W33+ W34+ W35+ W36+ W37+ W38+ W39+ W40+ W41+ W42+ W43+ W44+ W45+ W46+ W47+ W48+ W49+ W50+ W51+ W52+ W53 -1', dfUS).fit()

    # Predict Residuals
    dfUS['RIN_crude'] = m1.resid
    dfUS['RIN_crude_no_spr'] = m2.resid
    dfUS['RIN_inventory'] = m3.resid
    dfUS['RIN_inventory_no_spr'] = m4.resid

    # Concat Inventory Data with Weekly Spot Price
    dfUS = pd.concat([dfUS, dfSpot], axis=1)

    # Predict residuals
    dfUS['RINsqr_crude'] = dfUS['RIN_crude']**2
    dfUS['RINsqr_crude_no_spr'] = dfUS['RIN_crude_no_spr']**2
    dfUS['RINsqr_inventory'] = dfUS['RIN_inventory']**2
    dfUS['RINsqr_inventory_no_spr'] = dfUS['RIN_inventory_no_spr']**2

    # Substitue "Latest Week" observation to intraday spot price
    dfUS['WTI'].iloc[-1:] = dfIntraSpotWTI['Settle'].iloc[-1:].values

    # Predict forecast
    m5 = smf.ols('WTI ~ RIN_crude + RINsqr_crude', dfUS).fit()
    m6 = smf.ols('WTI ~ RIN_crude_no_spr + RINsqr_crude_no_spr', dfUS).fit()
    m7 = smf.ols('WTI ~ RIN_inventory + RINsqr_inventory', dfUS).fit()
    m8 = smf.ols(
        'WTI ~ RIN_inventory_no_spr + RINsqr_inventory_no_spr', dfUS).fit()

    dfUS['Forecast_crude'] = m5.fittedvalues
    dfUS['Forecast_crude_no_spr'] = m6.fittedvalues
    dfUS['Forecast_inventory'] = m7.fittedvalues
    dfUS['Forecast_inventory_no_spr'] = m8.fittedvalues

    # 95 % confidence interval
    prstd, iv_l_crude, iv_u_crude = wls_prediction_std(m5)
    prstd, iv_l_crude_no_spr, iv_u_crude_no_spr = wls_prediction_std(m6)
    prstd, iv_l_inventory, iv_u_inventory = wls_prediction_std(m7)
    prstd, iv_l_inventory_no_spr, iv_u_inventory_no_spr = wls_prediction_std(
        m8)

    iv_l_crude = pd.DataFrame(iv_l_crude)
    iv_u_crude = pd.DataFrame(iv_u_crude)
    iv_l_crude_no_spr = pd.DataFrame(iv_l_crude_no_spr)
    iv_u_crude_no_spr = pd.DataFrame(iv_u_crude_no_spr)
    iv_l_inventory = pd.DataFrame(iv_l_inventory)
    iv_u_inventory = pd.DataFrame(iv_u_inventory)
    iv_l_inventory_no_spr = pd.DataFrame(iv_l_inventory_no_spr)
    iv_u_inventory_no_spr = pd.DataFrame(iv_u_inventory_no_spr)

    iv_l_crude.columns = ["lower_crude"]
    iv_u_crude.columns = ["upper_crude"]
    iv_l_crude_no_spr.columns = ["lower_crude_no_spr"]
    iv_u_crude_no_spr.columns = ["upper_crude_no_spr"]
    iv_l_inventory.columns = ["lower_inventory"]
    iv_u_inventory.columns = ["upper_inventory"]
    iv_l_inventory_no_spr.columns = ["lower_inventory_no_spr"]
    iv_u_inventory_no_spr.columns = ["upper_inventory_no_spr"]

    # Concatenation
    dfUS = pd.concat([dfUS, iv_l_crude, iv_u_crude, iv_l_crude_no_spr, iv_u_crude_no_spr,
                      iv_l_inventory, iv_u_inventory, iv_l_inventory_no_spr, iv_u_inventory_no_spr], axis=1)

    # Create year variable to hue by year
    dfUS.reset_index(inplace=True)
    dfUS['Year'] = dfUS['Date'].dt.year
    dfUS['YearMonth'] = dfUS['Date'].map(lambda x: 100*x.year + x.month)
    dfUS.set_index('Date', inplace=True)
    dfUS['Year'] = dfUS['Year'].astype(str)
    dfUS['Year'].iloc[-1:] = 'Latest Week'

    # Log transformation
    dfOECD["CrudeTot"] = dfOECD.CrudeTot.astype(float)
    dfOECD["CrudeNonSpr"] = dfOECD.CrudeNonSpr.astype(float)
    dfOECD["stocks_oecd"] = dfOECD.stocks_oecd.astype(float)
    dfOECD["CrudeSPR"] = dfOECD.CrudeSPR.astype(float)

    dfOECD['crude_log'] = np.log(dfOECD.CrudeTot)
    dfOECD['crude_no_spr_log'] = np.log(dfOECD.CrudeNonSpr)
    dfOECD['inventory_log'] = np.log(dfOECD.stocks_oecd)
    dfOECD['inventory_no_spr_log'] = np.log(
        (dfOECD.stocks_oecd - dfOECD.CrudeSPR))

    # Linear Regression
    m9 = smf.ols(
        'crude_log ~ M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12 -1', dfOECD).fit()
    m10 = smf.ols(
        'crude_no_spr_log ~ M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12 -1', dfOECD).fit()
    m11 = smf.ols(
        'inventory_log ~ M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12 -1', dfOECD).fit()
    m12 = smf.ols(
        'inventory_no_spr_log ~ M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12 -1', dfOECD).fit()

    # Predict Residuals
    dfOECD['RIN_crude'] = m9.resid
    dfOECD['RIN_crude_no_spr'] = m10.resid
    dfOECD['RIN_inventory'] = m11.resid
    dfOECD['RIN_inventory_no_spr'] = m12.resid

    # Square relative inventory
    dfOECD['RINsqr_crude'] = dfOECD['RIN_crude']**2
    dfOECD['RINsqr_crude_no_spr'] = dfOECD['RIN_crude_no_spr']**2
    dfOECD['RINsqr_inventory'] = dfOECD['RIN_inventory']**2
    dfOECD['RINsqr_inventory_no_spr'] = dfOECD['RIN_inventory_no_spr']**2

    # Predict forecast
    m13 = smf.ols('Brent ~ RIN_crude + RINsqr_crude', dfOECD).fit()
    m14 = smf.ols(
        'Brent ~ RIN_crude_no_spr + RINsqr_crude_no_spr', dfOECD).fit()
    m15 = smf.ols('Brent ~ RIN_inventory + RINsqr_inventory', dfOECD).fit()
    m16 = smf.ols(
        'Brent ~ RIN_inventory_no_spr + RINsqr_inventory_no_spr', dfOECD).fit()

    dfOECD['Forecast_crude'] = m13.fittedvalues
    dfOECD['Forecast_crude_no_spr'] = m14.fittedvalues
    dfOECD['Forecast_inventory'] = m15.fittedvalues
    dfOECD['Forecast_inventory_no_spr'] = m16.fittedvalues

    # 95 % confidence interval
    prstd, iv_l_crude, iv_u_crude = wls_prediction_std(m13)
    prstd, iv_l_crude_no_spr, iv_u_crude_no_spr = wls_prediction_std(m14)
    prstd, iv_l_inventory, iv_u_inventory = wls_prediction_std(m15)
    prstd, iv_l_inventory_no_spr, iv_u_inventory_no_spr = wls_prediction_std(
        m16)

    iv_l_crude = pd.DataFrame(iv_l_crude)
    iv_u_crude = pd.DataFrame(iv_u_crude)
    iv_l_crude_no_spr = pd.DataFrame(iv_l_crude_no_spr)
    iv_u_crude_no_spr = pd.DataFrame(iv_u_crude_no_spr)
    iv_l_inventory = pd.DataFrame(iv_l_inventory)
    iv_u_inventory = pd.DataFrame(iv_u_inventory)
    iv_l_inventory_no_spr = pd.DataFrame(iv_l_inventory_no_spr)
    iv_u_inventory_no_spr = pd.DataFrame(iv_u_inventory_no_spr)

    iv_l_crude.columns = ["lower_crude"]
    iv_u_crude.columns = ["upper_crude"]
    iv_l_crude_no_spr.columns = ["lower_crude_no_spr"]
    iv_u_crude_no_spr.columns = ["upper_crude_no_spr"]
    iv_l_inventory.columns = ["lower_inventory"]
    iv_u_inventory.columns = ["upper_inventory"]
    iv_l_inventory_no_spr.columns = ["lower_inventory_no_spr"]
    iv_u_inventory_no_spr.columns = ["upper_inventory_no_spr"]

    # Concatenation
    dfOECD = pd.concat([dfOECD, iv_l_crude, iv_u_crude, iv_l_crude_no_spr, iv_u_crude_no_spr,
                        iv_l_inventory, iv_u_inventory, iv_l_inventory_no_spr, iv_u_inventory_no_spr], axis=1)

    # Create year variable to hue by year
    dfOECD.reset_index(inplace=True)
    dfOECD['Year'] = dfOECD['index'].dt.year
    dfOECD['YearMonth'] = dfOECD['index'].map(lambda x: 100*x.year + x.month)
    dfOECD.set_index('index', inplace=True)

    # Substitue "Latest Week" observation to intraday spot price
    dfOECD['Brent'].iloc[-1:] = dfIntraSpotBRENT['Settle'].iloc[-1:].values

    pd.set_option('colheader_justify', 'center')
    dfUStable = dfUS

    dfUStable["Date"] = dfUStable.index
    dfUStable["Forecast_crude"] = round(dfUStable["Forecast_crude"], 2)
    dfUStable["Forecast_crude_no_spr"] = round(
        dfUStable["Forecast_crude_no_spr"], 2)
    dfUStable["Forecast_inventory"] = round(dfUStable["Forecast_inventory"], 2)
    dfUStable["Forecast_inventory_no_spr"] = round(
        dfUStable["Forecast_inventory_no_spr"], 2)
    dfUStable["Error_crude"] = round(
        (dfUStable["Forecast_crude"] - dfUStable["WTI"]), 2)
    dfUStable["Error_crude_no_spr"] = round(
        (dfUStable["Forecast_crude_no_spr"] - dfUStable["WTI"]), 2)
    dfUStable["Error_inventory"] = round(
        (dfUStable["Forecast_inventory"] - dfUStable["WTI"]), 2)
    dfUStable["Error_inventory_no_spr"] = round(
        (dfUStable["Forecast_inventory_no_spr"] - dfUStable["WTI"]), 2)
    dfUStable["Inventory_no_spr"] = round(
        (dfUStable["inventory_no_spr"]/1000), 0).astype(int)
    dfUStable["Inventory"] = round(
        (dfUStable["inventory"]/1000), 0).astype(int)
    dfUStable["Crude"] = round((dfUStable["crude_oil"]/1000), 0).astype(int)
    dfUStable["Crude_no_spr"] = round(
        (dfUStable["crude_no_spr"]/1000), 0).astype(int)

    dfOECD = dfOECD.dropna()

    dfOECDtable = dfOECD
    dfOECDtable["Date"] = dfOECDtable.index
    dfOECDtable["Forecast_crude"] = round(dfOECDtable["Forecast_crude"], 2)
    dfOECDtable["Forecast_crude_no_spr"] = round(
        dfOECDtable["Forecast_crude_no_spr"], 2)
    dfOECDtable["Forecast_inventory"] = round(
        dfOECDtable["Forecast_inventory"], 2)
    dfOECDtable["Forecast_inventory_no_spr"] = round(
        dfOECDtable["Forecast_inventory_no_spr"], 2)
    dfOECDtable["Error_crude"] = round(
        (dfOECDtable["Forecast_crude"] - dfOECDtable["WTI"]), 2)
    dfOECDtable["Error_crude_no_spr"] = round(
        (dfOECDtable["Forecast_crude_no_spr"] - dfOECDtable["WTI"]), 2)
    dfOECDtable["Error_inventory"] = round(
        (dfOECDtable["Forecast_inventory"] - dfOECDtable["WTI"]), 2)
    dfOECDtable["Error_inventory_no_spr"] = round(
        (dfOECDtable["Forecast_inventory_no_spr"] - dfOECDtable["WTI"]), 2)
    dfOECDtable["Inventory_no_spr"] = round(
        (((dfOECD.stocks_oecd - dfOECD.CrudeSPR))), 0).astype(int)
    dfOECDtable["Inventory"] = round(
        (dfOECDtable["stocks_oecd"]), 0).astype(int)
    dfOECDtable["Crude"] = round((dfOECDtable["CrudeTot"]), 0).astype(int)
    dfOECDtable["Crude_no_spr"] = round(
        (dfOECDtable["CrudeNonSpr"]), 0).astype(int)

    Forecast_crude_corr = dfUS['Forecast_crude'].corr(dfUS['WTI'])
    Forecast_crude_no_spr_corr = dfUS['Forecast_crude_no_spr'] .corr(
        dfUS['WTI'])
    Forecast_inventory_corr = dfUS['Forecast_inventory'] .corr(dfUS['WTI'])
    Forecast_inventory_no_spr_corr = dfUS['Forecast_inventory_no_spr'].corr(
        dfUS['WTI'])

    seriesUS = pd.Series([Forecast_crude_corr, Forecast_crude_no_spr_corr,
                          Forecast_inventory_corr, Forecast_inventory_no_spr_corr])
    statsUS = pd.DataFrame(seriesUS).T
    statsUS.columns = ["Forecast_crude_corr", "Forecast_crude_no_spr_corr",
                       "Forecast_inventory_corr", "Forecast_inventory_no_spr_corr"]

    Forecast_crude_corr = dfOECD['Forecast_crude'].corr(dfOECD['WTI'])
    Forecast_crude_no_spr_corr = dfOECD['Forecast_crude_no_spr'].corr(
        dfOECD['WTI'])
    Forecast_inventory_corr = dfOECD['Forecast_inventory'] .corr(dfOECD['WTI'])
    Forecast_inventory_no_spr_corr = dfOECD['Forecast_inventory_no_spr'].corr(
        dfOECD['WTI'])

    seriesOECD = pd.Series([Forecast_crude_corr, Forecast_crude_no_spr_corr,
                            Forecast_inventory_corr, Forecast_inventory_no_spr_corr])
    statsOECD = pd.DataFrame(seriesOECD).T
    statsOECD.columns = ["Forecast_crude_corr", "Forecast_crude_no_spr_corr",
                         "Forecast_inventory_corr", "Forecast_inventory_no_spr_corr"]

    df1 = pd.read_excel('http://ir.eia.gov/wpsr/psw01.xls', "Data 2",
                        index_col="Date", parse_dates=["Date"], skiprows=2)

    df2 = pd.get_dummies(df1.index.week)
    df2.index = df1.index
    df3 = pd.concat([df2, df1], axis=1)

    # Rename cols
    df3_cols = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W20', 'W21', 'W22', 'W23', 'W24', 'W25', 'W26', 'W27', 'W28', 'W29', 'W30', 'W31', 'W32', 'W33', 'W34', 'W35', 'W36', 'W37', 'W38', 'W39', 'W40', 'W41', 'W42', 'W43', 'W44', 'W45', 'W46', 'W47', 'W48', 'W49', 'W50', 'W51', 'W52', 'W53', 'US_production_crude', 'Alaska_production_crude', 'lower48_production_crude', 'crude_netImports', 'crude_Imports', 'imports_excSpr', 'importsby_spr',
                'importsfor_spr', 'crude_exports', 'stock_change', 'SPR_change', 'change_excSPR', 'crude_unaccounted', 'refinery_input', 'refinery_production_netGas', 'gasLiquids_production', 'renewable_production', 'Oxygenate', 'Fuel-Oxygenates', ' Processing_Gain', 'netImports_products', 'products_imports', 'products_exports', 'products_change', 'supply_adjustment_products', 'products_supplied', 'Motor_Gasoline', 'Jet_Fue', 'Distillate_Fuel ', ' Residual_Fuel', ' Propane_Propylene', 'Other_Oils', 'netImports_petroleum_products']
    df3.columns = df3_cols

    wcrude_Imports = df3["crude_Imports"]
    wcrude_exports = -df3["crude_exports"]
    wUS_production_crude = df3["US_production_crude"]
    wrefinery_input = -df3["refinery_input"]
    wcrude_unaccounted = df3["crude_unaccounted"]
    wProducts_Imports = df3["products_imports"]
    wProducts_exports = -df3["products_exports"]
    wrefinery_input1 = df3["refinery_input"]
    wrefinery_production_netGas = df3["refinery_production_netGas"]
    wproducts_supplied = -df3["products_supplied"]
    wproducts_unaccounted = df3["supply_adjustment_products"]

    Water_data = pd.concat([wcrude_Imports, wcrude_exports, wUS_production_crude, wrefinery_input, wcrude_unaccounted, wProducts_Imports,
                            wProducts_exports, wrefinery_input1, wrefinery_production_netGas, wproducts_supplied, wproducts_unaccounted], axis=1)
    Water_data1 = Water_data.tail(1)
    Water_data1.columns = ["crude_Imports", "crude_exports", "US_production_crude", "refinery_input", "crude_unaccounted",
                           "Products_Imports", "Products_exports", "refinery_input1", "refinery_production_netGas", "products_supplied", "products_unaccounted"]
    Water_data1["Crude Change"] = Water_data1["crude_Imports"] + Water_data1["crude_exports"] + \
        Water_data1["US_production_crude"] + \
        Water_data1["refinery_input"] + Water_data1["crude_unaccounted"]
    Water_data1["Products Change"] = Water_data1["Products_Imports"] + Water_data1["Products_exports"] + Water_data1["refinery_input1"] + \
        Water_data1["refinery_production_netGas"] + \
        Water_data1["products_supplied"] + Water_data1["products_unaccounted"]
    Water_data1 = Water_data1.reindex(columns=["crude_Imports", "crude_exports", "US_production_crude", "refinery_input", "crude_unaccounted", "Crude Change",
                                               "Products_Imports", "Products_exports", "refinery_input1", "refinery_production_netGas", "products_supplied", "products_unaccounted", "Products Change"])
    Water_data1_crude = Water_data1.iloc[0:1, 0:6]
    Water_data1_products = Water_data1.iloc[0:1, 6:]


    crude_change_magnitude = []

    if (Water_data1_crude["Crude Change"][0] > 0):
        crude_change_magnitude = 'increased'
    if (Water_data1_crude["Crude Change"][0] < 0):
        crude_change_magnitude = 'fell'
    if (Water_data1_crude["Crude Change"][0] == 0):
        crude_change_magnitude = 'changed'

        
    products_change_magnitude = []

    if (Water_data1_products["Products Change"][0] > 0):
        products_change_magnitude = 'increased'
    if (Water_data1_products["Products Change"][0] < 0):
        products_change_magnitude = 'fell'
    if (Water_data1_products["Products Change"][0] == 0):
        products_change_magnitude = 'changed'


    # Store the data in the library
    library.write('dfUS', dfUS)
    library.write('dfOECD', dfOECD)
    library.write('dfUStable', dfUStable)
    library.write('dfOECDtable', dfOECDtable)
    library.write('Water_data1_crude', Water_data1_crude)
    library.write('Water_data1_products', Water_data1_products)
    library.write('statsUS', statsUS)
    library.write('statsOECD', statsOECD)
    library.write('statsOECD', statsOECD)
    library.write('crude_change_magnitude', crude_change_magnitude)
    library.write('products_change_magnitude', products_change_magnitude)


    print("--- %s seconds : oilAPI" % (time.time() - start_time))


if __name__ == '__main__':
    main()
