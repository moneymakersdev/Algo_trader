from Angle_Order import *




def place(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid, type, Qty):
    Angle_Buy_Order(Api, Api_Secret, Totp, ClientID, Password, symbol, token, strategy, userid[0], "INTRADAY", Qty)
