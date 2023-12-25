import asyncio
import websockets
import json






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




while True:
    data = asyncio.get_event_loop().run_until_complete(fetch_data("NIFTY BANK"))
    
    print(data)

    #while data!=None:
    #    print(data)