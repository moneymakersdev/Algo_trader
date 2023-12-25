import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Tokens import *




while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) <= str(data.date())+" 09:15:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:15:00.000000":

        while True:

            apikey = "o2GCxAN9"
            secretkey = "489816c2-5deb-40a3-ad4c-15c48e27fe88"
            user_id = "BBLM50549"
            password = "4568"
            totp = "DOQ76H5X6Q2RERYZIIZC7RZNDU"

            GetExpiry_Date = Nifty_Expiry_Date()
            Idx_Live = Nifty_Idx_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print(datetime.datetime.now())
            sleep(1)

            sql = "SELECT * FROM nifty_expiry ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()

            if myresult == None:
                Position = "0"
            else:
                Position = myresult[6]
            print("Position "+str(Position))


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = ""

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                if int(str(Idx_Live)[3:5]) <= 24:
                    strikeprice = int(str(Idx_Live)[:3]+"00")
                if int(str(Idx_Live)[3:5]) >= 25 and int(str(Idx_Live)[3:5]) <= 75:
                    strikeprice = int(float(str(Idx_Live)[:3]+"50"))
                if int(str(Idx_Live)[3:5]) >= 76:
                    strikeprice = int(str(Idx_Live)[:3]+"00")+150


                if str(datetime.datetime.now()) > str(data.date())+" 15:20:00.000000":
                    symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice+150)+"CE"
                    DhanSymbol = "NIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice+150)+" CALL"
                    AliceSymbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice+150)
                    UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice+150)+"CE"
                    #UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                    FyresSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice+150)+"CE"
                    MotilalSymbol = "NIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice+150)

                    Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice+150)+"CE"
                    #Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice+150)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+str(ExpiryDate)


                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    print(tokenresult)
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "nifty_expiry_ce", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice+150), "call", IciciExpiry)

                    trade = "INSERT INTO nifty_expiry (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'nifty_expiry_ce')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                
                    symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice-150)+"PE"
                    DhanSymbol = "NIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice-150)+" PUT"
                    AliceSymbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice-150)
                    UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice-150)+"PE"
                    #UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice-150)+"PE"   #Monthly Expiry
                    FyresSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice-150)+"PE"
                    MotilalSymbol = "NIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice-150)

                    Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice-150)+"PE"
                    #Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice-150)+"PE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+str(ExpiryDate)


                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "nifty_expiry_pe", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice-150), "put", IciciExpiry)

                    trade = "INSERT INTO nifty_expiry (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'nifty_expiry_pe')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                else:
                    break

            

            if Position == "1":
                sql = "SELECT * FROM nifty_expiry WHERE Token IN ( SELECT Token FROM nifty_expiry WHERE Type = 'BUY' GROUP BY Token HAVING COUNT(*) = 1 ) AND Token NOT IN ( SELECT Token FROM nifty_expiry WHERE Type = 'SELL' );"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()

                #print(myresult)

                for I in range(len(myresult)):
                    #print(myresult[I])
                    
                    Symbol_1 = myresult[I][0]
                    Token_1 = myresult[I][1]
                    Option_Price_1 = myresult[I][4]
                    Option_live_1 = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol_1, Token_1)               

                    print("Bought at: "+str(Option_Price_1))
                    print("Live at: "+str(Option_live_1))

                    if str(datetime.datetime.now()) < str(data.date())+" 09:20:00.000000":
                        #NIFTY22NOV2343800CE
                        Strike_Price = ''.join(list(Symbol_1)[16:21])
                        Exp_Date = ''.join(list(Symbol_1)[9:11])
                        Exp_Mon = ''.join(list(Symbol_1)[11:14])
                        Exp_Year = ''.join(list(Symbol_1)[14:16])
                        Type = ''.join(list(Symbol_1)[21:])


                        symbol = "NIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Strike_Price)+str(Type)
                        
                        if Type == "CE":
                            Type = "CALL"
                        if Type == "PE":
                            Type = "PUT"

                        DhanSymbol = "NIFTY "+str(Exp_Date)+" "+str(Exp_Mon)+" "+str(Strike_Price)+" "+str(Type)

                        #AliceSymbol = "NIFTY08NOV23C42600"
                        AliceSymbol = "NIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+"C"+str(Strike_Price)
                        #AliceSymbol = "NIFTY "+str(Exp_Mon)+" "+str(strikeprice)+" "+str(Type)
                        UpstoxSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        #UpstoxSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)   #Monthly Expiry
                        FyresSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        MotilalSymbol = "NIFTY "+str(Exp_Date)+"-"+str(Exp_Mon)+"-"+str(Exp_Year)+" "+str(Type)+" "+str(Strike_Price)
                        Zerodha = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        #Zerodha = "NIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)    #Monthly Expiry
                        IciciExpiry = "20"+str(Exp_Year)+"-"+str(Exp_Mon)+"-"+str(Exp_Date)


                        Sell_Order(symbol, Token_1, "nifty_expiry")
                        trade = "INSERT INTO nifty_expiry (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(Token_1.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live_1)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'nifty_expiry')"
                        mycursor.execute(trade)
                        mydb.commit()

                        pass