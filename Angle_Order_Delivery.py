from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
from conn import *
import datetime
from datetime import date
from time import sleep




def Angle_Buy_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid, producttype, quantity):
    print(producttype)
    #producttype = "INTRADAY"
    clientId = ClientID
    api_key = Api
    #quantity = 30
    pwd = Password
    smartApi = SmartConnect(api_key)
    # login api call
    print(symbol+" "+token+" "+strategy+" "+userid)

    try:
        Totptoken = Totp
        totp=pyotp.TOTP(Totptoken).now()
        data = smartApi.generateSession(clientId, pwd, totp)
        # print(data)
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']

        # fetch the feedtoken
        feedToken = smartApi.getfeedToken()

        # fetch User Profile
        res = smartApi.getProfile(refreshToken)
        smartApi.generateToken(refreshToken)
        res=res['data']['exchanges']

        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": "BUY",
            "exchange": "NFO",
            "ordertype": "MARKET",
            "producttype": "CARRYFORWARD",
            "duration": "DAY",
            "price": "0",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": quantity
            }

        orderId=smartApi.placeOrder(orderparams)
        print(orderId)

        orders = smartApi.orderBook()

        for I in range(len(orders.get("data"))):
            if orders.get("data")[I].get("orderid") == orderId:
                #print(orders.get("data")[I].get("averageprice"))
                Price = orders.get("data")[I].get("averageprice")

        print(Price)

        trade = "INSERT INTO orders (Symbol, Token, OrderID, Quantity, UserID, Type, DateTime, Strategy, Price) values ('"+symbol+"', '"+token+"', '"+orderId+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"', '"+str(Price)+"')"
        mycursor.execute(trade)
        mydb.commit()
        
        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()


    except Exception as e:
        print("error")
        pass







def Angle_Sell_Order_Delivery(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid, producttype, quantity):
    clientId = ClientID
    api_key = Api
    pwd = Password
    smartApi = SmartConnect(api_key)
    # login api call
    print(symbol+" "+token+" "+strategy+" "+userid)


    try:
        tokenotp = Totp
        totp=pyotp.TOTP(tokenotp).now()
        data = smartApi.generateSession(clientId, pwd, totp)
        # print(data)
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        
        # fetch the feedtoken
        feedToken = smartApi.getfeedToken()
        
        # fetch User Profile
        res = smartApi.getProfile(refreshToken)
        smartApi.generateToken(refreshToken)
        res=res['data']['exchanges']
    
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": "SELL",
            "exchange": "NFO",
            "ordertype": "MARKET",
            "producttype": "CARRYFORWARD",
            "duration": "DAY",
            "price": "0",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": quantity
            }
            
        orderId=smartApi.placeOrder(orderparams)
        print(orderId)

        orders = smartApi.orderBook()

        for I in range(len(orders.get("data"))):
            if orders.get("data")[I].get("orderid") == orderId:
                #print(orders.get("data")[I].get("averageprice"))
                Price = orders.get("data")[I].get("averageprice")

        print(Price)

        trade = "INSERT INTO orders (Symbol, Token, OrderID, Quantity, UserID, Type, DateTime, Strategy, Price) values ('"+symbol+"', '"+token+"', '"+orderId+"', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"', '"+str(Price)+"')"
        mycursor.execute(trade)
        mydb.commit()
        
        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

    except Exception as e:
        print("None")
        pass
