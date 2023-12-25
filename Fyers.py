from fyers_apiv3 import fyersModel
from conn import *
import datetime
from datetime import date



def Fyers_Buy_Order(client_id, client_secret, code, FyresSymbol, userid, strategy, product, quantity):
    print(client_id+" "+client_secret+" "+code+" "+FyresSymbol+" "+userid+" "+strategy+" "+product+" "+quantity)
    client_id = client_id
    redirect_uri= "https://moneymakers-algo.com/broker.php" 
    secret_key = client_secret 
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample" 

    try:
        appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
        generateTokenUrl = appSession.generate_authcode()
        #print((generateTokenUrl))  

        auth_code = code
        appSession.set_token(auth_code)
        response = appSession.generate_token()
        access_token = ""

        user = 'select * from api where UserID="'+userid+'"'
        mycursor.execute(user)
        tokenresult = mycursor.fetchall()


        if tokenresult[0][4] != "None":
            access_token = tokenresult[0][4]
        else:
            try: 
                access_token = response["access_token"]
                update = "update api set Client_ID='"+str(access_token)+"' where UserID='"+userid+"'"
                mycursor.execute(update)
                mydb.commit()
            except Exception as e:
                print(e,response)
                pass

            
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

        try:
            data = {
                "symbol":"NSE:"+FyresSymbol,
                "qty":int(quantity),
                "type":2,
                "side":1,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
            }
            response = fyers.place_order(data=data)
            order_id = response["id"]
            trade = "INSERT INTO fyres_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+FyresSymbol+"', '"+str(order_id)+"', '0', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
            mycursor.execute(trade)
            mydb.commit()

            update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
            mycursor.execute(update)
            mydb.commit()
        except:
            pass
    
    except:
            pass

    
    




def Fyers_Sell_Order(client_id, client_secret, code, FyresSymbol, userid, strategy, product, quantity): 

    client_id = client_id
    redirect_uri= "https://moneymakers-algo.com/broker.php" 
    secret_key = client_secret 
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample" 
    
    appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
    generateTokenUrl = appSession.generate_authcode()
    #print((generateTokenUrl))  
    
    auth_code = code
    appSession.set_token(auth_code)
    response = appSession.generate_token()
    access_token = ""
    
    user = 'select * from api where UserID="'+userid+'"'
    mycursor.execute(user)
    tokenresult = mycursor.fetchall()

    
    if tokenresult[0][4] != "None":
        access_token = tokenresult[0][4]
    else:
        try: 
            access_token = response["access_token"]
            update = "update api set Client_ID='"+str(access_token)+"' where UserID='"+userid+"'"
            mycursor.execute(update)
            mydb.commit()
        except Exception as e:
            print(e,response)
            pass

    
    # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")
    
    data = {
        "symbol":"NSE:"+FyresSymbol,
        "qty":int(quantity),
        "type":2,
        "side":-1,
        "productType":"INTRADAY",
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":False,
    }
    response = fyers.place_order(data=data)
    order_id = response["id"]

    trade = "INSERT INTO fyres_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+FyresSymbol+"', '"+str(order_id)+"', '0', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()

    update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
    mycursor.execute(update)
    mydb.commit()
    
    





def Fyers_Buy_Order_Delivery(client_id, client_secret, code, FyresSymbol, userid, strategy, product, quantity):
    print(client_id+" "+client_secret+" "+code+" "+FyresSymbol+" "+userid+" "+strategy+" "+product+" "+quantity)
    client_id = client_id
    redirect_uri= "https://moneymakers-algo.com/broker.php" 
    secret_key = client_secret 
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample" 

    try:
        appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
        generateTokenUrl = appSession.generate_authcode()
        #print((generateTokenUrl))  

        auth_code = code
        appSession.set_token(auth_code)
        response = appSession.generate_token()
        access_token = ""

        user = 'select * from api where UserID="'+userid+'"'
        mycursor.execute(user)
        tokenresult = mycursor.fetchall()


        if tokenresult[0][4] != "None":
            access_token = tokenresult[0][4]
        else:
            try: 
                access_token = response["access_token"]
                update = "update api set Client_ID='"+str(access_token)+"' where UserID='"+userid+"'"
                mycursor.execute(update)
                mydb.commit()
            except Exception as e:
                print(e,response)
                pass

            
        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

        try:
            data = {
                "symbol":"NSE:"+FyresSymbol,
                "qty":int(quantity),
                "type":2,
                "side":1,
                "productType":"MARGIN",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
            }
            response = fyers.place_order(data=data)
            order_id = response["id"]
            trade = "INSERT INTO fyres_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+FyresSymbol+"', '"+str(order_id)+"', '0', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
            mycursor.execute(trade)
            mydb.commit()

            update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
            mycursor.execute(update)
            mydb.commit()
        except:
            pass
    
    except:
            pass






def Fyers_Sell_Order_Delivery(client_id, client_secret, code, FyresSymbol, userid, strategy, product, quantity): 

    client_id = client_id
    redirect_uri= "https://moneymakers-algo.com/broker.php" 
    secret_key = client_secret 
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample" 
    
    appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
    generateTokenUrl = appSession.generate_authcode()
    #print((generateTokenUrl))  
    
    auth_code = code
    appSession.set_token(auth_code)
    response = appSession.generate_token()
    access_token = ""
    
    user = 'select * from api where UserID="'+userid+'"'
    mycursor.execute(user)
    tokenresult = mycursor.fetchall()

    
    if tokenresult[0][4] != "None":
        access_token = tokenresult[0][4]
    else:
        try: 
            access_token = response["access_token"]
            update = "update api set Client_ID='"+str(access_token)+"' where UserID='"+userid+"'"
            mycursor.execute(update)
            mydb.commit()
        except Exception as e:
            print(e,response)
            pass

    
    # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")
    
    data = {
        "symbol":"NSE:"+FyresSymbol,
        "qty":int(quantity),
        "type":2,
        "side":-1,
        "productType":"MARGIN",
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":False,
    }
    response = fyers.place_order(data=data)
    order_id = response["id"]

    trade = "INSERT INTO fyres_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+FyresSymbol+"', '"+str(order_id)+"', '0', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()

    update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
    mycursor.execute(update)
    mydb.commit()
