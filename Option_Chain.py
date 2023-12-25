# Libraries
import requests
import json
import math
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta
from datetime import timedelta
import pandas as pd
from time import sleep
from Live_Price import *
from datetime import datetime


# Python program to print
# colored text and background
def strRed(skk):         return "\033[91m {}\033[00m".format(skk)
def strGreen(skk):       return "\033[92m {}\033[00m".format(skk)
def strYellow(skk):      return "\033[93m {}\033[00m".format(skk)
def strLightPurple(skk): return "\033[94m {}\033[00m".format(skk)
def strPurple(skk):      return "\033[95m {}\033[00m".format(skk)
def strCyan(skk):        return "\033[96m {}\033[00m".format(skk)
def strLightGray(skk):   return "\033[97m {}\033[00m".format(skk)
def strBlack(skk):       return "\033[98m {}\033[00m".format(skk)
def strBold(skk):        return "\033[1m {}\033[0m".format(skk)

# Method to get nearest strikes
def round_nearest(x,num=50): return int(math.ceil(float(x)/num)*num)
def nearest_strike_bnf(x): return round_nearest(x,100)
def nearest_strike_nf(x): return round_nearest(x,50)

# Urls for fetching Data
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""

def set_header():
    global bnf_ul
    global nf_ul
    global bnf_nearest
    global nf_nearest
    response_text = get_data(url_indices)
    data = json.loads(response_text)
    for index in data["data"]:
        if index["index"]=="NIFTY BANK":
            bnf_ul = index["last"]
            #print("banknifty")
    bnf_nearest=nearest_strike_bnf(bnf_ul)


# Fetching CE and PE data based on Nearest Expiry Date
def Delta_CE(num,step,nearest,url):
    #CE DATA
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                #print(strCyan(str(item["strikePrice"])) + strGreen(" CE ") + "[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" + strRed(" CE ")+"[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]")
                #print(data["records"]["expiryDates"][0] + " " + str(item["strikePrice"]) + " CE " + "[ " + strBold(str(item["CE"]["lastPrice"]).rjust(10," ")) + " ]" + " CE " + "[ " + strBold(str(item["CE"]["lastPrice"]).rjust(10," ")) + " ]")
                strike = strike + step
                Option_LTP = float(str(item["CE"]["lastPrice"]).rjust(10," "))
                apikey = "USBzqs1v"
                secretkey = "d8004c20-097c-446f-80bd-1e0eb096f563"
                user_id = "A1403293"
                password = "1025"
                totp = "6PEKPAF64PHZ5UVIPTKXIBKTIU"

                Live_Index = bnf_ul
                
                Strike_Price = float(item["strikePrice"])
                Next_Expiry = (datetime(2023, 9, 13, 15, 30, 0) - datetime.now())/timedelta(days=1)/365
                Volatality = 0.1
                Type = "c"

                try:
                    IV = implied_volatility(Option_LTP, Live_Index, Strike_Price, Next_Expiry, Volatality, Type)
                    Delta_CE = delta(Type, Live_Index, Strike_Price, Next_Expiry, Volatality, IV)
                    
                    Symbol = ""
                    Delta = ""

                    if float(Delta_CE)*100 < 25 and float(Delta_CE)*100 > 20:
                        Symbol = str(Strike_Price)
                        Delta = Delta_CE*100

                        return Symbol, Delta

                    if float(Delta_CE)*100 > -25 and float(Delta_CE)*100 < -20:
                        Symbol = str(Strike_Price)
                        Delta = Delta_CE*100

                        return Symbol, Delta

                    else:
                        pass

                        
                except Exception as e:
                    pass



def Delta_PE(num,step,nearest,url):
    #PE DATA
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                #print(strCyan(str(item["strikePrice"])) + strGreen(" CE ") + "[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" + strRed(" PE ")+"[ " + strBold(str(item["PE"]["openInterest"]).rjust(10," ")) + " ]")
                #print(data["records"]["expiryDates"][0] + " " + str(item["strikePrice"]) + " CE " + "[ " + strBold(str(item["CE"]["lastPrice"]).rjust(10," ")) + " ]" + " PE " + "[ " + strBold(str(item["PE"]["lastPrice"]).rjust(10," ")) + " ]")
                strike = strike + step
                Option_LTP = float(str(item["PE"]["lastPrice"]).rjust(10," "))
                apikey = "USBzqs1v"
                secretkey = "d8004c20-097c-446f-80bd-1e0eb096f563"
                user_id = "A1403293"
                password = "1025"
                totp = "6PEKPAF64PHZ5UVIPTKXIBKTIU"

                Live_Index = bnf_ul
                
                Strike_Price = float(item["strikePrice"])
                Next_Expiry = (datetime(2023, 9, 13, 15, 30, 0) - datetime.now())/timedelta(days=1)/365
                Volatality = 0.1
                Type = "p"
                
                try:
                    IV = implied_volatility(Option_LTP, Live_Index, Strike_Price, Next_Expiry, Volatality, Type)
                    Delta_PE = delta(Type, Live_Index, Strike_Price, Next_Expiry, Volatality, IV)
                    
                    Symbol = ""
                    Delta = ""

                    if float(Delta_PE)*100 < 25 and float(Delta_PE)*100 > 20:
                        Symbol = str(Strike_Price)
                        Delta = Delta_PE*100

                        return Symbol, Delta
                    if float(Delta_PE)*100 > -25 and float(Delta_PE)*100 < -20:
                        Symbol = str(Strike_Price)
                        Delta = Delta_PE*100

                        return Symbol, Delta
                    else:
                        pass

                        
                except Exception as e:
                    pass
                                    





def Premium_Finder(num,step,nearest,url, Type, ltp):
    #PE DATA
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                #print(strCyan(str(item["strikePrice"])) + strGreen(" CE ") + "[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" + strRed(" PE ")+"[ " + strBold(str(item["PE"]["openInterest"]).rjust(10," ")) + " ]")
                #print(str(item["strikePrice"]) + " CE " + strBold(str(item["CE"]["lastPrice"]).rjust(10," ")))
                #print(str(item["strikePrice"]) + " PE " + strBold(str(item["PE"]["lastPrice"]).rjust(10," ")))
                strike = strike + step
                CE_Option_LTP = float(str(item["CE"]["lastPrice"]).rjust(10," "))
                PE_Option_LTP = float(str(item["PE"]["lastPrice"]).rjust(10," "))


                if Type == "PE":

                    if float(ltp) < float(str(item["CE"]["lastPrice"]).rjust(10," "))-50 and float(ltp) > float(str(item["CE"]["lastPrice"]).rjust(10," "))+50:

                        return str(item["strikePrice"]), CE_Option_LTP

                    if float(ltp) < float(str(item["CE"]["lastPrice"]).rjust(10," "))+50 and float(ltp) > float(str(item["CE"]["lastPrice"]).rjust(10," "))-50:
                        
                        return str(item["strikePrice"]), CE_Option_LTP
                    
                    else:
                        pass

                
                if Type == "CE":

                    if float(ltp) < float(str(item["PE"]["lastPrice"]).rjust(10," "))-50 and float(ltp) > float(str(item["PE"]["lastPrice"]).rjust(10," "))+50:

                        return str(item["strikePrice"]), PE_Option_LTP

                    if float(ltp) < float(str(item["PE"]["lastPrice"]).rjust(10," "))+50 and float(ltp) > float(str(item["PE"]["lastPrice"]).rjust(10," "))-50:

                        return str(item["strikePrice"]), PE_Option_LTP

                    else:
                        pass









set_header()

