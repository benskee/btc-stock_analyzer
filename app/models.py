from . import db
import requests
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Chart(db.Model):
    now = db.Column(db.String, primary_key=True)
    stock = db.Column(db.String(4))
    date_start = db.Column(db.String(8))
    date_end = db.Column(db.String(8))

def generate_graph():
    df = pd.read_csv('amzn.csv')

    btc_df = pd.read_csv('btc.csv')

    df_btc = btc_df[0:437]
    dfbtc = df_btc.rename(columns=lambda x: x.replace(' ', '').lower(), inplace=True)

    df_stock = df[0:316]

    for date in range(len(df_stock.Date)):
        df_stock.Date[date] = datetime.strptime(df_stock.Date[date], '%m/%d/%Y').date()

    for date in range(len(df_btc.date)):
        df_btc.date[date] = datetime.strptime(df_btc.date[date], '%m/%d/%Y').date()

    for c in [' Close/Last', ' Open', ' High', ' Low']:
        df_stock[c] = df_stock[c].str.replace('$', '').astype(float)

    df_stock.rename(columns=lambda x: x.replace(' ', '').lower(), inplace=True)

    avg_list = []
    for date in df_stock.index:
        avg = (df_stock.high[date] + df_stock.low[date])/2
        avg_list.append(avg)

    btc_list = []
    for date in df_btc.index:
        avg = round(((df_btc.high[date] + df_btc.low[date])/2), 2)
        btc_list.append(avg)

    df_btc['btc_avg'] = btc_list
    df_stock['stock_avg'] = avg_list

    df_premium = df_btc.drop(columns=['close/last', 'volume', 'open', 'high', 'low'], axis=1, inplace=False)

    df_premium.set_index("date", inplace=True)
    df_stock.set_index("date", inplace=True)

    df_premium['stock_avg'] = df_stock['stock_avg']
    df_premium = df_premium.reset_index()

    sats_price_list = []
    for date in df_premium.index:
        if df_premium.stock_avg[date]:
            sats_price = float(format(1/df_premium.btc_avg[date] * df_premium.stock_avg[date] * 10000, '.2f'))
            sats_price_list.append(sats_price)

    df_premium['sats_price'] = sats_price_list

    plt.subplots(figsize=(15, 12))
    plt.grid(True)
    plt.plot(df_premium.date[:10], df_premium.sats_price[:10].fillna(method='ffill'), color='orange')
    plt.plot(df_premium.date[:10], df_premium.stock_avg[:10].fillna(method='ffill'), color='green')
    plt.plot(df_premium.date[:10], df_premium.btc_avg[:10].fillna(method='ffill'), color='gray')
    plt.title('Daily Stock Price in Bitcoin', fontsize=18)
    plt.ylabel('Price in Tens of Thousands of Sats | Dollars', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.savefig('image_1.png')
    plt.legend(['Bitcoin', 'Dollars'], loc=2);