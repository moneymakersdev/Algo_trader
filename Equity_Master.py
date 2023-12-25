from conn import *
import pandas as pd
import datetime
from datetime import date
from Live_Price import *
from Expiry_Date import *
from Place_Order import *
import pandas_ta as ta


    

def calculate_ema(data, period):
    ema = data.ewm(span=period, adjust=False).mean()
    return ema


def ema_1(Symbol):
    while True:
            # Load data from CSV file
        csv_file = Symbol  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'High'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 121  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return format(round(last_ema_value, 2))
        #df = pd.read_csv('bnf_5m.csv')
        #ema = ta.ema(df['Close'], length=5)

        #return ema.iloc[-1]



def old_ema_1(Symbol):
    while True:
            # Load data from CSV file
        csv_file = Symbol  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'High'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 121  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-2]

        return format(round(last_ema_value, 2))

        #df = pd.read_csv('bnf_5m.csv')
        #ema = ta.ema(df['Close'], length=5)

        #return ema.iloc[-2]




def ema_2(Symbol):
    while True:
            # Load data from CSV file
        csv_file = Symbol  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Low'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 121  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-1]

        return format(round(last_ema_value, 2))
        #df = pd.read_csv('bnf_5m.csv')
        #ema = ta.ema(df['Close'], length=5)

        #return ema.iloc[-1]


def old_ema_2(Symbol):
    while True:
            # Load data from CSV file
        csv_file = Symbol  # Replace with the path to your CSV file
        data = pd.read_csv(csv_file)

            # Specify the column containing the data for which you want to calculate EMA
        data_column = 'Low'  # Replace with the actual column name

            # Specify the EMA period
        ema_period = 121  # Replace with the desired EMA period

            # Calculate EMA
        data['EMA'] = calculate_ema(data[data_column], ema_period)

            # Print only the last EMA value
        last_ema_value = data['EMA'].iloc[-2]

        return format(round(last_ema_value, 2))

        #df = pd.read_csv('bnf_5m.csv')
        #ema = ta.ema(df['Close'], length=5)

        #return ema.iloc[-2]



def Latest_Close(Symbol):
    csv_file = str(Symbol)
    df = pd.read_csv(csv_file)
    
    if not df.empty:
        last_row = df.iloc[-1]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None


def Previus_Close(Symbol):
    csv_file = str(Symbol)
    df = pd.read_csv(csv_file)
    
    if not df.empty:
        last_row = df.iloc[-2]
        last_close_price = last_row['Close']  # Replace 'Close' with your actual close price column name
        return last_close_price
    else:
        return None



symbol =['C://Xampp/htdocs/Algo_Trader/CSV_Files/TVS.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/M_M.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/HDFCBANK.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/INDUSINDBK.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/INFY.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/HAVELLS.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/SBILIFE.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ICICIGI.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/CHOLAFIN.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/HCLTECH.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/MUTHOOTCAP.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/TECHM.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/CIPLA.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/SUNPHARMA.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/MCDOWELL-N.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/GODREJCP.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ICICIBANK.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ADANIGREEN.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/VBL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/SBICARD.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/JSWSTEEL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/IRFC.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/JINDALSTEL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/LICI.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/TATAMOTORS.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/HDFCLIFE.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ATGL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ZYDUSLIFE.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/SBIN.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/DLF.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/BERGEPAINT.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/MARICO.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/DABUR.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ICICIPRULI.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/HINDALCO.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/ITC.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/TATAMTRDVR.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/AMBUJACEM.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/WIPRO.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/COALINDIA.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/TATAPOWER.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/NTPC.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/BPCL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/AWL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/MUTHOOTFIN.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/AXISBANK.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ADANIPORTS.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/BHARTIARTL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/KOTAKBANK.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/ONGC.csv', 
        'C://Xampp/htdocs/Algo_Trader/CSV_Files/POWERGRID.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/TATASTEEL.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/TATACONSUM.csv', 'C://Xampp/htdocs/Algo_Trader/CSV_Files/UPL.csv']



while True:
    data = datetime.datetime.now()
    
    if str(datetime.datetime.now()) > str(data.date())+" 10:15:10.000000":
        print("Market is Closed")
        sleep(1)
    if str(datetime.datetime.now()) <= str(data.date())+" 10:15:10.000000":

        while True:

            for I in range(len(symbol)):
                stocks= symbol[I]
                Live_Ema1 = ema_1(stocks)
                Live_Ema2 = ema_2(stocks)
                Old_Ema1 = old_ema_1(stocks)
                Old_Ema2 = old_ema_2(stocks)
                Lastest  = Latest_Close(stocks)
                Old_Close = Previus_Close(stocks)

                #print(stocks+" Latest: "+str(Live_Ema1)+" Ema1: "+str(Live_Ema1))
                #print(stocks+" Lastest: "+str(Live_Ema2)+" Ema2: "+str(Live_Ema2))

                #sql = "select * from trades ORDER BY DateTime DESC"
                #mycursor.execute(sql)
                #myresult = mycursor.fetchone()
                #Position = myresult[6]
                #print("Position "+str(Position))       

                Position = "0"

                if Position == "0":
                    if float(Lastest) > float(Live_Ema1) and float(Old_Close) < float(Live_Ema1):
                        
                        print(stocks+" Latest: "+str(Live_Ema1)+" Ema1: "+str(Live_Ema1))

                    else:
                        exit

                    exit