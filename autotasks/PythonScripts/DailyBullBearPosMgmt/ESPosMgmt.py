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


today = datetime.date.today( )

logging.basicConfig(filename='pythonlogs\DailyPosMgmtES' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('DailyPosMgmtES' + str(datetime.date.today()) + '.txt')
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
CCY1 = "E"
CCY2 = "S"
CCY1LE = 'L'
CCY2LE = 'E'
CCY1M6E = 'M'
CCY2M6E = '6E'
CCY1HE = 'H'
CCY2HE = 'E'
symbol   = CCY1
symbol2 = CCY2
secType  = 'FUT'
exchange = 'GLOBEX'
action   = 'Buy'
counter_action = 'Sell'
limit = 1
TriggerID = Order_entry
Strategy = "DailyBullBear"
Status = "Submitted"
Currency = CCY1 + CCY2
pos = ""
directionTrade = ""
timer = datetime.datetime.now().strftime("%I:%M%p")
logger.debug('Current Time is %s', timer)
#masteraccount = 'DU501213'
masteraccount = datalink.DB_Account
inPos = 0
logger.debug('Starting Pos Mgmt %s %s', CCY1,CCY2)

def reply_handler(msg):
    test0 = msg
    acct = msg.account
    global pos
    pos = msg.pos
    global con
    con = msg.contract
    logger.debug('Pos Mgmt %s', pos)
    
    if acct == datalink.DB_Account:
        logger.debug('Reply handler %s', test0)
        logger.debug('ccy1 Symbol with position is %s', con.m_symbol)
        logger.debug('ccy2 Currency with position is %s', con.m_currency)
        logger.debug('Position is %s', pos)        
        if(con.m_symbol == CCY1+CCY2 and pos != 0):
            logger.debug('In Position') 
            global inPos
            inPos = 1
            logger.debug('Position is %s', inPos)
    
def reply_handler_Orders(msg):
    test0 = msg
    logger.debug('Reply Handler Orders is %s', test0) 
    logger.debug('Order OrderID %s', msg.orderId)
    

def reply_handler_contract(msg):
    test0 = msg
    logger.debug('Reply Handler Contract is %s', test0) 

def reply_handler_Data(msg):
    test0 = msg.open
    logger.debug('Reply Handler Datat is %s', test0) 
    if float(test0) != -1:
        logger.debug('Reply %s', msg) 
        global test4
        test4 = msg.close
        logger.debug('Close is %s', test4) 
    
    
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
    contract.m_symbol = CCY1+CCY2
    contract.m_localSymbol = CCY1+CCY2 + datalink.monthcode + "8"
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

    
def make__short__order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        logger.debug('In Short Order Function')    
        order = Order()
        logger.debug('action is %s', action)  
        logger.debug('qty is %s', qty) 
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        #order.m_ocaGroup = OCAID[0]
        #query = ("Insert Into OCAGroup (OCAGroupcol) values(%s)""",(idOrder))
        #cur.execute(query)
        #logger.debug('Query is %s', query)
        #logger.debug('OCA group is %s', order.m_ocaGroup)
        #order.ocaType = 1
        profitlimitprice = truncate((float(profitVal[0])), 2)
        logger.debug('Profit Target MIT Order Price : %s', profitlimitprice)
        order.m_lmtPrice  = profitlimitprice
        order.m_auxPrice  = profitlimitprice
        order.m_orderType = 'MIT'
        order.m_triggerMethod = 4
        order.m_account = masteraccount
        order.m_transmit = transmit
        order.m_outsideRth = True
        logger.debug('transmitted SHORT order')
        return order    

#Profit target function for Sell Profit Orders (Long Trades)
def make_long_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        #order.m_ocaGroup = OCAID[0]
        #logger.debug('OCA group is %s', order.m_ocaGroup)
        #query = ("Insert Into OCAGroup (OCAGroupcol) values(%s)""",(idOrder))
        #cur.execute(query)
        #logger.debug('Query is %s', query)
        #order.ocaType = 1
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Long Order Function')
        order.m_lmtPrice  = truncate((float(profitVal[0])), 2)
        logger.debug('Profit Target MIT Order Price is is %s', order.m_lmtPrice)
        order.m_orderType = 'MIT'
        order.m_triggerMethod = 4
        order.m_account = masteraccount
        order.m_transmit = transmit
        order.m_outsideRth = True
        logger.debug('transmitted LONG order')
        return order    

def make_trail(action, qty, limit = None, transmit=True):
        logger.debug('In TRAIL STOP function')
        order = Order()
        order.m_action = action
        order.m_ocaGroup = 1
        order.ocaType = 1
        logger.debug('Order action %s', order.m_action) 
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('Limit value is %s', limit)
        order.m_orderType = 'TRAIL'
        order.m_outsideRth = True
        order.m_triggerMethod = 4
        #In This section when a long trade in effect
        if action == 'Sell':
            order.m_lmtPrice  = truncate(float(stopVal[0]),4)
            logger.debug('In Sell action. TRAIL price is %s', order.m_lmtPrice)
            stopPrice = 5
            logger.debug('In Sell action. AUX price is %s', stopPrice)
            order.m_auxPrice = stopPrice;
            order.m_account = masteraccount
            logger.debug('Transmit is %s', transmit)
            order.m_transmit = transmit
        
            #In this section when a short trade in effect
        if action == 'Buy':
            order.m_lmtPrice  = truncate(float(stopVal[0]),4)
            logger.debug('In Buy action. TRAIL price is %s', order.m_lmtPrice)
            stopPrice = 5
            order.m_auxPrice = stopPrice;
            order.m_account = masteraccount
            logger.debug('In Buy action. AUX Price price is %s', stopPrice)
            logger.debug('In Buy action. account is %s', order.m_account)
        # Important that we only send the order when all children are formed.
            order.m_transmit = transmit

        return order
         #give IB time to send us messages
logger.debug('Connecting to database')
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
#cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connected to database')
    
query = ("SELECT BB_ProfitID FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
logger.debug('Query is %s', query)
cur.execute(query)
for (BB_ProfitID) in cur:
    Order_profit = BB_ProfitID
    logger.debug('Order Profit is %s', Order_profit[0])

    
query = ("SELECT BB_StopID FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
logger.debug('Query is %s', query)
cur.execute(query)
for (BB_StopID) in cur:
    Order_stop = BB_StopID
    logger.debug('Stop ID is %s', Order_stop[0])
    
query = ("SELECT BB_EntryID FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
logger.debug('Query is %s', query)
cur.execute(query)
for (BB_EntryID) in cur:
    Order_entry = BB_EntryID
    logger.debug('Entry ID is %s', Order_entry[0])
    
query = ("select max(idOCAGroup) as OCA from OCAGroup")
logger.debug('Query is %s', query)
cur.execute(query)
for (OCA) in cur:
    OCAID = OCA
    logger.debug('OCA ID is %s', OCAID[0])


        
#Main code
logger.debug('Connecting to IBController')
conn = Connection.create(port=4002, clientId=999)
conn.connect() 
time.sleep(1)
logger.debug('Connected to IBController')

conn.register(reply_handler, 'Position')
conn.register(reply_handler_Orders, 'OpenOrder') 
conn.register(reply_handler_Status, 'OrderStatus')
#conn.register(reply_handler_Status, 'OrderStatus')
conn.register(reply_handler_Data, 'HistoricalData')
#conn.register(reply_handler_contract, 'Contract')     
conn.reqPositions() # will find the order if it was filled 
logger.debug('Position requested')
time.sleep(1)  
conn.reqAllOpenOrders() # will find the order if it's open
logger.debug('Open Orders requested')
time.sleep(1)

qqq = Contract()
qqq.m_symbol = CCY1+CCY2  
qqq.m_localSymbol = CCY1+CCY2 + datalink.monthcode + "8";
qqq.m_secType = 'FUT'  
qqq.m_exchange = 'GLOBEX'  
qqq.m_currency = 'USD' 
#conn.reqHistoricalData(1, qqq, '', '60 S', '1 min', 'Midpoint', 1, 2) 
#conn.reqContractDetails(1)  #TWS returns two messages  OrderStatus and Openorder  only for submitted orders or partial fills
time.sleep(1)

 #give IB time to send us messages
logger.debug('Connecting to database')
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connected to database')
##Quick pulls for Trade Details



      
query = ("SELECT BB_StopLossVal FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_StopLossVal) in cur:
    stopVal = BB_StopLossVal
    logger.debug('Stop loss value is %s', stopVal[0])
    
query = ("SELECT BB_ProfitPrice FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_ProfitPrice) in cur:
    profitVal = BB_ProfitPrice
    logger.debug('Stop loss value is %s', profitVal[0])
    
query = ("SELECT BB_EntryPrice FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_EntryPrice) in cur:
    EntryPrice = BB_EntryPrice
    logger.debug('EntryPrice value is %s', EntryPrice[0])
    
query = ("SELECT BB_StopQty FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_StopQty) in cur:
    qty = BB_StopQty
    logger.debug('Stop quantity %s', qty[0])
    
query = ("SELECT BB_direction FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_direction) in cur:
    directionTrade = BB_direction
    logger.debug('Direction is %s', BB_direction[0])
   
query = ("SELECT BB_Position FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_Position) in cur:
    curCount = BB_Position
    logger.debug('Count is %s', curCount[0])   
    
    
query = ("SELECT BB_StopLossFlag FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
logger.debug('Query is %s', query)
for (BB_StopLossFlag) in cur:
    curStopLossFlag = BB_StopLossFlag
    logger.debug('Stop Loss Flag is %s', curStopLossFlag[0])
    
    
query = ("SELECT max(idOrder) FROM Orders")
cur.execute(query)
logger.debug('Query is %s', query)
for (idOrder) in cur:
    maxID = idOrder
    logger.debug('Max ID Order is %s', maxID)
       
#Calculate yesterday's date
#Find today's date and Day of the week
today = datetime.date.today( )
logger.debug('Today is %s', today)
dayofweek = datetime.datetime.today().weekday()
logger.debug('Day of the week %s', dayofweek)
today2 = str(today)

##Convert Date to proper format and relative reference
if dayofweek == 0:  #if Today is Monday
    yesterday = today - datetime.timedelta(days=3)  #Get Previous Wednesday                   
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Yesterday is %s', yesterday2)  

else:
    yesterday = today - datetime.timedelta(days=1) #Take 3 Days back                    
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Yesterday is %s', yesterday2) 


logger.debug('In Position is  %s', inPos)
logger.debug('In Position is  %s', type(inPos)) 
logger.debug('curStopLossFlag is  %s', curStopLossFlag[0])
logger.debug('curStopLossFlag is  %s', type(curStopLossFlag[0])) 
logger.debug('Checking if Entry has been filled') 
#If Entry has been filled and Stop Loss not yet set
#
query = ("SELECT BBEntryPending from hasPosition where CCY =\'" + CCY1 + CCY2 +"\';")
logger.debug('query is %s', query)
cur.execute(query)
for (BBEntryPending) in cur:
    EntryPend = BBEntryPending
    
logger.debug('EntryPend is %s', EntryPend[0])
"""
Created on Sun Jan 08 09:16:43 2017
If Entry has been filled and Stop Loss not yet set


@author: Michael
"""
if (inPos == 1 and curStopLossFlag[0] == "0" and int(EntryPend[0]) == 1):
        # create a stop loss order, and THEN transmit(set transmit to true) the entire order by placing this last child order(note inTWS it looks like a tree with parent order and two sub orders inside)
    logger.debug('Identified Entry Order Has Been Filled: In Stop Loss creation')
    Bracket = "Stop Loss"        
    logger.debug('Order Profit is %s', Order_profit)
    OID = maxID[0] + 1
    OID2 = OID + 1
    logger.debug('Incremented Order ID for stop loss %s', OID)
    idOrder = OID
    Price = BB_StopLossVal
    logger.debug('Symbol, secType, exchange is %s %s %s', symbol, secType, exchange)
    PosSize = int(qty[0])
    TriggerID = Order_entry
    CONTRACT = create_contract(symbol, secType, exchange, exchange, 'USD')
    logger.debug('Contract is %s', CONTRACT)
    logger.debug('Entry Trade Direction is %s', directionTrade[0])
    
    if(directionTrade[0] == "Short"):
        logger.debug('In Short direction.')
        ORDER = make_trail(action, PosSize, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        logger.debug('Long stop order placed')
        #ORDER2 = make_long_order(action, PosSize, limit, transmit=True)
        #conn.placeOrder(OID2, CONTRACT, ORDER2)
        #logger.debug('Short stop order placed')
        
    if(directionTrade[0] == "Long"):
        logger.debug('In Long direction.')
        logger.debug('Counter action, qty, limit, OID and Pos Size are %s %s %s %s %s',counter_action, qty[0], limit, OID, PosSize)
        ORDER = make_trail(counter_action, PosSize, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        logger.debug('Long stop order placed')
        #logger.debug('Counter action, qty, limit, OID and Pos Size are %s %s %s %s %s',counter_action, qty[0], limit, OID, PosSize)
        #ORDER2 = make__short__order(counter_action, PosSize, limit, transmit=True)
        #conn.placeOrder(OID2, CONTRACT, ORDER2)
        #logger.debug('Long profit target order placed')
        #Update hasPosition Table
        
    query = ("UPDATE hasPosition SET BB_Position = " + "1" + " where CCY = \'" + CCY1 + CCY2 + "\'")
    logger.debug('Query is %s', query)
    logger.debug('BB POSITION Set to 1.  No More positions should be taken')
    cur.execute(query)
    cnx.commit()

#Sets the Master Fill and Cancels other LE orders
    query = ("UPDATE RiskParameters SET RiskParametersValue= " + "1" + " WHERE idRiskParameters='20'")
    cur.execute(query)
    cnx.commit()
    logger.debug('Master Fill set to 1')
 
    query = ("SELECT BB_EntryID FROM hasPosition where CCY = \'" + CCY1LE + CCY2LE + "\'")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (BB_EntryID) in cur:
        Order_entryLE = BB_EntryID
        logger.debug('Entry ID is %s', Order_entryLE[0])
    
    conn.cancelOrder(int(Order_entryLE[0]))
    logger.error('Canceled Order %s', Order_entryLE[0] )
    
    query = ("SELECT BB_EntryID FROM hasPosition where CCY = \'" + CCY1M6E + CCY2M6E + "\'")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (BB_EntryID) in cur:
        Order_entryM6E = BB_EntryID
        logger.debug('Entry ID is %s', Order_entryM6E[0])
    
    conn.cancelOrder(int(Order_entryM6E[0]))
    logger.error('Canceled Order %s', Order_entryM6E[0] )
    
    query = ("SELECT BB_EntryID FROM hasPosition where CCY = \'" + CCY1HE + CCY2HE + "\'")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (BB_EntryID) in cur:
        Order_entryHE = BB_EntryID
        logger.debug('Entry ID is %s', Order_entryHE[0])
    
    conn.cancelOrder(int(Order_entryHE[0]))
    logger.error('Canceled Order %s', Order_entryHE[0] )
        
    ##Update Orders Table
    query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_entryM6E[0]) + ";")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
    
    query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_entryLE[0]) + ";")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
    
    query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_entryHE[0]) + ";")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
        
    query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 15")
    cur.execute(query)
    for (RiskParametersValue) in cur:
        MaxPositions = RiskParametersValue
        logger.debug('Max Positions is %s', MaxPositions)
        
        
    MaxPositions2 = MaxPositions[0] + 1
    logger.debug('Max Positions2 is %s', MaxPositions2)
        
    query = ("UPDATE RiskParameters SET RiskParametersValue = " + str(MaxPositions2) + " where idRiskParameters = 15")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
        
    query = ("UPDATE hasPosition SET BBEntryPending = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
        
    query = ("UPDATE hasPosition SET BB_StopLossFlag = " + "1" + " where CCY = \'" + CCY1 + CCY2 + "\'")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
        
    StopLossVal2 = float(stopVal[0])
    logger.debug('StopLossVal2 is %s', StopLossVal2)
    
    ProfitTargetVal2 = float(profitVal[0])
    logger.debug('ProfitVal2 is %s', ProfitTargetVal2)
        
    cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, today, timer, Currency, TriggerID[0], str(StopLossVal2), Strategy, Bracket, Status))
    cnx.commit() #Stop Loss
    query = ("UPDATE hasPosition SET BB_StopID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
    cur.execute(query)
    cnx.commit()

    query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_entry[0]) + ";")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
    
    query = ("SELECT max(idOrder) FROM Orders")
    cur.execute(query)
    logger.debug('Query is %s', query)
    for (idOrder) in cur:
        maxID = idOrder
        logger.debug('Max ID Order is %s', maxID)
    
    OID = maxID[0] + 1
    logger.debug('Incremented Order ID for profit target %s', OID)
    idOrder = OID
    Bracket = "Profit Target"
    
    #cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, today, timer, Currency, TriggerID[0], str(ProfitTargetVal2), Strategy, Bracket, Status))
    #cnx.commit() #Profit Target
    #logger.debug('Profit target entered into Order Table')
    
    #query = ("UPDATE hasPosition SET BB_ProfitID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
    #cur.execute(query)
    #cnx.commit()
        
logger.debug('Try to Cancel Stop')    
logger.debug('Stop API ID %s', stop_api_id)   
logger.debug('Profit API ID %s', profit_api_id)   
logger.debug('Stop API ID %s', type(stop_api_id))   
logger.debug('Profit API ID %s', type(profit_api_id))          
logger.debug('Pos is %s', inPos)
logger.debug('CurCount is %s', curCount[0])
logger.debug('In Pos %s', inPos)
logger.debug('Stop ID is %s', Order_stop[0])

query = ("SELECT BBEntryPending from hasPosition where CCY =\'" + CCY1 + CCY2 +"\';")
logger.debug('query is %s', query)
cur.execute(query)
for (BBEntryPending) in cur:
    EntryPend = BBEntryPending
    
logger.debug('EntryPend is %s', EntryPend[0])
"""
Created on Sun Jan 08 09:16:43 2017

If Profit Target has been filled 
CHECK BY INVERSE  EURUSD STOPLOSS ORDERID SHOULD STILL BE OUT THERE

@author: Michael
""" 
    
#if (int(curCount[0]) == 1 and int(inPos) == 0 and int(stop_api_id) == int(Order_stop[0]) and int(profit_api_id) == 0):
#if (int(curCount[0]) == 1 and int(inPos) == 0  and int(EntryPend[0]) == 0):
#        logger.error('Profit Target Hit! Clearing Position information')
#        #logger.debug('Stop Order ID is %s', Order_stop[0])
#        #conn.cancelOrder(Order_stop[0])
#       
#        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        #Update Trades Table
#       
#       #Clear hasPosition Table
#        query = ("UPDATE hasPosition SET BB_Position = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_StopLossFlag = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_EntryID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_ProfitID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_StopID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_EntryPrice = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE hasPosition SET BB_ProfitPrice = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 15")
#        cur.execute(query)
#        for (RiskParametersValue) in cur:
#            MaxPositions = RiskParametersValue
#            logger.debug('Max Positions is %s', MaxPositions)
#        
#        MaxPositions2 = MaxPositions[0] - 1
#        logger.debug('Max Positions is %s', MaxPositions[0])
#        
#        query = ("UPDATE RiskParameters SET RiskParametersValue = " + str(MaxPositions2) + " where idRiskParameters = 15")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#
#logger.debug('Stop API ID %s', stop_api_id)   
#logger.debug('Profit API ID %s', profit_api_id)  
#logger.debug('Stop API ID %s', type(stop_api_id))   
#logger.debug('Profit API ID %s', type(profit_api_id))          
#logger.debug('Pos is %s', inPos)
#logger.debug('CurCount is %s', curCount[0])
#logger.debug('In Pos %s', inPos)
#logger.debug('profitID is %s', Order_profit[0])
#logger.debug('stopID is %s', Order_stop[0])

#-5 < pos2 < 5 and api_id == Order_stop[0] and


"""
Created on Sun Jan 08 09:16:43 2017

If Stop Loss has been filled 

@author: Michael
"""
logger.debug('CHECKING IF STOP LOSS FILLED')
#If Stop Loss has been filled     
#if(int(curCount[0]) == 1 and int(inPos) == 0 and int(profit_api_id) == int(Order_profit[0]) and int(stop_api_id) == 0):  #Position is 0 but Profit Target still exists
if(int(curCount[0]) == 1 and int(inPos) == 0  and int(EntryPend[0]) == 0):
        logger.debug('Stop Loss Hit! Clearing Position information')
#        logger.debug('ProfitId to cancel is %s',Order_profit[0])
#        conn.cancelOrder(Order_profit[0])
#        logger.debug('Order Canceled')
       
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
       
       #Clear hasPosition Table
        query = ("UPDATE hasPosition SET BB_Position = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopLossFlag = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_EntryID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_ProfitID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_EntryPrice = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_ProfitPrice = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 15")
        cur.execute(query)
        for (RiskParametersValue) in cur:
            MaxPositions = RiskParametersValue
            logger.debug('Max Positions is %s', MaxPositions)
        
        MaxPositions2 = MaxPositions[0] - 1
        logger.debug('Max Positions is %s', MaxPositions[0])
        
        query = ("UPDATE RiskParameters SET RiskParametersValue = " + str(MaxPositions2) + " where idRiskParameters = 15")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + "0" + " WHERE idRiskParameters='20'")
        cur.execute(query)
        cnx.commit()
        logger.debug('Master Fill set to 0')

        #api_id == Order_entry[0] and yesterday2 == entry_date and 
logger.debug('Entry Date is %s',entry_date)
logger.debug('confirming yesterday is %s', yesterday2)
logger.debug('Order Profit ID is %s', Order_profit[0])
logger.debug('Order Entry ID is %s', Order_entry[0])
logger.debug('API ID is  %s', api_id)
logger.debug('Current Position is %s', curCount[0])
logger.debug('Current Position is %s', type(curCount[0]))
logger.debug('Checking if Positions should be close at EOD')
time = datetime.datetime.now().time()
logger.debug('Time is %s', time.hour)
logger.debug('Time is %s', type(time.hour))
    #curCount[0] == 0 and and int(api_id) == int(Order_profit[0])
#


"""
Created on Sun Jan 08 09:16:43 2017
Cancel all Entries and Profit Targets at End of day


@author: Michael
"""

if (time.hour > 15 and int(curCount[0]) == 0):
        logger.error('Setup Never Executed. Clearing Position information and Orders')
        
        #conn.cancelOrder(int(Order_profit[0]))
        #logger.error('Canceled Order %s', Order_profit[0] )
        
        conn.cancelOrder(int(Order_entry[0]))
        logger.error('Canceled Order %s', Order_entry[0] )
        
        ##Update Orders Table
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_entry[0]) + ";")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
#        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
        
#        conn.cancelOrder(int(Order_stop[0]))
#        logger.error('Canceled Order %s', Order_stop[0] )
#        
#        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
        
      #Clear hasPosition Table  
        query = ("UPDATE hasPosition SET BB_StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_EntryID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_Position = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_ProfitID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_StopID = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BBEntryPending = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_EntryPrice = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_ProfitPrice = " + "0" + " where CCY = \'" + CCY1 + CCY2 + "\'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
#        query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 15")
#        cur.execute(query)
#        for (RiskParametersValue) in cur:
#            MaxPositions = RiskParametersValue
#            logger.debug('Max Positions is %s', MaxPositions)
#        
#        MaxPositions2 = MaxPositions[0] - 1
#        logger.debug('Max Positions is %s', MaxPositions[0])
#
#        query = ("UPDATE RiskParameters SET RiskParametersValue = " + str(MaxPositions2) + " where idRiskParameters = 15")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()

conn.disconnect()
logger.debug('Disconnected from IBController')
logger.debug('END POS MGMT SCRIPT :-!')