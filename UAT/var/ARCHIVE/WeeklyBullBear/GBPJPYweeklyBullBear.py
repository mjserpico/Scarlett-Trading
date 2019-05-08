# -*- coding: utf-8 -*-
"""
@author: Michael
"""
#
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 
import mysql.connector
import time
import datetime
import logging


#Variables Imported From Database
totalRiskPercent = 0.0
riskPerPosition = 0.0
currentPositions = 0.0
profitTarget = 0.0
stopLoss = 0.0
AcctBalanceBasis = 0.0
MaxPositions = 0
CurrentPositions = 0
RiskRewardRatio = 0
MovingAvg = 0
CCY1 = 'GBP'
CCY2 = 'JPY'
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
masteraccount = 'DU501213'

today = datetime.date.today( )
logger = logging.getLogger('GBPJPY')
hdlr = logging.FileHandler('log/GBPJPY' + str(today) + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
#logger.setLevel(logging.WARNING)
logger.error('Starting GBPJPY')


#TWS Async Reply handler
def reply_handler(msg):
    #test = msg.value
    print(msg)
    
def error_handler(msg):
    """Handles the capturing of error messages"""
    print(msg)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


        #bracket order function for Short Trades
def make__short__order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        print("In make order")
        if limit == 2:
            if action == 'BUY':
                print(ProfitPips)
                order.m_lmtPrice  = truncate(float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                print("In Profit Take")
                print(order.m_lmtPrice)
                print(RiskRewardRatio)
                order.m_orderType = 'LMT'
                order.m_account = masteraccount
                order.m_transmit = transmit
#            elif action == 'SELL':
#                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
#                order.m_lmtPrice  = float(truncate(float(tLow[0]),4)) - 0.0005
#                print("In Profit Take")
#                print(RiskRewardRatio)
            order.m_transmit = transmit
        elif limit == 1:
       	# ENTRY   A simple stop order
            order.m_orderType = 'STP'
            if action == 'BUY':
                print(ProfitPips)
                print(RiskRewardRatio)
                order.m_lmtPrice  = truncate(float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                stopPrice = truncate(float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                print("In Profit Take")
                print(stopPrice)
                order.m_auxPrice = stopPrice
                #order.m_parentId = parentId
                order.m_account = masteraccount
                order.m_transmit = transmit

            if action == 'SELL':
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                order.m_lmtPrice  = float(truncate(float(tLow[0]),4)) - 0.0005
                stopPrice = float(truncate(float(tLow[0]),4)) - 0.0005
                order.m_auxPrice = stopPrice;
                order.m_parentId = parentId
                order.m_account = masteraccount
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit

        return order    

#Bracket Order function for Long Trades
def make_order2(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        print("In make order2")
        print(limit)
        if limit == 2:
            if action == 'SELL':
                print(ProfitPips)
                order.m_lmtPrice  = truncate(float(tHigh[0]) + ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                print("In limit order of make order2")
                print(order.m_lmtPrice)
                print(RiskRewardRatio)
                order.m_orderType = 'LMT'
                order.m_account = masteraccount
                order.m_transmit = transmit
#            elif action == 'SELL':
#                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
#                order.m_lmtPrice  = float(truncate(float(tLow[0]),4)) - 0.0005
#                print("In Profit Take")
#                print(RiskRewardRatio)
            order.m_transmit = transmit
        elif limit == 1:
       	# ENTRY   A simple stop order
            order.m_orderType = 'STP'
            print("in limit 1 of makeorder2")
            print(action)
            if action == 'BUY':
            	# Rounding is due to FX, we cannot create an order with bad price, and FX book increments at 0.00005 only!
                #order.m_lmtPrice  = limit - int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                order.m_lmtPrice  = float(truncate(float(tHigh[0]),4)) + 0.0005
                stopPrice = float(truncate(float(tHigh[0]),4)) + 0.0005
                order.m_auxPrice = stopPrice;
                order.m_parentId = parentId
                order.m_account = masteraccount
            elif action == 'SELL':
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                order.m_lmtPrice  = float(truncate(float(tLow[0]),4)) - 0.0005
                stopPrice = float(truncate(float(tLow[0]),4)) - 0.0005
                order.m_auxPrice = stopPrice;
                order.m_parentId = parentId
                order.m_account = masteraccount
                print("in stp order of make order2")
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit

        return order    
        
def create_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

#Main Function of code
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cur = cnx.cursor()
logger.error('Connecting To Database')
##Quick checks for Trade Eligibility
query = ("SELECT Count from hasPosition where CCY =\'" + CCY1 + CCY2+"\';")
cur.execute(query)
for (Count) in cur:
    hasPosition = Count

print(hasPosition)  
if hasPosition == 1:
    exit(1)

query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 4")
cur.execute(query)
for (RiskParametersValue) in cur:
    MaxPositions = RiskParametersValue

print(MaxPositions) 
  
if MaxPositions == 5:
    exit(1)    
#
#   
#Risk Parameter Values
#
#
#TotalRiskPercent
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 1")
cur.execute(query)
for (RiskParametersValue) in cur:
    totalRiskPercent = RiskParametersValue

print(totalRiskPercent)  

#TotalRiskPercent
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 2")
cur.execute(query)
for (RiskParametersValue) in cur:
    riskPerPosition = RiskParametersValue

print(riskPerPosition) 
  
#AcctBalanceBasis
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 3")
cur.execute(query)
for (RiskParametersValue) in cur:
    AcctBalanceBasis = RiskParametersValue

print(AcctBalanceBasis)
   
#MaxPositions
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 4")
cur.execute(query)
for (RiskParametersValue) in cur:
    MaxPositions = RiskParametersValue

print(MaxPositions)  

#CurrentPositions
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 5")
cur.execute(query)
for (RiskParametersValue) in cur:
    CurrentPositions = RiskParametersValue

print(CurrentPositions) 

#RiskRewardRatio
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 6")
cur.execute(query)
for (RiskParametersValue) in cur:
    RiskRewardRatio = RiskParametersValue

print(RiskRewardRatio)

#stoploss
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 7")
cur.execute(query)
for (RiskParametersValue) in cur:
    stopLoss = RiskParametersValue

print(stopLoss)  

#profittarget
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 8")
cur.execute(query)
for (RiskParametersValue) in cur:
    profitTarget = RiskParametersValue

print(profitTarget)  

#MovingAvg Length
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 10")
cur.execute(query)
for (RiskParametersValue) in cur:
    MovingAvg = RiskParametersValue
    
print(MovingAvg) 

#Today's OHLC value

query = ("SELECT Open from w" + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (Open) in cur:
    tOpen = Open

print(tOpen)  

query = ("SELECT High from w" + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (High) in cur:
    tHigh = High

print(tHigh)  

query = ("SELECT Low from w" + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (Low) in cur:
   tLow = Low

print(tLow)  

query = ("SELECT Close from w" + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (Close) in cur:
    tClose = Close

print(tClose)  

#Calculate yesterday's date
#Find today's date and Day of the week
today = datetime.date.today( )
print("Today is " + str(today))
dayofweek = datetime.datetime.today().weekday()
print(dayofweek)


##Convert Date to proper format and relative reference
if dayofweek == 0:  #if Today is Monday
    yesterday = today - datetime.timedelta(days=3)  #Get Friday                   
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    print(yesterday2)

else:
    yesterday = today - datetime.timedelta(days=1) #Take 1 Day back                    
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    print("Yesterday was " + str(yesterday2))

#Yesterday's OHLC value

query = ("SELECT Open from w" + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (Open) in cur:
    yOpen = Open

print(yOpen)  

query = ("SELECT High from w" + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (High) in cur:
    yHigh = High

print(yHigh)  

query = ("SELECT Low from w" + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (Low) in cur:
    yLow = Low

print(yLow)  

query = ("SELECT Close from w" + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (Close) in cur:
    yClose = Close

print(yClose)  
 
#MovingAverage Calculation
#Step 1 Get earliest Date to calculate avg from
#reformat date to DB convention first
print("Today is still " + str(today))
backdate = today - datetime.timedelta(days=50)
print("Date shifted back 50 is" + str(backdate))
dayofweek = backdate.weekday()

#Adjust for Saturdays and Sundays: No price data available.  
if dayofweek == 6:
    backdate = today - datetime.timedelta(days = 49)
if dayofweek == 5:
    backdate = today - datetime.timedelta(days = 48)
    
month = (str(0) + str(backdate.month))
day = (str(0)+ str(backdate.day))
backdate2 = (month[-2:] +"/"+ day[-2:] +"/"+str(backdate.year))
print("First Date of Moving Average is " + str(backdate2)) #date which gives first datapoint in Moving Average

#Select ID from EURUSD where Date in ('12/19/2016', '02/07/2017');
#Select round(Avg(Close),5) from EURUSD where ID BETWEEN 3881 AND 3915;
query = ("SELECT ID from w" + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (ID) in cur:
    ID1 = ID
query = ("SELECT ID from w" + CCY1 + CCY2 + " where Date = \"" + backdate2 + "\"")
cur.execute(query)
for (ID) in cur:
    ID2 = ID
print("ID1 is " + str(ID1)) 
print("ID2 is " + str(ID2))

#query = ("SELECT round(Avg(Close),5) as Avg from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID2[0]) + " AND " +  str(ID1[0]) + ";")
#cur.execute(query)
#for (Avg) in cur:
#    MovAvg = Avg   #Final Moving Average Value
#print(MovAvg)
#
###Puts Moving Average Value in hasPosition Table for Reference with intraday strategies
#query = ("UPDATE hasPosition SET BB_DailyMovingAvgValue = " + str(MovAvg[0]) + " where CCY =\'" + CCY1 + CCY2 +"\';")
#print(query)
#cur.execute(query)
#cnx.commit()

# Order ID Management
# Pull Last OID from Database and set OID to that plus 1
query = ("SELECT max(idOrder) from Orders;")
cur.execute(query)
for (idOrder) in cur:
    OID = int(idOrder[0]) + 1
print("Order Id for next trade is " + str(OID))

##Position Size Calculation
DollarLoss = AcctBalanceBasis[0] * riskPerPosition[0]  # allowable Dollar loss per trade
print("Dollar Loss permitted is " + str(DollarLoss))
print(tHigh)
print(tLow)
StopLossPips = int(round((float(tHigh[0]) - float(tLow[0]))*10000,0))  # Stop Loss Pips for Position Sizing ratio
print(StopLossPips)
PositionSize = (DollarLoss/StopLossPips)*10000   # Position Size to Take
print("Position Size for trade is " + str(PositionSize))
ProfitPips = (StopLossPips * int(RiskRewardRatio[0]))
print(ProfitPips)
#amountProfit = 10000*ProfitPips
#print(amountProfit)

##Strategy Logic
##Only try to place trades if eligible slot exists
if (CurrentPositions < MaxPositions):
    logger.error('There is an available position slot for USDZAR')
    symbol = CCY1
    symbol2 = CCY2
    secType  = 'CASH'
    exchange = 'IDEALPRO'
    action   = 'BUY'
    counter_action = 'SELL'
    idOrder = int(OID)
    qty = int(PositionSize)
    limit = 1 
    Date = today
    time = "6:00"  #placeholder for Orders. Use when intraday strategies go into effect
    Currency = CCY1+CCY2
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    Price = float(truncate(float(tHigh[0]),4)) + 0.0005
    Strategy = "WeeklyBullBear"
    Bracket = "Entry"
    Status = "Submitted"
    parentId = OID
    RiskReward = RiskRewardRatio

#LONG TRADES

    if (#float(tClose[0]) > MovAvg[0] and  #{ If Price Above the Average }
        tClose > tOpen and  # if Up day
        tHigh > yHigh and  # if engulfing candle (high and low today bigger than yesterday)
        tLow < yLow and
        yClose < yOpen # if yesterday was a down day
        ):
        print("Long trade Entry")
        logger.error('Long trade Found')
        #TWS Connection
        conn = Connection.create(port=4002, clientId=999)
        conn.registerAll(reply_handler)
        conn.connect()
        #time.sleep(1) #give IB time to send us messages
        
        #Order Query 
#        amount = float(truncate(float(tHigh[0]),4)) + 0.0005  # Stop Price for Long trades
#        idOrder = int(OID)
#        Date = today
#        time = "6:00"  #placeholder for Orders. Use when intraday strategies go into effect
#        Currency = CCY1+CCY2
#        TriggerID = OID
#        Price = float(truncate(float(tHigh[0]),4)) + 0.0005
#        Strategy = "DailyBullBear"
#        Bracket = "Entry"
#        Status = "Submitted"
#        qty = int(PositionSize)
#        limit = 1   #tick mark to set up limit

#Create Stp Buy Order 5 pips above High
        CONTRACT = create_contract(symbol, secType, exchange, exchange, symbol2)
        ORDER = make_order2(action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit() #Primary Trade

# create a profit take order of some kind
        limit = 2
        Price = float(tHigh[0]) + ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0]))
        Bracket = "Profit Target"
        OID = OID + 1
        idOrder = OID
        ORDER = make_order2(counter_action, qty, limit, parentId=OID, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit() #Profit Target

        #Update CurrentPosition
        newCurPos = CurrentPositions[0] + 1
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + str(newCurPos) + " WHERE idRiskParameters='5'")
        cur.execute(query)
        cnx.commit()
        
        #Put StopLoss Value in hasPosition Table as Placeholder
        StopLossvalue = float(truncate(float(tLow[0]),4)) - 0.0005
        query = ("UPDATE hasPosition SET w_StopLossVal = " + str(StopLossvalue) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET w_StopQty = " + str(qty) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET w_direction = 'Long' WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        
        conn.disconnect()
#        ##Update Orders Table
#        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
#        cnx.commit()#Stop Loss
   
#SHORT TRADES

    action   = 'SELL'
    counter_action = 'BUY'
    idOrder = int(OID)
    qty = int(PositionSize)
    limit = 1 
    Date = today
    time = "6:00"  #placeholder for Orders. Use when intraday strategies go into effect
    Currency = CCY1+CCY2
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    Price = float(truncate(float(tLow[0]),4)) - 0.0005
    Strategy = "WeeklyBullBear"
    Bracket = "Entry"
    Status = "Submitted"
    parentId = OID
    RiskReward = RiskRewardRatio
        
    if (#float(tClose[0]) < MovAvg[0] and   #{ If Price below the Average }
        tClose < tOpen and     # bar closes down
        tHigh > yHigh and   # 
        tLow < yLow and
        yClose > yOpen
        ):
        print("Short trade entry")
        logger.error('Short trade Found')
        #TWS Connection
        conn = Connection.create(port=4002, clientId=999)
        conn.registerAll(reply_handler)
        conn.connect()
        #time.sleep(1) #give IB time to send us messages
        
#Create STP Sell order 5 pips below Low
        CONTRACT = create_contract(symbol, secType, exchange, exchange, symbol2)
        ORDER = make__short__order(action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)

        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit() #Primary Trade
        
 #Update CurrentPosition
        newCurPos = CurrentPositions[0] + 1
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + str(newCurPos) + " WHERE idRiskParameters='5'")
        cur.execute(query)
        cnx.commit()

# create a profit take order of some kind
        print(RiskReward)
        Price = float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0]))
        print(Price)
        Bracket = "Profit Target"
        OID = OID + 1
        idOrder = OID
        limit = 2
        ORDER = make__short__order(counter_action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit()#Profit Target 
        
        StopLossvalue = float(truncate(float(tHigh[0]),4)) + 0.0005
        query = ("UPDATE hasPosition SET w_StopLossVal = " + str(StopLossvalue) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET w_StopQty = " + str(qty) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET w_direction = 'Short' WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        
        conn.disconnect()
        
logger.removeHandler(hdlr)
logging.shutdown()