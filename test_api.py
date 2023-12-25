from Live_Price import *
from conn import *
from Angle_Order import *
from time import sleep
from Upstox import *
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
import datetime
from datetime import date
import pandas as pd



#token = 'select * from running_bots where Script="BNF"'
#mycursor.execute(token)
#tokenresult = mycursor.fetchall()

def test():

    token = 'select * from api where UserID="Aji8101"'
    mycursor.execute(token)
    tokenresult = mycursor.fetchall()

    for I in range(len(tokenresult)): 
        #print(I)
        UserID = tokenresult[I][0].replace(" ", "")
        Api_Key = tokenresult[I][1].replace(" ", "")
        Secret_Key = tokenresult[I][2].replace(" ", "")
        TOTP_Secret = tokenresult[I][3].replace(" ", "")
        Client_ID = tokenresult[I][4].replace(" ", "")
        Password = tokenresult[I][5].replace(" ", "")
        Broker = tokenresult[I][6].replace(" ", "")
        DateTime = tokenresult[I][7].replace(" ", "")

        Options = Bnf_Idx_Price(Api_Key, Secret_Key, Client_ID, Password, TOTP_Secret)

        return Options

while True:
    print(test())

#print(list(test().iloc[-1])[5])
#print(list(test().iloc[-2])[5])
#print(list(test().iloc[-3])[5])
#print(list(test().iloc[-4])[5])
#print(list(test().iloc[-5])[5])