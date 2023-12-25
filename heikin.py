import pandas as pd

# Function to calculate Heikin-Ashi values
def calculate_heikin_ashi(df):
    ha_open = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    ha_close = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_high = df[['High', 'Open', 'Close']].max(axis=1)
    ha_low = df[['Low', 'Open', 'Close']].min(axis=1)

    return pd.DataFrame({'DateTime': df['DateTime'], 'Open': ha_open, 'High': ha_high, 'Low': ha_low, 'Close': ha_close})

# Read the input CSV file
input_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/bnf_5m.csv'
candlestick_data = pd.read_csv(input_file)

# Calculate Heikin-Ashi data
heikin_ashi_data = ta.ha(my_df["o"], my_df["h"], my_df['l'], my_df['c'])


# Write Heikin-Ashi data to a new CSV file
output_file = 'C://Xampp/htdocs/Algo_Trader/CSV_Files/heikin_bnf_5m.csv'
heikin_ashi_data.to_csv(output_file, index=False)

print(f'Heikin-Ashi data saved to {output_file}')
