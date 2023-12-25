import requests
from datetime import date
import os
import json
import pandas_ta as ta
import pandas as pd
import numpy as np
import datetime
import csv
from time import sleep
from Zerodha_Auth import *

url = "https://kite.zerodha.com/oms/instruments/historical/{0}/{1}?user_id=KRE393&oi=1&from={2}&to={3}"




def getCandels(symbol, fromDate, toDate, timeframe):

    headers = {
        'authorization': 'enctoken '+auth_code()
    }

    curUrl = url.format(tickerData[symbol]["id"], timeframe, fromDate, toDate)
    #print(curUrl)
    try:
        session = requests.session()
        r = session.get(curUrl, headers=headers).json()
    except Exception as error:
        print(error)
        pass
    #print(r)
    history = r['data']['candles']
    history = pd.DataFrame(history)

    history = history.rename(
        columns={0: "DateTime", 1: "Open", 2: "High", 3: "Low", 4: "Close", 5: "Volume", 6: "OI"})

    history["DateTime"] = pd.to_datetime(history["DateTime"])
    history = history.set_index('DateTime')

    return history

data = datetime.datetime.now()
Today = datetime.date.today()



def calculate_heikin_ashi(df):
    ha_open = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    ha_close = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_high = df[['High', 'Open', 'Close']].max(axis=1)
    ha_low = df[['Low', 'Open', 'Close']].min(axis=1)
    ha_io = df['OI']

    return pd.DataFrame({'Open': ha_open, 'High': ha_high, 'Low': ha_low, 'Close': ha_close, 'IO': ha_io})



tickerData = {
    'NIFTYFuture': {
        'id': Nifty_Future()
    },
    'BANKNIFTYFuture': {
        'id': Bnf_Future()
    },
    'NIFTY': {
        'id': 256265
    },
    'BANKNIFTY': {
        'id': 260105
    },    
    'FINNIFTY': {
        'id': FinNifty_Future()
    },
}

KI = {
    '1m': 'minute',
    '3m': '3minute',
    '5m': '5minute',
    '15m': '15minute',
    '60m': '60minute',
    'day': 'day',
    'month': 'month'
}



sdate = ["2023-01-01","2023-02-01","2023-03-01","2023-04-01","2023-05-01","2023-06-01","2023-07-01","2023-08-01","2023-09-01","2023-10-01","2023-11-01","2023-12-01"]
edate = ["2023-01-31","2023-02-28","2023-03-31","2023-04-30","2023-05-31","2023-06-30","2023-07-31","2023-08-30","2023-09-30","2023-10-31","2023-11-30","2023-12-31"]


for I in range(len(sdate)):

    print("start")
    
    #bar = ["minute", "5minute", "15minute"]

    bar = "15minute"

    symbol_data = getCandels("NIFTY", sdate[I], edate[I], bar)
    my_df = pd.DataFrame(symbol_data)
    print(my_df)

    print(calculate_heikin_ashi(my_df))

    #if bar == "minute":
    #    output_file = "C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_1m"
    #    my_df.to_csv(r'{}.csv'.format(output_file), mode="a", index=True, header=False)
    #    heikin = calculate_heikin_ashi(pd.DataFrame(symbol_data))
    #    output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_1m.csv'
    #    heikin.to_csv(output_file, index=True, mode="a", header=False)    
    #
    #if bar == "5minute":
    #    output_file = "C://Xampp/htdocs/Algo_Trader/CSV_Files/finnifty_Fut_5m"
    #    my_df.to_csv(r'{}.csv'.format(output_file), mode="a", index=True, header=False)
    #    heikin = calculate_heikin_ashi(pd.DataFrame(symbol_data))
    #    output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_finnifty_Fut_5m.csv'
    #    heikin.to_csv(output_file, index=True, mode="a", header=False)
    #
    if bar == "15minute":
        output_file = "C://Xampp/htdocs/Algo_Trader/CSV_Files/Nifty_15m"
        my_df.to_csv(r'{}.csv'.format(output_file), mode="a", index=True, header=False)
        heikin = calculate_heikin_ashi(pd.DataFrame(symbol_data))
        output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_Nifty_15m.csv'
        heikin.to_csv(output_file, index=True, mode="a", header=False)
    #
    #if bar == "60minute":
    #    output_file = "C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1H"
    #    my_df.to_csv(r'{}.csv'.format(output_file), mode="a", index=True, header=False)
    #    heikin = calculate_heikin_ashi(pd.DataFrame(symbol_data))
    #    output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv'
    #    heikin.to_csv(output_file, index=True, mode="a", header=False)