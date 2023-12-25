import sys

sys.path.insert(1, 'C:/xampp/htdocs/Algo_Trader')
from Expiry_Date import *
from Tokens import *



def auth_code():
    code = "sq7p+YzgKgcVpZuPgDgSUUtjXnTVMJf3lM/jdXcW3hOu5eVDC2ER1GWVdlJmdrd8ihmg9mpLVj0/BcjD8prF2gyTZNzXh0syPt+roVcKxkC0cWgEHFWPQQ=="

    return code


def Bnf_Future():
    Code = "15776514"
    return Code


def Nifty_Future():
    Code = "16178434"
    return Code


def FinNifty_Future():
    Code = "8984578"
    return Code


def Angle_Bnf_Token():
    expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    GetExpiry_Date = Monthly_Expiry()
    ExpiryYear = str(GetExpiry_Date[0])[2:]
    ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
    ExpiryDate = GetExpiry_Date[2]

    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
    tokenresult = Angel_Data(symbol)

    return tokenresult

