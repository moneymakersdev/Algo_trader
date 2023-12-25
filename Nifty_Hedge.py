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




def Latest_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


def Previous_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_15m.csv")
    
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

            apikey = "hLiQVXsy"
            secretkey = "20a5f243-6bf5-405d-85ab-968c3a76a0e4"
            user_id = "ANMV1237"
            password = "4849"
            totp = "LVAMEXZBKHF2DPYICW564DTIFI"

            GetExpiry_Date = Nifty_Expiry_Date()
            Idx_Live = nifty_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print(datetime.datetime.now())
            sleep(1)

            sql = "SELECT * FROM nifty_hedge WHERE DATE(DateTime) = CURRENT_DATE;"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            print(myresult)
            if myresult == None:
                Position = "0"
            else:
                Position = myresult[6]
            print("Position "+str(Position))


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(int(float(strikeprice)+100))+"CE"
                DhanSymbol = "NIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(int(float(strikeprice)+100))+" CALL"
                #AliceSymbol = "NIFTY08NOV23C42600"
                AliceSymbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(int(float(strikeprice)+100))
                #AliceSymbol = "NIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)+100))+"CE"
                #UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                FyresSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)+100))+"CE"
                MotilalSymbol = "NIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)+" CE "+str(int(float(strikeprice)+100))
                Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)+100))+"CE"
                #Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                tokenresult = Angel_Data(symbol)
                print(tokenresult)
                option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                Short_Order(symbol, tokenresult, "nifty_hedged", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, strikeprice, "call", IciciExpiry)

                trade = "INSERT INTO nifty_hedge (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'SHORT', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'nifty_hedge')"
                mycursor.execute(trade)
                mydb.commit()

                

                symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(int(float(strikeprice)+200))+"CE"
                DhanSymbol = "NIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(int(float(strikeprice)+200))+" CALL"
                #AliceSymbol = "NIFTY08NOV23C42600"
                AliceSymbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(int(float(strikeprice)+200))
                #AliceSymbol = "NIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)+200))+"CE"
                #UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                FyresSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)+200))+"CE"
                MotilalSymbol = "NIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)+" CE "+str(int(float(strikeprice)+200))
                Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)+200))+"CE"
                #Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"    #Monthly Expiry
                IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                tokenresult = Angel_Data(symbol)
                print(tokenresult)
                option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                Short_Order(symbol, tokenresult, "nifty_hedged", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, strikeprice, "call", IciciExpiry)
                
                trade = "INSERT INTO nifty_hedge (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'SHORT', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'nifty_hedge')"
                mycursor.execute(trade)
                mydb.commit()



                symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(int(float(strikeprice)-100))+"PE"
                DhanSymbol = "NIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(int(float(strikeprice)-100))+" PUT"
                #AliceSymbol = "NIFTY08NOV23C42600"
                AliceSymbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(int(float(strikeprice)-100))
                #AliceSymbol = "NIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)-100))+"PE"
                #UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                FyresSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)-100))+"PE"
                MotilalSymbol = "NIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)+" PE "+str(int(float(strikeprice)-100))
                Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)-100))+"PE"
                #Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry
                IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                tokenresult = Angel_Data(symbol)
                print(tokenresult)
                option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                Short_Order(symbol, tokenresult, "nifty_hedged", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(int(float(strikeprice)-100)), "call", IciciExpiry)

                trade = "INSERT INTO nifty_hedge (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'SHORT', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'nifty_hedge')"
                mycursor.execute(trade)
                mydb.commit()



                symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(int(float(strikeprice)-200))+"PE"
                DhanSymbol = "NIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(int(float(strikeprice)-200))+" PUT"
                #AliceSymbol = "NIFTY08NOV23C42600"
                AliceSymbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(int(float(strikeprice)-200))
                #AliceSymbol = "NIFTY "+str(ExpiryMonth)+" "+str(strikeprice)+" PE"
                UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)-200))+"PE"
                #UpstoxSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"   #Monthly Expiry
                FyresSymbol = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)-200))+"PE"
                MotilalSymbol = "NIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-"+str(ExpiryYear)+" PE "+str(int(float(strikeprice)-200))
                Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(int(float(strikeprice)-200))+"PE"
                #Zerodha = "NIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"PE"    #Monthly Expiry
                IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)


                tokenresult = Angel_Data(symbol)
                print(tokenresult)
                option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))

                Short_Order(symbol, tokenresult, "nifty_hedged", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(int(float(strikeprice)-200)), "call", IciciExpiry)

                trade = "INSERT INTO nifty_hedge (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'SHORT', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'nifty_hedge')"
                mycursor.execute(trade)
                mydb.commit()

                break


            if Position == "1":
                sql = "SELECT * FROM nifty_hedge WHERE Token IN ( SELECT Token FROM nifty_hedge WHERE Type = 'SHORT' AND Type != 'SHORTEXIT' AND Type!='SHORTSL' GROUP BY Token HAVING COUNT(*) = 1 ) AND DATE(DateTime) = CURDATE();"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()

                for I in range(len(myresult)):
                    #print(myresult[I])
                    
                    Symbol_1 = myresult[I][0]
                    Token_1 = myresult[I][1]
                    Option_Price_1 = myresult[I][4]
                    Option_live_1 = Option_Idx_Price(apikey, secretkey, user_id, password, totp, Symbol_1, Token_1)               
                    SL_1 = (float(Option_Price_1)*25/100)+float(Option_Price_1)   
                    
                    print("Bought at: "+str(Option_Price_1))
                    print("Live at: "+str(Option_live_1))
                    print("SL: "+str(SL_1))
                    
                    if float(Option_live_1) >= float(SL_1):

                        Strike_Price = ''.join(list(Symbol_1)[12:17])
                        Exp_Date = ''.join(list(Symbol_1)[5:7])
                        Exp_Mon = ''.join(list(Symbol_1)[7:10])
                        Exp_Year = ''.join(list(Symbol_1)[10:12])
                        Type = ''.join(list(Symbol_1)[17:])


                        symbol = "NIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Strike_Price)+str(Type)
                        
                        if Type == "CE":
                            Type = "CALL"
                        if Type == "PE":
                            Type = "PUT"

                        DhanSymbol = "NIFTY "+str(Exp_Date)+" "+str(Exp_Mon)+" "+str(Strike_Price)+" "+str(Type)

                        Type = ''.join(list(Symbol_1)[17:])
                        #AliceSymbol = "NIFTY08NOV23C42600"
                        AliceSymbol = "NIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Type[0])+str(Strike_Price)
                        #AliceSymbol = "NIFTY "+str(Exp_Mon)+" "+str(strikeprice)+" "+str(Type)
                        UpstoxSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        #UpstoxSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)   #Monthly Expiry
                        FyresSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        MotilalSymbol = "NIFTY "+str(Exp_Date)+"-"+str(Exp_Mon)+"-"+str(Exp_Year)+" "+str(Type)+" "+str(Strike_Price)
                        Zerodha = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        #Zerodha = "NIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)    #Monthly Expiry
                        IciciExpiry = "20"+str(Exp_Year)+"-"+str(Exp_Mon)+"-"+str(Exp_Date)

                        if Type == "CE":
                            Type = "call"
                        if Type == "PE":
                            Type = "put"

                        Buy_Order(str(symbol.replace("'", "")), str(Token_1), "nifty_hedge", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(Strike_Price), str(Type), IciciExpiry)

                        trade = "INSERT INTO nifty_hedge (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(Token_1.replace("'", ""))+"', 'SHORTSL', '30', '"+str(Option_live_1)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'nifty_hedge')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break

                        
                    if str(datetime.datetime.now()) > str(data.date())+" 15:10:00.000000":

                        Strike_Price = ''.join(list(Symbol_1)[12:17])
                        Exp_Date = ''.join(list(Symbol_1)[5:7])
                        Exp_Mon = ''.join(list(Symbol_1)[7:10])
                        Exp_Year = ''.join(list(Symbol_1)[10:12])
                        Type = ''.join(list(Symbol_1)[17:])

                        print(Strike_Price)
                        print(Exp_Date)
                        print(Exp_Mon)
                        print(Exp_Year)
                        print(Type)

                        symbol = "NIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Strike_Price)+str(Type)
                        
                        if Type == "CE":
                            Type = "CALL"
                        if Type == "PE":
                            Type = "PUT"

                        DhanSymbol = "NIFTY "+str(Exp_Date)+" "+str(Exp_Mon)+" "+str(Strike_Price)+" "+str(Type)

                        Type = ''.join(list(Symbol_1)[17:])

                        #AliceSymbol = "NIFTY08NOV23C42600"
                        AliceSymbol = "NIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Type[0])+str(Strike_Price)
                        #AliceSymbol = "NIFTY "+str(Exp_Mon)+" "+str(strikeprice)+" "+str(Type)
                        UpstoxSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        #UpstoxSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)   #Monthly Expiry
                        FyresSymbol = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        MotilalSymbol = "NIFTY "+str(Exp_Date)+"-"+str(Exp_Mon)+"-"+str(Exp_Year)+" "+str(Type)+" "+str(Strike_Price)
                        Zerodha = "NIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                        #Zerodha = "NIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)    #Monthly Expiry
                        IciciExpiry = "20"+str(Exp_Year)+"-"+str(Exp_Mon)+"-"+str(Exp_Date)

                        if Type == "CE":
                            Type = "call"
                        if Type == "PE":
                            Type = "put"

                        Buy_Order(str(symbol.replace("'", "")), str(Token_1), "nifty_hedge", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(Strike_Price), str(Type), IciciExpiry)

                        trade = "INSERT INTO nifty_hedge (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(Token_1.replace("'", ""))+"', 'SHORTEXIT', '30', '"+str(Option_live_1)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'nifty_hedge')"
                        mycursor.execute(trade)
                        mydb.commit()

                        exit()


                    else:
                        break
            
            else:
                break