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


def MACD_Live():
    # Read data from a CSV file (replace 'your_data.csv' with your file name)
    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_15m.csv')  # Make sure your CSV file has columns like 'Close'

    # Define indicator parameters
    fast_length = 5
    slow_length = 13
    signal_length = 9

    # Calculate the moving averages
    df['fast_ma'] = df['Close'].ewm(span=fast_length).mean()
    df['slow_ma'] = df['Close'].ewm(span=slow_length).mean()

    # Calculate MACD
    df['macd'] = df['fast_ma'] - df['slow_ma']

    # Calculate Signal line
    df['signal'] = df['macd'].ewm(span=signal_length).mean()

    # Calculate histogram
    df['hist'] = df['macd'] - df['signal']

    # Alert conditions
    conditions = [
        (df['hist'].shift(1) >= 0) & (df['hist'] < 0),
        (df['hist'].shift(1) <= 0) & (df['hist'] > 0)
    ]
    messages = ['Rising to falling', 'Falling to rising']
    df['alert'] = np.select(conditions, messages, default='')

    # Display the DataFrame with the calculated values
    return df[['macd']].iloc[-1].iloc[0], df[['signal']].iloc[-1].iloc[0], df[['hist']].iloc[-1].iloc[0]


def MACD_Old():
    # Read data from a CSV file (replace 'your_data.csv' with your file name)
    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_15m.csv')  # Make sure your CSV file has columns like 'Close'

    # Define indicator parameters
    fast_length = 5
    slow_length = 13
    signal_length = 9

    # Calculate the moving averages
    df['fast_ma'] = df['Close'].ewm(span=fast_length).mean()
    df['slow_ma'] = df['Close'].ewm(span=slow_length).mean()

    # Calculate MACD
    df['macd'] = df['fast_ma'] - df['slow_ma']

    # Calculate Signal line
    df['signal'] = df['macd'].ewm(span=signal_length).mean()

    # Calculate histogram
    df['hist'] = df['macd'] - df['signal']

    # Alert conditions
    conditions = [
        (df['hist'].shift(1) >= 0) & (df['hist'] < 0),
        (df['hist'].shift(1) <= 0) & (df['hist'] > 0)
    ]
    messages = ['Rising to falling', 'Falling to rising']
    df['alert'] = np.select(conditions, messages, default='')

    # Display the DataFrame with the calculated values
    return df[['macd']].iloc[-2].iloc[0], df[['signal']].iloc[-2].iloc[0], df[['hist']].iloc[-2].iloc[0]



