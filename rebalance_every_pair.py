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
    print(check[['symbol','orderId','origQty','type','price','side']])

def rebalance():
    coin_1,coin_2,coin_pair = input_coin()
    ask = pd.DataFrame(data=client.get_order_book(symbol=coin_pair)).loc[0,"asks"]
    bid = pd.DataFrame(data=client.get_order_book(symbol=coin_pair)).loc[0,"bids"]
    BTC = float(client.get_asset_balance(asset=coin_2)['free'])/float(client.get_recent_trades(symbol=coin_pair)[0]['price'])
    print(coin_2," =",BTC,coin_1)
    XLM = float(client.get_asset_balance(asset=coin_1)['free'])
    print(coin_1," =",XLM,coin_1)
    quantity = int('%.d' % (int((float('%.1f' % (abs(BTC-XLM)/2)))*0.9995)))
    print(quantity)
    if quantity > (0.1*XLM+0.1):
        if BTC < XLM : 
            client.order_limit_sell(symbol=coin_pair,quantity = float(quantity), price= ('%.8f' % (float(ask[0]))))
            after_rebalance(coin_1,coin_2,coin_pair)
        elif XLM < BTC:
            client.order_limit_buy(symbol=coin_pair,quantity = float(quantity), price = ('%.8f' % (float(bid[0]))))
            after_rebalance(coin_1,coin_2,coin_pair)
    else:
        print("The order is too small to rebalance")
     
i = int(input("How many pair do you to rebalance \nFill your number: "))
for i in range(0,i):
    rebalance()