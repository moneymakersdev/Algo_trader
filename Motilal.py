from MOFSLOPENAPI import MOFSLOPENAPI
import pyotp
import ast
from conn import *
import datetime
from datetime import date



def MOFSL_Buy_Order(Api, DOB, Totp, ClientID, Password, symbol, token, strategy, userid, producttype, quantity):
    ApiKey = Api 
    totp=pyotp.TOTP(Totp).now()
    # userid and password is your trading account username and password
    userid = ClientID
    password = Password   
    Two_FA = DOB
    vendorinfo = ClientID
    clientcode = None

    SourceID = "Desktop"            # Web,Desktop
    browsername = "chrome"      
    browserversion = "104"
    totp = totp

    Base_Url = "https://openapi.motilaloswal.com"

    try:
        Mofsl = MOFSLOPENAPI(ApiKey, Base_Url, clientcode, SourceID, browsername, browserversion)
        Mofsl.login(userid, password, Two_FA, totp, vendorinfo)
        Orderinfo = {
            "clientcode":clientcode,      
            "exchange":"NSEFO",
            "symboltoken":token,
            "buyorsell":"BUY",
            "ordertype":"MARKET",
            "producttype":"NORMAL",
            "orderduration":"DAY",
            "price":0,
            "triggerprice":0,
            "quantityinlot":quantity,
            "disclosedquantity":0,
            "amoorder":"N"
        }
        orderId = Mofsl.PlaceOrder(Orderinfo).get('uniqueorderid')
        print(orderId)

        trade = "INSERT INTO mosl_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+symbol+"', '"+token+"', '"+orderId+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

    except:
        print("error")
        pass
    






def MOFSL_Sell_Order(Api, DOB, Totp, ClientID, Password, symbol, token, strategy, userid, producttype, quantity):
    ApiKey = Api 
    totp=pyotp.TOTP(Totp).now()
    # userid and password is your trading account username and password
    userid = ClientID
    password = Password   
    Two_FA = DOB
    vendorinfo = ClientID
    clientcode = None

    SourceID = "Desktop"            # Web,Desktop
    browsername = "chrome"      
    browserversion = "104"
    totp = totp

    Base_Url = "https://openapi.motilaloswal.com"

    try:
        Mofsl = MOFSLOPENAPI(ApiKey, Base_Url, clientcode, SourceID, browsername, browserversion)

        Mofsl.login(userid, password, Two_FA, totp, vendorinfo)

        Orderinfo = {
            "clientcode":clientcode,
            "exchange":"NSEFO",
            "symboltoken":token,
            "buyorsell":"SELL",
            "ordertype":"MARKET",
            "producttype":"NORMAL",
            "orderduration":"DAY",
            "price":0,
            "amoorder":"N",
            "quantityinlot":quantity,
        }

        orderId = Mofsl.PlaceOrder(Orderinfo).get('uniqueorderid')

        print(orderId)

        trade = "INSERT INTO mosl_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+symbol+"', '"+token+"', '"+orderId+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()
    
    
    except Exception as e:
        print("error")
        pass







def MOFSL_Buy_Order_Delivery(Api, DOB, Totp, ClientID, Password, symbol, token, strategy, userid, producttype, quantity):
    ApiKey = Api 
    totp=pyotp.TOTP(Totp).now()
    # userid and password is your trading account username and password
    userid = ClientID
    password = Password   
    Two_FA = DOB
    vendorinfo = ClientID
    clientcode = None

    SourceID = "Desktop"            # Web,Desktop
    browsername = "chrome"      
    browserversion = "104"
    totp = totp

    Base_Url = "https://openapi.motilaloswal.com"

    try:
        Mofsl = MOFSLOPENAPI(ApiKey, Base_Url, clientcode, SourceID, browsername, browserversion)
        Mofsl.login(userid, password, Two_FA, totp, vendorinfo)
        Orderinfo = {
            "clientcode":clientcode,      
            "exchange":"NSEFO",
            "symboltoken":token,
            "buyorsell":"BUY",
            "ordertype":"MARKET",
            "producttype":"DELIVERY",
            "orderduration":"DAY",
            "price":0,
            "triggerprice":0,
            "quantityinlot":quantity,
            "disclosedquantity":0,
            "amoorder":"N"
        }
        orderId = Mofsl.PlaceOrder(Orderinfo).get('uniqueorderid')
        print(orderId)

        trade = "INSERT INTO mosl_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+symbol+"', '"+token+"', '"+orderId+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

    except:
        print("error")
        pass





def MOFSL_Sell_Order_Delivery(Api, DOB, Totp, ClientID, Password, symbol, token, strategy, userid, producttype, quantity):
    ApiKey = Api 
    totp=pyotp.TOTP(Totp).now()
    # userid and password is your trading account username and password
    userid = ClientID
    password = Password   
    Two_FA = DOB
    vendorinfo = ClientID
    clientcode = None

    SourceID = "Desktop"            # Web,Desktop
    browsername = "chrome"      
    browserversion = "104"
    totp = totp

    Base_Url = "https://openapi.motilaloswal.com"

    try:
        Mofsl = MOFSLOPENAPI(ApiKey, Base_Url, clientcode, SourceID, browsername, browserversion)

        Mofsl.login(userid, password, Two_FA, totp, vendorinfo)

        Orderinfo = {
            "clientcode":clientcode,
            "exchange":"NSEFO",
            "symboltoken":token,
            "buyorsell":"SELL",
            "ordertype":"MARKET",
            "producttype":"DELIVERY",
            "orderduration":"DAY",
            "price":0,
            "amoorder":"N",
            "quantityinlot":quantity,
        }

        orderId = Mofsl.PlaceOrder(Orderinfo).get('uniqueorderid')

        print(orderId)

        trade = "INSERT INTO mosl_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+symbol+"', '"+token+"', '"+orderId+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()
    
    
    except Exception as e:
        print("error")
        pass
