from dhanhq import dhanhq
from conn import *
import datetime
from datetime import date

def Dhan_Buy_Order(Client_Id, Access_Token, DhanSymbol, DhanSymbolToken, userid, strategy, product_type, quantity):
    dhan = dhanhq(Client_Id,  Access_Token)
    #print(DhanSymbolToken)

    try:
        Order = dhan.place_order(security_id=DhanSymbolToken,
            exchange_segment=dhan.FNO,
            transaction_type=dhan.BUY,
            quantity=quantity,
            validity=dhan.DAY,
            order_type=dhan.MARKET,
            product_type=dhan.INTRA,
            after_market_order=False,
            amo_time="OPEN",
            price=0)

        print(Order)        

        trade = "INSERT INTO dhan_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+DhanSymbol+"', '"+DhanSymbolToken+"', '"+Order.get("data").get('orderId')+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()



    except:
        pass




def Dhan_Sell_Order(Client_Id, Access_Token, DhanSymbol, DhanSymbolToken, userid, strategy, product_type, quantity):
    print(Client_Id+" "+Access_Token+" "+DhanSymbol+" "+DhanSymbolToken+" "+userid)
    dhan = dhanhq(Client_Id,  Access_Token)

    try:
        Order = dhan.place_order(security_id=DhanSymbolToken,
            exchange_segment=dhan.FNO,
            transaction_type=dhan.SELL,
            quantity=quantity,
            validity=dhan.DAY,
            order_type=dhan.MARKET,
            product_type=dhan.INTRA,
            after_market_order=False,
            amo_time="OPEN",
            price=0)

        print(Order)

        #price = dhan.get_order_by_id(Order).get("data").get("price")

        trade = "INSERT INTO dhan_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+DhanSymbol+"', '"+DhanSymbolToken+"', '"+Order.get("data").get('orderId')+"', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

    except:
        pass








def Dhan_Buy_Order_Delivery(Client_Id, Access_Token, DhanSymbol, DhanSymbolToken, userid, strategy, product_type, quantity):
    dhan = dhanhq(Client_Id,  Access_Token)
    #print(DhanSymbolToken)

    try:
        Order = dhan.place_order(security_id=DhanSymbolToken,
            exchange_segment=dhan.FNO,
            transaction_type=dhan.BUY,
            quantity=quantity,
            validity=dhan.DAY,
            order_type=dhan.MARKET,
            product_type=dhan.CNC,
            after_market_order=False,
            amo_time="OPEN",
            price=0)

        print(Order)        

        trade = "INSERT INTO dhan_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+DhanSymbol+"', '"+DhanSymbolToken+"', '"+Order.get("data").get('orderId')+"', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()



    except:
        pass






def Dhan_Sell_Order_Delivery(Client_Id, Access_Token, DhanSymbol, DhanSymbolToken, userid, strategy, product_type, quantity):
    print(Client_Id+" "+Access_Token+" "+DhanSymbol+" "+DhanSymbolToken+" "+userid)
    dhan = dhanhq(Client_Id,  Access_Token)

    try:
        Order = dhan.place_order(security_id=DhanSymbolToken,
            exchange_segment=dhan.FNO,
            transaction_type=dhan.SELL,
            quantity=quantity,
            validity=dhan.DAY,
            order_type=dhan.MARKET,
            product_type=dhan.CNC,
            after_market_order=False,
            amo_time="OPEN",
            price=0)

        print(Order)

        #price = dhan.get_order_by_id(Order).get("data").get("price")

        trade = "INSERT INTO dhan_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+DhanSymbol+"', '"+DhanSymbolToken+"', '"+Order.get("data").get('orderId')+"', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

    except:
        pass
