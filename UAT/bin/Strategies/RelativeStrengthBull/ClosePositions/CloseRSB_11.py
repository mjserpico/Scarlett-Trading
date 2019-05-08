# -*- coding: utf-8 -*-
"""
@author: Michael
"""
#
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection
from datetime import timedelta
import mysql.connector
import datetime
import logging
#import sys
import datalink  #universal logins for environment
import time
import csv
# test test test
logging.basicConfig(filename='CloseRelativeStrengthBull_11' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('CloseRelativeStrengthBull_11' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
#logger.addHandler(ch)
logger.debug('****************************************************')

#Variables Imported From Database
profitTarget = 0.0
stopLoss = 0.0
AcctBalanceBasis = 0.0
MaxPositions = 0
CurrentPositions = 0
MovingAvg = 0
tOpen = 0.0
tHigh = 0.0
tLow = 0.0
tClose = 0.0
yOpen = 0.0
yHigh = 0.0
yLow = 0.0
yClose = 0.0
ID1 = 0.0
ID2 = 0.0
Flag = 0
o = 0.0
h = 0.0
l = 0.0
c = 0.0
v = 0
Position = 0
global Order_entry
Order_entry = 0
logger.debug('order_entry is %s', Order_entry)
global Order_stop
Order_stop = 0
logger.debug('order_stop is %s', Order_stop)
global Order_profit
Order_profit = 0
logger.debug('order_profit is %s', Order_profit)

masteraccount = 'DU1240329'
logger.debug('Starting Close Relative Strength Bull')

#TWS Async Reply handler
#def reply_handler(msg):
#    #test = msg.value
#    print(msg)
#    logger.debug('Reply: %s', msg)
    
def reply_handler_Orders(msg):
    test0 = msg
    logger.debug('Reply Handler Orders is %s', test0) 
    logger.debug('Order OrderID %s', msg.orderId)
    

def reply_handler_Status(msg):
    test0 = msg
    order_status = msg.status
    order_Identify = msg.orderId
    logger.debug('reply handler status %s', test0)
    logger.debug('Order status %s', order_status)
    logger.debug('Order Identification %s', order_Identify)
    logger.debug('Order Identification %s', type(order_Identify))
    
#    if(order_Identify == int(Order_stop)):
#        global stop_api_id
#        stop_api_id = order_Identify
#        logger.debug('Stop API ID is %s', stop_api_id)
#    
#    if(order_Identify == int(Order_profit)):
#        global profit_api_id
#        profit_api_id = order_Identify
#        logger.debug('Profit API ID is %s', profit_api_id)
#        
#    if(order_Identify == int(entrytrade)):
#        global entry_api_id
#        entry_api_id = order_Identify
#        logger.debug('Entry API ID is %s', entry_api_id)


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


#Bracket Order function for Sell to Close Trades
def make_sell_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty[0]
        logger.debug('qty is %s', qty[0])
        logger.debug('qty type is %s', type(qty))
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Sell Order Function')
        logger.debug('Limit Value is %s', limit)
       	# ENTRY   A simple stop order
        order.m_orderType = 'MKT'
        order.m_outsideRth = True
        order.m_sweepToFill = 1
        logger.debug('In Sell Order Function when Limit is 1')
        logger.debug('Action is %s', action)
     #order.m_lmtPrice  = limit - int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005               
        #order.m_triggerMethod = 4
        order.m_parentId = parentId
        order.m_account = masteraccount
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
##Quick checks for Trade Eligibility

yesterday = datetime.date.today() - timedelta(1)
#f = open('C:/Program Files/Serpico/bin/relativestrengthrank' + str(yesterday) +'.csv')
f = open('C:/Program Files/Serpico/bin/relativestrengthrank' + str(yesterday) +'.csv')
csv_f = csv.reader(f)
logger.debug('Connecting to IBController')
conn = Connection.create(port=4002, clientId=999)
conn.connect() 
time.sleep(1)
logger.debug('Connected to IBController')

for row in csv_f:
    Ticker = row
    
    #KEY FIELDS TO MONITOR 
    
#Order ID
    query = ("SELECT EntryID from hasPosition WHERE CCY =\'" + Ticker[0] +"\';")
    logger.debug('hasPosition query is %s',query)
    cur.execute(query)
    for (EntryID) in cur:
        entrytrade = EntryID[0]
        logger.debug('Entry Id to close is %s', entrytrade)
#Stop ID    
    query = ("SELECT StopID from hasPosition WHERE CCY =\'" + Ticker[0] +"\';")
    logger.debug('hasPosition query is %s',query)
    cur.execute(query)
    for (StopID) in cur:
        Order_stop = StopID[0]
        logger.debug('Stop Id to close is %s', Order_stop)
#Profit ID    
    query = ("SELECT ProfitID from hasPosition WHERE CCY =\'" + Ticker[0] +"\';")
    logger.debug('hasPosition query is %s',query)
    cur.execute(query)
    for (ProfitID) in cur:
        Order_profit = ProfitID[0]
        logger.debug('Profit Id to close is %s', Order_profit)

#EntryPending
    query = ("SELECT EntryPending from hasPosition where CCY = \'" + Ticker[0] +"\';")
    logger.debug('hasPosition query is %s',query)
    cur.execute(query)
    for (EntryPending) in cur:
        EntryPend = EntryPending
        logger.debug('Entry Pending is %s', EntryPend)

#In Position
    query = ("SELECT Position from hasPosition where CCY = \'" + Ticker[0] +"\';")
    logger.debug('hasPosition query is %s',query)
    cur.execute(query)
    for (Position) in cur:
        Pos = Position
        logger.debug('Pos is %s', Pos)
#Stop Loss Flag
    query = ("SELECT StopLossFlag from hasPosition WHERE CCY =\'" + Ticker[0] +"\';")
    logger.debug('StopLossFlag query is %s',query)
    cur.execute(query)
    for (StopLossFlag) in cur:
        stopflag = StopLossFlag
        logger.debug('stopflag is %s', stopflag)

#Profit Target Flag
    query = ("SELECT ProfitTarget from hasPosition WHERE CCY =\'" + Ticker[0] +"\';")
    logger.debug('ProfitTarget query is %s',query)
    cur.execute(query)
    for (ProfitTarget) in cur:
        profitflag = ProfitTarget
        logger.debug('profitflag is %s', profitflag)                
        
    conn.register(reply_handler_Orders, 'OpenOrder') 
 
    conn.reqAllOpenOrders() # will find the order if it's open
    logger.debug('Open Orders requested')
    time.sleep(1)
        
    qqq = Contract()
    qqq.m_symbol = Ticker[0]  
    qqq.m_secType = 'STK'  
    qqq.m_exchange = 'SMART'  
    qqq.m_currency = 'USD' 
    
    logger.debug('EntryPend is %s', int(EntryPend[0]))
    logger.debug('Position is %s', int(Position[0]))
    logger.debug('stopflag is %s', int(stopflag[0]))
    logger.debug('profitflag is %s', int(profitflag[0]))
    logger.debug('Check if Stop Loss Hit')
#Stop Loss Hit
    if (int(EntryPend[0]) == 0 and int(Position[0]) == 0 and int(stopflag[0]) == 0 and int(profitflag[0]) == 1):
        #Clear Fields For the day

        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
    
#Cancel Profit Target     
        query = ("SELECT ProfitID from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (ProfitID) in cur:
            profittrade = ProfitID
            logger.debug('Profit ID is %s', profittrade[0])
    
        conn.cancelOrder(int(profittrade[0]))
        
#Clear hasPosition Table  
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET Position = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET EntryPending = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET EntryPrice = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET ProfitTarget = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()

    logger.debug('EntryPend is %s', int(EntryPend[0]))
    logger.debug('Position is %s', int(Position[0]))
    logger.debug('stopflag is %s', int(stopflag[0]))
    logger.debug('profitflag is %s', int(profitflag[0]))
    logger.debug('Check if Profit Target Hit')
#Profit Target Hit      
    if (int(EntryPend[0]) == 0 and int(Position[0]) == 0 and int(stopflag[0]) == 1 and int(profitflag[0]) == 0):

        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
       #Cancel Stop Loss     
        query = ("SELECT StopID from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (StopID) in cur:
            stoptrade = StopID
            logger.debug('Stop ID ID is %s', stoptrade[0])
        
        conn.cancelOrder(int(stoptrade[0]))
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrders = " + str(stoptrade[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()   
        
        #Clear hasPosition Table  
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET Position = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET EntryPending = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET EntryPrice = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET ProfitTarget = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        
    logger.debug('EntryPend is %s', int(EntryPend[0]))
    logger.debug('Position is %s', int(Position[0]))
    logger.debug('stopflag is %s', int(stopflag[0]))
    logger.debug('profitflag is %s', int(profitflag[0]))
    logger.debug('Order Filled no Target Hit')
#Order Filled but does not hit Profit Target or Stop Loss...Cancel 2 and Close 1
    if (int(EntryPend[0]) == 0 and int(Position[0]) == 1 and int(stopflag[0]) == 1 and int(profitflag[0]) == 1):

#Close Filled Order at Market

        action = 'Sell'        
        query = ("SELECT max(idOrders) from Orders;")
        cur.execute(query)
        for (idOrders) in cur:
            OID = idOrders
            logger.debug('OLD Order ID is %s', OID[0])
            
        query = ("SELECT StopQty from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (StopQty) in cur:
            Shares = StopQty
            logger.debug('Shares is %s', Shares)
#Order Query 
        idOrder = OID[0] + 1
        qty = Shares
        MKTPrice = "MKT"
        Status = "MKT"
        Date = datetime.date.today()
        yesterday = Date #Take 1 Day back                    
        month = (str(0) + str(yesterday.month))
        day = (str(0)+ str(yesterday.day))
        yesterday3 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
        logger.debug('Todays date is %s', yesterday3)
        Date = yesterday3
        
        Strategy = "RelativeStrength"
        Bracket = "Close"
        timer = datetime.datetime.now().strftime("%I:%M%p")
        logger.debug('time is %s',time)#placeholder for Orders. Use when intraday strategies go into effect
        
        query = ("SELECT StopID from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (StopID) in cur:
            stoptrade = StopID
            logger.debug('Stop ID is %s', stoptrade[0])
            
        query = ("SELECT Exchange from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (Exchange) in cur:
            defaultexc = Exchange
            logger.debug('Stop ID is %s', defaultexc[0])
            
        CONTRACT = create_contract(Ticker[0], 'STK', 'SMART', defaultexc[0], 'USD')
        ORDER = make_sell_order(action, qty)
        conn.placeOrder(idOrder, CONTRACT, ORDER) 
        
        #, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status , Date, time, Currency, str(TriggerID), str(Price), Strategy, Bracket, Status)
        cur.execute("""Insert Into Orders (idOrders, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status, Size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, timer, Ticker[0], OID[0], MKTPrice, Strategy, Bracket, Status, Shares[0]))
        logger.debug('Order query is %s',query)
        #cur.execute(query)
        cnx.commit() #Primary Trade
        logger.debug('Order added to database')
        
        query = ("UPDATE Orders SET Status = \'" + "Closed" + "\' where idOrders = " + str(entrytrade) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
#Cancel Stop Loss      
        logger.debug('Stop Trade ID is %s', stoptrade[0])
        conn.cancelOrder(int(stoptrade[0]))      

        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrders = " + str(stoptrade[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("SELECT ProfitID from hasPosition where CCY = \'" + Ticker[0] +"\';")
        cur.execute(query)
        for (ProfitID) in cur:
            profittrade = ProfitID
            logger.debug('Profit ID is %s', profittrade[0])
        
#Cancel Profit Target                 
        logger.debug('Profit ID is %s', profittrade[0])
        conn.cancelOrder(int(profittrade[0]))
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrders = " + str(profittrade[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()  
        
        query = ("UPDATE hasPosition SET ProfitTarget = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()

#Clear all remaining Fields in hasPosition    
#        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
                
        query = ("UPDATE hasPosition SET Position = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET EntryPending = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
                
        query = ("UPDATE hasPosition SET EntryPrice = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
#        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
    
#Order never filled
#    if (int(EntryPend[0]) == 1 and int(Position[0]) == 0 and int(stopflag[0]) == 0 and int(profitflag[0]) == 0):
#        logger.error('Setup Never Executed. Clearing Position information and Orders')
#        
#        
#        query = ("SELECT EntryID from hasPosition where CCY = \'" + Ticker[0] +"\';")
#        cur.execute(query)
#        for (EntryID) in cur:
#            entrytrade = EntryID
#            logger.debug('Entry ID is %s', entrytrade[0])
#        
#        logger.error(type(entrytrade))
#        logger.error('Canceled Order %s', int(entrytrade[0]))
#        conn.cancelOrder(int(entrytrade[0]))
#        logger.error('Canceled Order %s', entrytrade[0])
#                
#        ##Update Orders Table
#        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrders = " + str(entrytrade[0]) + ";")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#    #Clear hasPosition Table  
##        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
##        logger.debug('Query is %s', query)
##        cur.execute(query)
##        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
##        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + Ticker[0] +"\';")
##        logger.debug('Query is %s', query)
##        cur.execute(query)
##        cnx.commit()
#                
#        query = ("UPDATE hasPosition SET Position = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#                
#        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#                
#        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#                
#        query = ("UPDATE hasPosition SET EntryPending = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#                
#        query = ("UPDATE hasPosition SET EntryPrice = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#                
#        query = ("UPDATE hasPosition SET ProfitTarget = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
    
logger.debug('Disconnected from IBController')    
conn.disconnect()    
logging.debug('%%%%%%%%%%%%%% END Close Relative Strength Bull')
