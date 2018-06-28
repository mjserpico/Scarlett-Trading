# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 20:19:49 2017

@author: Michael
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""

from ib.ext.Contract import Contract
from ib.ext.Order import Order
import mysql.connector
from ib.opt import Connection
import time
import datetime
import logging
import datalink  #universal logins for environment

logging.basicConfig(filename='pythonlogs\DailyPosMgmt' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('DailyPosMgmt' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')


Order_entry = 1
Order_profit = 1
Order_stop = 1
stop_api_id = 0
profit_api_id = 0
entry_api_id = 0
entry_date = "10"
order_status = "?"
submit = "Submitted"
entry = "Entry"
profits = "Profit Target"
stoploss = "Stop Loss"
api_id = 0
api_profitid = 0
api_status = "?"
CCY1 = "GBP"
CCY2 = "USD"
symbol   = CCY1
symbol2 = CCY2
secType  = 'CASH'
exchange = 'IDEALPRO'
action   = 'Buy'
counter_action = 'Sell'
limit = 1
TriggerID = Order_entry
Strategy = "DailyBullBear"
Status = "Submitted"
Currency = CCY1 + CCY2
pos = ""
directionTrade = ""
timer = "6:00"
masteraccount = datalink.DB_Account
inPos = 0
logger.debug('Starting PosMgmt %s%s',CCY1,CCY2)

def reply_handler(msg):
    test0 = msg
    acct = msg.account
    logger.debug('Reply Handler %s', test0)
    global pos
    pos = msg.pos
    global con
    con = msg.contract
    logger.debug('Reply handler: Contract is %s', con)
    logger.debug('Reply handler: Position is %s', pos)
    logger.debug('Reply handler: acct is %s', acct)
    
    if acct =='DU501213':
        logger.debug('Reviewing details for acct %s', acct)
        logger.debug('Symbol is', con.m_symbol)
        logger.debug('Symbol2 is', con.m_currency)
        if(con.m_symbol == CCY1 and con.m_currency == CCY2 and pos != 0):
            global inPos
            inPos = 1
            logger.debug('In Position is %s', inPos)
    
def reply_handler_Orders(msg):
    test0 = msg
    logger.debug('Reply Handler Orders is %s', test0)
    logger.debug('OrderID is: %s', msg.orderId)
    global api_id
    api_id = msg.orderId
    logger.debug('OrderID is API ID is: %s',api_id)

def reply_handler_contract(msg):
    test0 = msg
    logger.debug('Reply Handler contract is %s',test0)


def reply_handler_Data(msg):
    test0 = msg.open
    logger.debug('Reply Handler data is %s',test0)
    if float(test0) != -1:
        logger.debug('Reply:', msg)
        global test4
        test4 = msg.close
        logger.debug('Close is %s',test4)
    
    
def reply_handler_Status(msg):
    test0 = msg
    order_status = msg.status
    order_Identify = msg.orderId
    logger.debug('reply handler status %s', test0)
    logger.debug('Order status %s', order_status)
    logger.debug('Order Identification %s', order_Identify)
    logger.debug('Order Identification %s', type(order_Identify))
    logger.debug('Profit ID from database is %s', Order_profit[0])
    logger.debug('Profit ID from database is %s', type(Order_profit[0]))
    logger.debug('Stop ID database is %s', Order_stop[0])
    logger.debug('Entry ID database is %s', Order_entry[0])
    
    if(order_Identify == int(Order_stop[0])):
        global stop_api_id
        stop_api_id = order_Identify
        logger.debug('Stop API ID is %s', stop_api_id)
    
    if(order_Identify == int(Order_profit[0])):
        global profit_api_id
        profit_api_id = order_Identify
        logger.debug('Profit API ID is %s', profit_api_id)
        
    if(order_Identify == int(Order_entry[0])):
        global entry_api_id
        entry_api_id = order_Identify
        logger.debug('Entry API ID is %s', entry_api_id)
    
def create_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
    
#Bracket Order function for Long Trades
def make_order_stop(action, qty, limit = None, transmit=True):
        order = Order()
        order.m_action = action
        logger.debug('Action is %s',order.m_action)
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Stop Order Function')
        order.m_orderType = 'STP'

        if action == 'Sell':
            order.m_lmtPrice  = float(stopVal[0])
            logger.debug('In Sell section of Stop order')
            stopPrice = float(stopVal[0])
            logger.debug(' Stop price is %s', stopPrice)
            order.m_auxPrice = stopPrice;
            order.m_account = masteraccount
                #order.m_parentId = parentId
            order.m_transmit = transmit
            logger.debug(' Transmit is %s', transmit)
        if action == 'Buy':
            logger.debug('In Buy section of Stop order')
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
            order.m_lmtPrice  = float(stopVal[0])
            logger.debug(' Stop price is %s', order.m_lmtPrice)
            stopPrice = float(stopVal[0])
            order.m_auxPrice = stopPrice;
            logger.debug(' Stop price is %s', stopPrice)
            order.m_account = masteraccount
            logger.debug(' MAster account is %s', masteraccount)
            #order.m_parentId = parentId
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit
        logger.debug(' Transmit is %s', order.m_transmit)
        return order
        
def make_breakeven(action, qty, limit = None, transmit=True):
        logger.debug('In Breakeven function')
        order = Order()
        order.m_action = action
        logger.debug('Action is %s',order.m_action)
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Breakeven Order Function')
        order.m_orderType = 'STP'

        if action == 'Sell':
            order.m_lmtPrice  = float(curBreakeven[0])
            logger.debug('In Sell section of Breakeven order')
            breakevenPrice = float(curBreakeven[0])
            logger.debug('break even price is %s', breakevenPrice)
            order.m_auxPrice = breakevenPrice;
            order.m_account = masteraccount
                #order.m_parentId = parentId
            order.m_transmit = transmit
            logger.debug(' Transmit is %s', transmit)
        if action == 'Buy':
            logger.debug('In Buy section of breakeven order')
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
            order.m_lmtPrice  = float(curBreakeven[0])
            logger.debug(' Break even price is %s', order.m_lmtPrice)
            breakevenPrice = float(curBreakeven[0])
            order.m_auxPrice = breakevenPrice;
            logger.debug(' Stop price is %s', breakevenPrice)
            order.m_account = masteraccount
            #order.m_parentId = parentId
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit
        logger.debug(' Transmit is %s', order.m_transmi)
        return order       
#Main code

#give IB time to send us messages
logger.debug('Connecting to database')
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
#cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connected to databaSe')
##Quick pulls for Trade Details

query = ("SELECT EntryID FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (EntryID) in cur:  #was idOrder
    Order_entry = EntryID
    logger.debug('Order entry is %s',Order_entry[0])

query = ("SELECT ProfitID FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (ProfitID) in cur:
    Order_profit = ProfitID
    logger.debug('Order Profit is %s',Order_profit[0])

query = ("SELECT StopID FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (StopID) in cur:
    Order_stop = StopID
    logger.debug('Order_stop is %s',Order_stop[0])



logger.debug('Connecting to IBcontroller')
conn = Connection.create(port=4002, clientId=999)
conn.connect() 
time.sleep(1)
logger.debug('Connected To IBController')

conn.register(reply_handler, 'Position')
conn.register(reply_handler_Orders, 'OpenOrder') 
conn.register(reply_handler_Status, 'OrderStatus')
conn.register(reply_handler_Status, 'OrderStatus')
conn.register(reply_handler_Data, 'HistoricalData')
#conn.register(reply_handler_contract, 'Contract')     
logger.debug('Requesting Positions')
conn.reqPositions() # will find the order if it was filled 
logger.debug('Finished Positions')
time.sleep(1) 
logger.debug('Requesting Open Orders') 
conn.reqAllOpenOrders() # will find the order if it's open
time.sleep(1)
logger.debug('Finished Open Orders')

qqq = Contract()  
qqq.m_symbol = CCY1  
qqq.m_secType = 'CASH'  
qqq.m_exchange = 'IDEALPRO'  
qqq.m_currency = CCY2 
logger.debug('Requesting historical data') 
conn.reqHistoricalData(1, qqq, '', '60 S', '5 mins', 'Midpoint', 1, 1)
logger.debug('Returned from Reply Handler')
#qqq = Contract()  
#qqq.m_symbol = 'EUR'  
#qqq.m_secType = 'CASH'  
#qqq.m_exchange = 'IDEALPRO'  
#qqq.m_currency = 'USD'  
#conn.reqHistoricalData(1, qqq, '', '60 S', '1 min', 'Midpoint', 1, 2) 
##conn.reqContractDetails(1)  #TWS returns two messages  OrderStatus and Openorder  only for submitted orders or partial fills
#time.sleep(1)


query = ("SELECT Date FROM Orders where Currency = \'" + CCY1 + CCY2 + "\'"" and Status = \'" + submit + "\'"" and Bracket = " + "\'" + entry + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (Date) in cur:
    entry_date = Date
    logger.debug('entry_date is %s', entry_date)
    
query = ("SELECT StopLossVal FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (StopLossVal) in cur:
    stopVal = StopLossVal
    logger.debug('stopVal is %s',stopVal)
    
query = ("SELECT StopQty FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (StopQty) in cur:
    qty = StopQty
    logger.debug('Stop qty is %s',qty)
    
query = ("SELECT direction FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (direction) in cur:
    directionTrade = direction
    logger.debug('directionTrade is %s',directionTrade)
    
query = ("SELECT Count FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (Count) in cur:
    curCount = Count
    logger.debug('curCount is %s',curCount)
    
query = ("SELECT StopLossFlag FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (StopLossFlag) in cur:
    curStopLossFlag = StopLossFlag
    logger.debug('curStopLossFlag is %s',curStopLossFlag)

query = ("SELECT Breakeven FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s',query)
for (Breakeven) in cur:
    curBreakeven = Breakeven
    logger.debug('curBreakeven is %s',curBreakeven)
       
#Calculate yesterday's date
#Find today's date and Day of the week
today = datetime.date.today( )
logger.debug('Today is %s', today)

dayofweek = datetime.datetime.today().weekday()
today2 = str(today)
logger.debug('Today2 is %s', today2)

##Convert Date to proper format and relative reference
if dayofweek == 0:  #if Today is Monday
    yesterday = today - datetime.timedelta(days=3)  #Get Previous Wednesday                   
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Yesterday was %s', yesterday2)

else:
    yesterday = today - datetime.timedelta(days=1) #Take 3 Days back                    
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Yesterday was %s', yesterday2)

logger.debug('In Pos is %s', inPos)
logger.debug('curStopLossFlag[0] is %s', curStopLossFlag[0])
logger.debug('Checking if Entry is filled')
#If Entry has been filled and Stop Loss not yet set
if (inPos == 1 and curStopLossFlag[0] != 1):
    # create a stop loss order, and THEN transmit(set transmit to true) the entire order by placing this last child order(note inTWS it looks like a tree with parent order and two sub orders inside)  
        logger.debug('Identified Entry Order Has Been Filled: In Stop Loss creation')
        Bracket = "Stop Loss"
        logger.debug('Order Profit type is %s', Order_profit)
        OID = int(Order_profit[0]) + 1
        logger.debug('incremented Order ID is  %s', OID)
        idOrder = OID
        Price = StopLossVal
        logger.debug('Price is  %s', StopLossVal)
        logger.debug('symbol, sectype and exchange is  %s %s %s', symbol,secType,exchange)
        PosSize = int(qty[0])
        TriggerID = Order_entry
        CONTRACT = create_contract(symbol, secType, exchange, exchange, symbol2)
        logger.debug('contract is %s', CONTRACT)
        if(directionTrade[0] == "Short"):
            ORDER = make_order_stop(action, PosSize, limit, transmit=True)
            conn.placeOrder(OID, CONTRACT, ORDER)  
            logger.debug('Placed Order')
        if(directionTrade[0] == "Long"):
            logger.debug('Direction is Long')
            ORDER = make_order_stop(counter_action, PosSize, limit, transmit=True)
            conn.placeOrder(OID, CONTRACT, ORDER)    
            logger.debug('Placed Order')
        #Update hasPosition Table
        query = ("UPDATE hasPosition SET Count = " + "1" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        
        query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 5")
        cur.execute(query)
        for (RiskParametersValue) in cur:
            MaxPositions = RiskParametersValue
            logger.debug('Max Positions is %s', MaxPositions)
        
        MaxPositions2 = MaxPositions[0] + 1
        logger.debug('Max Positions2 is %s', MaxPositions2)
        
        query = ("UPDATE RiskParameters SET RiskParametersValue = " + str(MaxPositions2) + " where idRiskParameters = 5")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopLossFlag = " + "1" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        StopLossVal2 = float(StopLossVal[0])
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, today2[0], timer, Currency, TriggerID[0], str(StopLossVal2), Strategy, Bracket, Status))
        cnx.commit() #Stop Loss
        query = ("UPDATE hasPosition SET StopID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()

        logger.debug('Order entry Type is %s', Order_entry[0])
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_entry[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
logger.debug('Try to Cancel Stop')    
logger.debug('Stop API ID %s', stop_api_id)   
logger.debug('Profit API ID %s', profit_api_id)         
logger.debug('Pos is %s', inPos)
logger.debug('CurCount is %s', curCount[0])
logger.debug('In Pos %s', inPos)
logger.debug('Stop ID is %s', Order_stop[0])

     
#If Profit Target has been filled     CHECK BY INVERSE  EURUSD STOPLOSS ORDERID SHOULD STILL BE OUT THERE
if (curCount[0] == 1 and int(inPos) == 0 and int(stop_api_id) == int(Order_stop[0]) and int(profit_api_id) != int(Order_profit[0])):
        logger.error('Profit Target Hit! Clearing Position information')
        logger.debug('Stop Order ID is %s', Order_stop[0])
        conn.cancelOrder(Order_stop[0])
       
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        #Update Trades Table
       
       #Clear hasPosition Table
        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 5")
        cur.execute(query)
        for (RiskParametersValue) in cur:
            MaxPositions = RiskParametersValue
            logger.debug('Max Positions is %s', MaxPositions)
        
        MaxPositions[0] = MaxPositions[0] - 1
        logger.debug('Max Positions is %s', MaxPositions[0])
        
        query = ("UPDATE RiskParameters SET RiskParametersValue = " + MaxPositions[0] + " where idRiskParameters = 5")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()

logger.debug('Stop API ID %s', stop_api_id)   
logger.debug('Profit API ID %s', profit_api_id)             
logger.debug('Pos is %s', inPos)
logger.debug('CurCount is %s', curCount[0])
logger.debug('In Pos %s', inPos)
logger.debug('profitID is %s', Order_profit[0])
logger.debug('stopID is %s', Order_stop[0])

#-5 < pos2 < 5 and api_id == Order_stop[0] and
        #
#If Stop Loss has been filled     
if(int(curCount[0]) == 1 and int(inPos) == 0 and int(profit_api_id) == int(Order_profit[0]) and int(stop_api_id) != int(Order_stop[0])):  #Position is 0 but Profit Target still exists
        logger.debug('Stop Loss Hit! Clearing Position information')
        logger.debug('ProfitId to cancel is %s',Order_profit[0])
        conn.cancelOrder(Order_profit[0])
        logger.debug('Order Canceled')
       
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
       
       #Clear hasPosition Table
        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopLossFlag = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()

logger.error('Checking to cancel when Setup Never Executed')
logger.debug('Yesterday2 is %s', yesterday2)      
logger.debug('Entry Date %s', entry_date)
logger.debug('CurCount is %s', curCount[0])
logger.debug('API ID is %s', api_id)
logger.debug('profitID is %s', int(Order_profit[0]))
logger.debug('entryID is %s', int(Order_entry[0]))

#Cancel all Entries and Profit Targets after 3 days
if (curCount[0] == 0 and yesterday2 == entry_date and int(api_id) == int(Order_profit[0])):
        logger.error('Setup Never Executed. Clearing Position information and Orders')
        conn.cancelOrder(int(Order_profit[0]))
        conn.cancelOrder(int(Order_entry[0]))
        ##Update Orders Table
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_entry[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
      #Clear hasPosition Table  
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET ProfitID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()

query = ("SELECT BreakevenTrigger from hasPosition where CCY =\'" + CCY1 + CCY2+"\';")
cur.execute(query)
for (BreakevenTrigger) in cur:
    breakeven_price = BreakevenTrigger
    logger.debug('breakeven_price %s', breakeven_price[0])

logger.debug('Checking for Breakeven credentials')  
logger.debug('test4 for price is %s', float(test4))    
logger.debug('CurCount is %s', curCount[0])
logger.debug('direction is %s', direction)
logger.debug('Position Size is %s', PosSize)  
logger.debug('Stop Quantity is %s', StopQty)  
    
 ###Break even Function       
if (curCount[0] == 1 and float(test4) >= breakeven_price[0]):
        logger.debug('Moving Stop Loss to Break Even')
        
        ORDER = make_breakeven(direction, PosSize, StopQty, transmit=True)
        conn.placeOrder(Order_stop[0], CONTRACT, ORDER) 
        ##Update Orders Table
        query = ("UPDATE Orders SET Status = \'" + "BreakEven" + "\' where idOrder = " + str(Order_stop[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
conn.disconnect()
logger.debug('Disconnect')