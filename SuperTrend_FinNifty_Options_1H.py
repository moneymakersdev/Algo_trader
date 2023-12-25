import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
import numpy as np


def Supertrend_04(data, atr_length, factor):

    tr1 = data['High'] - data['Low']
    tr2 = abs(data['High'] - data['Close'].shift(1))
    tr3 = abs(data['Low'] - data['Close'].shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(atr_length).mean()

    data['upper_band'] = data['High'] - atr * factor
    data['lower_band'] = data['Low'] + atr * factor

    uptrend = True
    trend = []

    for i, row in data.iterrows():
        if uptrend:
            if row['Close'] <= row['lower_band']:
                uptrend = False
            trend.append(row['lower_band'])
        else:
            if row['Close'] >= row['upper_band']:
                uptrend = True
            trend.append(row['upper_band'])

    data['supertrend'] = trend

    return data['supertrend'].iloc[-1]



def Supertrend_08(data, atr_length, factor):
    
    tr1 = data['High'] - data['Low']
    tr2 = abs(data['High'] - data['Close'].shift(1))
    tr3 = abs(data['Low'] - data['Close'].shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.rolling(atr_length).mean()

    data['upper_band'] = data['High'] - atr * factor
    data['lower_band'] = data['Low'] + atr * factor

    uptrend = True
    trend = []

    for i, row in data.iterrows():
        if uptrend:
            if row['Close'] <= row['lower_band']:
                uptrend = False
            trend.append(row['lower_band'])
        else:
            if row['Close'] >= row['upper_band']:
                uptrend = True
            trend.append(row['upper_band'])

    data['supertrend'] = trend

    return data['supertrend'].iloc[-1]



def calculate_ema(data, period):
    ema = data.ewm(span=period, adjust=False).mean()
    return ema


def ema():
    while True:
            # Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_finnifty_Fut_1H.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 3  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return format(round(last_ema_value, 2))



def Latest_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_finnifty_Fut_1H.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


def Previous_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_finnifty_Fut_1H.csv")
    
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

            apikey = "XAW2htsL"
            secretkey = "0317b544-ac5a-4665-a671-8203e4c9111f"
            user_id = "A50899954"
            password = "2727"
            totp = "AOFEJWENZV2FR4ADGULSMBN3RI"

            #Supertrend0_4 = list(Supertrend_04())
            #Supertrend0_8 = list(Supertrend_08())
            
            #Supertrend_0_4 = Supertrend0_4[0]
            #Supertrend_0_8 = Supertrend0_8[0]

            data = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_FinNifty_Fut_1H.csv')

            Supertrend0_4 = Supertrend_04(data, 10, 0.4)
            Supertrend0_8 = Supertrend_08(data, 10, 0.8)

            
            Supertrend_0_4 = Supertrend0_4
            Supertrend_0_8 = Supertrend0_8

            #Old_Supertrend_0_4 = Old_Supertrend_04()
            #Old_Supertrend_0_8 = Old_Supertrend_08()
            ema1 = ema()
            Latest = Latest_Close()
            Previous = Previous_Close()
            GetExpiry_Date = Expiry_Date()

            Idx_Live = finnifty_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Latest "+str(Latest))
            print("Supertrend_0_4: "+str(Supertrend_0_4))
            print("Supertrend_0_8: "+str(Supertrend_0_8))
            print("Previous "+str(Previous))
            #print("Old Supertrend_0_4: "+str(Old_Supertrend_0_4))
            #print("Old Supertrend_0_8: "+str(Old_Supertrend_0_8))
            print("ema: "+str(ema1))
            print(datetime.datetime.now())

            sleep(1)

            sql = "select * from delta_finnifty_opt_orders_1h ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))

            GetExpiry_Date = Fin_Nifty_Monthly_Expiry()


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                if float(Latest) > float(Supertrend_0_4) and float(Latest) > float(Supertrend_0_8) and float(Latest) > float(ema1) and float(Previous) < float(Supertrend_0_4):# and float(Previous) < float(Supertrend_0_8) and float(Previous) < float(ema1):
                    symbol = "FINNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"CE"
                    DhanSymbol = "FINNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" CALL"
                    AliceSymbol = "FINNIFTY "+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice)
                    UpstoxSymbol = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"
                    FyresSymbol = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"
                    MotilalSymbol = "FINNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)+" CE "+str(strikeprice)
                    #Zerodha = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    Zerodha = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry


                    token = 'select token from instruments where symbol="'+symbol+'"'
                    mycursor.execute(token)
                    tokenresult = mycursor.fetchone()
                    
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "VPS_FIN_Option", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha)

                    trade = "INSERT INTO delta_finnifty_opt_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', 'None', 'BUY', '30', '0', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(Latest) < float(Supertrend_0_4) and float(Latest) < float(Supertrend_0_8) and float(Latest) < float(ema1) and float(Previous) > float(Supertrend_0_4): #and float(Previous) > float(Supertrend_0_8) and float(Previous) > float(ema1):
                    symbol = "FINNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"PE"
                    DhanSymbol = "FINNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" PUT"
                    AliceSymbol = "FINNIFTY "+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice)
                    UpstoxSymbol = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"
                    FyresSymbol = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"
                    MotilalSymbol = "FINNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)+" PE "+str(strikeprice)
                    #Zerodha = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    Zerodha = "FINNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry

                     
                    token = 'select token from instruments where symbol="'+symbol+'"'
                    mycursor.execute(token)
                    tokenresult = mycursor.fetchone()


                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "VPS_FIN_Option", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha)

                    trade = "INSERT INTO delta_finnifty_opt_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', 'None', 'SHORT', '30', '0', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                else:
                    break



            if Position == "1":
                sql = "select * from delta_finnifty_opt_orders_1h ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Type = myresult[2]
                Symbol = myresult[0]
                Token = myresult[1]

                if Type == "BUY":

                    if float(Latest) < float(Supertrend_0_4) and float(Latest) < float(Supertrend_0_8) and float(Latest) < float(ema1):

                        Sell_Order(Symbol, Token, "VPS_FIN_Option")

                        trade = "INSERT INTO delta_finnifty_opt_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('FINNIFTY_FUTURE', 'None', 'SELL', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()
                        
                        break


                if Type == "SHORT":
                    if float(Latest) > float(Supertrend_0_4) and float(Latest) > float(Supertrend_0_8) and float(Latest) > float(ema1):

                        Sell_Order(Symbol, Token, "VPS_FIN_Option")

                        trade = "INSERT INTO delta_finnifty_opt_orders_1h (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('FINNIFTY_FUTURE', 'None', 'SHORTEXIT', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                else:
                    break
            

            else:
                break