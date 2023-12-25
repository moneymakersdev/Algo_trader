import pandas as pd

from stocktrends import indicators


df = pd.read_csv('CSV_Files/test.csv')
df.columns = [i.lower() for i in df.columns]
rows = 5

pnf = indicators.PnF(df)
pnf.box_size = 10
pnf.reversal_size = 3

lb = indicators.LineBreak(df)

print('\n\nLine break chart')
lb.line_number = 3
data = lb.get_ohlc_data()
print(data.tail(rows))