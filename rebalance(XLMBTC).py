#This code I create the library to rebalance between two crytrocurrencies as XLM and BTC, which is same idea with liqulity swap. Plase feel free to comment below my library
#The rebalance model can apply to use more product which reduce more risk and let to asset allocation model.
#I hope you enjoin to adjust my code. Moreover, you can use while loop to rebalance everyday same as liqudity-sawp in the binance or more frequency than 1 time a day.

import pandas as pd
import binance.client
from binance.client import Client
import time
from binance.enums import *
from binance.helpers import round_step_size
from time import sleep

api_key = "fill up by your self by https://www.binance.com/en/support/faq/360002502072"
api_secret = "fill up by your self by https://www.binance.com/en/support/faq/360002502072"
client = Client(api_key, api_secret)

def after_rebalance(coin_1,coin_2,coin_pair):
    print("Your limited order is :")
    check = pd.DataFrame(data=client.get_open_orders(symbol=coin_pair))
    print(check[['symbol','orderId','origQty','type','price','side']])
    print("After rebalance")
    sleep(10)
    BTC_1 = float(client.get_asset_balance(asset=coin_2)['free'])/float(client.get_recent_trades(symbol=coin_pair)[0]['price'])
    print("If you want to collect XLM, you should look at this results.")
    print("Your Net",coin_2," = ",BTC_1,coin_1)
    XLM_1 = float(client.get_asset_balance(asset=coin_1)['free'])
    print("Your Net",coin_1," = ",XLM_1,coin_1,"\nTotal = ",XLM_1+BTC_1)
    print("If you want to collect BTC, you should look at this results.")
    BTC_1 = float(client.get_asset_balance(asset=coin_2)['free'])
    print("Your Net",coin_2," = ",BTC_1,coin_2)
    XLM_1 = float(client.get_asset_balance(asset=coin_1)['free'])*float(client.get_recent_trades(symbol=coin_pair)[0]['price'])
    print("Your Net",coin_1," = ",XLM_1,coin_2,"\nTotal = ",XLM_1+BTC_1)
    
def rebalance():
    ask = pd.DataFrame(data=client.get_order_book(symbol='XLMBTC')).loc[0,"asks"]
    bid = pd.DataFrame(data=client.get_order_book(symbol='XLMBTC')).loc[0,"bids"]
    BTC = float(client.get_asset_balance(asset='BTC')['free'])/float(client.get_recent_trades(symbol='XLMBTC')[0]['price'])
    print("BTC =",BTC," XLM")
    XLM = float(client.get_asset_balance(asset='XLM')['free'])
    print("XLM =",XLM," XLM")
    quantity = int('%.d' % ((abs(BTC-XLM)/2)*0.9995))

    if BTC + 20 < XLM : 
        client.order_limit_sell(symbol="XLMBTC",quantity = int(quantity), price= ('%.8f' % (float(ask[0]))))
        after_rebalance("XLM","BTC","XLMBTC")
    elif XLM +20 < BTC:
        client.order_limit_buy(symbol="XLMBTC",quantity = int(quantity), price = ('%.8f' % (float(bid[0]))))
        after_rebalance("XLM","BTC","XLMBTC")
    else:
        print("The order is too small to rebalance")
    
    
rebalance()
