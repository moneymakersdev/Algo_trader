from conn import *
from Option_Chain import *
from Place_Order import *
from Expiry_Date import *




while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:30:10.000000":
        print("Market is Closed")
    if str(datetime.datetime.now()) > str(data.date())+" 09:30:10.000000":

        while True:

            CE_Delta = Delta_CE(10,100,bnf_nearest,url_bnf)
            PE_Delta = Delta_PE(10,100,bnf_nearest,url_bnf)


            CE_Delta_Str_Price = str(CE_Delta[0])
            CE_Delta_Value = "%.2f" % round(CE_Delta[1], 2)

            PE_Delta_Str_Price = str(PE_Delta[0])
            PE_Delta_Value = "%.2f" % round(PE_Delta[1], 2)

            apikey = "h6jSmhjF"
            secretkey = "8d9b5028-218e-4bfb-9e44-c8c52d3e2dce"
            user_id = "VJVG1338"
            password = "0107"
            totp = "VLSNN2YQT2TEBDDVFCVK34KZAE"
            
            GetExpiry_Date = Expiry_Date()
            Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)

            print("Idx live: "+str(Idx_Live))

            print(datetime.datetime.now())

            sql = "select * from delta_trades ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print(Position)


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                ce_strikeprice = int(float(CE_Delta_Str_Price))
                Pe_strikeprice = int(float(PE_Delta_Str_Price))

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = "0"+str(GetExpiry_Date[2])

                ce_symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(ce_strikeprice)+"CE"
                pe_symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(Pe_strikeprice)+"PE"

                print(ce_symbol)
                print(pe_symbol)

                token = 'select token from instruments where symbol="'+ce_symbol+'"'
                mycursor.execute(token)
                ce_tokenresult = mycursor.fetchone()

                print(token)

                token = 'select token from instruments where symbol="'+pe_symbol+'"'
                mycursor.execute(token)
                pe_tokenresult = mycursor.fetchone()

                ce_option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(ce_symbol.replace("'", "")), str(ce_tokenresult.replace("'", "")))
                pe_option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(pe_symbol.replace("'", "")), str(pe_tokenresult.replace("'", "")))

                print(ce_option_live)
                print(pe_option_live)


                #Sell_Order(ce_symbol, ce_tokenresult, "Delta_King")
                #Sell_Order(pe_symbol, pe_tokenresult, "Delta_King")

                trade = "INSERT INTO delta_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(ce_symbol.replace("'", ""))+"', '"+str(ce_tokenresult[0].replace("'", ""))+"', 'SHORT', '30', '"+str(ce_option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                mycursor.execute(trade)
                mydb.commit()

                trade = "INSERT INTO delta_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(pe_symbol.replace("'", ""))+"', '"+str(pe_tokenresult[0].replace("'", ""))+"', 'SHORT', '30', '"+str(pe_option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                mycursor.execute(trade)
                mydb.commit()

                trade = "INSERT INTO delta_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(ce_symbol.replace("'", ""))+"', '"+str(ce_tokenresult[0].replace("'", ""))+"', 'SHORT', '30', '"+str(ce_option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                mycursor.execute(trade)
                mydb.commit()

                trade = "INSERT INTO delta_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(pe_symbol.replace("'", ""))+"', '"+str(pe_tokenresult[0].replace("'", ""))+"', 'SHORT', '30', '"+str(pe_option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                mycursor.execute(trade)
                mydb.commit()

                break

            
            
            if Position == "1":
                sql = "select * from delta_orders where Type='SHORT' ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()

                PE_Entry = myresult[0]
                CE_Entry = myresult[1]

                PE_Symbol = PE_Entry[0]
                CE_Symbol = CE_Entry[0]

                PE_Token = PE_Entry[1]
                CE_Token = CE_Entry[1]

                PE_Price = PE_Entry[4]
                CE_Price = CE_Entry[4]

                ce_option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(CE_Symbol), str(CE_Token))
                pe_option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(PE_Symbol), str(PE_Token))

                print("PE Live: "+str(pe_option_live))
                print("CE Live: "+str(ce_option_live))
                print("PE short: "+str(PE_Price))
                print("CE short: "+str(CE_Price))
                print("PE short SL: "+str((float(PE_Entry[4])*25/100)+float(PE_Entry[4])))
                print("CE short SL: "+str((float(CE_Price)*25/100)+float(CE_Price)))

                print(str(ce_option_live)+" "+str(float(CE_Price)*25/100+float(CE_Price)))
                print(str(pe_option_live)+" "+str(float(PE_Price)*25/100+float(PE_Price)))

                if ce_option_live >= (float(CE_Price)*25/100+float(CE_Price)):
    
                    print((float(PE_Entry[4])*25/100)+float(PE_Entry[4]))
                    #Buy_Order(str(PE_Symbol), str(PE_Token), "Delta_King", None)
                    
                    trade = "delete from delta_orders where Name='"+str(PE_Symbol)+"'"
                    mycursor.execute(trade)
                    mydb.commit()

                    trade = "INSERT INTO delta_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+PE_Symbol+"', '"+str(PE_Token)+"', 'SHORTEXIT', '30', '"+str(ce_option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    Second_Options = Premium_Finder(20,100,bnf_nearest,url_bnf, "CE", ce_option_live)

                    Second_Strike = Second_Options[0].replace("'", "")
                    Second_Price = Second_Options[1]

                    ce_symbol = "'BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(Second_Strike)+"CE'"

                    token = 'select token from instruments where symbol="'+ce_symbol+'"'
                    mycursor.execute(token)
                    ce_tokenresult = mycursor.fetchone()

                    
                    #Sell_Order(ce_symbol, ce_tokenresult, "Delta_King")

                    trade = "INSERT INTO delta_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+ce_symbol+"', '"+str(ce_tokenresult)+"', 'SHORT', '30', '"+str(ce_option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()


                    break


                if pe_option_live >= (float(PE_Price)*25/100+float(PE_Price)):
    
                    print((float(PE_Price)*25/100)+float(PE_Price))
                    #Buy_Order(str(CE_Symbol), str(CE_Token), "Delta_King", None)

                    trade = "delete from delta_orders where Name='"+str(CE_Symbol)+"'"
                    mycursor.execute(trade)
                    mydb.commit()

                    trade = "INSERT INTO delta_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+CE_Symbol+"', '"+str(CE_Token)+"', 'SHORTEXIT', '30', '"+str(pe_option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    Second_Options = Premium_Finder(20,100,bnf_nearest,url_bnf, "PE", pe_option_live)

                    Second_Strike = Second_Options[0].replace("'", "")
                    Second_Price = Second_Options[1]

                    pe_symbol = "'BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+str(Second_Strike)+"PE'"

                    token = 'select token from instruments where symbol="'+ce_symbol+'"'
                    mycursor.execute(token)
                    pe_tokenresult = mycursor.fetchone()


                    #Sell_Order(pe_symbol, pe_tokenresult, "Delta_King")

                    trade = "INSERT INTO delta_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+pe_symbol+"', '"+str(pe_tokenresult)+"', 'SHORT', '30', '"+str(pe_option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()

                    break


                if ce_option_live+50 >= pe_option_live or ce_option_live+50 <= pe_option_live:
                    

                    if pe_option_live <= (float(PE_Price)-float(PE_Price)*25/100):

                        #Buy_Order(str(PE_Symbol), str(PE_Token), "Delta_King", None)

                        trade = "delete from delta_orders where Name='"+str(PE_Symbol)+"'"
                        mycursor.execute(trade)
                        mydb.commit()

                        trade = "INSERT INTO delta_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+PE_Symbol+"', '"+str(PE_Token)+"', 'SHORTEXIT', '30', '"+str(ce_option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()


                    if ce_option_live <= (float(CE_Price)-float(CE_Price)*25/100):

                        #Buy_Order(str(CE_Symbol), str(CE_Token), "Delta_King", None)
                        
                        trade = "delete from delta_orders where Name='"+str(CE_Symbol)+"'"
                        mycursor.execute(trade)
                        mydb.commit()  
    
                        trade = "INSERT INTO delta_trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+CE_Symbol+"', '"+str(CE_Token)+"', 'SHORTEXIT', '30', '"+str(pe_option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()


                    else:
                        break


                    break

                
                else:
                    break

            
            else: 
                break