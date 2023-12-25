import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Tokens import *
from time import sleep
import numpy as np
import pandas_ta as ta



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



#def TA_SuperTrend():
#    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1m.csv')
#    
#    # Input parameters
#    atr_period = 10
#    factor = 1
#
#    supert = ta.supertrend(df, atr_period, factor)
#
#    print(supert)
#
#    return supert 


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

    return sti.iloc[-2].iloc[0]

    #return df[['SuperTrend']].iloc[-1]



def Supertrend_01_Trading_View():
    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1m.csv')
    
    return ta.supertrend(df["High"], df["Low"], df["Close"], length=10, multiplier=1)['SUPERT_10_1.0'].iloc[-2]



def Latest_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1m.csv")
    
    return df["Close"].iloc[[-1]].iloc[0]



def Latest_Opening():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1m.csv")
    
    return df["Open"].iloc[-1]



def Previous_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_Fut_1m.csv")
    
    return df["Close"].iloc[[-2]].iloc[0]


while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:17:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:17:00.000000":

        while True:
            apikey = "h6jSmhjF"
            secretkey = "8d9b5028-218e-4bfb-9e44-c8c52d3e2dce"
            user_id = "VJVG1338"
            password = "0107"
            totp = "VLSNN2YQT2TEBDDVFCVK34KZAE"

            Supertrend0_1 = Supertrend_01()
            TA_SuperTrend_1 = Supertrend_01_Trading_View()
            Supertrend_0_1 = Supertrend0_1

            Latest = Latest_Close()
            Previous = Previous_Close()
            GetExpiry_Date = Expiry_Date()
            Open = Latest_Opening()

            Idx_Live = bnf_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass
            
            print("Live: "+str(Idx_Live))
            print("Latest "+str(Latest))
            print("Previous "+str(Previous))
            print("Supertrend_0_1: "+str(Supertrend_0_1))
            print("TA_SuperTrend_1: "+str(TA_SuperTrend_1))
            print("Previous "+str(Previous))

            filedata = "SuperTrend: "+str(Supertrend_0_1)+" TA_SuperTrend_1: "+str(TA_SuperTrend_1)+" Latest: "+str(Latest)+" Previous: "+str(Previous)+" DateTime: "+str(datetime.datetime.now())+"\n"

            supertrend = open('scalper_master_reverse_Reverse.txt', 'a')
            supertrend.write(filedata)
            supertrend.close()

            print(datetime.datetime.now())

            sql = "select * from scalper_master_reverse ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"
                

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                if str(datetime.datetime.now()) >= str(data.date())+" 15:00:00.000000":
                    print("Market Closed")
                    exit()
                    

                if float(Latest) > float(TA_SuperTrend_1) and float(Previous) < float(TA_SuperTrend_1):
                    strikeprice = int(strikeprice)-100
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"CE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" CALL"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice)
                    #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+str(ExpiryDate)



                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    #tokenresult = mycursor.fetchone()

                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                    #Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "scalper_master_reverse", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(round(float(strikeprice)-100)), "CALL", IciciExpiry)

                    trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '15', '"+str(option_live)+"', '"+str(Open)+"', '1', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(Latest) < float(TA_SuperTrend_1) and float(Previous) > float(TA_SuperTrend_1):
                    strikeprice = int(strikeprice)+100

                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"PE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" PUT"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice)
                    #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+str(ExpiryDate)



                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    #tokenresult = mycursor.fetchone()

                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                    #Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "scalper_master_reverse", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(round(float(strikeprice)+100)), "PUT", IciciExpiry)

                    trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '15', '"+str(option_live)+"', '"+str(Open)+"', '1', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                else:
                    break



            if Position == "1":
                sql = "select * from scalper_master_reverse ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Type = myresult[2]
                Symbol = myresult[0]
                Token = myresult[1]
                Bough_Idx = myresult[5]

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)

                P_L_Profit = float(Bough_Idx)+(float(Bough_Idx)*0.10/100)
                P_L_Loss = float(Bough_Idx)-(float(Bough_Idx)*0.10/100)

                print("Bought IDx: "+str(Bough_Idx))
                print("P_L_Profit: "+str(P_L_Profit))
                print("P_L_Loss: "+str(P_L_Loss))


                if str(datetime.datetime.now()) >= str(data.date())+" 15:10:00.000000":
                    #Sell_Order(Symbol, Token, "scalper_master_reverse")

                    trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '15', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if "CE" in str(Symbol):

                    if float(Idx_Live) >= float(P_L_Profit):
                        
                        #Sell_Order(Symbol, Token, "scalper_master_reverse")

                        trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '15', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        #sleep(60)
                        break


                    if float(Idx_Live) <= float(P_L_Loss):
                        
                        #Sell_Order(Symbol, Token, "scalper_master_reverse")

                        trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '15', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        #sleep(60)
                        break

                    break


                if "PE" in str(Symbol):
                    
                    if float(Idx_Live) <= float(P_L_Loss):

                        #Sell_Order(Symbol, Token, "scalper_master_reverse")

                        trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '15', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        #sleep(60)
                        break


                    if float(Idx_Live) >= float(P_L_Profit):
                        
                        #Sell_Order(Symbol, Token, "scalper_master_reverse")

                        trade = "INSERT INTO scalper_master_reverse (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '15', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'scalper_master_reverse', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        #sleep(60)
                        break

                    break


                else:
                    break


            else:
                break