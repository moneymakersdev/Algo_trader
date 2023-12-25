from conn import *
from datetime import date
from breeze_connect import BreezeConnect
import datetime



def Icici_Buy_Order(Api, Api_Secret, Totp, strikeprice, types, Expiry, userid, strategy, Qty):
    print(userid)
    # Initialize SDK
    breeze = BreezeConnect(api_key=Api)

    # Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
    # Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
    import urllib
    print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(Api))

    session = Totp

    # Generate Session
    breeze.generate_session(api_secret=Api_Secret,
                            session_token=session)


    # Generate ISO8601 Date/DateTime String

    data = datetime.datetime.now()

    iso_date_string = datetime.datetime.strptime(str(data.date()),"%Y-%m-%d").isoformat()[:10] + 'T06:00:00.000Z'
    iso_date_time_string = datetime.datetime.strptime(str(data.date())+" 23:59:59","%Y-%m-%d %H:%M:%S").isoformat()[:19] + '.000Z'

    order = breeze.place_order(stock_code="CNXBAN",
                        exchange_code="NFO",
                        product="options",
                        action="buy",
                        order_type="market",
                        stoploss="",
                        quantity=int(Qty),
                        price="",
                        validity="day",
                        validity_date=iso_date_string,
                        disclosed_quantity="0",
                        expiry_date=str(Expiry)+"T06:00:00.000Z",
                        right=types,
                        strike_price=strikeprice)

    

    print(order)

    trade = "INSERT INTO icici_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Expiry, Strategy) values ('BANKNIFTY', '"+types+"', '"+strikeprice+"', '"+Qty+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+Expiry+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()


    update = "update running_bots set Orders='1' where UserID='"+userid+"'"
    mycursor.execute(update)
    mydb.commit()





def Icici_Sell_Order(Api, Api_Secret, Totp, strikeprice, types, Expiry, userid, strategy, Qty):

    # Initialize SDK
    breeze = BreezeConnect(api_key=Api)

    # Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
    # Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
    import urllib
    print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(Api))

    session = Totp

    # Generate Session
    breeze.generate_session(api_secret=Api_Secret,
                            session_token=session)

    # Generate ISO8601 Date/DateTime String

    data = datetime.datetime.now()


    iso_date_string = datetime.datetime.strptime(str(data.date()),"%d/%m/%Y").isoformat()[:10] + 'T06:00:00.000Z'
    iso_date_time_string = datetime.datetime.strptime(str(data.date())+" 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'


    order = breeze.place_order(stock_code="CNXBAN",
                        exchange_code="NFO",
                        product="options",
                        action="sell",
                        order_type="market",
                        stoploss="",
                        quantity=int(Qty),
                        price="",
                        validity="day",
                        validity_date=iso_date_string,
                        disclosed_quantity="0",
                        expiry_date=Expiry+"T06:00:00.000Z",
                        right=types,
                        strike_price=strikeprice)

    print(order)


    trade = "INSERT INTO icici_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Expiry, Strategy) values ('BANKNIFTY', '"+types+"', '"+strikeprice+"', '"+Qty+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+Expiry+"', '"+str(strategy)+"')"
    mycursor.execute(trade)
    mydb.commit()


    update = "update running_bots set Orders='0' where UserID='"+userid+"'"
    mycursor.execute(update)
    mydb.commit()

