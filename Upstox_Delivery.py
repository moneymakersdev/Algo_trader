import json
import requests
from conn import *
import datetime
from datetime import date

# for get code from web page

# 8369617040

def Upstox_Buy_Order_Delivery(client_id, client_secret, code, UpstoxSymbol, userid, strategy, product, quantity):
    print(client_id)
    validation_url = 'https://api-v2.upstox.com/login/authorization/token'
    redirect_url = "https://moneymakers-algo.com/broker.php"

    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    code_without_spaces = ''.join(char for char in code if not char.isspace())
    data = {
        'code': str(code.lstrip()),
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_url,
        'grant_type': 'authorization_code'
    }

    response = requests.post(validation_url, headers=headers, data=data)
    
    global access_token

    if response.status_code == 200:
        response_json = response.json()
        #global access_token
        access_token = response_json.get('access_token')

    else:
        # Request failed, print the status code and response content
        print("Request failed with status code:", response.status_code)

    place_order_url = 'https://api-v2.upstox.com/order/place'
    # print('\n\naccess_token',str(access_token))

    Authorization = ""

    user = 'select * from api where UserID="'+userid+'"'
    mycursor.execute(user)
    tokenresult = mycursor.fetchall()

        
    if tokenresult[0][4] != "None":
        Authorization = tokenresult[0][4]
    else:
        Authorization = 'Bearer {access_token}'.format(access_token = access_token)
        update = "update api set Client_ID='"+str(Authorization)+"' where UserID='"+userid+"'"
        mycursor.execute(update)
        mydb.commit()

    #print(Authorization)
    headers = {
        'accept':'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/json',
        'Authorization': Authorization
    }
    data = {
      "quantity": quantity,
      "product": "D",
      "validity": "DAY",
      "price": 0,
      "tag": "string",
      "instrument_token": UpstoxSymbol,
      "order_type": "MARKET",
      "transaction_type": "BUY",
      "disclosed_quantity": 0,
      "trigger_price": 0,
      "is_amo": False
    }

    
    response = requests.post(place_order_url, headers=headers, json=data)
    json_formatted = json.dumps(response.json(), indent=2)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        order_id = data.get('order_id')


        trade = "INSERT INTO upstox_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+UpstoxSymbol+"', '"+str(order_id)+"', '0', '"+str(quantity)+"', '"+userid+"', 'BUY', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()

        update = "update running_bots set Orders='1' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

        return order_id
    else:
        # Request failed, print the status code and response content
        print("Request failed with status code:", response.status_code)

        pass











def Upstox_Sell_Order_Delivery(client_id, client_secret, code, UpstoxSymbol, userid, strategy, product, quantity):
    validation_url = 'https://api-v2.upstox.com/login/authorization/token'
    redirect_url = "https://moneymakers-algo.com/broker.php"

    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    code_without_spaces = ''.join(char for char in code if not char.isspace())
    data = {
        'code': str(code.lstrip()),
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_url,
        'grant_type': 'authorization_code'
    }

    response = requests.post(validation_url, headers=headers, data=data)
    
    global access_token

    if response.status_code == 200:
        response_json = response.json()
    #    global access_token
        access_token = response_json.get('access_token')

    else:
        # Request failed, print the status code and response content
        print("Request failed with status code:", response.status_code)

    place_order_url = 'https://api-v2.upstox.com/order/place'
    # print('\n\naccess_token',str(access_token))

    Authorization = ""

    user = 'select * from api where UserID="'+userid+'"'
    mycursor.execute(user)
    tokenresult = mycursor.fetchall()
        
    if tokenresult[0][4] != "None":
        Authorization = tokenresult[0][4]
    else:
        Authorization = 'Bearer {access_token}'.format(access_token = access_token)
        update = "update api set Client_ID='"+str(Authorization)+"' where UserID='"+userid+"'"
        mycursor.execute(update)
        mydb.commit()


    print(Authorization)
    headers = {
        'accept':'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/json',
        'Authorization': Authorization
    }
    data = {
      "quantity": quantity,
      "product": "D",
      "validity": "DAY",
      "price": 0,
      "tag": "string",
      "instrument_token": UpstoxSymbol,
      "order_type": "MARKET",
      "transaction_type": "SELL",
      "disclosed_quantity": 0,
      "trigger_price": 0,
      "is_amo": False
    }

    
    response = requests.post(place_order_url, headers=headers, json=data)
    json_formatted = json.dumps(response.json(), indent=2)
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        order_id = data.get('order_id')

        trade = "INSERT INTO upstox_orders (Symbol, Token, Price, Quantity, UserID, Type, DateTime, Strategy) values ('"+UpstoxSymbol+"', '"+str(order_id)+"', '0', '"+str(quantity)+"', '"+userid+"', 'SELL', '"+str(datetime.datetime.now())+"', '"+str(strategy)+"')"
        mycursor.execute(trade)
        mydb.commit()
    
        update = "update running_bots set Orders='0' where UserID='"+userid+"' and Script='"+strategy+"'"
        mycursor.execute(update)
        mydb.commit()

        return order_id
    else:
        # Request failed, print the status code and response content
        print("Request failed with status code:", response.status_code)
        pass