while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) <= str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) >= str(data.date())+" 09:30:00.000000":

        while True:
            apikey = "AxPiryh1"
            secretkey = "0e621141-bf1b-4774-9ccb-578855c1fdbd"
            user_id = "A50735132"
            password = "8951"
            totp = "IZBMW5B2T4YF56PUNQIFIL6XLE"

            Slow_Line_Live = MACD_Live()[1]
            #Slow_Line_Live = MACD_Live()[2]
            Fast_Line_Live = MACD_Live()[0]

            Slow_Line_Old = MACD_Old()[1]
            #Slow_Line_Old = MACD_Old()[2]
            Fast_Line_Old = MACD_Old()[0]
            GetExpiry_Date = Expiry_Date()
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)


            if Idx_Live == None:
                break
            else:
                pass
            

            print("Idx live: "+str(Idx_Live))
            print("Fast_Line live: "+str(Fast_Line_Live))
            print("Slow_Line live: "+str(Slow_Line_Live))
            #print("Zero_Line live: "+str(Zero_Line_Live))
            print("Fast_Line old: "+str(Fast_Line_Old))
            print("Slow_Line old: "+str(Slow_Line_Old))
            #print("Zero_Line old: "+str(Zero_Line_Old))
            print(datetime.datetime.now())
            sleep(1)


            sql = "select * from trades ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))


            if str(datetime.datetime.now()) >= str(data.date())+" 15:25:00.000000":
                print("Market Closed")
                exit()


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = ""

                if int(str(Idx_Live)[3:5]) <= 50:
                    strikeprice = int(str(Idx_Live)[:3]+"00")
                if int(str(Idx_Live)[3:5]) >= 51:
                    strikeprice = int(float(str(Idx_Live)[:3]+"00")+100)

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                if float(Fast_Line_Live) > float(Slow_Line_Live) and float(Fast_Line_Old) < float(Slow_Line_Old):
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
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "call", IciciExpiry)

                    SL = float(Idx_Live)-80

                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF', '"+str(SL)+"')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(Fast_Line_Live) < float(Slow_Line_Live) and float(Fast_Line_Old) > float(Slow_Line_Old):
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
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "put", IciciExpiry)

                    SL = float(Idx_Live)+80

                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF', '"+str(SL)+"')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break


                if float(Fast_Line_Live) > 0 and float(Fast_Line_Old) < 0:
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
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "call", IciciExpiry)

                    SL = float(Idx_Live)-80

                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF', '"+str(SL)+"')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(Fast_Line_Live) < 0 and float(Fast_Line_Old) > 0:
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
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "put", IciciExpiry)

                    SL = float(Idx_Live)+80

                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF', '"+str(SL)+"')"
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
                Idx_bought_Price = myresult[5]
                Bought_DateTime = myresult[7]
                Sl = myresult[9]

                original_datetime = datetime.datetime.strptime(Bought_DateTime, '%Y-%m-%d %H:%M:%S.%f')

                # Add 30 minutes
                modified_datetime = original_datetime + timedelta(minutes=30)

                # Convert the modified datetime back to the string format
                Target_DateTime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)
                    
                print(Symbol)
                #print(Token)
                print("Bought at: "+str(Option_Price))
                print("Live Option: "+str(Option_live))
                print("Trailing SL: "+str(Sl))

                Profit = ""
                
                if "CE" in Symbol:
                    Profit = float(Idx_bought_Price)+80
                    print("Profit: "+str(Profit))
                    #Sl = float(Idx_bought_Price)-40

                    if float(Idx_Live) >= float(Profit):
                        #Trailing_SL = float(Idx_Live)-50
#
                        #trade = "update trades set SL='"+str(Trailing_SL)+"' where DateTime='"+str(Bought_DateTime)+"'"
                        #mycursor.execute(trade)
                        #mydb.commit()

                        Sell_Order(Symbol, Token, "BNF")
                        trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, '0') values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
                        mycursor.execute(trade)
                        mydb.commit()
                        exit()


                    if float(Idx_Live) <= float(Sl):

                        Sell_Order(Symbol, Token, "BNF")
                        trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        exit()



                if "PE" in Symbol:
                    Profit = float(Idx_bought_Price)-80
                    print("Profit: "+str(Profit))
                    #Sl = float(Idx_bought_Price)+60

                    if float(Idx_Live) <= float(Profit):
                        #Trailing_SL = float(Profit)+50
#
                        #trade = "update trades set SL='"+str(Trailing_SL)+"' where DateTime='"+str(Bought_DateTime)+"'"
                        #mycursor.execute(trade)
                        #mydb.commit()

                        Sell_Order(Symbol, Token, "BNF")
                        trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
                        mycursor.execute(trade)
                        mydb.commit()
                        exit()


                    if float(Idx_Live) >= float(Sl):
                    
                        Sell_Order(Symbol, Token, "BNF")
                        trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
                        mycursor.execute(trade)
                        mydb.commit()
    
                        exit()


                #if str(datetime.datetime.now()) >= str(Target_DateTime):
                #    Sell_Order(Symbol, Token, "BNF")
                #    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
                #    mycursor.execute(trade)
                #    mydb.commit()
                #
                #    exit()


                if str(datetime.datetime.now()) >= str(data.date())+" 15:10:00.000000":

                    Sell_Order(Symbol, Token, "BNF")
                    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()


                else:
                    break

            else:
                break