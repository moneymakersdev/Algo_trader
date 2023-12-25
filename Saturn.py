import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
import csv
from time import sleep
from Tokens import *
from datetime import timedelta



def Candle_9_20():
    date = datetime.date.today()
    file_path = './CSV_Files/bnf_5m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)
    
    # Get current datetime
    current_datetime = datetime.now()

    # Calculate datetime for yesterday
    yesterday_datetime = current_datetime - timedelta(days=1)

    # Format yesterday's datetime as desired
    yesterday_datetime = yesterday_datetime.strftime('%Y-%m-%d')
    target_datetime_str = str(yesterday_datetime)+' 09:20:00+05:30'
    target_datetime = pd.to_datetime(target_datetime_str, format="ISO8601", utc=True)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]

    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        close_price = filtered_data['Close'].values[0]
        return close_price
    else:
        return None



def Latest_Close():
    df = pd.read_csv("./CSV_Files/bnf_5m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 11:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 11:30:00.000000":

        while True:

            apikey = "PlL6NEOc"
            secretkey = "c6a3a09e-80f0-4ad0-9316-2ee896d4a6ae"
            user_id = "V613816"
            password = "7488"
            totp = "4MHESI7A2QF74OEKBEPNEWBHPY"

            Close_920 = Candle_9_20()
            Last_Close = Latest_Close()

            GetExpiry_Date = Expiry_Date()
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print(datetime.datetime.now())

            sql = "select * from saturn_trades ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print(Position)
            print("9 20 close: "+str(Close_920))
            print("latest: "+str(Last_Close))
            sleep(1)


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                if float(Last_Close) > float(Close_920):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"CE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" CALL"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice)
                    ##UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"CE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)



                    print(symbol)
                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    #tokenresult = mycursor.fetchone()
                    #print(tokenresult)
                    tokenresult = Angel_Data(symbol)
                    print(tokenresult)

                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "Saturn", str(DhanSymbol), AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "CALL", IciciExpiry)

                    trade = "INSERT INTO saturn_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Saturn', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                if float(Last_Close) < float(Close_920):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"PE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" PUT"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice)
                    ##UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)



                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult.replace("'", "")), "Saturn", str(DhanSymbol), AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "PUT", IciciExpiry)

                    trade = "INSERT INTO saturn_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Saturn', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break
                
                else:
                    break



            if Position == "1":
                sql = "select * from saturn_trades ORDER BY DateTime DESC"
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


                if Profit > 500:

                    Sell_Order(Symbol, Token, "Saturn")
                    trade = "INSERT INTO saturn_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Saturn', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if Profit < -700:

                    Sell_Order(Symbol, Token, "Saturn")
                    trade = "INSERT INTO saturn_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Saturn', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                else:
                    break
            

            else:
                break