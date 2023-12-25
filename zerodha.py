from kite_trade import *
import pyotp
from conn import *
import datetime
from datetime import date
from time import sleep

def Zrodha_Buy_Order(Api, Api_Secret, Totp, symbol, token, strategy, userid, producttype, quantity):
    api_key = Api
    Secret = Api_Secret

    try:
        Totptoken=pyotp.TOTP(Totp).now()
        print(Totptoken)

        enctoken = get_enctoken(api_key, Secret, Totptoken)
        kite = KiteApp(enctoken=enctoken)

        orderId = kite.place_order(variety=kite.VARIETY_AMO,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=symbol,
                         transaction_type=kite.TRANSACTION_TYPE_BUY,
                         quantity=int(quantity),
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="MoneyMakers Algo")

        print(orderId)
        sleep(1)
        orders = kite.orders()

        for I in range(len(orders)):
            if orders[I].get("order_id") == orderId:
                #print(orders[I])
                Price = orders[I].get("average_price")

        print(Price)

        trade = "INSERT INTO zerodha_orders (Symbol, OrderID, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+str(symbol)+"', '"+str(orderId)+"', '"+str(Price)+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

    except Exception as e:
        print("error")
        pass




def Zerodha_Sell_Order(Api, Api_Secret, Totp, symbol, token, strategy, userid, producttype, quantity):
    api_key = Api
    Secret = Api_Secret

    try:
        Totptoken=pyotp.TOTP(Totp).now()
        print(Totptoken)

        enctoken = get_enctoken(api_key, Secret, Totptoken)
        kite = KiteApp(enctoken=enctoken)

        orderId = kite.place_order(variety=kite.VARIETY_REGULAR,
                         exchange=kite.EXCHANGE_NFO,
                         tradingsymbol=symbol,
                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                         quantity=int(quantity),
                         product=kite.PRODUCT_MIS,
                         order_type=kite.ORDER_TYPE_MARKET,
                         price=None,
                         validity=kite.VALIDITY_DAY,
                         disclosed_quantity=None,
                         trigger_price=None,
                         squareoff=None,
                         stoploss=None,
                         trailing_stoploss=None,
                         tag="MoneyMakers Algo")

        print(orderId)
        sleep(1)
        orders = kite.orders()

        for I in range(len(orders)):
            if orders[I].get("order_id") == orderId:
                #print(orders[I])
                Price = orders[I].get("average_price")

        print(Price)

        trade = "INSERT INTO zerodha_orders (Symbol, OrderID, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+str(symbol)+"', '"+str(orderId)+"', '"+str(Price)+"', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

        
    except Exception as e:
        print("None")
        pass
        