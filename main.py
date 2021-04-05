# MODULES
from os import system
import time
import datetime
from datetime import datetime
import ast
import os.path
# - basic
import numpy as np 
import pandas as pd 
# - Binance 
import binance
from binance.client import Client
from binance.websockets import BinanceSocketManager
#from binance import BinanceAPIException

'''
# grant access
def test_connection(k,s):
    try:
        client = Client(k,s)
        test = client.get_account()
    except:
        print('Can not connect with adresses you gave,\nCheck if you gave them in the right order, first key then secret. \nAlso, you may have missed a character.')
        grant_access = False
        return grant_access, client
    else:
        print(f'successfully connected!\n')
        grant_access = True
        return grant_access, client
# vars
user_api_key = ''
user_api_secret = ''
follower_api_key = ''
follower_api_secret = ''
grant_access = False
while grant_access == False:
    system('cls')
    print('Do not show anyone these adresses!')
    user_api_key = input('What is your api KEY? - ')
    user_api_secret = input('What is your api SECRET? - ')
    print('Testing connection...')
    grant_access, user_client = test_connection(user_api_key,user_api_secret)
    time.sleep(5)
grant_access = False
while grant_access == False:
    system('cls')
    print('Do not show anyone these adresses!')
    print(f'user api key - {user_api_key}')
    print(f'user api secret - {user_api_secret}')
    follower_api_key = input('What is your followers api KEY? - ')
    follower_api_secret = input('What is your followers api SECRET? - ')
    if follower_api_key == user_api_key or follower_api_key == user_api_secret:
        print('You can not connect to the same address')
        time.sleep(5)
    elif follower_api_secret == user_api_key or follower_api_secret == user_api_secret:
        print('You can not connect to the same address')
        time.sleep(5)
    else: 
        print('Testing connection...')
        grant_access, follower_client = test_connection(follower_api_key,follower_api_secret)
        time.sleep(5)
print('You are connected.')
'''

def create_start_time():
    # Create start time
    # create timestamp instead.. difference in timezones might interfear??.
    '''
    time = datetime.now()
    time_stamp = str(datetime.timestamp(time))
    readable_ts = time_stamp[:-3].replace('.','')
    start_time = int(readable_ts)
    print(start_time)
    '''
    new_orders = user_client.futures_get_all_orders()
    orders = pd.DataFrame(new_orders)
    start_time = int(orders['time'][-1:])
    start_time += 1 # add one e milisecond
    return start_time 

def SavedInfo():
    # read save file
    while True:
        if os.path.isfile('savedInfo.txt'):
            print ("File exist")
        else:
            print ("File does not exist")
            save = open("savedinfo.txt","w+")
            save.write('{0:0}')
            save.close()
        try:
            save = open("savedinfo.txt","r")
        except IOError:

            print('could not parse data')
        else:
            unfilled_orders_raw = save.readlines()
            save.close()
            unfilled_orders = ast.literal_eval(unfilled_orders_raw[0])
            unfilled_orders = monitor_orders(unfilled_orders)
            break
    print('opened saved file')
    return unfilled_orders

def monitor_orders(unfilled_orders):
    # moniter unfilled orders
    all_orders = user_client.futures_get_all_orders()
    for order in all_orders:
        order_id = order['orderId']
        if order_id in unfilled_orders:
            if order['status'] == 'CANCELED':
                follower.cancel_order(order,unfilled_orders)
                del unfilled_orders[order_id]
            elif order['orderId'] == 'FILLED':
                del unfilled_orders[order_id]
            else:
                pass
                # Order is in the same condition as previously
    '''
    iterate = 0
    while iterate <= len(all_orders):
        order_id = all_orders[iterate]['orderId']
        # unfilled 
        if order_id in unfilled_orders:
            if all_orders[iterate]['status'] == 'CANCELED':
                follower.cancel_order(all_orders[iterate])
                del unfilled_orders[order_id]
            elif all_orders[iterate]['orderId'] == 'FILLED':
                del unfilled_orders[order_id]
            else:
                pass
                # Order is in the same condition as previously
        iterate += 1
    '''
    save = open("savedinfo.txt","w")
    save.write(str(unfilled_orders))
    save.close()
    '''
    unfilled_orders_pd = pd.DataFrame(unfilled_orders)   
    unfilled_orders_pd.to_csv('unfilled_orders.csv')
    '''
    #
    return unfilled_orders

