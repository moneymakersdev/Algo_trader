from conn import *
from Angle_Order import *
from Dhan_Order import *
from AliceBlue import *
from Upstox import *
from Fyers import *
from Tokens import *
from Motilal import *
from zerodha import *
from Icici_Order import *
from place import *
from Expiry_Date import *
from zerodha_delivery import *
from Angle_Order_Delivery import *
from Upstox_Delivery import *



def Buy_Order(symbol, token, strategy, DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, ZerodhaSymbol, IciciStrike, Icicitypes, IciciExpiry):
    USerID = 'select UserID, Qty from running_bots where Script="'+strategy+'" and Orders="0"'
    mycursor.execute(USerID)
    USerIDresult = mycursor.fetchall()
    
    for userid in USerIDresult:
        if userid[0] != []:
            user = 'select * from api where UserID="'+userid[0]+'"'
            mycursor.execute(user)
            tokenresult = mycursor.fetchall()
            
            if tokenresult != []:
                Broker = tokenresult[0][6].replace(" ", "")
                Lot = Angle_Lotsize(symbol)

                if Broker == "ANGEL":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    ClientID = tokenresult[0][4].replace(" ", "")
                    Password = tokenresult[0][5].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    print(symbol+" "+token+" "+strategy+" "+DhanSymbol+" "+AliceSymbol+" "+UpstoxSymbol+" "+FyresSymbol+" "+MotilalSymbol+" "+ZerodhaSymbol)
                    print(Api+" "+Api_Secret+" "+Totp+" "+ClientID+" "+Password+" "+symbol+" "+str(token)+" "+strategy+" "+str(userid[0])+" "+ "INTRADAY"+" "+str(Qty))

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Angle_Buy_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "CARRYFORWARD", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Angle_Buy_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "CARRYFORWARD", Qty)
                    else:
                        Angle_Buy_Order(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "INTRADAY", Qty)
                        #place(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "INTRADAY", Qty)


                if Broker == "DHAN":
                    DhanSymbolToken = Dhan_Data(DhanSymbol)

                    UserID = tokenresult[0][1].replace(" ", "")
                    Access_Token = tokenresult[0][2].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)


                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Dhan_Buy_Order_Delivery(UserID, Access_Token, DhanSymbol, str(DhanSymbolToken).replace("'", ""), userid[0], strategy, "CNC", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Dhan_Buy_Order_Delivery(UserID, Access_Token, DhanSymbol, str(DhanSymbolToken).replace("'", ""), userid[0], strategy, "CNC", Qty)
                    else:
                        Dhan_Buy_Order(UserID, Access_Token, DhanSymbol, str(DhanSymbolToken).replace("'", ""), userid[0], strategy, "INTRADAY", Qty)


                if Broker == "ALICE":
                    UserID = tokenresult[0][1].replace(" ", "")
                    API = tokenresult[0][2].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    try:
                        if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                            Alice_Buy_Order_Delivery(UserID, API, AliceSymbol, userid[0], strategy, "ProductType.Delivery", Qty)
                        if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                            Alice_Buy_Order_Delivery(UserID, API, AliceSymbol, userid[0], strategy, "ProductType.Delivery", Qty)
                        else:
                            Alice_Buy_Order(UserID, API, AliceSymbol, userid[0], strategy, "ProductType.Intraday", Qty)
                    except:
                        pass

                if Broker == "UPSTOX":
                    #AliceToken = 'select instrument_key from upstox_instrument where tradingsymbol="'+UpstoxSymbol+'"'
                    #mycursor.execute(AliceToken)
                    #UpstoxSymbolToken = mycursor.fetchall()
                    UpstoxSymbolToken = Upstox_Data(str(UpstoxSymbol))
                    Qty = int(userid[1])*int(Lot)
                    print(Qty)
                    try:       
                        #USerIDresult = mycursor.fetchone()
                        Api = tokenresult[0][1].replace(" ", "")
                        Api_Secret = tokenresult[0][2].replace(" ", "")
                        Totp = tokenresult[0][3].replace(" ", "")
                        Token = UpstoxSymbolToken

                        if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                            Upstox_Buy_Order_Delivery(Api, Api_Secret, Totp, Token, userid[0], strategy, "D", str(Qty))
                        if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                            Upstox_Buy_Order_Delivery(Api, Api_Secret, Totp, Token, userid[0], strategy, "D", str(Qty))
                        else:
                            Upstox_Buy_Order(Api, Api_Secret, Totp, Token, userid[0], strategy, "I", str(Qty))

                    except:
                        pass


                if Broker == "FYERS":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Fyers_Buy_Order_Delivery(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "CNC", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Fyers_Buy_Order_Delivery(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "CNC", Qty)
                    else:
                        Fyers_Buy_Order(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "INTRADAY", Qty)                    


                if Broker == "MOFSL":
                    Api = tokenresult[0][1].replace(" ", "")
                    DOB = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    ClientID = tokenresult[0][4].replace(" ", "")
                    Password = tokenresult[0][5].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)
                    try:
                        Token = MOSL_Data(MotilalSymbol)
                    except:
                        pass

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        MOFSL_Buy_Order_Delivery(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Delivery", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        MOFSL_Buy_Order_Delivery(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Delivery", Qty)
                    else:
                        MOFSL_Buy_Order(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Normal", Qty)             



                if Broker == "ZERODHA":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)


                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Zrodha_Buy_Order_NRML(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_NRML", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Zrodha_Buy_Order_NRML(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_NRML", Qty)
                    else:
                        Zrodha_Buy_Order(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_MIS", Qty)


                if Broker == "ICICI":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Icici_Buy_Order(Api, Api_Secret, Totp, IciciStrike, Icicitypes, IciciExpiry, userid, strategy, Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Icici_Buy_Order(Api, Api_Secret, Totp, IciciStrike, Icicitypes, IciciExpiry, userid, strategy, Qty)
                    else:
                        Icici_Buy_Order(Api, Api_Secret, Totp, IciciStrike, Icicitypes, IciciExpiry, userid, strategy, Qty)


            else:
                pass

        else:
            pass




def Sell_Order(symbol, Token, strategy):
    
    token = 'select UserID, Qty from running_bots where Orders="1" and Script="'+strategy+'"'
    mycursor.execute(token)
    tokenresult = mycursor.fetchall()
    print(tokenresult)

    for userid in tokenresult:
        user = 'select * from api where UserID="'+userid[0]+'"'
        mycursor.execute(user)
        tokenresult = mycursor.fetchall()
        

        if tokenresult != []:
            Broker = tokenresult[0][6].replace(" ", "")
            Lot = Angle_Lotsize(symbol)

            if Broker == "ANGEL":

                Api = tokenresult[0][1].replace(" ", "")
                Api_Secret = tokenresult[0][2].replace(" ", "")
                Totp = tokenresult[0][3].replace(" ", "")
                ClientID = tokenresult[0][4].replace(" ", "")
                Password = tokenresult[0][5].replace(" ", "")
                Qty = int(userid[1])*int(Lot)

                if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                    Angle_Sell_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, Token, strategy, userid[0], "CARRYFORWARD", Qty)
                if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                    Angle_Sell_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, Token, strategy, userid[0], "CARRYFORWARD", Qty)
                else:
                    Angle_Sell_Order(Api, Api_Secret, Totp, ClientID, Password, symbol, Token, strategy, userid[0], "INTRADAY", Qty)


            if Broker == "DHAN":

                sql = "select * from dhan_orders  ORDER BY DateTime DESC"
                mycursor.execute(sql)
                DhanTrades = mycursor.fetchone()

                DhanSymbol = DhanTrades[0]
                DhanSymbolToken = DhanTrades[1]
                Qty = int(userid[1])*int(Lot)

                user = 'select * from api where UserID="'+userid[0]+'"'
                mycursor.execute(user)
                tokenresult = mycursor.fetchall()
                UserID = tokenresult[0][1].replace(" ", "")
                Access_Token = tokenresult[0][2].replace(" ", "")

                if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                    Dhan_Sell_Order_Delivery(UserID, Access_Token, DhanSymbol, DhanSymbolToken, userid[0], strategy, "CNC", Qty)
                if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                    Dhan_Sell_Order_Delivery(UserID, Access_Token, DhanSymbol, DhanSymbolToken, userid[0], strategy, "CNC", Qty)
                else:
                    Dhan_Sell_Order(UserID, Access_Token, DhanSymbol, DhanSymbolToken, userid[0], strategy, "INTRA", Qty)



            if Broker == "ALICE":

                sql = "select * from alice_orders  ORDER BY DateTime DESC"
                mycursor.execute(sql)
                AliceTrades = mycursor.fetchone()
                Qty = int(userid[1])*int(Lot)

                AliceSymbol = AliceTrades[0]

                user = 'select * from api where UserID="'+userid[0]+'"'
                mycursor.execute(user)
                tokenresult = mycursor.fetchall()
                UserID = tokenresult[0][1].replace(" ", "")
                Access_Token = tokenresult[0][2].replace(" ", "")

                if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                    Alice_Sell_Order_Delivery(UserID, Access_Token, AliceSymbol, userid[0], strategy, "ProductType.Delivery", Qty)
                if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                    Alice_Sell_Order_Delivery(UserID, Access_Token, AliceSymbol, userid[0], strategy, "ProductType.Delivery", Qty)
                else:
                    Alice_Sell_Order(UserID, Access_Token, AliceSymbol, userid[0], strategy, "ProductType.Intraday", Qty)



            if Broker == "UPSTOX":

                sql = "select * from upstox_orders  ORDER BY DateTime DESC"
                mycursor.execute(sql)
                UpstoxTrades = mycursor.fetchone()
                Qty = int(userid[1])*int(Lot)

                try:
                    UpstoxSymbol = UpstoxTrades[0]

                    user = 'select * from api where UserID="'+userid[0]+'"'
                    mycursor.execute(user)
                    tokenresult = mycursor.fetchall()
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Upstox_Sell_Order_Delivery(Api, Api_Secret, Totp, UpstoxSymbol, userid[0], strategy, "D", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Upstox_Sell_Order_Delivery(Api, Api_Secret, Totp, UpstoxSymbol, userid[0], strategy, "D", Qty)
                    else:
                        Upstox_Sell_Order(Api, Api_Secret, Totp, UpstoxSymbol, userid[0], strategy, "I", Qty)
                except:
                    pass



            if Broker == "FYERS":
                sql = "select * from fyres_orders  ORDER BY DateTime DESC"
                mycursor.execute(sql)
                UpstoxTrades = mycursor.fetchone()
                Qty = int(userid[1])*int(Lot)

                FyresSymbol = UpstoxTrades[0]

                user = 'select * from api where UserID="'+userid[0]+'"'
                mycursor.execute(user)
                tokenresult = mycursor.fetchall()
                Api = tokenresult[0][1].replace(" ", "")
                Api_Secret = tokenresult[0][2].replace(" ", "")
                Totp = tokenresult[0][3].replace(" ", "")

                if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                    Fyers_Sell_Order_Delivery(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "CNC", Qty)
                if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                    Fyers_Sell_Order_Delivery(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "CNC", Qty)
                else:
                    Fyers_Sell_Order(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "INTRADAY", Qty)



            if Broker == "MOFSL":
                sql = "select * from mosl_orders  ORDER BY DateTime DESC"
                mycursor.execute(sql)
                MofslTrades = mycursor.fetchone()

                MotilalSymbol = MofslTrades[0]
                Token = MofslTrades[1]

                Api = tokenresult[0][1].replace(" ", "")
                DOB = tokenresult[0][2].replace(" ", "")
                Totp = tokenresult[0][3].replace(" ", "")
                ClientID = tokenresult[0][4].replace(" ", "")
                Password = tokenresult[0][5].replace(" ", "")
                Qty = int(userid[1])*int(Lot)

                if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                    MOFSL_Sell_Order_Delivery(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Delivery", Qty)
                if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                    MOFSL_Sell_Order_Delivery(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Delivery", Qty)
                else:
                    MOFSL_Sell_Order(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Normal", Qty)             


            if Broker == "ZERODHA":
                sql = "select * from zerodha_orders  ORDER BY DateTime DESC"
                mycursor.execute(sql)
                ZerodhaTrades = mycursor.fetchone()

                ZerodhaSymbol = ZerodhaTrades[0]
               
                Api = tokenresult[0][1].replace(" ", "")
                Api_Secret = tokenresult[0][2].replace(" ", "")
                Totp = tokenresult[0][3].replace(" ", "")
                Qty = int(userid[1])*int(Lot)

                if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                    Zerodha_Sell_Order_NRML(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_NRML", Qty)
                if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                    Zerodha_Sell_Order_NRML(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_NRML", Qty)
                else:
                    Zerodha_Sell_Order(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_MIS", Qty)


            if Broker == "ICICI":
                try:
                    expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

                    GetExpiry_Date = Expiry_Date()
                    ExpiryYear = str(GetExpiry_Date[0])[2:]
                    ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                    ExpiryDate = GetExpiry_Date[2]

                    Expiry = str(ExpiryYear)+"-"+str(ExpiryMonth)+"-"+str(ExpiryDate)

                    sql = "select * from icici_orders  ORDER BY DateTime DESC"
                    mycursor.execute(sql)
                    ZerodhaTrades = mycursor.fetchone()

                    types = ZerodhaTrades[1]
                    strikeprice = ZerodhaTrades[2]

                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    Icici_Sell_Order(Api, Api_Secret, Totp, strikeprice, types, Expiry, userid[0], strategy, Qty)
                except:
                    pass
        else:
            pass






def Short_Order(symbol, token, strategy, DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, ZerodhaSymbol, IciciStrike, Icicitypes, IciciExpiry):
    USerID = 'select UserID, Qty from running_bots where Script="'+strategy+'" and Orders="0"'
    mycursor.execute(USerID)
    USerIDresult = mycursor.fetchall()
    
    for userid in USerIDresult:
        if userid[0] != []:
            user = 'select * from api where UserID="'+userid[0]+'"'
            mycursor.execute(user)
            tokenresult = mycursor.fetchall()
            
            if tokenresult != []:
                Broker = tokenresult[0][6].replace(" ", "")
                Lot = Angle_Lotsize(symbol)

                if Broker == "ANGEL":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    ClientID = tokenresult[0][4].replace(" ", "")
                    Password = tokenresult[0][5].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Angle_Sell_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "CARRYFORWARD", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Angle_Sell_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "CARRYFORWARD", Qty)
                    else:
                        Angle_Sell_Order(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "INTRADAY", Qty)


                if Broker == "DHAN":
                    #DhanToken = 'select SEM_SMST_SECURITY_ID from dhan_instruments where SEM_CUSTOM_SYMBOL="'+DhanSymbol+'"'
                    #mycursor.execute(DhanToken)
                    #DhanSymbolToken = mycursor.fetchall()
                    DhanSymbolToken = Dhan_Data(DhanSymbol)

                    #USerIDresult = mycursor.fetchone()
                    UserID = tokenresult[0][1].replace(" ", "")
                    Access_Token = tokenresult[0][2].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Dhan_Sell_Order_Delivery(UserID, Access_Token, DhanSymbol, DhanSymbolToken.replace("'", ""), userid[0], strategy, "CNC", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Dhan_Sell_Order_Delivery(UserID, Access_Token, DhanSymbol, DhanSymbolToken.replace("'", ""), userid[0], strategy, "CNC", Qty)
                    else:
                        Dhan_Sell_Order(UserID, Access_Token, DhanSymbol, DhanSymbolToken.replace("'", ""), userid[0], strategy, "INTRA", Qty)


                if Broker == "ALICE":
                    #AliceToken = 'select Trading_Symbol from alice_instruments where Formatted_Ins_Name="'+AliceSymbol+'"'
                    #mycursor.execute(AliceToken)
                    #AliceSymbolToken = mycursor.fetchall()

                    #USerIDresult = mycursor.fetchone()
                    UserID = tokenresult[0][1].replace(" ", "")
                    API = tokenresult[0][2].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Alice_Sell_Order_Delivery(UserID, API, AliceSymbol.replace("'", ""), userid[0], strategy, "ProductType.Delivery", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Alice_Sell_Order_Delivery(UserID, API, AliceSymbol.replace("'", ""), userid[0], strategy, "ProductType.Delivery", Qty)
                    else:
                        Alice_Sell_Order(UserID, API, AliceSymbol.replace("'", ""), userid[0], strategy, "ProductType.Intraday", Qty)


                if Broker == "UPSTOX":
                    AliceToken = 'select instrument_key from upstox_instrument where tradingsymbol="'+UpstoxSymbol+'"'
                    mycursor.execute(AliceToken)
                    UpstoxSymbolToken = mycursor.fetchall()
                    Qty = int(userid[1])*int(Lot)

                    #print(UpstoxSymbolToken[0][0])

                    #USerIDresult = mycursor.fetchone()
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Token = UpstoxSymbolToken[0][0].replace(" ", "")

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Upstox_Sell_Order_Delivery(Api, Api_Secret, Totp, Token, userid[0], strategy, "D", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Upstox_Sell_Order_Delivery(Api, Api_Secret, Totp, Token, userid[0], strategy, "D", Qty)
                    else:
                        Upstox_Sell_Order(Api, Api_Secret, Totp, Token, userid[0], strategy, "I", Qty)


                if Broker == "FYERS":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Fyers_Sell_Order_Delivery(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "CNC", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Fyers_Sell_Order_Delivery(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "CNC", Qty)
                    else:
                        Fyers_Sell_Order(Api, Api_Secret, Totp, FyresSymbol, userid[0], strategy, "INTRADAY", Qty)                    



                if Broker == "MOFSL":
                    Api = tokenresult[0][1].replace(" ", "")
                    DOB = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    ClientID = tokenresult[0][4].replace(" ", "")
                    Password = tokenresult[0][5].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)
                    Token = MOSL_Data(MotilalSymbol)

                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        MOFSL_Sell_Order_Delivery(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Delivery", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        MOFSL_Sell_Order_Delivery(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Delivery", Qty)
                    else:
                        MOFSL_Sell_Order(Api.replace(" ", ""), DOB, Totp, ClientID, Password, MotilalSymbol, Token, strategy, userid[0], "Normal", Qty)             



                if Broker == "ZERODHA":
                    Api = tokenresult[0][1].replace(" ", "")
                    Api_Secret = tokenresult[0][2].replace(" ", "")
                    Totp = tokenresult[0][3].replace(" ", "")
                    Qty = int(userid[1])*int(Lot)


                    if strategy == "bnf_expiry_ce" and strategy == "bnf_expiry_pe":
                        Zerodha_Sell_Order_NRML(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_NRML", Qty)
                    if strategy == "nifty_expiry_ce" and strategy == "nifty_expiry_pe":
                        Zerodha_Sell_Order_NRML(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_NRML", Qty)
                    else:
                        Zerodha_Sell_Order(Api, Api_Secret, Totp, ZerodhaSymbol, token, strategy, userid[0], "kite.PRODUCT_MIS", Qty)


            else:
                pass

        else:
            pass
