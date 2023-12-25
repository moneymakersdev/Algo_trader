import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Angle_Order import *
import numpy as np
import pandas_ta as ta    




def Direction(factor, atr_period, High, Low, Close):
    hl2 = (High + Low) / 2
    atr = pd.Series(High - Low).abs().rolling(atr_period).mean()
    upper_band = hl2 + (factor * atr)
    Lower_band = hl2 - (factor * atr)
    
    supertrend = pd.Series(np.nan, index=Close.index)
    direction = pd.Series(np.nan, index=Close.index)
    
    in_uptrend = True
    for i in range(1, len(Close)):
        if Close[i - 1] > upper_band[i - 1]:
            in_uptrend = False
            supertrend[i] = upper_band[i]
            direction[i] = -1
        elif Close[i - 1] < Lower_band[i - 1]:
            in_uptrend = True
            supertrend[i] = Lower_band[i]
            direction[i] = 1
        else:
            if in_uptrend:
                supertrend[i] = Lower_band[i]
                direction[i] = 1
            else:
                supertrend[i] = upper_band[i]
                direction[i] = -1
    
    return direction.iloc[[-1]].iloc[0]



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



def supertrend_4():    
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv")
    
    supertrend = ta.supertrend(high=df['High'], low=df['Low'], close=df['Close'], length=10, multiplier=0.4)
    
    return supertrend.iloc[-1].iloc[0]



def supertrend_8():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv")
    
    supertrend = ta.supertrend(high=df['High'], low=df['Low'], close=df['Close'], length=10, multiplier=0.8)
    
    return supertrend.iloc[-1].iloc[0]


def calculate_ema(data, period):
    ema = data.ewm(span=period, adjust=False).mean()
    return ema


def ema():
    while True:
            # Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 5  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return last_ema_value



def Latest_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv")

    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


def Previous_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv")
    
    if not df.empty:
        last_row = df.iloc[-2]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:30:00.000000":

        while True:

            apikey = "CORXEN7R"
            secretkey = "3d6f8384-4af5-45fe-8291-0803b381a9e1"
            user_id = "M684394"
            password = "1724"
            totp = "FDCRAN5RACK6W3RBXR2ZYOV3AY"

            #Supertrend0_4 = list(Supertrend_04())
            #Supertrend0_8 = list(Supertrend_08())
            
            #Supertrend_0_4 = Supertrend0_4[0]
            #Supertrend_0_8 = Supertrend0_8[0]

            data = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_1H.csv')

            Supertrend0_4 = supertrend_4()
            Supertrend0_8 = supertrend_8()
            
            Supertrend_0_4 = Supertrend0_4
            Supertrend_0_8 = Supertrend0_8

            #Old_Supertrend_0_4 = Old_Supertrend_04()
            #Old_Supertrend_0_8 = Old_Supertrend_08()
            ema1 = ema()
            Latest = Latest_Close()
            Previous = Previous_Close()

            Idx_Live = bnf_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Latest "+str(Latest))
            print("Supertrend_0_4: "+str(Supertrend_0_4))
            print("Supertrend_0_8: "+str(Supertrend0_8))
            print("Previous "+str(Previous))
            #print("Old Supertrend_0_4: "+str(Old_Supertrend_0_4))
            #print("Old Supertrend_0_8: "+str(Old_Supertrend_0_8))
            print("ema: "+str(ema1))
            print(datetime.datetime.now())
            sleep(1)

            sql = "select * from delta_bnf_fut_orders_1h ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))

            GetExpiry_Date = Monthly_Expiry()


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                if float(Latest) > float(Supertrend_0_4) and float(Latest) > float(Supertrend_0_8) and float(Latest) > float(ema1) and float(Previous) < float(Supertrend_0_4):# and float(Previous) < float(Supertrend_0_8) and float(Previous) < float(ema1):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
                    DhanSymbol = "BANKNIFTY "+" "+str(ExpiryMonth)+" "+" FUT"
                    AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+" FUT"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)



                    token = 'select token from instruments where symbol="'+symbol+'"'
                    mycursor.execute(token)
                    tokenresult = mycursor.fetchone()

                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "VPS_BNF_Future", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "CALL", IciciExpiry)

                    trade = "INSERT INTO delta_bnf_fut_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'BUY', '30', '0', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'VPS_BNF_Future', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(Latest) < float(Supertrend_0_4) and float(Latest) < float(Supertrend_0_8) and float(Latest) < float(ema1) and float(Previous) > float(Supertrend_0_4): #and float(Previous) > float(Supertrend_0_8) and float(Previous) > float(ema1):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
                    DhanSymbol = "BANKNIFTY "+" "+str(ExpiryMonth)+" "+" FUT"
                    AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+" FUT"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)



                    token = 'select token from instruments where symbol="'+symbol+'"'
                    mycursor.execute(token)
                    tokenresult = mycursor.fetchone()

                    Short_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "VPS_BNF_Future", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha)

                    trade = "INSERT INTO delta_bnf_fut_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SHORT', '30', '0', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'VPS_BNF_Future', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                else:
                    break



            if Position == "1":
                sql = "select * from delta_bnf_fut_orders_1h ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Type = myresult[2]
                Symbol = myresult[0]
                Token = myresult[1]

                if Type == "BUY":

                    if float(Latest) < float(Supertrend_0_4) and float(Latest) < float(Supertrend_0_8) and float(Latest) < float(ema1):
                        
                        Sell_Order(Symbol, Token, "VPS_BNF_Future")

                        trade = "INSERT INTO delta_bnf_fut_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SELL', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'VPS_BNF_Future', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break
                    break


                if Type == "SHORT":
                    expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                    strikeprice = str(Idx_Live)[:3]+"00"

                    ExpiryYear = str(GetExpiry_Date[0])[2:]
                    ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                    ExpiryDate = GetExpiry_Date[2]

                    ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                    if float(Latest) > float(Supertrend_0_4) and float(Latest) > float(Supertrend_0_8) and float(Latest) > float(ema1):
                        symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
                        DhanSymbol = "BANKNIFTY "+" "+str(ExpiryMonth)+" "+" FUT"
                        AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+" FUT"
                        UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                        FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                        MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)
                        IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                        Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                        IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                        Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                        IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                        token = 'select token from instruments where symbol="'+symbol+'"'
                        mycursor.execute(token)
                        tokenresult = mycursor.fetchone()
                        
                        Buy_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "VPS_BNF_Future", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "CALL", IciciExpiry)

                        trade = "INSERT INTO delta_bnf_fut_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SHORTEXIT', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'VPS_BNF_Future', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break
                    break


                else:
                    break
            

            else:
                break