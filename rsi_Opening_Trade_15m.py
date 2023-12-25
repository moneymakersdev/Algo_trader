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
import ast



def ma_cal(source, length, type):
    if type == "SMA":
        return ta.trend.sma_indicator(source, length)
    elif type == "EMA":
        return ta.trend.ema_indicator(source, length)
    elif type == "SMMA (RMA)":
        return ta.trend.rma_indicator(source, length)
    elif type == "WMA":
        return ta.trend.wma_indicator(source, length)
    elif type == "VWMA":
        return ta.volume.volume_weighted_average_price(source, length)
    


def MA():
    file_path = './CSV_Files/bnf_15m.csv'
    df = pd.read_csv(file_path)
    
    # Parameters
    length = 20
    src = df['Open']
    offset = 5  # Adjust the offset value if needed
    
    # Calculate SMA
    out = ta.trend.sma_indicator(src, length)

    return out.iloc[-1]




def Candle_9_15_High():
    date = datetime.date.today()
    file_path = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_15m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)

    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="ISO8601", utc=True)

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = str(date)+' 09:15:00' #'2023-12-22 09:15:00'#str(date)+' 09:15:00'

    target_datetime = pd.to_datetime(target_datetime_str, format="ISO8601", utc=True)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        close_price = filtered_data['High'].values[0]
        return close_price
    #else:
    #    return None



def Candle_9_15_Low():
    date = datetime.date.today()
    file_path = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_15m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)

    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="ISO8601", utc=True)

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = str(date)+' 09:15:00' #'2023-12-22 09:15:00'#str(date)+' 09:15:00'
    
    target_datetime = pd.to_datetime(target_datetime_str, format="ISO8601", utc=True)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        close_price = filtered_data['Low'].values[0]
        return close_price
    #else:
    #    return None




while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) <= str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) >= str(data.date())+" 09:30:00.000000":

        while True:
            apikey = "cb1YqABV"
            secretkey = "f18e4d5d-6721-440f-8dea-f5dab9131163"
            user_id = "A1393565"
            password = "1008"
            totp = "KVSWSGQ3KMSVGHIUZJ2BU6AEA4"
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            High_15 = Candle_9_15_High()
            Low_15 = Candle_9_15_Low()
            GetExpiry_Date = Expiry_Date()
            MA_New = MA()
            
            print("Idx live: "+str(Idx_Live))
            print("15 High: "+str(High_15))
            print("15 Low: "+str(Low_15))
            print("MA "+str(MA_New))
            print(datetime.datetime.now())

            sql = "select * from rsi_Opening_Trade_15m ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))


            if str(datetime.datetime.now()) >= str(data.date())+" 10:00:00.000000":
                print("Market Closed")
                exit()


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                if float(Idx_Live) > float(High_15):
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
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "Rsi_Trades", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "call", IciciExpiry)


                    if float(Idx_Live) > float(MA_New):                    
                        trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', 'MA', 'None', '"+str(float(option_live)+40)+"')"
                        mycursor.execute(trade)
                        mydb.commit()
                    else:
                        trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', 'None', 'MA', '"+str(float(option_live)+40)+"')"
                        mycursor.execute(trade)
                        mydb.commit()


                    data = "{'TSL': '0', 'Target': '"+str(float(option_live)+40)+"'}"
                    with open('rsi_Opening_Trade_15m.json', 'w') as outfile:
                        outfile.write(data)
                        outfile.close()
                    
                    break 



                if float(Idx_Live) < float(Low_15):
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
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "Rsi_Trades", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "put", IciciExpiry)

                    if float(Idx_Live) < float(MA_New):                    
                        trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', 'None', 'MA', '"+str(float(option_live)+40)+"')"
                        mycursor.execute(trade)
                        mydb.commit()
                    else:
                        trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', 'MA', 'None', '"+str(float(option_live)+40)+"')"
                        mycursor.execute(trade)
                        mydb.commit()

                    data = "{'TSL': '0', 'Target': '"+str(float(option_live)+40)+"'}"
                    with open('rsi_Opening_Trade_15m.json', 'w') as outfile:
                        outfile.write(data)
                        outfile.close()

                    break



            if Position == "1":
                sql = "select * from rsi_Opening_Trade_15m ORDER BY DateTime DESC"
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

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)
                
                print(Symbol)
                print("Bought at: "+str(Option_Price))
                print("Live Option: "+str(Option_live))
                print("SL: "+str(Sl))
                print("TSL: "+str(Tsl))
                print("Profit: "+str(MA_New))

                with open('rsi_Opening_Trade_15m.json', 'r') as outfile:
                   data = outfile.read()

                jsondata = ast.literal_eval(data)

                Tsl = jsondata["TSL"]
                Target = jsondata["Target"]


                if float(Option_live) <= float(Option_Price)-30:
                    Sell_Order(Symbol, Token, "Rsi_Trades")
                    trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', '0', '0', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    exit()


                if float(Option_live) >= float(Target):
                    data = "{'TSL': '"+str(float(Option_live)-30)+"', 'Target': '"+str(Option_live)+"'}"
                    with open('rsi_Opening_Trade_15m.json', 'w') as outfile:
                        outfile.write(data)
                        outfile.close()
                    break


                data = datetime.datetime.now()

                if str(datetime.datetime.now()) >= str(data.date())+" 15:27:00.000000":

                    Sell_Order(Symbol, Token, "Rsi_Trades")
                    trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', '0', '0', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if "CE" in Symbol:
                    if Sl == "MA":
                        if float(Idx_Live) <= MA_New:
                            Sell_Order(Symbol, Token, "Rsi_Trades")
                            trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            exit()

                    if Profit == "MA":
                        if float(Idx_Live) >= MA_New:
                            Sell_Order(Symbol, Token, "Rsi_Trades")
                            trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            exit()



                if "PE" in Symbol:
                    if Sl == "MA":
                        if float(Idx_Live) >= MA_New:
                            Sell_Order(Symbol, Token, "Rsi_Trades")
                            trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            exit()

                    if Profit == "MA":
                        if float(Idx_Live) <= MA_New:
                            Sell_Order(Symbol, Token, "Rsi_Trades")
                            trade = "INSERT INTO rsi_Opening_Trade_15m (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL, Profit, TSL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Rsi_Trades', '0', '0', '0')"
                            mycursor.execute(trade)
                            mydb.commit()
                            exit()


                else:
                    break

            else:
                break
