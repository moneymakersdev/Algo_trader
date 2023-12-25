from SmartApi import SmartConnect
import pyotp
from time import sleep
import time
import logging
from datetime import date
import datetime
from ast import literal_eval
from Expiry_Date import *
from conn import *
import pandas as pd
from Tokens import *


import asyncio
import websockets
import json



#from truedata_ws.websocket.TD import TD
#from copy import deepcopy
#import pandas as pd
#from datetime import date
#import time
#from time import sleep


#username = 'tdwsp495'
#password = 'amit@495'
#
#realtime_port = 8086
#
#td_app = TD(username, password, live_port=realtime_port, historical_api=False)




async def fetch_data(Symbol):
    async with websockets.connect("wss://push.truedata.in:8084?user=tdwsp495&password=amit@495") as websocket:
        # Define the "addsymbol" request
        add_symbol_request = {
            "method": "addsymbol",
            "symbols": [Symbol]
        }
        
        # Convert the request to JSON
        add_symbol_request_json = json.dumps(add_symbol_request)

        # Send the "addsymbol" request
        await websocket.send(add_symbol_request_json)

        while True:
            try:
                data = await websocket.recv()
                #print(f"Received data: {data}")
                parsed_data = json.loads(data)

                if 'trade' in parsed_data:
                    trade_data = parsed_data['trade']
                    return trade_data
                
                if 'symbollist' in parsed_data:
                    symbollist_data = parsed_data['symbollist']
                    return symbollist_data[0][3]

            except websockets.exceptions.ConnectionClosed:
                #print("Connection closed")
                break




def Bnf_Idx_Price(apikey, secretkey, user_id, password, totp):
    #sleep(1)
    #apikey = apikey
    #secretkey = secretkey
    #user_id = user_id
    #password = password
    #totp = pyotp.TOTP(totp).now()
#
    #obj = SmartConnect(api_key=apikey)
    #
    #data = obj.generateSession(user_id, password, totp)
    #try:
    #    refreshToken = data['data']['refreshToken']
    #    #jwtToken = data['data']['jwtToken']
    #except Exception as e:
    #    pass
    #feedToken = obj.getfeedToken()
    #LTP = obj.ltpData("NSE", "BANKNIFTY", "99926009")
    #close = LTP["data"]["ltp"]
#
    #return close
    #sleep(1)
    return asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY BANK"))

    #return asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY BANK"))

    #symbols = ["NIFTY BANK"]
#
    #req_ids = td_app.start_live_data(symbols)
    #live_data_objs = {}
#
    #time.sleep(0.1)
#
    #for req_id in req_ids:
    #    live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
    #    data = td_app.touchline_data[req_id]
    #    ltp = data.ltp
    #    return ltp





def nifty_Fut_Price(apikey, secretkey, user_id, password, totp):
    sleep(1)
    GetExpiry_Date = Monthly_Expiry()
    expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

    ExpiryYear = str(GetExpiry_Date[0])[2:]
    ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
    ExpiryDate = GetExpiry_Date[2]

    symbol = "NIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
    #token = 'select token from instruments where symbol="'+symbol+'"'
    #mycursor.execute(token)
    #tokenresult = mycursor.fetchone()
    tokenresult = Angel_Data(symbol)

    apikey = apikey
    secretkey = secretkey
    user_id = user_id
    password = password
    totp = pyotp.TOTP(totp).now()

    obj = SmartConnect(api_key=apikey)
    
    data = obj.generateSession(user_id, password, totp)
    try:
        refreshToken = data['data']['refreshToken']
        #jwtToken = data['data']['jwtToken']
    except Exception as e:
        pass
    feedToken = obj.getfeedToken()
    LTP = obj.ltpData("NFO", symbol, tokenresult[0])
    close = LTP["data"]["ltp"]

    return close
    #sleep(1)
#
    #return asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY-I"))

    #return asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY-I"))

    #symbols = ["NIFTY-I"]
#
    #req_ids = td_app.start_live_data(symbols)
    #live_data_objs = {}
#
    #time.sleep(0.1)
#
    #for req_id in req_ids:
    #    live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
    #    data = td_app.touchline_data[req_id]
    #    ltp = data.ltp
    #    return ltp




def finnifty_Fut_Price(apikey, secretkey, user_id, password, totp):
    sleep(1)
    GetExpiry_Date = Fin_Nifty_Monthly_Expiry()
    expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

    ExpiryYear = str(GetExpiry_Date[0])[2:]
    ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
    ExpiryDate = GetExpiry_Date[2]

    symbol = "FINNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
    #token = 'select token from instruments where symbol="'+symbol+'"'
    #mycursor.execute(token)
    #tokenresult = mycursor.fetchone()
    tokenresult = Angel_Data(symbol)

    apikey = apikey
    secretkey = secretkey
    user_id = user_id
    password = password
    totp = pyotp.TOTP(totp).now()

    obj = SmartConnect(api_key=apikey)
    
    data = obj.generateSession(user_id, password, totp)
    try:
        refreshToken = data['data']['refreshToken']
        #jwtToken = data['data']['jwtToken']
    except Exception as e:
        pass
    feedToken = obj.getfeedToken()
    LTP = obj.ltpData("NFO", symbol, tokenresult)
    close = LTP["data"]["ltp"]

    return close