# check and copy
def check_user(unfilled_orders,lastUpdate):
    
    stop_options = ['STOP','STOP_MARKET','TAKE_PROFIT','TAKE_PROFIT_MARKET','TRAILING_STOP_MARKET']

    new_orders = user_client.futures_get_all_orders(startTime=lastUpdate)
    print(lastUpdate)
    print(new_orders)
    print(unfilled_orders)
    x = 1
    if len(new_orders) != 0: # Check if there are any new orders
        print('new order')
        for order in new_orders:
            '''
            neat_order = f'{x}.\n'
            for data in order:
                neat_order += f'{data}: {order[data]}'
                neat_order += '\n'
            
            unfilled_orders = [2343255,32535325,326236236,62363]
            unfilled_orders = [(1231242,2421452),(123231,424125),(john,follower)]
            unfilled_orders = {21324:12412,214214:241424,124214:21442,john:follower} this one
            '''
            
            # create new order 
            if order['type'] == 'MARKET': 
                unfilled_orders = follower.create_order(order,unfilled_orders)
            elif order['type'] in stop_options:
                unfilled_orders[order['orderId']] = None
                unfilled_orders = follower.create_order(order,unfilled_orders)
            elif order['type'] == 'LIMIT':
                unfilled_orders[order['orderId']] = None
                unfilled_orders = follower.create_order(order,unfilled_orders)
            print(f'previous last update - {lastUpdate}')
            lastUpdate = (order['time'] + 1) # update to current order 
            print(f'lastUpdate - {lastUpdate}')
            # if john manged to cancel a limit or stoploss order just before it gets filled
            # and gets filled on follower account, how to fix this?.

            # out of sync checker. warning pop up.
            
            
            x += 1
    else:
        print('no new orders')
    return unfilled_orders, lastUpdate


