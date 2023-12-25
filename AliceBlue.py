from pya3 import *
from conn import *
import datetime
from datetime import date



def Alice_Buy_Order(Client_Id, Access_Token, AliceSymbol, userid, strategy, product_type, quantity):
    User = Client_Id
    API = Access_Token
    

    alice = Aliceblue(user_id=User ,api_key=API)

    alice.get_session_id()

    Order =  alice.place_order(transaction_type = TransactionType.Buy,
                    instrument = alice.get_instrument_by_symbol('NFO', AliceSymbol),
                    quantity = int(quantity),
                    order_type = OrderType.Market,
                    product_type = ProductType.Intraday,
                    price = 0.0,
                    trigger_price = None,
                    stop_loss = None,
                    square_off = None,
                    trailing_sl = None,
                    is_amo = False)


    print(Order)

    trade = "INSERT INTO alice_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+AliceSymbol+"', '"+str(Order.get('NOrdNo'))+"', '0', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()

    update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
    mycursor.execute(update)
    mydb.commit()





def Alice_Sell_Order(Client_Id, Access_Token, AliceSymbol, userid, strategy, product_type, quantity):
    User = Client_Id
    API = Access_Token

    alice = Aliceblue(user_id=User ,api_key=API)

    alice.get_session_id()

    Order =  alice.place_order(transaction_type = TransactionType.Sell,
                    instrument = alice.get_instrument_by_symbol('NFO', AliceSymbol),
                    quantity = int(quantity),
                    order_type = OrderType.Market,
                    product_type = ProductType.Intraday,
                    price = 0.0,
                    trigger_price = None,
                    stop_loss = None,
                    square_off = None,
                    trailing_sl = None,
                    is_amo = False)

    print(Order)                        

    trade = "INSERT INTO alice_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+AliceSymbol+"', '"+str(Order.get('NOrdNo'))+"', '0', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()

    update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
    mycursor.execute(update)
    mydb.commit()







def Alice_Buy_Order_Delivery(Client_Id, Access_Token, AliceSymbol, userid, strategy, product_type, quantity):
    User = Client_Id
    API = Access_Token

    alice = Aliceblue(user_id=User ,api_key=API)

    alice.get_session_id()

    Order =  alice.place_order(transaction_type = TransactionType.Buy,
                    instrument = alice.get_instrument_by_symbol('NFO', AliceSymbol),
                    quantity = int(quantity),
                    order_type = OrderType.Market,
                    product_type = ProductType.Delivery,
                    price = 0.0,
                    trigger_price = None,
                    stop_loss = None,
                    square_off = None,
                    trailing_sl = None,
                    is_amo = False)


    print(Order)

    trade = "INSERT INTO alice_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+AliceSymbol+"', '"+str(Order.get('NOrdNo'))+"', '0', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()

    update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
    mycursor.execute(update)
    mydb.commit()





def Alice_Sell_Order_Delivery(Client_Id, Access_Token, AliceSymbol, userid, strategy, product_type, quantity):
    User = Client_Id
    API = Access_Token

    alice = Aliceblue(user_id=User ,api_key=API)

    alice.get_session_id()

    Order =  alice.place_order(transaction_type = TransactionType.Sell,
                    instrument = alice.get_instrument_by_symbol('NFO', AliceSymbol),
                    quantity = int(quantity),
                    order_type = OrderType.Market,
                    product_type = ProductType.Delivery,
                    price = 0.0,
                    trigger_price = None,
                    stop_loss = None,
                    square_off = None,
                    trailing_sl = None,
                    is_amo = False)

    print(Order)                        

    trade = "INSERT INTO alice_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+AliceSymbol+"', '"+str(Order.get('NOrdNo'))+"', '0', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()

    update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
    mycursor.execute(update)
    mydb.commit()



