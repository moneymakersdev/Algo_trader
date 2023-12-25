import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from conn import *
from Place_Order import *




# Calculate the ATR
def calculate_atr(df, atr_period):
    df['TR'] = df.apply(lambda row: max(row['High'] - row['Low'], abs(row['High'] - row['close_prev']), abs(row['Low'] - row['close_prev'])), axis=1)
    df['ATR'] = df['TR'].rolling(atr_period).mean()
    return df

# Calculate Supertrend
def calculate_supertrend(df, factor, atr_period):
    df['Upper Basic'] = (df['High'] + df['Low']) / 2 + factor * df['ATR']
    df['Lower Basic'] = (df['High'] + df['Low']) / 2 - factor * df['ATR']
    df['Upper Band'] = df['Upper Basic']
    df['Lower Band'] = df['Lower Basic']
    df['Trend'] = 1

    for i in range(1, len(df)):
        if df.at[i, 'Close'] > df.at[i-1, 'Upper Band']:
            df.at[i, 'Upper Band'] = max(df.at[i-1, 'Upper Basic'], df.at[i-1, 'Upper Band'])
        else:
            df.at[i, 'Upper Band'] = df.at[i-1, 'Upper Basic']

        if df.at[i, 'Close'] < df.at[i-1, 'Lower Band']:
            df.at[i, 'Lower Band'] = min(df.at[i-1, 'Lower Basic'], df.at[i-1, 'Lower Band'])
        else:
            df.at[i, 'Lower Band'] = df.at[i-1, 'Lower Basic']

        if df.at[i, 'Close'] > df.at[i, 'Upper Band']:
            df.at[i, 'Trend'] = 1
            df.at[i, 'Lower Band'] = df.at[i, 'Upper Band']
        elif df.at[i, 'Close'] < df.at[i, 'Lower Band']:
            df.at[i, 'Trend'] = -1
            df.at[i, 'Upper Band'] = df.at[i, 'Lower Band']
        else:
            df.at[i, 'Trend'] = df.at[i-1, 'Trend']

    
    df['SuperTrend'] = 0.0
    for i in range(atr_period, len(df)):
        if df['Close'][i-1] <= df['Upper Band'][i-1]:
            df.loc[i, 'SuperTrend'] = df['Upper Band'][i]
        else:
            df.loc[i, 'SuperTrend'] = df['Lower Band'][i]


    return df




def Supertrend_04():

    # Load price data from a CSV file (replace 'price_data.csv' with your file)
    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_15m.csv')
    
    # Input parameters
    atr_period = 10
    factor = 0.4

    # Calculate ATR and Supertrend
    df['close_prev'] = df['Close'].shift(1)
    df = calculate_atr(df, atr_period)
    df = calculate_supertrend(df, factor, atr_period)

    # Print the Supertrend data
    import pandas_ta as ta
    sti = ta.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=0.4)

    return sti.iloc[-1][0]

    #return df[['SuperTrend']].iloc[-1]



def Supertrend_08():

    # Load price data from a CSV file (replace 'price_data.csv' with your file)
    df = pd.read_csv('C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_15m.csv')

    # Input parameters
    atr_period = 10
    factor = 0.8

    # Calculate ATR and Supertrend
    df['close_prev'] = df['Close'].shift(1)
    df = calculate_atr(df, atr_period)
    df = calculate_supertrend(df, factor, atr_period)

    # Print the Supertrend data
    import pandas_ta as ta
    sti = ta.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=0.8)

    return sti.iloc[-1][0]

    #return df[['SuperTrend']].iloc[-1]


def calculate_ema(data, period):
    ema = data.ewm(span=period, adjust=False).mean()
    return ema


def ema():
    while True:
            # Load data from CSV file
        csv_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_15m.csv'  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Close'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 3  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return format(round(last_ema_value, 2))



def Latest_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


