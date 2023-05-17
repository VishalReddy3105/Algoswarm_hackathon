from blueshift.api import symbol, order_target_percent, schedule_function, date_rules, time_rules, get_open_orders, cancel_order
import numpy as np 
import pandas as pd
import talib as ta

def initialize(context):
    """
    A function to define things to do at the start of the strategy
    """
    context.asset = symbol('HAL')
    # universe selection
    context.freq = "1minute"
    context.rsi_lookback = 30
    context.order_size = 1.0
    context.rsi_oversold = 30
    context.rsi_overbought = 70    
    context.stop_loss = 0.95
    context.stop_loss_trigerred = False
    schedule_function(rebalance, date_rules.every_day(), time_rules.every_hour())

def rebalance(context, data):
    orders = get_open_orders()
    for order in orders:
        cancel_order(order)
    prices = data.history(context.asset, 'close', context.rsi_lookback+1, '1min')
    rsi = ta.RSI(prices, timeperiod=context.rsi_lookback)
    ma = data.history(context.asset, 'close', 200, '1d').mean()
    if (prices[-1] > ma) and (rsi[-1] < context.rsi_oversold):
        order_target_percent(context.asset, 1.0)
    elif (prices[-1] < prices[-2]) and (rsi[-1] > context.rsi_overbought):
        order_target_percent(context.asset, -1.0)
    else :
        if context.stop_loss_trigerred:
            return
