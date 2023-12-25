import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *
from Tokens import *


def Yes_Close():
    file_path = './CSV_Files/bnf_5m.csv'

    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path)
    
    data['DateTime'] = pd.to_datetime(data['DateTime'])

    # Get current datetime
    current_datetime = datetime.datetime.now()

    # Calculate datetime for yesterday
    yesterday_datetime = current_datetime - timedelta(days=1)
    
    # Format yesterday's datetime as desired
    yesterday_datetime = yesterday_datetime.strftime('%Y-%m-%d')
    target_datetime_str = str(yesterday_datetime)+' 15:30:00'
    print(target_datetime_str)
    target_datetime = pd.to_datetime(target_datetime_str)

    # Filter data based on the target DateTime
    filtered_data = data[data['DateTime'] == target_datetime]
    
    # If the target DateTime has only one corresponding entry, you can directly access the Close price
    if len(filtered_data) == 1:
        close_price = filtered_data['Close'].values[0]
        return close_price
    else:
        return None



while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:15:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:15:00.000000":

        while True:

            apikey = "ef1zHKeB"
            secretkey = "1e503c5f-25f9-4af2-b9e6-75fbd4e50445"
            user_id = "VJVG1165"
            password = "7788"
            totp = "MJNJ2CWLVLTJ646R4CK6OOEAME"

            GetExpiry_Date = Expiry_Date()
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)
            Yesterday_Close = Yes_Close()

            if Idx_Live == None:
                break
            else:
                pass

            print("Idx live: "+str(Idx_Live))
            print(datetime.datetime.now())
            sleep(1)

            sql = "SELECT * FROM bnf_expiry ORDER BY DateTime DESC"
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
                
                if int(str(Idx_Live)[3:5]) <= 50:
                    strikeprice = int(str(Idx_Live)[:3]+"00")
                if int(str(Idx_Live)[3:5]) >= 51:
                    strikeprice = int(float(str(Idx_Live)[:3]+"00")+100)


                if str(datetime.datetime.now()) >= str(data.date())+" 15:15:00.000000":
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice+300)+"CE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice+300)+" CALL"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"C"+str(strikeprice+300)
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice+300)+"CE"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice)+"CE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice+300)+"CE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" CE "+str(strikeprice+300)

                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice+300)+"CE"
                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice+300)+"CE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+str(ExpiryDate)


                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    print(tokenresult)
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "bnf_expiry_ce", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice+300), "call", IciciExpiry)

                    trade = "INSERT INTO bnf_expiry (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'bnf_expiry')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(strikeprice-300)+"PE"
                    DhanSymbol = "BANKNIFTY "+str(ExpiryDate)+" "+str(ExpiryMonth)+" "+str(strikeprice-300)+" PUT"
                    AliceSymbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"P"+str(strikeprice-300)
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice-300)+"PE"
                    #UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice-300)+"PE"   #Monthly Expiry
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice-300)+"PE"
                    MotilalSymbol = "BANKNIFTY "+str(ExpiryDate)+"-"+str(ExpiryMonth)+"-20"+str(ExpiryYear)+" PE "+str(strikeprice-300)

                    Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth[0])+str(ExpiryDate)+str(strikeprice-300)+"PE"
                    #Zerodha = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+str(strikeprice-300)+"PE"    #Monthly Expiry
                    IciciExpiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+str(ExpiryDate)


                    #token = 'select token from instruments where symbol="'+symbol+'"'
                    #mycursor.execute(token)
                    tokenresult = Angel_Data(symbol)
                    
                    option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))
                    #str(tokenresult[0].replace("'", ""))
                    Buy_Order(str(symbol.replace("'", "")), str(tokenresult), "bnf_expiry_pe", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, str(strikeprice-300), "put", IciciExpiry)

                    trade = "INSERT INTO bnf_expiry (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'bnf_expiry')"
                    mycursor.execute(trade)
                    mydb.commit()

                    exit()

                else:
                    break

            

            if Position == "1":
                print("IDX Live: "+str(Idx_Live))
                print("Yesterday_Close: "+str(Yesterday_Close))
                print('Difference: '+str(float(Idx_Live)-float(Yesterday_Close)))

                if float(Idx_Live)-float(Yesterday_Close) >= 120 or float(Idx_Live)-float(Yesterday_Close) <= -120:
                    sql = "SELECT * FROM bnf_expiry WHERE Token IN ( SELECT Token FROM bnf_expiry WHERE Type = 'BUY' GROUP BY Token HAVING COUNT(*) = 1 ) AND Token NOT IN ( SELECT Token FROM bnf_expiry WHERE Type = 'SELL' );"
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

                        if str(datetime.datetime.now()) <= str(data.date())+" 09:45:00.000000":
                            #BANKNIFTY22NOV2343800CE
                            Strike_Price = ''.join(list(Symbol_1)[16:21])
                            Exp_Date = ''.join(list(Symbol_1)[9:11])
                            Exp_Mon = ''.join(list(Symbol_1)[11:14])
                            Exp_Year = ''.join(list(Symbol_1)[14:16])
                            Type = ''.join(list(Symbol_1)[21:])


                            symbol = "BANKNIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Strike_Price)+str(Type)

                            if Type == "CE":
                                Type = "CALL"
                            if Type == "PE":
                                Type = "PUT"

                            DhanSymbol = "BANKNIFTY "+str(Exp_Date)+" "+str(Exp_Mon)+" "+str(Strike_Price)+" "+str(Type)

                            Type = ''.join(list(Symbol_1)[21:])
                            #AliceSymbol = "BANKNIFTY08NOV23C42600"
                            AliceSymbol = "BANKNIFTY"+str(Exp_Date)+str(Exp_Mon)+str(Exp_Year)+str(Type[0])+str(Strike_Price)
                            #AliceSymbol = "BANKNIFTY "+str(Exp_Mon)+" "+str(strikeprice)+" "+str(Type)
                            UpstoxSymbol = "BANKNIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                            #UpstoxSymbol = "BANKNIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)   #Monthly Expiry
                            FyresSymbol = "BANKNIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                            MotilalSymbol = "BANKNIFTY "+str(Exp_Date)+"-"+str(Exp_Mon)+"-"+str(Exp_Year)+" "+str(Type)+" "+str(Strike_Price)
                            Zerodha = "BANKNIFTY"+str(Exp_Year)+str(Exp_Mon[0])+str(Exp_Date)+str(Strike_Price)+str(Type)
                            #Zerodha = "BANKNIFTY"+str(Exp_Year)+str(Exp_Mon)+str(strikeprice)+str(Type)    #Monthly Expiry
                            ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(Expiry_Date)


                            Sell_Order(symbol, Token_1, "bnf_expiry")
                            trade = "INSERT INTO bnf_expiry (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy) values ('"+str(symbol.replace("'", ""))+"', '"+str(Token_1.replace("'", ""))+"', 'SELL', '30', '"+str(Option_live_1)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'bnf_expiry')"
                            mycursor.execute(trade)
                            mydb.commit()

                            exit()
                
                else:
                    break