def bnf_Fut_Price(apikey, secretkey, user_id, password, totp):
    sleep(1)
    GetExpiry_Date = Monthly_Expiry()
    expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

    ExpiryYear = str(GetExpiry_Date[0])[2:]
    ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
    ExpiryDate = GetExpiry_Date[2]

    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
    #token = 'select token from instruments where symbol="'+symbol+'"'
    #mycursor.execute(token)
    #tokenresult = mycursor.fetchone()
    tokenresult = Angel_Data(symbol)

    apikey = apikey
    secretkey = secretkey
    user_id = user_id
    password = password
    totp = pyotp.TOTP(totp).now()

    obj = SmartConnect(api_key=apikey)
    
    data = obj.generateSession(user_id, password, totp)
    try:
        refreshToken = data['data']['refreshToken']
        #jwtToken = data['data']['jwtToken']
    except Exception as e:
        pass
    feedToken = obj.getfeedToken()
    LTP = obj.ltpData("NFO", symbol, tokenresult)
    close = LTP["data"]["ltp"]

    return close
    #sleep(1)
#
    #return asyncio.get_event_loop().run_until_complete(fetch_data("BANKNIFTY-I"))


    #return asyncio.get_event_loop().run_until_complete(fetch_data("BANKNIFTY-I"))


#    symbols = ["BANKNIFTY-I"]
#
#    req_ids = td_app.start_live_data(symbols)
#    live_data_objs = {}
#
#    time.sleep(0.1)
#
#    for req_id in req_ids:
#        live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
#        data = td_app.touchline_data[req_id]
#        ltp = data.ltp
#        return ltp




def Nifty_Idx_Price(apikey, secretkey, user_id, password, totp):
    sleep(1)
    apikey = apikey
    secretkey = secretkey
    user_id = user_id
    password = password
    totp = pyotp.TOTP(totp).now()

    obj = SmartConnect(api_key=apikey)
    
    data = obj.generateSession(user_id, password, totp)
    try:
        refreshToken = data['data']['refreshToken']
        #jwtToken = data['data']['jwtToken']
    except Exception as e:
        pass
    feedToken = obj.getfeedToken()
    LTP = obj.ltpData("NSE", "NIFTY", "99926000")
    close = LTP["data"]["ltp"]

    return close
    #sleep(1)
#
    #return asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY 50"))


    #return asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY-I"))


    #symbols = ["NIFTY 50"]
#
    #req_ids = td_app.start_live_data(symbols)
    #live_data_objs = {}
#
    #time.sleep(0.1)
#
    #for req_id in req_ids:
    #    live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
    #    data = td_app.touchline_data[req_id]
    #    ltp = data.ltp
    #    return ltp



def Option_Idx_Price(apikey, secretkey, user_id, password, totp, symbol, token):
    sleep(1)
    apikey = apikey
    secretkey = secretkey
    user_id = user_id
    password = password
    totp = pyotp.TOTP(totp).now()

    obj = SmartConnect(api_key=apikey)
    data = obj.generateSession(user_id, password, totp)
    try:
        refreshToken = data['data']['refreshToken']
        #jwtToken = data['data']['jwtToken']
    except Exception as e:
        pass
    print(symbol)
    print(token)
    feedToken = obj.getfeedToken()
    LTP = obj.ltpData("NFO", symbol, token)
    close = LTP["data"]["ltp"]
    
    return close




def Options_OI_CE(Api_Key, TOTP_Secret, Client_ID, Password, Token):
    Api_Key = Api_Key
    TOTP_Secret = TOTP_Secret
    Client_ID = Client_ID
    Password = Password
    data = datetime.datetime.now()
    smartApi = SmartConnect(Api_Key)
    totp=pyotp.TOTP(TOTP_Secret).now()
    data = smartApi.generateSession(Client_ID, Password, totp)
    # print(data)
    #authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    date = datetime.datetime.today()

    #print (str(date.date()))

    try:
        historicParam={
        "exchange": "NFO",
        "symboltoken": Token,
        "interval": "FIFTEEN_MINUTE",
        "fromdate": str(date.date())+" 09:00",
        "todate": str(date.date())+" 15:30"
        }
        history = smartApi.getCandleData(historicParam)['data']
        history = pd.DataFrame(history)
        return history

    except Exception as e:
        print("Historic Api failed: {}".format(e.message))




def Options_OI_PE(Api_Key, TOTP_Secret, Client_ID, Password, Token):
    Api_Key = Api_Key
    TOTP_Secret = TOTP_Secret
    Client_ID = Client_ID
    Password = Password
    data = datetime.datetime.now()
    smartApi = SmartConnect(Api_Key)
    totp=pyotp.TOTP(TOTP_Secret).now()
    data = smartApi.generateSession(Client_ID, Password, totp)
    # print(data)
    #authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    date = datetime.datetime.today()

    #print (str(date.date()))

    try:
        historicParam={
        "exchange": "NFO",
        "symboltoken": Token,
        "interval": "FIFTEEN_MINUTE",
        "fromdate": str(date.date())+" 09:00",
        "todate": str(date.date())+" 15:30"
        }
        history = smartApi.getCandleData(historicParam)['data']
        history = pd.DataFrame(history)
        return history

    except Exception as e:
        print("Historic Api failed: {}".format(e.message))







async def fetch_data(Symbol):
    async with websockets.connect("wss://push.truedata.in:8086?user=tdwsp495&password=amit@495") as websocket:
        # Define the "addsymbol" request
        add_symbol_request = {
            "method": "addsymbol",
            "symbols": [Symbol]
        }
        
        # Convert the request to JSON
        add_symbol_request_json = json.dumps(add_symbol_request)

        # Send the "addsymbol" request
        await websocket.send(add_symbol_request_json)

        while True:
            try:
                data = await websocket.recv()
                #print(f"Received data: {data}")
                parsed_data = json.loads(data)

                if 'trade' in parsed_data:
                    trade_data = parsed_data['trade']
                    return trade_data
                
                if 'symbollist' in parsed_data:
                    symbollist_data = parsed_data['symbollist'] 
                    return symbollist_data[0][3]

            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break