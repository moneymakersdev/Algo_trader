from truedata_ws.websocket.TD import TD
import pandas as pd
import datetime
import csv
from time import sleep

username = 'wssand044'
password = 'techy044'

td_app = TD(username, password, live_port=None)

symbol = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK'
, 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BHARTIARTL', 'BPCL', 'BRITANNIA'
, 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH'
, 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR', 'ICICIBANK', 'INDUSINDBK'
, 'INFY', 'ITC', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'LTIM', 'M&M', 'MARUTI', 'NESTLEIND', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE'
, 'SBIN', 'SBILIFE', 'SUNPHARMA', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN', 'ULTRACEMCO', 'UPL', 'WIPRO']



barsize = 'eod'


data = datetime.datetime.now()


for I in range(51):

    print(I)
    hist_data_3 = td_app.get_historic_data(symbol[I], duration='1 D', bar_size=barsize)
    df_hist_data = pd.DataFrame(hist_data_3)
    print('\nSymbol > %s' %symbol[I])
    print('Bar Interval > %s\n' %barsize)
    df_hist_data.iloc[[-1]].to_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/'+symbol[I]+'.csv', mode='a', index = None, header=None)
