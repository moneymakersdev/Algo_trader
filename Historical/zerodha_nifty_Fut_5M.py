import requests
from datetime import date
import os
import json
import pandas as pd
import numpy as np
import datetime
import csv
from time import sleep
from Zerodha_Auth import *
import pandas_ta as ta
url = "https://kite.zerodha.com/oms/instruments/historical/{0}/{1}?user_id=KRE393&oi=1&from={2}&to={3}"

tickerData = {
    'NIFTY': {
        'id': Nifty_Future()
    },
    'BANKNIFTY': {
        'id': 260105
    }
}

KI = {
    '3m': '3minute',
    '5m': '5minute',
    '15m': '15minute',
    '60m': '60minute',
    'day': 'day'
}


def getCandels(symbol, fromDate, toDate, timeframe):

    headers = {
        'authorization': 'enctoken '+auth_code()
    }

    curUrl = url.format(tickerData[symbol]["id"], timeframe, fromDate, toDate)
    print(curUrl)
    try:
        session = requests.session()
        r = session.get(curUrl, headers=headers).json()
    except Exception as error:
        print(error)
    print(r)
    history = r['data']['candles']
    history = pd.DataFrame(history)

    history = history.rename(
        columns={0: "DateTime", 1: "Open", 2: "High", 3: "Low", 4: "Close", 5: "Volume"})

    history["DateTime"] = pd.to_datetime(history["DateTime"])
    history = history.set_index('DateTime')

    return history


#def calculate_heikin_ashi(df):
#    ha_open = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
#    ha_close = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
#    ha_high = df[['High', 'Open', 'Close']].max(axis=1)
#    ha_low = df[['Low', 'Open', 'Close']].min(axis=1)
#
#    return pd.DataFrame({'Open': ha_open, 'High': ha_high, 'Low': ha_low, 'Close': ha_close})


def calculate_heikin_ashi(df):
    ha_time = df["time"]
    ha_open = (df['o'].shift(1) + df['c'].shift(1)) / 2
    ha_close = (df['o'] + df['h'] + df['l'] + df['c']) / 4
    ha_high = df[['h', 'o', 'c']].max(axis=1)
    ha_low = df[['l', 'o', 'c']].min(axis=1)

    return pd.DataFrame({'DateTime': ha_time, 'Open': ha_open, 'High': ha_high, 'Low': ha_low, 'Close': ha_close})


Today = datetime.date.today()


while True:
    while True:
        if str(datetime.datetime.now()) <= str(Today)+" 09:20:00.000000":
            print("Market is Closed")
            sleep(1)
            break
        if str(datetime.datetime.now()) >= str(Today)+" 09:20:00.000000":
            print("start")
            #symbol_data = getCandels("NIFTY", str(Today), str(Today), KI["5m"])
            #print(symbol_data)
            from truedata_ws.websocket.TD import TD
            import pandas as pd
            import datetime


            username = 'tdwsp495'
            password = 'amit@495'


            td_app = TD(username, password, live_port=None)

            symbol_data = td_app.get_historic_data("NIFTY-I", bar_size="5 mins")

            my_df = pd.DataFrame(symbol_data)
            print(my_df)
            my_df.to_csv(r'{}.csv'.format("C://Xampp/htdocs/Algo_Trader/CSV_Files/nifty_Fut_5m"), mode="a", index=True, header=False)
            candlestick_data = my_df

            # Calculate Heikin-Ashi data
            heikin_ashi_data = calculate_heikin_ashi(my_df)
            #heikin_ashi_data = ta.ha(my_df["o"], my_df["h"], my_df['l'], my_df['c'])


            # Write Heikin-Ashi data to a new CSV file
            output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_nifty_Fut_5m.csv'
            heikin_ashi_data.to_csv(output_file, index=True, mode="a", header=False)

            print(f'Heikin-Ashi data saved to {output_file}')


            while True:
                sleep(300)
                #symbol_data = getCandels("NIFTY", str(Today), str(Today), KI["5m"])
                symbol_data = td_app.get_historic_data("NIFTY-I", bar_size="5 mins")

                print(symbol_data)
                my_df = pd.DataFrame(symbol_data)
                print(my_df)
                my_df.iloc[[-1]].to_csv(r'{}.csv'.format("C://Xampp/htdocs/Algo_Trader/CSV_Files/nifty_Fut_5m"), mode="a", index=True, header=False)
                
                candlestick_data = my_df

                # Calculate Heikin-Ashi data
                heikin_ashi_data = calculate_heikin_ashi(my_df)
            #heikin_ashi_data = ta.ha(my_df["o"], my_df["h"], my_df['l'], my_df['c'])


                # Write Heikin-Ashi data to a new CSV file
                output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_nifty_Fut_5m.csv'
                heikin_ashi_data.iloc[[-1]].to_csv(output_file, index=True, mode="a", header=False)

                print(f'Heikin-Ashi data saved to {output_file}')

                if str(datetime.datetime.now()) >=str(Today)+" 15:31:00.000000":
                    exit()
                else:
                    pass