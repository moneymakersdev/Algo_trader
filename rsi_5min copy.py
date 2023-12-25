import pandas as pd
import datetime
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Tokens import *
import numpy as np
from datetime import timedelta
from datetime import date
import ta




def RSI(live_price):
    file_path = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_5m.csv'
    df = pd.read_csv(file_path)

    # Define a function to calculate RSI
    def calculate_rsi(data, window_length=14):
        return ta.momentum.RSIIndicator(data, window=window_length).rsi()

    apikey = "u7rkA2GW"
    secretkey = "912dba65-1e62-40e9-bcf6-774c4d9fcdd6"
    user_id = "A52847556"
    password = "9325"
    totp = "EUZRJY5DE4PQFSIYQFBTKECEKE"


    live_price = Idx_Live

    # Append new price to the DataFrame
    df = df._append({'Close': live_price}, ignore_index=True)

    # Calculate RSI for the updated DataFrame
    close = df['Close']
    rsi_length = 20
    rsi = calculate_rsi(close, window_length=rsi_length)

    return rsi.iloc[-1]





def RSI_Old(live_price):
    file_path = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_5m.csv'
    df = pd.read_csv(file_path)

    # Define a function to calculate RSI
    def calculate_rsi(data, window_length=14):
        return ta.momentum.RSIIndicator(data, window=window_length).rsi()

    apikey = "u7rkA2GW"
    secretkey = "912dba65-1e62-40e9-bcf6-774c4d9fcdd6"
    user_id = "A52847556"
    password = "9325"
    totp = "EUZRJY5DE4PQFSIYQFBTKECEKE"


    live_price = Idx_Live

    # Append new price to the DataFrame
    df = df._append({'Close': live_price}, ignore_index=True)

    # Calculate RSI for the updated DataFrame
    close = df['Close']
    rsi_length = 20
    rsi = calculate_rsi(close, window_length=rsi_length)

    return rsi.iloc[-2]



def MA():
    file_path = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_5m.csv'
    df = pd.read_csv(file_path)

    # Parameters
    length = 20
    src = df['Open']
    offset = 4  # Adjust the offset value if needed

    # Calculate SMA
    source = ta.trend.sma_indicator(src, length)

    # Calculate smoothing line
    length = 5

    smoothingLine = ta.trend.sma_indicator(source, length)

    # Print or use the values as needed
    return smoothingLine.iloc[-1]




def MA_Old():
    file_path = './CSV_Files/bnf_5m.csv'
    df = pd.read_csv(file_path)
    
    # Parameters
    length = 20
    src = df['Open']
    offset = 4  # Adjust the offset value if needed
    
    # Calculate SMA
    source = ta.trend.sma_indicator(src, length)
    
    # Calculate smoothing line
    length = 5
    
    smoothingLine = ta.trend.sma_indicator(source, length)
    
    # Print or use the values as needed
    return smoothingLine.iloc[-2]



