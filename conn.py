import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="V7B9S7@Ocean",
  database="dc_bull",
)

mycursor = mydb.cursor(buffered=True)
