from conn import *

trade = "DELETE FROM running_bots where Orders='0'"
mycursor.execute(trade)
mydb.commit()

update = "update api set TOTP_Secret='None', Client_ID='None' where Broker='ICICI' or Broker='UPSTOX' or Broker='FYERS'"
mycursor.execute(update)
mydb.commit()

