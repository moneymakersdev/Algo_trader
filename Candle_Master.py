import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
import csv
from Tokens import *


def Candle_1_20_High():
    date = datetime.date.today()
    file_path = './CSV_Files/heikin_bnf_Fut_5m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)

    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="ISO8601", utc=True)

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = str(date)+' 13:20:00+05:30'
    
    target_datetime = pd.to_datetime(target_datetime_str, format="ISO8601", utc=True)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        close_price = filtered_data['High'].values[0]
        return close_price
    #else:
    #    return None


def Candle_1_20_Low():
    date = datetime.date.today()
    file_path = './CSV_Files/heikin_bnf_Fut_5m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)

    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="ISO8601", utc=True)

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = str(date)+' 13:20:00+05:30'
    target_datetime = pd.to_datetime(target_datetime_str, format="ISO8601", utc=True)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        close_price = filtered_data['Low'].values[0]
        return close_price
    else:
        return None


def Latest_Close():
    df = pd.read_csv("./CSV_Files/heikin_bnf_Fut_5m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 13:25:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 13:25:00.000000":

        while True:

            apikey = "USBzqs1v"
            secretkey = "d8004c20-097c-446f-80bd-1e0eb096f563"
            user_id = "A1403293"
            password = "1025"
            totp = "6PEKPAF64PHZ5UVIPTKXIBKTIU"

            High_120 = Candle_1_20_High()
            Low_120 = Candle_1_20_Low()
            Close = Latest_Close()
            GetExpiry_Date = Expiry_Date()
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print("Close "+str(Close))
            print("1 20 High: "+str(High_120))
            print("1 20 Low: "+str(Low_120))
            print(datetime.datetime.now())

            sql = "select * from candle_master_trades ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]
                
                if float(Close) > float(High_120):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"CE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" CALL"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice)
                    #AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                    #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)



                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    #tokenresult = mycursor.fetchone()
                    tokenresult = Angel_Data(symbol)
                    
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "Candle_Master", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "CALL", IciciExpiry)

                    trade = "INSERT INTO candle_master_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Candle_Master', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                if float(Close) < float(Low_120):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"PE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" PUT"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice)
                    #AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                    #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)



                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    #tokenresult = mycursor.fetchone()
                    tokenresult = Angel_Data(symbol) 
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "Candle_Master", str(DhanSymbol), AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "PUT", IciciExpiry)

                    trade = "INSERT INTO candle_master_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Candle_Master', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break

                else:
                    break



            if Position == "1":
                sql = "select * from candle_master_trades ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Symbol = myresult[0]
                Token = myresult[1]
                Option_Price = myresult[4]

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)
                
                Profit = (float(Option_live)*30)-(float(Option_Price)*30)

                print("Bought at: "+str(Option_Price))
                print("Live Option: "+str(Option_live))
                print("Profit: "+str(Profit))
                print(Symbol)
                #print(Token)

                if Profit > 700:

                    Sell_Order(Symbol, Token, "Candle_Master")
                    trade = "INSERT INTO candle_master_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Candle_Master', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if Profit < -700:

                    Sell_Order(Symbol, Token, "Candle_Master")
                    trade = "INSERT INTO candle_master_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Candle_Master', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                else:
                    break
            
            
            else:
                break