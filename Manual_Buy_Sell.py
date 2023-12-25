from Place_Order import *
from Live_Price import *
from conn import *
from time import sleep
from Tokens import *
import datetime
from datetime import date



apikey = "ef1zHKeB"
secretkey = "1e503c5f-25f9-4af2-b9e6-75fbd4e50445"
user_id = "VJVG1165"
password = "7788"
totp = "MJNJ2CWLVLTJ646R4CK6OOEAME"


Symbol = "BANKNIFTY"
Strike = "47900"
Type = "PE"
Order = "SELL"


symbol = str(Symbol)+"28DEC23"+str(Strike)+str(Type)

if Type == "CE":
    Type = "CALL"
if Type == "PE":
    Type = "PUT"

DhanSymbol = str(Symbol)+" 28 DEC "+str(Strike)+" "+str(Type)

if Type == "CALL":
    Type = "CE"
if Type == "PUT":
    Type = "PE"

AliceSymbol = str(Symbol)+"28DEC23"+str(Type[0])+str(Strike)
UpstoxSymbol = str(Symbol)+"23DEC"+str(Strike)+str(Type)
FyresSymbol = str(Symbol)+"28DEC23"+str(Type[0])+str(Strike)
MotilalSymbol = str(Symbol)+" 28-DEC-2023 "+str(Type)+" "+str(Strike)
Zerodha = str(Symbol)+"23DEC"+str(Strike)+str(Type)
IciciExpiry = "2023-12-28"

tokenresult = Angel_Data(symbol)
print(tokenresult)


Idx_Live = Bnf_Idx_Price(apikey, secretkey, user_id, password, totp)
option_live = Option_Idx_Price(apikey, secretkey, user_id, password, totp, str(symbol.replace("'", "")), str(tokenresult.replace("'", "")))


if Type == "CE":
    Type = "call"
if Type == "PE":
    Type = "put"



if Order == "BUY":
    Buy_Order(symbol, tokenresult, "BNF", DhanSymbol, AliceSymbol, UpstoxSymbol, FyresSymbol, MotilalSymbol, Zerodha, Strike, Type, IciciExpiry)
    
    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'BUY', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
    mycursor.execute(trade)
    mydb.commit()



if Order == "SELL":
    Sell_Order(symbol, tokenresult, "BNF")
    
    trade = "INSERT INTO trades (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('"+str(symbol.replace("'", ""))+"', '"+str(tokenresult.replace("'", ""))+"', 'SELL', '30', '"+str(option_live)+"', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'BNF', '0')"
    mycursor.execute(trade)
    mydb.commit()