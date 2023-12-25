import pandas as pd
import mysql.connector
from mysql.connector import Error
import csv
import pandas as pd


#with open('OpenAPIScripMaster.json', encoding='utf-8') as inputfile:
#    df = pd.read_json(inputfile)
#
#df.to_csv('Angle_Instu.csv', encoding='utf-8', index=False)



connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="vivek123",
  database="dc_bull",
  autocommit=True
)

cursor = connection.cursor(buffered=True)

csv_file_path = "data/bnf_trades.csv"
data = pd.read_csv(csv_file_path)

data = data.where(pd.notna(data), None)


insert_query = f"INSERT INTO {'trades'} ({', '.join(data.columns)}) VALUES ({', '.join(['%s'] * len(data.columns))})"
values = [tuple(row) for index, row in data.where(pd.notna(data), None).iterrows()]


try:
    cursor.executemany(insert_query, values)
    connection.commit()
    print("Rows inserted successfully")
except Error as e:
    print("Error inserting rows", e)

# Close the cursor and the connection
cursor.close()
connection.close()
print("MySQL connection closed")


