import pandas as pd
import requests
from io import StringIO
import json


def Angel_Data(Symbol):
    # Load JSON data from a file
    json_file_path = 'Instru_Files/Smart_Api.json'  # Replace with your JSON file path
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Unable to decode JSON data - {str(e)}")
        exit(1)

    # Symbol to search for
    desired_symbol = Symbol  # Replace with the symbol you want

    # Filter data based on the desired symbol
    matching_tokens = [item['token'] for item in data if item.get('symbol') == desired_symbol]

    # Print the token numbers for the matching symbol
    if matching_tokens:
        #print(f"Token numbers for symbol {desired_symbol}:")
        for token in matching_tokens:
            return token
    else:
        return "None"




def Angle_Lotsize(Symbol):
    # Load JSON data from a file
    json_file_path = 'Instru_Files/Smart_Api.json'  # Replace with your JSON file path
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Unable to decode JSON data - {str(e)}")
        exit(1)

    # Symbol to search for
    desired_symbol = Symbol  # Replace with the symbol you want

    # Filter data based on the desired symbol
    matching_tokens = [item['lotsize'] for item in data if item.get('symbol') == desired_symbol]

    # Print the token numbers for the matching symbol
    if matching_tokens:
        #print(f"Token numbers for symbol {desired_symbol}:")
        for token in matching_tokens:
            return token
    else:
        return "None"





def Dhan_Data(Symbol):
    # Load CSV data into a DataFrame
    csv_file_path = 'Instru_Files/Dhan_Insru.csv'  # Replace with your CSV file path
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        #print(f"Error: CSV file not found at {csv_file_path}")
        exit(1)
    except pd.errors.ParserError as e:
        #print(f"Error: Unable to parse CSV data - {str(e)}")
        exit(1)

    # Symbol to search for
    desired_symbol = Symbol

    # Filter data based on the desired symbol
    matching_tokens = df.loc[df['SEM_CUSTOM_SYMBOL'] == desired_symbol, 'SEM_SMST_SECURITY_ID']

    # Print the token numbers for the matching symbol
    if not matching_tokens.empty:
        #print(f"Token numbers for symbol {desired_symbol}:")
        for token in matching_tokens:
            return token
    else:
        return "None"




def Upstox_Data(Symbol):
    # Load CSV data into a DataFrame
    csv_file_path = 'Instru_Files/upstox.csv'  # Replace with your CSV file path
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        #print(f"Error: CSV file not found at {csv_file_path}")
        exit(1)
    except pd.errors.ParserError as e:
        #print(f"Error: Unable to parse CSV data - {str(e)}")
        exit(1)

    # Symbol to search for
    desired_symbol = Symbol

    # Filter data based on the desired symbol
    matching_tokens = df.loc[df['tradingsymbol'] == desired_symbol, 'instrument_key']

    # Print the token numbers for the matching symbol
    if not matching_tokens.empty:
        #print(f"Token numbers for symbol {desired_symbol}:")
        for token in matching_tokens:
            return token
    else:
        return "None"





def Alice_Data(Symbol):
    # Load JSON data from a file
    json_file_path = 'Instru_Files/Alice_Insru.json'  # Replace with your JSON file path
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Unable to decode JSON data - {str(e)}")
        exit(1)

    # Symbol to search for
    desired_symbol = Symbol  # Replace with the symbol you want

    # Filter data based on the desired symbol
    matching_tokens = [item["Trading Symbol"] for item in data if item.get("Formatted Ins Name") == desired_symbol]

    # Print the token numbers for the matching symbol
    if matching_tokens:
        print(f"Token numbers for symbol {desired_symbol}:")
        for token in matching_tokens:
            return token
    else:
        return "None"




def MOSL_Data(Symbol):
    # Load CSV data into a DataFrame
    csv_file_path = 'Instru_Files/Motilal_Instru.csv'  # Replace with your CSV file path
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        #print(f"Error: CSV file not found at {csv_file_path}")
        exit(1)
    except pd.errors.ParserError as e:
        #print(f"Error: Unable to parse CSV data - {str(e)}")
        exit(1)

    # Symbol to search for
    desired_symbol = Symbol

    # Filter data based on the desired symbol
    matching_tokens = df.loc[df['scripname'] == desired_symbol, 'scripcode']

    # Print the token numbers for the matching symbol
    if not matching_tokens.empty:
        #print(f"Token numbers for symbol {desired_symbol}:")
        for token in matching_tokens:
            return token
    else:
        return "None"

