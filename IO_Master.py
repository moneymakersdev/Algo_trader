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


def Last_BNF_OI():
    df = pd.read_csv("./CSV_Files/bnf_fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['6']
        return last_close_price
    else:
        return None


def Second_Last_BNF_OI():
    df = pd.read_csv("./CSV_Files/bnf_fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-2]
        last_close_price = last_row['6']
        return last_close_price
    else:
        return None


def Third_Last_BNF_OI():
    df = pd.read_csv("./CSV_Files/bnf_fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-3]
        last_close_price = df.iloc[-3].iloc[6]
        close = df.iloc[-3].iloc[4]
        return last_close_price, close
    else:
        return None


def Latest_Close():
    df = pd.read_csv("./CSV_Files/bnf_fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


def SL_Price_CE():
    df = pd.read_csv("./CSV_Files/bnf_fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        Last_Total = float(last_row['Close']) - float(last_row['Open'])

        print("Last Total: "+str(Last_Total))

        Second_last_row = df.iloc[-1]
        Second_Last_Total = float(Second_last_row['Close']) - float(Second_last_row['Open'])

        print("Last Total: "+str(Second_Last_Total))
        
        Third_last_row = df.iloc[-1]
        Third_Last_Total = float(Third_last_row['Close']) - float(Third_last_row['Open'])

        print("Last Total: "+str(Third_Last_Total))

        Total = (Last_Total+Second_Last_Total+Third_Last_Total)/2
        
        print("Last SL: "+str(Total))

        return Total
    else:
        return None



def SL_Price_PE():
    df = pd.read_csv("./CSV_Files/bnf_fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        Last_Total = float(last_row['Open']) - float(last_row['Close'])

        print("Last Total: "+str(Last_Total))

        Second_last_row = df.iloc[-1]
        Second_Last_Total = float(Second_last_row['Open']) - float(Second_last_row['Close'])

        print("Last Total: "+str(Second_Last_Total))
        
        Third_last_row = df.iloc[-1]
        Third_Last_Total = float(Third_last_row['Open']) - float(Third_last_row['Close'])

        print("Last Total: "+str(Third_Last_Total))

        Total = (Last_Total+Second_Last_Total+Third_Last_Total)/2
        
        print("Last SL: "+str(Total))




while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:30:00.000000":

        while True:

            apikey = "hLiQVXsy"
            secretkey = "20a5f243-6bf5-405d-85ab-968c3a76a0e4"
            user_id = "ANMV1237"
            password = "4849"
            totp = "LVAMEXZBKHF2DPYICW564DTIFI"

            Last_Candle = Last_BNF_OI()
            Second_Last = Second_Last_BNF_OI()
            Third_Last = Third_Last_BNF_OI()[0]
            Last_Close = Latest_Close()
            Third_Candle_Close = Third_Last_BNF_OI()[1]

            GetExpiry_Date = Expiry_Date()
            Idx_Live = bnf_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print(datetime.datetime.now())

            sql = "select * from rsi_trades ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print(Position)
            print("Last_Candle: "+str(Last_Candle))
            print("Second_Last: "+str(Second_Last))
            print("Third_Last: "+str(Third_Last))
            sleep(1)


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                if float(Last_Candle) > float(Second_Last) and float(Second_Last) > float(Third_Last):
                    
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


                    tokenresult = Angel_Data(symbol)
                    print(symbol)
                    print(tokenresult)

                    Options_OI = Options_OI_CE(apikey, totp, user_id, password, tokenresult)
                    #print(Options_OI)
                    Option_OI_1 = list(Options_OI.iloc[-1])[5]
                    Option_OI_2 = list(Options_OI.iloc[-2])[5]
                    Option_OI_3 = list(Options_OI.iloc[-3])[5]
                    #Option_OI_4 = list(Options_OI.iloc[-4])[5]
                    #Option_OI_5 = list(Options_OI.iloc[-5])[5]

                    print("Last Option: "+str(symbol)+" "+str(Option_OI_1))
                    print("Second Last Option: "+str(symbol)+" "+str(Option_OI_2))
                    print("Third Last Option: "+str(symbol)+" "+str(Option_OI_3))
                    #print("Option: "+str(symbol)+" "+str(Option_OI_4))
                    #print("Option: "+str(symbol)+" "+str(Option_OI_5))

                    if float(Option_OI_1) > float(Option_OI_2) and float(Option_OI_2) > float(Option_OI_3):

                        print(symbol)
                        #token = 'select token from instruments where symbol="'+symbol+'"'
                        #mycursor.execute(token)
                        #tokenresult = mycursor.fetchone()
                        #print(tokenresult)

                        option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                        #Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "CALL", IciciExpiry)

                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'IO', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                    sleep(2)
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice)+"PE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice)+" PUT"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice)
                    #AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                    #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice)

                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice)+"PE"
                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                    tokenresult = Angel_Data(symbol)
                    print(symbol)
                    print(tokenresult)

                    Options_OI = Options_OI_PE(apikey, totp, user_id, password, tokenresult)

                    Option_OI_1 = list(Options_OI.iloc[-1])[5]
                    Option_OI_2 = list(Options_OI.iloc[-2])[5]
                    Option_OI_3 = list(Options_OI.iloc[-3])[5]
                    #Option_OI_4 = list(Options_OI.iloc[-4])[5]
                    #Option_OI_5 = list(Options_OI.iloc[-5])[5]

                    print("Last Option: "+str(symbol)+" "+str(Option_OI_1))
                    print("Second Last Option: "+str(symbol)+" "+str(Option_OI_2))
                    print("Third Last Option: "+str(symbol)+" "+str(Option_OI_3))
                    #print("Option: "+str(symbol)+" "+str(Option_OI_4))
                    #print("Option: "+str(symbol)+" "+str(Option_OI_5))

                    if float(Option_OI_1) > float(Option_OI_2) and float(Option_OI_2) > float(Option_OI_3):

                        print(symbol)

                        #token = 'select token from instruments where symbol="'+symbol+'"'
                        #mycursor.execute(token)
                        #tokenresult = Angel_Data(symbol)

                        option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                        #Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice), "PUT", IciciExpiry)

                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'IO', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                    else:
                        break
                
                else:
                    break



            if Position == "1":
                sql = "select * from rsi_trades ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Symbol = myresult[0]
                Token = myresult[1]
                Idx_Price = myresult[5]

                Option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol, Token)
                
                print("Bought at: "+str(Idx_Price))
                print("Symbol: "+str(Symbol))
                print("Live Option: "+str(Option_live))


                if "CE" in str(Symbol):
                    SL = float(Idx_Price)-float(SL_Price_CE())
                    Profit = float(Idx_Live)-float(Idx_Price)

                    if Profit >= 90:

                        #Sell_Order(Symbol, Token, "IO")
                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'IO', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                    if Profit <= float(SL):

                        #Sell_Order(Symbol, Token, "IO")
                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'IO', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break



                if "PE" in str(Symbol):
                    SL = float(Idx_Price)+float(SL_Price_PE())
                    Profit = float(Idx_Live)-float(Idx_Price)

                    if Profit <= 90:

                        #Sell_Order(Symbol, Token, "IO")
                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'IO', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break


                    if Profit >= float(SL):

                        #Sell_Order(Symbol, Token, "IO")
                        trade = "INSERT INTO rsi_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(Symbol.replace("'", ""))+"', '"+str(Token.replace("'", ""))+"', 'SL', '30', '"+str(Option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'IO', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break

                else:
                    break
            

            else:
                break