def Previous_Close():
    df = pd.read_csv("C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_Fut_15m.csv")
    
    if not df.empty:
        last_row = df.iloc[-2]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) < str(data.date())+" 09:30:00.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) > str(data.date())+" 09:30:00.000000":

        while True:
            print("15 min")
            apikey = "0gBDe3ih"
            secretkey = "e59be0e4-ede5-453b-9600-43261a80bc0a"
            user_id = "S50233582"
            password = "1111"
            totp = "DODP5DHQUTCPASWVBYTIUXZEZQ"

            #Supertrend0_4 = list(Supertrend_04())
            #Supertrend0_8 = list(Supertrend_08())
            
            #Supertrend_0_4 = Supertrend0_4[0]
            #Supertrend_0_8 = Supertrend0_8[0]

            Supertrend0_4 = Supertrend_04()
            Supertrend0_8 = Supertrend_08()
            
            Supertrend_0_4 = Supertrend0_4
            Supertrend_0_8 = Supertrend0_8

            #Old_Supertrend_0_4 = Old_Supertrend_04()
            #Old_Supertrend_0_8 = Old_Supertrend_08()
            ema1 = ema()
            Latest = Latest_Close()
            Previous = Previous_Close()
            GetExpiry_Date = Expiry_Date()

            Idx_Live = bnf_Fut_Price(apikey, secretkey, user_id, password, totp)

            if Idx_Live == None:
                break
            else:
                pass

            print("Latest "+str(Latest))
            print("Supertrend_0_4: "+str(Supertrend_0_4))
            print("Supertrend_0_8: "+str(Supertrend_0_8))
            print("Previous "+str(Previous))
            #print("Old Supertrend_0_4: "+str(Old_Supertrend_0_4))
            #print("Old Supertrend_0_8: "+str(Old_Supertrend_0_8))
            print("ema: "+str(ema1))
            print(datetime.datetime.now())
            sleep(1)

            sql = "select * from delta_bnf_fut_orders ORDER BY DateTime DESC"
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            Position = myresult[6]
            print("Position "+str(Position))

            GetExpiry_Date = Monthly_Expiry()


            if Position == "0":
                expiry_month = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
                strikeprice = str(Idx_Live)[:3]+"00"

                ExpiryYear = str(GetExpiry_Date[0])[2:]
                ExpiryMonth = expiry_month[GetExpiry_Date[1]-1]
                ExpiryDate = GetExpiry_Date[2]

                ICICI_Expiry = str(GetExpiry_Date[0])+"-"+str(GetExpiry_Date[1])+"-"+"0"+str(ExpiryDate)

                if float(Latest) > float(Supertrend_0_4) and float(Latest) > float(Supertrend_0_8) and float(Latest) > float(ema1) and float(Previous) < float(Supertrend_0_4):# and float(Previous) < float(Supertrend_0_8) and float(Previous) < float(ema1):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
                    DhanSymbol = "BANKNIFTY "+" "+str(ExpiryMonth)+" "+" FUT"
                    AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+" FUT"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"

                    token = 'select token from instruments where symbol="'+symbol+'"'
                    mycursor.execute(token)
                    tokenresult = mycursor.fetchone()

                    #Buy_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "delta_trades", DhanSymbol)

                    trade = "INSERT INTO delta_bnf_fut_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'BUY', '30', '0', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break



                if float(Latest) < float(Supertrend_0_4) and float(Latest) < float(Supertrend_0_8) and float(Latest) < float(ema1) and float(Previous) > float(Supertrend_0_4): #and float(Previous) > float(Supertrend_0_8) and float(Previous) > float(ema1):
                    symbol = "BANKNIFTY"+str(ExpiryDate)+str(ExpiryMonth)+str(ExpiryYear)+"FUT"
                    DhanSymbol = "BANKNIFTY "+" "+str(ExpiryMonth)+" "+" FUT"
                    AliceSymbol = "BANKNIFTY "+str(ExpiryMonth)+" "+" FUT"
                    UpstoxSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"
                    FyresSymbol = "BANKNIFTY"+str(ExpiryYear)+str(ExpiryMonth)+"FUT"

                    token = 'select token from instruments where symbol="'+symbol+'"'
                    mycursor.execute(token)
                    tokenresult = mycursor.fetchone()
                    
                    #Buy_Order(str(symbol.replace("'", "")), str(tokenresult[0].replace("'", "")), "delta_trades", DhanSymbol)

                    trade = "INSERT INTO delta_bnf_fut_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SHORT', '30', '0', '"+str(Idx_Live)+"', '1', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                    mycursor.execute(trade)
                    mydb.commit()
                    
                    break

                
                else:
                    break
                



            if Position == "1":
                sql = "select * from delta_bnf_fut_orders ORDER BY DateTime DESC"
                mycursor.execute(sql)
                myresult = mycursor.fetchone()

                Type = myresult[2]


                if Type == "BUY":
                    if float(Latest) < float(Supertrend_0_4) and float(Latest) < float(Supertrend_0_8) and float(Latest) < float(ema1):

                        #Sell_Order(Symbol, Token, "Delta")

                        trade = "INSERT INTO delta_bnf_fut_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SELL', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break

                    if str(datetime.datetime.now()) >= str(data.date())+" 15:10:00.000000":
                        #Sell_Order(Symbol, Token, "Delta")

                        trade = "INSERT INTO delta_bnf_fut_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SELL', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        exit()


                    else:
                        break


                if Type == "SHORT":
                    
                    if float(Latest) > float(Supertrend_0_4) and float(Latest) > float(Supertrend_0_8) and float(Latest) > float(ema1):

                        #Sell_Order(Symbol, Token, "Delta")

                        trade = "INSERT INTO delta_bnf_fut_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SHORTEXIT', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        break

                    if str(datetime.datetime.now()) >= str(data.date())+" 15:10:00.000000":
                        #Sell_Order(Symbol, Token, "Delta")

                        trade = "INSERT INTO delta_bnf_fut_orders (Name, Token, Type, Qty, Price, IdxPrice, Position, DateTime, Strategy, SL) values ('BANKNIFTY_FUTURE', 'None', 'SHORTEXIT', '30', 'None', '"+str(Idx_Live)+"', '0', '"+str(datetime.datetime.now())+"', 'Delta', '0')"
                        mycursor.execute(trade)
                        mydb.commit()

                        exit()


                    else:
                        break

                else:
                    break            

            else:
                break