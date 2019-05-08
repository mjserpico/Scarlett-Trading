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

Order_entry = 0
Order_profit = 0
Order_stop = 0
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
masteraccount = 'DU501213'

def reply_handler(msg):
    test0 = msg
    acct = msg.account
    global pos
    pos = msg.pos
    print(pos)
    if acct =='DU501213':
        print("FULL MESSAGE is ")
        print(test0)
        print(pos)
    
def reply_handler_Orders(msg):
    test0 = msg
    print("FULL MESSAGE is ")
    print(test0)


def reply_handler_Status(msg):
    test0 = msg
    order_status = msg.status
    print("FULL MESSAGE is ")
    print(test0)
    print(order_status)

    
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
        print(qty)
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        print("In make order_stop")
        print(limit)
        order.m_orderType = 'STP'

        if action == 'Sell':
            order.m_lmtPrice  = float(stopVal[0])
            print(order.m_lmtPrice)
            stopPrice = float(stopVal[0])
            print(stopPrice)
            order.m_auxPrice = stopPrice;
            order.m_account = masteraccount
                #order.m_parentId = parentId
            print(transmit)
            order.m_transmit = transmit
            print("In sell of make order stop")
        if action == 'Buy':
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
            order.m_lmtPrice  = float(stopVal[0])
            stopPrice = float(stopVal[0])
            order.m_auxPrice = stopPrice;
            order.m_account = masteraccount
            #order.m_parentId = parentId
            print("in stp order of make order2")
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit

        return order
        
#Main code
    
conn = Connection.create(port=4002, clientId=999)
conn.connect() 
time.sleep(1)

cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cur = cnx.cursor()

##Quick pulls for Trade Details

query = ("SELECT idOrder FROM Orders where Currency = \'" + CCY1 + CCY2 + "\'"" and Status = \'" + submit + "\'"" and Bracket = " + "\'" + entry + "\'")
print(query)
cur.execute(query)
print(query)
for (idOrder) in cur:
    Order_entry = idOrder
    print("Order entry is")
    print(Order_entry)
    
query = ("SELECT idOrder FROM Orders where Currency = \'" + CCY1 + CCY2 + "\'"" and Status = \'" + submit + "\'"" and Bracket = " + "\'" + profits + "\'")
cur.execute(query)
for (idOrder) in cur:
    Order_profit = idOrder
    print("Order Profit is")
    print(Order_profit)
    
query = ("SELECT idOrder FROM Orders where Currency = \'" + CCY1 + CCY2 + "\'"" and Status = \'" + submit + "\'"" and Bracket = " + "\'" + stoploss + "\'")
cur.execute(query)
for (idOrder) in cur:
    Order_stop = idOrder
    print("Order Stop is")
    print(Order_stop)
    
query = ("SELECT Date FROM Orders where Currency = \'" + CCY1 + CCY2 + "\'"" and Status = \'" + submit + "\'"" and Bracket = " + "\'" + entry + "\'")
cur.execute(query)
for (Date) in cur:
    entry_date = Date
    print(entry_date)
    
query = ("SELECT StopLossVal FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
for (StopLossVal) in cur:
    stopVal = StopLossVal
    print(stopVal)
query = ("SELECT StopQty FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
for (StopQty) in cur:
    qty = StopQty
    print(qty)
query = ("SELECT direction FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
for (direction) in cur:
    directionTrade = direction
    print(directionTrade)
query = ("SELECT Count FROM hasPosition where CCY = \'" + CCY1 + CCY2 + "\'")
cur.execute(query)
for (Count) in cur:
    curCount = Count
    print(curCount)
       
#Calculate yesterday's date
#Find today's date and Day of the week
today = datetime.date.today( )
print("Today is " + str(today))
dayofweek = datetime.datetime.today().weekday()
print(dayofweek)
today2 = str(today)

##Convert Date to proper format and relative reference
if dayofweek == 0:  #if Today is Monday
    yesterday = today - datetime.timedelta(days=6)  #Get Previous Wednesday                   
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    print(yesterday2)

else:
    yesterday = today - datetime.timedelta(days=3) #Take 3 Days back                    
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    print("Yesterday was " + str(yesterday2))
    


conn.register(reply_handler, 'Position')
conn.register(reply_handler_Orders, 'OpenOrder') 
conn.register(reply_handler_Status, 'OrderStatus')      
conn.reqAllOpenOrders() # will find the order if it's open
time.sleep(1)  #TWS returns two messages  OrderStatus and Openorder  only for submitted orders or partial fills
conn.reqPositions() # will find the order if it was filled
time.sleep(1)
 #give IB time to send us messages
print(pos)
pos2 = int(pos)
print(type(pos2))
print(pos2)

#If Entry has been filled
if (pos2 != 0):
    # create a stop loss order, and THEN transmit(set transmit to true) the entire order by placing this last child order(note inTWS it looks like a tree with parent order and two sub orders inside)
        print("in Stop loss")
        Bracket = "Stop Loss"
        print(Order_profit)
        OID = int(Order_profit[0]) + 1
        print(OID)
        idOrder = OID
        Price = StopLossVal
        print(symbol)
        print(secType)
        print(exchange)
        PosSize = int(qty[0])
        TriggerID = Order_entry[0]
        CONTRACT = create_contract(symbol, secType, exchange, exchange, symbol2)
        print(CONTRACT)
        if(directionTrade[0] == "Short"):
            ORDER = make_order_stop(action, PosSize, limit, transmit=True)
            conn.placeOrder(OID, CONTRACT, ORDER)  
            print("called place order")
        if(directionTrade[0] == "Long"):
            print(counter_action)
            print(qty[0])
            print(limit)
            print(OID)
            print(PosSize)
            ORDER = make_order_stop(counter_action, PosSize, limit, transmit=True)
            conn.placeOrder(OID, CONTRACT, ORDER)    
            print("called Long section")
        
        #Update hasPosition Table
        query = ("UPDATE hasPosition SET Count = " + "1" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        StopLossVal2 = float(StopLossVal[0])
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, today2, timer, Currency, TriggerID, StopLossVal2, Strategy, Bracket, Status))
        cnx.commit() #Profit Target
        
        print(type(Order_entry[0]))
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_entry[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
       
#If Profit Target has been filled     
if (-5 < pos2 < 5 and api_id == Order_profit[0] and curCount == 1):

        conn.cancelOrder(Order_stop[0])
       
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
        #Update Trades Table
       
       #Clear hasPosition Table
        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()


        
#If Stop Loss has been filled     
if (-5 < pos2 < 5 and api_id == Order_stop[0] and curCount == 1):

        conn.cancelOrder(Order_profit[0])
       
        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrder = " + str(Order_stop[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
       
       #Clear hasPosition Table
        query = ("UPDATE hasPosition SET Count = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()

#Cancel all Entries and Profit Targets after 3 days
if (api_id == Order_entry[0] and yesterday2 == entry_date and curCount == 0):

        conn.cancelOrder(Order_profit[0])
        conn.cancelOrder(Order_entry[0])
        ##Update Orders Table
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_entry[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE Orders SET Status = \'" + "Canceled" + "\' where idOrder = " + str(Order_profit[0]) + ";")
        print(query)
        cur.execute(query)
        cnx.commit()
        
      #Clear hasPosition Table  
        query = ("UPDATE hasPosition SET StopLossVal = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET StopQty = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()
        query = ("UPDATE hasPosition SET direction = " + "0" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        cur.execute(query)
        cnx.commit()

conn.disconnect()