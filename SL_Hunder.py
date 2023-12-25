import pandas as pd
import datetime
from datetime import datetime, timedelta, timezone
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Tokens import *
from time import sleep
import numpy as np
import pandas_ta as ta



def Candle_9_15_High():
    date = datetime.date.today()
    file_path = './CSV_Files/bnf_1m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)
    
    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'])

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = str(date)+' 09:15:00'
    target_datetime = pd.to_datetime(target_datetime_str)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        High = filtered_data['High'].values[0]
        Low = filtered_data['Low'].values[0]
        return High, Low
    else:
        return None


def Candle_9_15_High_Fut():
    date = datetime.date.today()
    file_path = './CSV_Files/bnf_Fut_1m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)
    
    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'])

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = str(date)+' 09:15:00'
    target_datetime = pd.to_datetime(target_datetime_str)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        High = filtered_data['High'].values[0]
        Low = filtered_data['Low'].values[0]
        return High, Low
    else:
        return None



def Target_DateTime(Target_Time):
    date = datetime.date.today()
    file_path = './CSV_Files/bnf_Fut_1m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)
    
    # Convert the DateTime column to datetime format
    data['DateTime'] = pd.to_datetime(data['DateTime'])

    # Replace 'target_datetime' with the DateTime you're interested in
    target_datetime_str = Target_Time
    target_datetime = pd.to_datetime(target_datetime_str)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        Open = filtered_data['Open'].values[0]
        Close = filtered_data['Close'].values[0]

        if float(Close) > float(Open):
            return "Green"
        if float(Close) < float(Open):
            return "Red"

    else:
        return None



while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:16:15.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:16:15.000000":

        while True:
            apikey = "h6jSmhjF"
            secretkey = "8d9b5028-218e-4bfb-9e44-c8c52d3e2dce"
            user_id = "VJVG1338"
            password = "0107"
            totp = "VLSNN2YQT2TEBDDVFCVK34KZAE"

            Fut_First_Candle_High = Candle_9_15_High_Fut()[0]
            First_Candle_High = Candle_9_15_High()[0]
            Fut_First_Candle_Low = Candle_9_15_High_Fut()[1]
            First_Candle_Low = Candle_9_15_High()[1]


            GetExpiry_Date = Expiry_Date()

            Idx_Live_Fut = bnf_Fut_Price(apikey, secretkey, user_id, password, totp)
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)


            if Idx_Live == None:
                break
            else:
                pass
            
            print("Fut Latest "+str(Idx_Live_Fut))
            print("Fut Candle High "+str(Fut_First_Candle_High))
            print("Fut Candle Low "+str(Fut_First_Candle_High))

            print("Idx Latest "+str(Idx_Live))
            print("Spot Candle High "+str(First_Candle_High))
            print("Spot Candle Low "+str(First_Candle_Low))

            print(datetime.datetime.now())

            sql = "select * from rsi_trades ORDER BY DateTime DESC"
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


                #if str(datetime.datetime.now()) >= str(data.date())+" 09:30:00.000000":
                #    print("Market Closed")
                #    exit()


                if float(Idx_Live_Fut) < float(Fut_First_Candle_High) or float(Idx_Live) < float(First_Candle_High):

                    current_datetime = datetime.datetime.now()
                    print("Current "+str(current_datetime))

                    new_datetime = current_datetime + datetime.timedelta(minutes=2)
                    print("New Time: "+str(new_datetime))

                    given_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:00")
                    print("Given " +str(given_datetime))
                    
                    sleeptime = (new_datetime.replace(second=0, microsecond=0) - current_datetime).total_seconds()
                    print("Seconds: "+str(sleeptime))
                    sleep(sleeptime)
                    #after sleep

                    Target_Candle = Target_DateTime(given_datetime)

                    print("Target " +str(Target_Candle))


                    if Target_Candle == "Green":

                        symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"CE"
                        DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" CALL"
                        AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice)
                        #AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" CE"
                        #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                        UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                        FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                        MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice)

                        #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                        Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                        IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                        print(symbol)

                        tokenresult = Angel_Data(symbol)
                        print(tokenresult)

                        option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                        #Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "Saturn", str(DhanSymbol), AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "PUT", IciciExpiry)

                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Saturn', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                    else:
                        break



                if float(Idx_Live_Fut) > float(Fut_First_Candle_Low) or float(Idx_Live) > float(First_Candle_Low):

                    current_datetime = datetime.datetime.now()
                    print("Current "+str(current_datetime))

                    new_datetime = current_datetime + datetime.timedelta(minutes=2)
                    print("New Time: "+str(new_datetime))

                    given_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:00+05:30")
                    print("Given " +str(given_datetime))
                    
                    sleeptime = (new_datetime.replace(second=0, microsecond=0) - current_datetime).total_seconds()
                    print("Seconds: "+str(sleeptime))
                    sleep(sleeptime)
                    #after sleep

                    Target_Candle = Target_DateTime(given_datetime)

                    print("Target " +str(Target_Candle))

                    if Target_Candle == "Red":

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


                        print(symbol)

                        tokenresult = Angel_Data(symbol)
                        print(tokenresult)

                        option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                        #Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "Saturn", str(DhanSymbol), AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "PUT", IciciExpiry)

                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Saturn', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                else:
                    break



            if Position == "1":
                sql = "select * from rsi_trades ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Symbol = myresult[0]
                Token = myresult[1]
                Option_Price = myresult[4]
                Idx_Price = myresult[5]

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)
                
                Profit = float(Idx_Price)+55
                Sl = float(Idx_Price)-30
                print(Symbol)
                print(Token)
                print("Bought IDX: "+str(Idx_Price))
                print("Bought at: "+str(Option_Price))
                print("Live Option: "+str(Option_live))


                if float(Option_live) >= float(Profit):
                    #Sell_Order(Symbol, Token, "BNF")
                    
                    trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                if float(Option_live) <= float(Sl):

                    #Sell_Order(Symbol, Token, "BNF")
                    trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if str(datetime.datetime.now()) >= str(data.date())+" 15:10:00.000000":

                    #Sell_Order(Symbol, Token, "BNF")
                    trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                
                else:
                    break

            else:
                break