def Latest_Close():
    df = pd.read_csv("./CSV_Files/bnf_5m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None
    

def Latest_Low():
    df = pd.read_csv("./CSV_Files/bnf_5m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Low']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None
    

def Latest_High():
    df = pd.read_csv("./CSV_Files/bnf_5m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['High']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None
    


def Old_Close():
    df = pd.read_csv("./CSV_Files/bnf_5m.csv")
    
    if not df.empty:
        last_row = df.iloc[-2]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None



while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) <= str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) >= str(data.date())+" 09:30:00.000000":

        while True:
            apikey = "ubGYgaFb"
            secretkey = "619f397c-67fb-4584-bc02-9206b2e96a97"
            user_id = "P489657"
            password = "1985"
            totp = "QEZQTYRWA3Y4A7C2JA3SPXNLVA"
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)

            RSI_New = RSI(Idx_Live)
            MA_New = MA()
            rsi_Old = RSI_Old(Idx_Live)
            ma_old = MA_Old()
            latest_close = Latest_Close()
            latest_low = Latest_Low()
            latest_high = Latest_High()
            old_close = Old_Close()
            GetExpiry_Date = Expiry_Date()

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print("RSI_New: "+str(RSI_New))
            print("rsi_Old: "+str(rsi_Old))
            print("MA_New: "+str(MA_New))
            print("ma_old: "+str(ma_old))
            print("Latest Close: "+str(latest_close))
            print("Latest High: "+str(latest_high))
            print("Latest Low: "+str(latest_low))
            print("Old Close: "+str(old_close))
            print(datetime.datetime.now())
            #sleep(1)

            sql = "select * from rsi_trades_5m ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))


            if str(datetime.datetime.now()) >= str(data.date())+" 15:27:00.000000":
                print("Market Closed")
                exit()


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"


                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                if float(RSI_New) > 30 and float(rsi_Old) < 30:
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
                    tokenresult = Angel_Data(symbol)
                    print(tokenresult)
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "Rsi_Trades_5m", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "call", IciciExpiry)


                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', 'RSI20', '"+str(MA_New)+"', '"+str(float(option_live)+50)+"')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(latest_close) > float(MA_New) and float(latest_low) < float(ma_old):
                    strikeprice = int(strikeprice)+100

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
                    tokenresult = Angel_Data(symbol)
                    print(tokenresult)
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "Rsi_Trades_5m", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "call", IciciExpiry)


                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '"+str(MA_New)+"', 'RSI_75', '"+str(float(option_live)+50)+"')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(RSI_New) < 75 and float(RSI_New) > 75:
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
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "Rsi_Trades_5m", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "put", IciciExpiry)


                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', 'RSI_80', '"+str(MA_New)+"', '"+str(float(option_live)+50)+"')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break


                if float(latest_close) < float(MA_New) and float(latest_high) > float(ma_old):
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
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "Rsi_Trades_5m", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "put", IciciExpiry)

                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '"+str(MA_New)+"', 'RSI20', '"+str(float(option_live)+50)+"')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break





            if Position == "1":
                sql = "select * from rsi_trades_5m ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Symbol = myresult[0]
                Token = myresult[1]
                Option_Price = myresult[4]
                Idx_bought_Price = myresult[5]
                Bought_DateTime = myresult[7]
                Sl = myresult[9]
                Profit = myresult[10]
                Tsl = myresult[11]

                original_datetime = datetime.datetime.strptime(Bought_DateTime, '%Y-%m-%d %H:%M:%S.%f')

                # Add 30 minutes
                modified_datetime = original_datetime + timedelta(minutes=30)

                # Convert the modified datetime back to the string format
                Target_DateTime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)

                print(Symbol)
                print("Bought at: "+str(Option_Price))
                print("Live Option: "+str(Option_live))
                print("SL: "+str(Sl))
                print("TSL: "+str(Tsl))
                print("Profit: "+str(MA_New))


                if float(Option_live) <= float(Option_Price)-30:
                    Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    current_datetime = datetime.datetime.now()
                    
                    # Calculate the next 5-minute interval after the given current datetime
                    next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                    next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)
                    # Ensure the next candle datetime is greater than the current time
                    if next_candle_datetime <= current_datetime:
                        next_candle_datetime += timedelta(minutes=5)
                    # Add 5 seconds to the next candle datetime
                    next_candle_datetime += timedelta(seconds=10)
                    # Calculate the difference in seconds
                    difference_seconds = (next_candle_datetime - current_datetime).total_seconds()
                    sleep(difference_seconds)
                    break


                if float(Option_live) >= float(Tsl):
                    trade = "update rsi_trades_5m set TSL='"+str(float(Tsl)-30)+"' where DateTime='"+str(Bought_DateTime)+"'"
                    mycursor.execute(trade)
                    mydb.commit()
                    break


                if float(Option_live) <= float(Tsl):
                    Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    current_datetime = datetime.datetime.now()
                    
                    # Calculate the next 5-minute interval after the given current datetime
                    next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                    next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)
                    # Ensure the next candle datetime is greater than the current time
                    if next_candle_datetime <= current_datetime:
                        next_candle_datetime += timedelta(minutes=5)
                    # Add 5 seconds to the next candle datetime
                    next_candle_datetime += timedelta(seconds=10)
                    # Calculate the difference in seconds
                    difference_seconds = (next_candle_datetime - current_datetime).total_seconds()
                    sleep(difference_seconds)
                    break




                if "CE" in Symbol:

                    if Sl == "RSI20":
                        if float(RSI_New) <= 20:
                        
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                        if float(Idx_Live) >= float(MA_New):
                            
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                    if Profit == "RSI_75":
                        if float(RSI_New) >= 75:
                        
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                        if float(Idx_Live) <= float(MA_New):
                            
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                if "PE" in Symbol:

                    if float(Option_live) <= float(Option_Price)-30:
                        Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                        trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                        mycursor.execute(trade)
                        mydb.commit()
                        current_datetime = datetime.datetime.now()
                        
                        # Calculate the next 5-minute interval after the given current datetime
                        next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                        next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)
                        # Ensure the next candle datetime is greater than the current time
                        if next_candle_datetime <= current_datetime:
                            next_candle_datetime += timedelta(minutes=5)
                        # Add 5 seconds to the next candle datetime
                        next_candle_datetime += timedelta(seconds=10)
                        # Calculate the difference in seconds
                        difference_seconds = (next_candle_datetime - current_datetime).total_seconds()
                        sleep(difference_seconds)
                        break

                    
                    if Sl == "RSI80":
                        if float(RSI_New) >= 77:
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                        if float(Idx_Live) <= float(MA_New):
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                    if Profit == "RSI20":
                        if float(RSI_New) <= 30:
                        
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                        if float(Idx_Live) >= float(MA_New):
                            
                            Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                            trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            current_datetime = datetime.datetime.now()

                            # Calculate the next 5-minute interval after the given current datetime
                            next_candle_datetime = (current_datetime + timedelta(minutes=5)).replace(second=0, microsecond=0)
                            next_candle_datetime -= timedelta(minutes=next_candle_datetime.minute % 5)

                            # Ensure the next candle datetime is greater than the current time
                            if next_candle_datetime <= current_datetime:
                                next_candle_datetime += timedelta(minutes=5)

                            # Add 5 seconds to the next candle datetime
                            next_candle_datetime += timedelta(seconds=10)

                            # Calculate the difference in seconds
                            difference_seconds = (next_candle_datetime - current_datetime).total_seconds()

                            sleep(difference_seconds)
                            break


                if str(datetime.datetime.now()) >= str(data.date())+" 15:27:00.000000":

                    Sell_Order(Symbol, Token, "Rsi_Trades_5m")
                    trade = "INSERT INTO rsi_trades_5m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades_5m', '0', '0', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                else:
                    break

            else:
                break
