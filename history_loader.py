# analysis of financial markets
from moexalgo import session, Ticker
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# получаем данные для авторизации на бирже: адрес почты и пороль при регистрации на Московской бирже
username = ""
password = ""
# авторизуемся на бирже
session.authorize(username, password)

def upload_history(start_date, end_date, stock, timeframes):
    # создаем рыночный инструмент
    financial_instrument = Ticker(stock)
    # получаем историю за период
    df = financial_instrument.candles(start=start_date, end=end_date, period=timeframes)        
    
    return df

STOCK = "RUAL"
TIMEFRAMES = ["1h", "10min"]
START_DATE = "2024-07-01"
END_DATE = "2024-07-19"

df_1h = upload_history(start_date=START_DATE, end_date=END_DATE, stock=STOCK, timeframes=TIMEFRAMES[0])
df_10min = upload_history(start_date=START_DATE, end_date=END_DATE, stock=STOCK, timeframes=TIMEFRAMES[1])

display(df_1h)
display(df_10min)