class Follower():

    def __init__(self):
        pass
    def create_order(self,order,unfilled_orders):
        stop_options = ['STOP','STOP_MARKET','TAKE_PROFIT','TAKE_PROFIT_MARKET','TRAILING_STOP_MARKET']
        # info
        symbol = order['symbol']
        side = order['side']
        order_type = order['type']
        order_id = order['orderId']
        order_time = order['time']
        price = order['price']
        stopPrice = order['stopPrice']
        time_in_force = order['timeInForce']

        reduceOnly = order['reduceOnly'] # fix reduce only

        if order_type == 'TRAILING_STOP_MARKET':
            callbackRate = order['priceRate']

        # adjust leverage
        position_information = user_client.futures_position_information()
        for i in position_information:
            if i['symbol'] == symbol:
                client_leverage = int(i['leverage'])
        follower_client.futures_change_leverage(symbol=symbol,leverage=client_leverage,timestamp=order_time)

        # calculate amount
        other_order_info_raw = user_client.futures_exchange_info()
        other_order_info_sym = other_order_info_raw['symbols']
        for i in other_order_info_sym:
            if i['symbol'] == symbol:
                stepSize = float(i['filters'][1]['stepSize'])
                minQty = float(i['filters'][1]['minQty'])
        
        data = pd.DataFrame(user_client.futures_mark_price())
        mark_price_raw = list(np.where(data['symbol'] == symbol,data['markPrice'],0))
        for i in mark_price_raw:
            
            if type(i) == str:
                #print(i)
                mark_price = float(i)

        user_balance = float(user_client.futures_account_balance()[0]['balance'])
        follower_balance = float(follower_client.futures_account_balance()[0]['balance'])
        order_quant = float(order['origQty'])        
        percentage = (((float(order['origQty']) * float(mark_price)) / int(client_leverage)) / user_balance)
        trade_quantity_raw = (((float(follower_client.futures_account_balance()[0]['balance']) * percentage) / mark_price) * client_leverage)
        #print(f'({order_quant} * {mark_price}) / {client_leverage}) / {user_balance} = {percentage} | {follower_balance} * {percentage} = {trade_quantity_raw}')
        rounder = {0.001:round(trade_quantity_raw,3),0.01:round(trade_quantity_raw,2),0.1:1,1:round(trade_quantity_raw)}
        
        trade_quantity = rounder[stepSize]
        
        print(f'{symbol} {side} {order_type} {order_id} {order_time} {price} {stopPrice} {client_leverage} {trade_quantity}')
        
        
        if order['type'] == 'MARKET':
            lap = 0
            while True:
                try:
                    follower_client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=trade_quantity)
                except: #BinanceAPIException as e:
                    #print(e.status_code)
                    #print(e.message)
                    print('Couldnt create order')
                    time.sleep(1)
                    lap += 1
                    if lap >= 3:
                        #out of sync notifier
                        print('Out of sync')
                        break
                else:
                    break
        elif order['type'] == 'LIMIT':
            lap = 0
            while True:
                try:
                    follower_client.futures_create_order(symbol=symbol, price=price, side=side, type=order_type, quantity=trade_quantity,timeInForce=time_in_force)
                except: #BinanceAPIException as e:
                    #print(e.status_code)
                    #print(e.message)
                    print('Couldnt create order')
                    time.sleep(1)
                    lap += 1
                    if lap >= 3:
                        #out of sync notifier
                        print('Out of sync')
                        break
                else:
                    break
            #order_time -= 1
            while True:
                try:
                    follower_orders = follower_client.futures_get_all_orders(startTime=order_time)
                    print('follower order pair:')
                    print(follower_orders)
                    unfilled_orders[order_id] = follower_orders[0]['orderId']
                except:
                    print('order not found yet')
                    time.sleep(1)
                else:
                    break
        elif order['type'] in stop_options:
            lap = 0
            while True:
                try:
                    if order['type'] != 'TRAILING_STOP_MARKET':
                        follower_client.futures_create_order(symbol=symbol,side=side,type=order_type,stopPrice=stopPrice,quantity=trade_quantity,timeInForce=time_in_force)
                    else:
                        follower_client.futures_create_order(symbol=symbol,side=side,type=order_type,stopPrice=stopPrice,quantity=trade_quantity,timeInForce=time_in_force,priceRate=callbackRate)
                except:# BinanceAPIException as e:
                    #print(e.status_code)
                    #print(e.message)
                    print('Couldnt create order')
                    time.sleep(1)
                    lap += 1
                    if lap >= 3:
                        #out of sync notifier
                        print('Out of sync')
                        break
                else:
                    break
            #order_time -= 1
            while True:
                try:
                    follower_orders = follower_client.futures_get_all_orders(startTime=order_time)
                    print('follower order pair:')
                    print(follower_orders)
                    unfilled_orders[order_id] = follower_orders[0]['orderId']
                except:
                    print('order not found yet')
                    time.sleep(1)
                else:
                    break
        else:
            print('unneccessary order call')

        return unfilled_orders
        # needs info
        # create binance order
        # adjust leverage futures_change_leverage(**params)
        # calculate amount
        # pair followers orderID and johns s one that is johns and one that is followers that "is the same order"
    
    #def set_stop_loss(symbol,mark_price,amount):
    #def close_position(symbol,mark_price,amount,side):
    
    def cancel_order(self,order,unfilled_orders):
        #symbol = order['symbol']
        client_orderId = order['orderId']
        timestamp = (order['time'] - 1)
        follower_orderId = unfilled_orders[client_orderId]
        orders = follower_client.futures_get_all_orders(startTime=timestamp)
        for follower_order in orders:
            if follower_order['orderId'] == follower_orderId:
                symbol = follower_order['symbol']
                timestamp = follower_order['time']
                lap = 0
                while True:
                    try:
                        follower_client.futures_cancel_order(symbol=symbol,orderId=follower_orderId,timestamp=timestamp)
                    except: #BinanceAPIException as e:
                        #print(e.status_code)
                        #print(e.message)
                        print(f'could not cancel order - {follower_orderId}')
                        time.sleep(1)
                        lap += 1
                        if lap >= 3:
                            print('out of sync')
                            break
                    else:
                        break
            else:
                pass 

follower_client = Client(follower_key,follower_secret)
follower = Follower()

run = True
start_time = create_start_time()
lastUpdate = start_time
unfilled_orders = SavedInfo() # read saved_info.txt check if still relevant


while run == True:

    time.sleep(1)
    
    # web app information 
    # what to connect to
    # what coins to use and not to use
    # run a flask script that save info to a file which we read here.
    # a dictionary of all coins, enables and disables this will block disabled coins.

    # check user & update follower
    unfilled_orders,lastUpdate = check_user(unfilled_orders,lastUpdate)
    # monitor orders
    unfilled_orders = monitor_orders(unfilled_orders)
