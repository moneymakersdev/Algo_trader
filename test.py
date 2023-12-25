from truedata_ws.websocket.TD import TD
import time
import logging
import pandas as pd
import warnings


## Calculate the ATR
def calculate_atr(df, atr_period):
    df['TR'] = df.apply(lambda row: max(row['High'] - row['Low'], abs(row['High'] - row['close_prev']), abs(row['Low'] - row['close_prev'])), axis=1)
    df['ATR'] = df['TR'].rolling(atr_period).mean()
    return df

# Calculate Supertrend
def calculate_supertrend(df, factor, atr_period):
    df['Upper Basic'] = (df['High'] + df['Low']) / 2 + factor * df['ATR']
    df['Lower Basic'] = (df['High'] + df['Low']) / 2 - factor * df['ATR']
    df['Upper Band'] = df['Upper Basic']
    df['Lower Band'] = df['Lower Basic']
    df['Trend'] = 1

    for i in range(1, len(df)):
        if df.at[i, 'Close'] > df.at[i-1, 'Upper Band']:
            df.at[i, 'Upper Band'] = max(df.at[i-1, 'Upper Basic'], df.at[i-1, 'Upper Band'])
        else:
            df.at[i, 'Upper Band'] = df.at[i-1, 'Upper Basic']

        if df.at[i, 'Close'] < df.at[i-1, 'Lower Band']:
            df.at[i, 'Lower Band'] = min(df.at[i-1, 'Lower Basic'], df.at[i-1, 'Lower Band'])
        else:
            df.at[i, 'Lower Band'] = df.at[i-1, 'Lower Basic']

        if df.at[i, 'Close'] > df.at[i, 'Upper Band']:
            df.at[i, 'Trend'] = 1
            df.at[i, 'Lower Band'] = df.at[i, 'Upper Band']
        elif df.at[i, 'Close'] < df.at[i, 'Lower Band']:
            df.at[i, 'Trend'] = -1
            df.at[i, 'Upper Band'] = df.at[i, 'Lower Band']
        else:
            df.at[i, 'Trend'] = df.at[i-1, 'Trend']

    
    df['SuperTrend'] = 0.0
    for i in range(atr_period, len(df)):
        if df['Close'][i-1] <= df['Upper Band'][i-1]:
            df.loc[i, 'SuperTrend'] = df['Upper Band'][i]
        else:
            df.loc[i, 'SuperTrend'] = df['Lower Band'][i]


    return df



def Supertrend_01():

    # Load price data from a CSV file (replace 'price_data.csv' with your file)
    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1m.csv')
    
    # Input parameters
    atr_period = 10
    factor = 1.1

    # Calculate ATR and Supertrend
    df['close_prev'] = df['Close'].shift(1)
    df = calculate_atr(df, atr_period)
    df = calculate_supertrend(df, factor, atr_period)

    # Print the Supertrend data
    import pandas_ta as ta
    sti = ta.supertrend(df['High'], df['Low'], df['Close'], length=atr_period, multiplier=factor)

    return sti


with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(Supertrend_01())