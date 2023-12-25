import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Tokens import *
import pandas_ta as ta


def calculate_ema(data, period):
    ema = data.ewm(span=period, adjust=False).mean()
    return ema


def ema_1():
    while True:
            # Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_15m.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 5  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return format(round(last_ema_value, 2))

        #ema = ta.ema(data['Close'], length=5)
#
        #return ema.iloc[-1]


def old_ema_1():
    while True:
            # Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_15m.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 5  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-3]

        return format(round(last_ema_value, 2))

        #ema = ta.ema(data['Close'], length=5)

        #return ema.iloc[-2]


def ema_2():
    while True:
            # Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_15m.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 13  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return format(round(last_ema_value, 2))

        #ema = ta.ema(data['Close'], length=13)
#
        #return ema.iloc[-1]



def old_ema_2():
    while True:
        #Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_15m.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

        # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

        # Specify the EMA period
        ema_period = 13  # Replace with the desired EMA period

        # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

        # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-3]

        return format(round(last_ema_value, 2))

        #ema = ta.ema(data['Close'], length=13)
#
        #return ema.iloc[-2]




while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) <= str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) >= str(data.date())+" 09:30:00.000000":

        while True:
            apikey = "USBzqs1v"
            secretkey = "d8004c20-097c-446f-80bd-1e0eb096f563"
            user_id = "A1403293"
            password = "1025"
            totp = "6PEKPAF64PHZ5UVIPTKXIBKTIU"

            Ema_1 = ema_1()
            Ema_2 = ema_2()
            Old_Ema_1 = old_ema_1()
            Old_Ema_2 = old_ema_2()
            GetExpiry_Date = Expiry_Date()
            Idx_Live = bnf_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print("Ema 1: "+str(Ema_1))
            print("Ema 2: "+str(Ema_2))
            print("Old Ema 1: "+str(Old_Ema_1))
            print("Old Ema 2: "+str(Old_Ema_2))
            print(datetime.datetime.now())
            #sleep(1)

            sql = "select * from trades ORDER BY DateTime DESC"
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


                if float(Ema_1) > float(Ema_2) and float(Old_Ema_1) < float(Old_Ema_2):
                    symbol = "BANKNIFTY0"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"CE"
                    DhanSymbol = "BANKNIFTY 0"+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" CALL"
                    AliceSymbol = "BANKNIFTY0"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice)
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+"0"+str(ExpiryDate)+str(strikeprice)+"CE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+"0"+str(ExpiryDate)+str(strikeprice)+"CE"
                    MotilalSymbol = "BANKNIFTY 0"+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice)

                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+"0"+str(ExpiryDate)+str(strikeprice)+"CE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    print(tokenresult)
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "call", IciciExpiry)

                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                if float(Ema_1) < float(Ema_2) and float(Old_Ema_1) > float(Old_Ema_2):
                    symbol = "BANKNIFTY0"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"PE"
                    DhanSymbol = "BANKNIFTY 0"+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" PUT"
                    AliceSymbol = "BANKNIFTY0"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice)
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+"0"+str(ExpiryDate)+str(strikeprice)+"PE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+"0"+str(ExpiryDate)+str(strikeprice)+"PE"
                    MotilalSymbol = "BANKNIFTY 0"+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice)

                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+"0"+str(ExpiryDate)+str(strikeprice)+"PE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "put", IciciExpiry)

                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break

                else:
                    break



            if Position == "1":
                sql = "select * from trades ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Symbol = myresult[0]
                Token = myresult[1]
                Option_Price = myresult[4]

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)
            
                Profit = float(Option_Price)+40
                Sl = float(Option_Price)-30
                print(Symbol)
                print(Token)
                print("Bought at: "+str(Option_Price))
                print("Live Option: "+str(Option_live))


                if float(Option_live) >= float(Profit):

                    Sell_Order(Symbol, Token, "BNF")
                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if float(Option_live) <= float(Sl):

                    Sell_Order(Symbol, Token, "BNF")
                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                if str(datetime.datetime.now()) >= str(data.date())+" 15:10:00.000000":

                    Sell_Order(Symbol, Token, "BNF")
                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                else:
                    break

            else:
                break