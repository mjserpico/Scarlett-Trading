# -*- coding: utf-8 -*-
"""
@author: Michael
"""
#
#Standard Python Libs
import mysql.connector
from datetime import timedelta
import datetime
import logging
import sys
import time
import pandas as pd
import numpy as np
import os
import csv

#Scarlett Trading Lib
import datalink  #universal logins for environment
#IB Library
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 

"""
List of Symbols to find Relative Strength
Lists begin with [0] in python
"""

count = 0

#Quantopian Library
#import zipline as zl
# test test test
logging.basicConfig(filename='RelativeStrengthBull' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('RelativeStrengthBull' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

masteraccount = 'DU1240329'
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connecting To Database')

def reply_handler(msg):
    #test = msg.value
    print(msg)
    logger.debug('Reply: %s', msg)
    
def error_handler(msg):
    """Handles the capturing of error messages"""
    print(msg)
    logger.debug('Error Reply: %s', msg)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def make_long_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty[0]
        logger.debug('qty is %s', qty[0])
        logger.debug('qty type is %s', type(qty))
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Long Order Function')
        logger.debug('Limit Value is %s', limit)
       	# ENTRY   A simple stop order
        order.m_orderType = 'STP'
        logger.debug('In Long Order Function when Limit is 1')
        logger.debug('Action is %s', action)
            	# Rounding is due to FX, we cannot create an order with bad price, and FX book increments at 0.00005 only!
                #order.m_lmtPrice  = limit - int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
        logger.debug('In Buy action')
        
        lmtPrice = float(truncate((float(yHigh[0]) + (float(ATRentrymultiple[0])*float(ATRVal[0]))),2))
        logger.debug('Buy Stop Limit"Limit" Price or better to buy %s', lmtPrice)
        float(lmtPrice)
        logger.debug('lmt price type is %s', type(lmtPrice))
        
        order.m_lmtPrice  = lmtPrice
        
        stopPrice = float(truncate((float(yHigh[0]) + (float(ATRentrymultiple[0])*float(ATRVal[0]))),2))
        logger.debug('Buy Stop Limit"Stop" Price to fire a buy order %s', stopPrice)
        float(stopPrice)
        logger.debug('stop price type is %s', type(stopPrice))
        order.m_auxPrice = stopPrice
       
        order.m_triggerMethod = 2
        order.m_parentId = parentId
        order.m_account = masteraccount
        logger.debug('Buy Upper Limit Price %s', order.m_lmtPrice)
        logger.debug('Buy Upper Limit Type %s', type(order.m_lmtPrice))
        logger.debug('Stop Entry Trigger Price %s ', stopPrice)
        logger.debug('Stop Entry Trigger Type %s ', type(stopPrice))
        logger.debug('Parent ID %s', order.m_parentId)
        logger.debug('Account is %s', order.m_account)
        order.m_transmit = transmit
        return order    
        
def create_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_localSymbol = symbol;
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = 'USD'
    return contract
    logger.debug('Contract created')

cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connecting To Database')


#f = open('relativestrengthrank' + str(datetime.date.today()) +'.csv')
#csv_f = csv.reader(f)

#for row in csv_f:
#    print(row)
yesterday = datetime.date.today() - timedelta(1)
f = open('C:/Program Files/Serpico/bin/relativestrengthrank' + str(yesterday) +'.csv')
#f = open('relativestrengthrank' + str(yesterday) +'.csv')
csv_f = csv.reader(f)

for row in csv_f:
    Ticker = row
    logger.debug('Ticker is %s', Ticker[0])
    query = ("SELECT max(ID) from " + Ticker[0])
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (ID) in cur:
        ID1 = ID
        logger.debug('ID1 is %s', ID1)
    
    #MovingAverage
    query = ("SELECT MovingAvgValue from hasPosition where CCY = \'" + Ticker[0] +"\';")
    print(query)
    cur.execute(query)
    for (MovingAvgValue) in cur:
        MovAvg = MovingAvgValue
        logger.debug('MovingAvgValue is %s', MovAvg[0])
    #ATRValue   
    query = ("SELECT ATRValue from hasPosition where CCY = \'" + Ticker[0] +"\';")
    cur.execute(query)
    for (ATRValue) in cur:
        ATRVal = ATRValue
        logger.debug('ATRValue is %s', ATRVal)
    
    #ATR Entry Multiplier    
    query = ("Select EntryATRMultiple from hasPosition where CCY = \'" + Ticker[0] +"\';")
    cur.execute(query)
    for (EntryATRMultiple) in cur:
        ATRentrymultiple = EntryATRMultiple
        logger.debug('ATRentrymultiple is %s', ATRentrymultiple)
    
    #Yesterday's High
    query = ("SELECT High from " + Ticker[0] + " where ID = " + str(ID1[0]) + ";")
    cur.execute(query)
    for (High) in cur:
        yHigh = High
        logger.debug('yesterday High is %s', yHigh[0])
    
    #EntryPending
    query = ("SELECT EntryPending from hasPosition where CCY = \'" + Ticker[0] +"\';")
    cur.execute(query)
    for (EntryPending) in cur:
        EntryPend = EntryPending
        logger.debug('Entry Pending is %s', EntryPend)
    
    #Max Quantity
    query = ("SELECT Qtylimit from hasPosition where CCY = \'" + Ticker[0] +"\';")
    cur.execute(query)
    for (QtyLimit) in cur:
        maxQty = QtyLimit
        logger.debug('Max Qty is %s', maxQty)
    
    #Yesterday's Close
    query = ("SELECT Close from " + Ticker[0] + " where ID = " + str(ID1[0]) + ";")
    cur.execute(query)
    for (Close) in cur:
        yClose = Close
        logger.debug('yesterdays Close is %s', yClose[0])
    
    #Order ID
    query = ("SELECT max(idOrders) from Orders;")
    cur.execute(query)
    for (idOrders) in cur:
        OID = idOrders
        logger.debug('OLD Order ID is %s', OID)
    
    logger.debug('yClose %s', yClose[0])
    logger.debug('EntryPend is %s', EntryPend[0])
    logger.debug('Mov Avg %s', MovAvg[0])
    #If No Entry is already Pending and yesterday's Close is above the Moving Average then the Stock filtered is eligible for trading    
    if (float(EntryPend[0]) == 0 and float(yClose[0]) > float(MovAvg[0])): #
        logger.debug('Valid setup Found')
        #TWS Connection
        conn = Connection.create(port=4002, clientId=999)
        conn.registerAll(reply_handler)
        conn.connect()
        logger.debug('Connected to Database')
        #time.sleep(1) #give IB time to send us messages
        
        #Create entry pending in hasPosition Table
        query = ("UPDATE hasPosition SET EntryPending = " + "1" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("SELECT StopQty from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (StopQty) in cur:
            Shares = StopQty
            logger.debug('Shares is %s', Shares)
        
        #Order Query 
        idOrder = OID[0] + 1
        
        Date = datetime.date.today()
        yesterday = Date #Take 1 Day back                    
        month = (str(0) + str(yesterday.month))
        day = (str(0)+ str(yesterday.day))
        yesterday3 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
        logger.debug('Todays date is %s', yesterday3)
        Date = yesterday3
        
        logger.debug('Shares is %s', Shares[0])
        logger.debug('maxQty is %s', maxQty[0])
        logger.debug('Shares type is %s', type(Shares[0]))
        logger.debug('maxQty type is %s', type(maxQty[0]))
        ##Compare Max Quantity to calculated quantity
        if float(Shares[0]) > float(maxQty[0]):
            SharesMax = maxQty
            logger.debug('Max Qty is %s', maxQty[0])
            logger.debug('maxQty type is %s', type(maxQty[0]))
        else:
            SharesMax = Shares
            logger.debug('maxQty is %s', Shares[0])
            logger.debug('Shares type is %s', type(Shares[0]))
            
        logger.debug('Max Shares is %s', SharesMax)
        timer = datetime.datetime.now().strftime("%I:%M%p")
        logger.debug('time is %s',time)#placeholder for Orders. Use when intraday strategies go into effect
        
        Currency = 'USD'
        TriggerID = idOrder
        logger.debug('yHigh is %s',type(yHigh[0]))
        logger.debug('ATRValue is %s',type(ATRValue[0]))
        type(yHigh[0])
        type(ATRValue[0])
        Price = float(truncate((float(yHigh[0]) + (float(ATRentrymultiple[0])*float(ATRVal[0]))),2))
        print(Price)
        Strategy = "RelativeStrength"
        Bracket = "Entry"
        Status = "Submitted"
        qty = SharesMax
        limit = 1   #tick mark to set up limit
        logger.debug('Quantity %s ',  qty)
        action   = 'BUY'
        counter_action = 'SELL'
        logger.debug('idOrder %s ', idOrder)
        logger.debug('Ticker %s ', Ticker[0])
        #Create ENTRY Stp Buy Order 2 pips above High
        CONTRACT = create_contract(Ticker[0], 'STK', 'SMART', 'ARCA', 'USD')
        logger.debug('Contract Created')
        print(CONTRACT)
        logger.debug('Contract %s ',  CONTRACT)
        ORDER = make_long_order(action, qty)
        logger.debug('order Created')
        print(ORDER)
        logger.debug('Order %s ',  ORDER)
        logger.debug('idOrder %s ', idOrder)
        logger.debug('idOrder type %s ', type(idOrder))
        conn.placeOrder(idOrder, CONTRACT, ORDER)
        logger.debug('order placed')
        logger.debug('idOrder %s ', idOrder)
        logger.debug('Date %s ', Date)
        logger.debug('Price %s ',  Price)
        logger.debug('time %s ',  time)
        logger.debug('currency %s ',  Currency)
        logger.debug('TriggerID %s ',  OID)
        logger.debug('idOrder %s ', type(idOrder))
        logger.debug('Date %s ', type(Date))
        logger.debug('Price %s ',  type(Price))
        logger.debug('time %s ',  type(time))
        logger.debug('currency %s ',  type(Currency))
        logger.debug('TriggerID %s ',  type(OID))
        logger.debug('Size %s ',  type(Shares))
        
        #, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status , Date, time, Currency, str(TriggerID), str(Price), Strategy, Bracket, Status)
        cur.execute("""Insert Into Orders (idOrders, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status, Size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, timer, Ticker[0], TriggerID, Price, Strategy, Bracket, Status, Shares[0]))
        logger.debug('Order query is %s',query)
        #cur.execute(query)
        cnx.commit() #Primary Trade
        logger.debug('Order added to database')
        
        query = ("UPDATE hasPosition SET EntryID = " + str(idOrder) + " WHERE CCY =\'" + Ticker[0] +"\';")
        logger.debug('hasPosition query is %s',query)
        cur.execute(query)
        cnx.commit()
        logger.debug('hasPosition Entry ID set to %s ', idOrder)
        
        query = ("UPDATE hasPosition SET EntryPrice = " + str(Price) + " WHERE CCY =\'" + Ticker[0] + "\';")
        logger.debug('hasPosition query is %s',query)
        cur.execute(query)
        cnx.commit()
        logger.debug('hasPosition Entry Price set to %s ', Price)
        
        
        query = ("UPDATE hasPosition SET StopQty = " + str(qty[0]) + " WHERE CCY =\'" + Ticker[0] +"\';")
        cur.execute(query)
        logger.debug('hasPosition query is %s',query)
        cnx.commit()
        logger.debug('Stop Loss Quantity set to %s', qty[0])
        conn.disconnect()
        time.sleep(5)
        logger.debug('Database disconnected')
        
        #        ##Update Orders Table
        #        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        #        cnx.commit()#Stop Loss

logging.debug('%%%%%%%%%%%%%% END STRATEGY %s%s')

