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
import sys
import datalink  #universal logins for environment


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
CCY1 = 'Z'
CCY2 = 'C'
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
masteraccount = datalink.DB_Account

logging.basicConfig(filename='pythonlogs\DailyBullBear' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('DailyBullBear' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')
logger.debug('Starting Daily Bull Bear %s %s', CCY1,CCY2)

#TWS Async Reply handler
def reply_handler(msg):
    #test = msg.value
    logger.debug('Reply Handler %s', msg)
    
def error_handler(msg):
    """Handles the capturing of error messages"""
    logger.debug('Error Handler %s', msg)

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
        logger.debug('In Short Order Function')
        if limit == 2:
            logger.debug('In Limit is 2 section')
            if action == 'BUY':
                logger.debug('In Buy sections Profit Take')
                order.m_lmtPrice  = truncate(float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                logger.debug('Limit Price is %s', order.m_lmtPrice)
                logger.debug('RiskReward Ratio is %s', RiskRewardRatio)
                order.m_orderType = 'LMT'
                order.m_account = masteraccount
                order.m_transmit = transmit
            order.m_transmit = transmit
        elif limit == 1:
       	# ENTRY   A simple stop order
            logger.debug('In Limit is 1 Function')
            order.m_orderType = 'STP'
            if action == 'BUY':
                logger.debug('In Limit 1. in Buy action')
                logger.debug('RiskReward Ratio is %s', RiskRewardRatio)
                order.m_lmtPrice  = truncate(float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                stopPrice = truncate(float(tLow[0]) - ((float(truncate(float(tHigh[0]),4))- float(truncate(float(tLow[0]),4))) * int(RiskReward[0])),4)
                logger.debug('Stop Price is %s', stopPrice)
                #order.m_parentId = parentId
                order.m_account = masteraccount
                order.m_transmit = transmit

            if action == 'SELL':
                logger.debug('In Limit 1. in Sell action')
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
        logger.debug('In Long Order Function')
        print(limit)
        if limit == 2:
            if action == 'SELL':
                print(ProfitPips)
                order.m_lmtPrice  = truncate(float(tHigh[0]) + ((float(truncate(float(tHigh[0]),1))- float(truncate(float(tLow[0]),1))) * int(RiskReward[0])),1)
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
                order.m_lmtPrice  = float(truncate(float(tHigh[0]),1)) + 0.2
                stopPrice = float(truncate(float(tHigh[0]),1)) + 0.2
                order.m_auxPrice = stopPrice;
                order.m_parentId = parentId
                order.m_account = masteraccount
            elif action == 'SELL':
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                order.m_lmtPrice  = float(truncate(float(tLow[0]),1)) - 0.2
                stopPrice = float(truncate(float(tLow[0]),1)) - 0.2
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
    contract.m_localSymbol = CCY1+CCY2 + datalink.monthcode + "7";
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract
    logger.debug('Contract created')
    
logger.debug('Connecting To Database')    
#Main Function of code
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
#cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connected To Database')
##Quick checks for Trade Eligibility

query = ("SELECT Count from hasPosition where CCY =\'" + CCY1 + CCY2+"\';")
logger.debug('Query is %s', query)
cur.execute(query)
for (Count) in cur:
    hasPosition = Count

logger.debug('count is %s', hasPosition[0])

 
if hasPosition[0] == '1':
    logger.debug('Has Position is 1. Exiting')
    sys.exit(1)

query = ("SELECT BB_Position from hasPosition where CCY =\'" + CCY1 + CCY2+"\';")
logger.debug('Query is %s', query)
cur.execute(query)
for (BB_Position) in cur:
    BBPosition = BB_Position

logger.debug('count is %s', BBPosition[0])

if BBPosition[0] == '1':
    logger.debug('BBPosition is 1. Exiting')
    sys.exit(1)
    
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 5")
logger.debug('Query is %s', query)
cur.execute(query)
for (RiskParametersValue) in cur:
    MaxPositions = RiskParametersValue

logger.debug('Max Positions %s', MaxPositions)
  
if MaxPositions[0] == 5:
    logger.debug('Max Position is 5. Exiting')
    sys.exit(1)    
#
#   
#Risk Parameter Values
#
#
#TotalRiskPercent
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 1")
logger.debug('Query is %s', query)
cur.execute(query)
for (RiskParametersValue) in cur:
    totalRiskPercent = RiskParametersValue

logger.debug('totalRiskPercent is %s', totalRiskPercent) 

#TotalRiskPercent
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 2")
cur.execute(query)
for (RiskParametersValue) in cur:
    riskPerPosition = RiskParametersValue

logger.debug('riskPerPosition is %s', riskPerPosition) 
  
#AcctBalanceBasis
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 3")
cur.execute(query)
for (RiskParametersValue) in cur:
    AcctBalanceBasis = RiskParametersValue

logger.debug('AcctBalanceBasis is %s', AcctBalanceBasis) 
   
#MaxPositions
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 4")
cur.execute(query)
for (RiskParametersValue) in cur:
    MaxPositions = RiskParametersValue
logger.debug('MaxPositions is %s', MaxPositions)   

#CurrentPositions
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 5")
cur.execute(query)
for (RiskParametersValue) in cur:
    CurrentPositions = RiskParametersValue

logger.debug('MaxPositions is %s', MaxPositions)   

#RiskRewardRatio
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 6")
cur.execute(query)
for (RiskParametersValue) in cur:
    RiskRewardRatio = RiskParametersValue

logger.debug('RiskRewardRatio is %s', RiskRewardRatio) 

#stoploss
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 7")
cur.execute(query)
for (RiskParametersValue) in cur:
    stopLoss = RiskParametersValue

logger.debug('stopLoss is %s', stopLoss) 

#profittarget
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 8")
cur.execute(query)
for (RiskParametersValue) in cur:
    profitTarget = RiskParametersValue

logger.debug('profitTarget is %s', profitTarget)   

#MovingAvg Length
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 10")
cur.execute(query)
for (RiskParametersValue) in cur:
    MovingAvg = RiskParametersValue
    
logger.debug('MovingAvg is %s', MovingAvg)  

query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 19")
cur.execute(query)
for (RiskParametersValue) in cur:
    BreakevenVal = RiskParametersValue
    
logger.debug('Breakeven Val is %s', BreakevenVal)  

#Today's OHLC value

query = ("SELECT Open from " + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (Open) in cur:
    tOpen = Open

logger.debug('tOpen is %s', tOpen)   

query = ("SELECT High from " + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (High) in cur:
    tHigh = High

logger.debug('tHigh is %s', tHigh)   

query = ("SELECT Low from " + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (Low) in cur:
   tLow = Low

logger.debug('tLow is %s', tLow)    

query = ("SELECT Close from " + CCY1 + CCY2 + " where Date = \"" + time.strftime("%m/%d/%Y")+ "\"")
cur.execute(query)
for (Close) in cur:
    tClose = Close

logger.debug('tClose is %s', tClose)   

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
    logger.debug('Yesterday2 was %s', str(yesterday2))

else:
    yesterday = today - datetime.timedelta(days=1) #Take 1 Day back                    
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Yesterday2 was %s', str(yesterday2)) 
    

#Yesterday's OHLC value

query = ("SELECT Open from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (Open) in cur:
    yOpen = Open

logger.debug('yOpen is %s', yOpen)  

query = ("SELECT High from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (High) in cur:
    yHigh = High

logger.debug('yHigh is %s', yHigh)   

query = ("SELECT Low from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (Low) in cur:
    yLow = Low

logger.debug('yLow is %s', yLow)  

query = ("SELECT Close from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (Close) in cur:
    yClose = Close

logger.debug('yClose is %s', yClose[0])   
 
#MovingAverage Calculation
#Step 1 Get earliest Date to calculate avg from
#reformat date to DB convention first
logger.debug('Today is still  %s', today)
backdate = today - datetime.timedelta(days=50)
logger.debug('Date shifted back 50 is %s', backdate)
dayofweek = backdate.weekday()

#Adjust for Saturdays and Sundays: No price data available.  
if dayofweek == 6:
    backdate = today - datetime.timedelta(days = 49)
if dayofweek == 5:
    backdate = today - datetime.timedelta(days = 48)
    
month = (str(0) + str(backdate.month))
day = (str(0)+ str(backdate.day))
backdate2 = (month[-2:] +"/"+ day[-2:] +"/"+str(backdate.year))
logger.debug('First Date of Moving Average is %s', backdate2)

#Select ID from EURUSD where Date in ('12/19/2016', '02/07/2017');
#Select round(Avg(Close),5) from EURUSD where ID BETWEEN 3881 AND 3915;
query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
cur.execute(query)
for (ID) in cur:
    ID1 = ID
    
query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \"" + backdate2 + "\"")
cur.execute(query)
for (ID) in cur:
    ID2 = ID
logger.debug('ID1 is %s', ID1)
logger.debug('ID2 is %s', ID2)


query = ("SELECT round(Avg(Close),5) as Avg from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID2[0]) + " AND " +  str(ID1[0]) + ";")
cur.execute(query)
for (Avg) in cur:
    MovAvg = Avg   #Final Moving Average Value
logger.debug('MovAvg is %s', MovAvg)

##Puts Moving Average Value in hasPosition Table for Reference with intraday strategies
query = ("UPDATE hasPosition SET BullBearMovingAvgValue = " + str(MovAvg[0]) + " where CCY =\'" + CCY1 + CCY2 +"\';")
logger.debug('Query is %s', query)
cur.execute(query)
cnx.commit()

#MovingAverage Calculation
#Step 1 Get earliest Date to calculate avg from
#reformat date to DB convention first
logger.debug('Today is still  %s', today)
backdate = today - datetime.timedelta(days=10)
logger.debug('Date shifted back 10 is %s', backdate)
dayofweek = backdate.weekday()

#Adjust for Saturdays and Sundays: No price data available.  
if dayofweek == 6:
    backdate = today - datetime.timedelta(days = 9)
if dayofweek == 5:
    backdate = today - datetime.timedelta(days = 8)
    
month = (str(0) + str(backdate.month))
day = (str(0)+ str(backdate.day))
backdate2 = (month[-2:] +"/"+ day[-2:] +"/"+str(backdate.year))
logger.debug('First Date of BB Moving Average is %s', backdate2)

#Select ID from EURUSD where Date in ('12/19/2016', '02/07/2017');
#Select round(Avg(Close),5) from EURUSD where ID BETWEEN 3881 AND 3915;
query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
logger.debug('Query is %s', query)
cur.execute(query)
for (ID) in cur:
    ID1 = ID
    
query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \"" + backdate2 + "\"")
logger.debug('Query is %s', query)
cur.execute(query)
for (ID) in cur:
    ID2 = ID
logger.debug('BB ID1 is %s', ID1)
logger.debug('BB ID2 is %s', ID2)


query = ("SELECT round(Avg(Close),5) as Avg from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID2[0]) + " AND " +  str(ID1[0]) + ";")
logger.debug('Query is %s', query)
cur.execute(query)
for (Avg) in cur:
    BBMovAvg = Avg   #Final Moving Average Value
logger.debug('BBMovAvg is %s', BBMovAvg)

##Puts Moving Average Value in hasPosition Table for Reference with intraday strategies
query = ("UPDATE hasPosition SET BB_STRATMovingAvgValue = " + str(BBMovAvg[0]) + " where CCY =\'" + CCY1 + CCY2 +"\';")
logger.debug('Query is %s', query)
cur.execute(query)
cnx.commit()



# Order ID Management
# Pull Last OID from Database and set OID to that plus 1
query = ("SELECT max(idOrder) from Orders;")
cur.execute(query)
for (idOrder) in cur:
    OID = int(idOrder[0]) + 1
    logger.debug('Order ID for next trade is %s', OID)


##Position Size Calculation
DollarLoss = AcctBalanceBasis[0] * riskPerPosition[0]  # allowable Dollar loss per trade
logger.debug('Dollar Loss permitted is %s', DollarLoss)
logger.debug('Current High %s', tHigh[0])
logger.debug('current Low %s', tLow[0])

StopLossPips = int(round((float(tHigh[0]) - float(tLow[0]))*10,0))  # Stop Loss Pips for Position Sizing ratio
logger.debug('StopLossPips is %s', StopLossPips)
PositionSize = 1#(DollarLoss/StopLossPips)*10000   # Position Size to Take
logger.debug('Position Size for trade is %s', PositionSize)

ProfitPips = (StopLossPips * int(RiskRewardRatio[0]))
logger.debug('ProfitPips is %s', ProfitPips)
#amountProfit = 10000*ProfitPips
#print(amountProfit)

##Strategy Logic
##Only try to place trades if eligible slot exists
logger.debug('Checking if a position can be entered')
logger.debug('Current Position is %s', CurrentPositions)
logger.debug('Max Position is %s', MaxPositions)
if (CurrentPositions < MaxPositions):
    logger.debug('There is an available position slot for %s%s', CCY1,CCY2)
    symbol   = CCY1+CCY2
    symbol2 = 'USD'
    secType  = 'FUT'
    exchange = 'GLOBEX'
    action   = 'BUY'
    counter_action = 'SELL'
    idOrder = int(OID)
    qty = int(PositionSize)
    limit = 1 
    Date = time.strftime("%m/%d/%Y")
    time = datetime.datetime.now().strftime("%I:%M%p")
    logger.debug('Time is %s', time)
    #placeholder for Orders. Use when intraday strategies go into effect
    Currency = CCY1+CCY2
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    Price = round(float(truncate(float(tHigh[0]),1)) + 0.2,1)
    Strategy = "DailyBullBear"
    Bracket = "Entry"
    Status = "Submitted"
    parentId = OID
    RiskReward = RiskRewardRatio

#LONG TRADES

    logger.debug('Checking for long trades')
    logger.debug('Today Close %s', tClose[0])
    logger.debug('Moving Avg is %s', MovAvg[0])
    logger.debug('tOpen is is %s', tOpen[0])
    logger.debug('tHigh is %s', tHigh[0])
    logger.debug('yHigh is %s', yHigh[0])
    logger.debug('tLow is %s', tLow[0])
    logger.debug('yLow is %s', yLow[0])
    logger.debug('yClose is %s', yClose[0])
    logger.debug('yOpen is %s', yOpen[0])

    if (float(tClose[0]) > MovAvg[0] and  #{ If Price Above the Average }
        tClose[0] > tOpen[0] and  # if Up day
        tHigh[0] > yHigh[0] and  # if engulfing candle (high and low today bigger than yesterday)
        tLow[0] < yLow[0] and
        yClose[0] < yOpen[0] # if yesterday was a down day
        ):
        logger.debug('Valid Long Entry Found')
        #TWS Connection
        logger.debug('connecting to database')
        conn = Connection.create(port=4002, clientId=999)
        logger.debug('connecting reply ')
        conn.registerAll(reply_handler)
        conn.connect()
        logger.debug('Valid Long Entry Found')

#Create Stp Buy Order 5 pips above High
        CONTRACT = create_contract(symbol, secType, exchange, exchange, 'USD')
        ORDER = make_order2(action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit() #Primary Trade
        query = ("UPDATE hasPosition SET EntryID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('query is %s', query)
        cur.execute(query)
        cnx.commit()

# create a profit take order of some kind
        limit = 2
        Price = round(float(tHigh[0]) + ((float(truncate(float(tHigh[0]),1))- float(truncate(float(tLow[0]),1))) * int(RiskReward[0])),1)
        logger.debug('Profit Target Price is %s', Price)
        Bracket = "Profit Target"
        OID = OID + 1
        idOrder = OID
        logger.debug('idOrder is %s', idOrder)
        ORDER = make_order2(counter_action, qty, limit, parentId=OID, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit() #Profit Target
        
        query = ("UPDATE hasPosition SET ProfitID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('query is %s', query)
        cur.execute(query)
        cnx.commit()

        #Update CurrentPosition
        newCurPos = CurrentPositions[0] + 1
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + str(newCurPos) + " WHERE idRiskParameters='5'")
        logger.debug('query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        #Put StopLoss Value in hasPosition Table as Placeholder
        StopLossvalue = round(float(truncate(float(tLow[0]),4)) - 0.0005,4)
        query = ("UPDATE hasPosition SET StopLossVal = " + str(StopLossvalue) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        Breakeven = round(float(truncate(float(tHigh[0]),4)) + 0.0005,4)
        logger.debug('Breakeven %s',Breakeven)
        query = ("UPDATE hasPosition SET Breakeven = " + str(Breakeven) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        logger.debug('Query is %s',type(float(tHigh[0])))
        logger.debug('Query is %s',type(float(truncate(float(tHigh[0]),4))))
        logger.debug('Query is %s',type(float(truncate(float(tLow[0]),4))))
        logger.debug('Query is %s',type(int(RiskReward[0])))
        logger.debug('Query is %s',type(float(BreakevenVal[0])))
                          
        BreakevenTrigger = round(float(tHigh[0]) + ((float(truncate(float(tHigh[0]),1))- float(truncate(float(tLow[0]),1))) * (int(RiskReward[0])* float(BreakevenVal[0]))),1)
        logger.debug('BreakevenTrigger %s', BreakevenTrigger)
        query = ("UPDATE hasPosition SET BreakevenTrigger = " + str(BreakevenTrigger) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + str(qty) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET direction = 'Long' WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('query is %s', query)
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
    time = datetime.datetime.now().strftime("%I:%M%p")
    logger.debug('Time is %s', time)    
    Currency = CCY1+CCY2
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    Price = round(float(truncate(float(tLow[0]),1)) - 0.2,1)
    Strategy = "DailyBullBear"
    Bracket = "Entry"
    Status = "Submitted"
    parentId = OID
    RiskReward = RiskRewardRatio

    logger.debug('Checking for short trades')
    logger.debug('Today Close %s', tClose[0])
    logger.debug('Moving Avg is %s', MovAvg[0])
    logger.debug('tOpen is is %s', tOpen[0])
    logger.debug('tHigh is %s', tHigh[0])
    logger.debug('yHigh is %s', yHigh[0])
    logger.debug('tLow is %s', tLow[0])
    logger.debug('yLow is %s', yLow[0])
    logger.debug('yClose is %s', yClose[0])
    logger.debug('yOpen is %s', yOpen[0])
        
    if (float(tClose[0]) < MovAvg[0] and   #{ If Price below the Average }
        tClose[0] < tOpen[0] and     # bar closes down
        tHigh[0] > yHigh[0] and   # 
        tLow[0] < yLow[0] and
        yClose[0] > yOpen[0]
        ):
        logger.debug('Valid ShortEntry Found')
        #TWS Connection
        conn = Connection.create(port=4002, clientId=999)
        conn.registerAll(reply_handler)
        conn.connect()
        logger.debug('Connected to IBController')
        #time.sleep(1) #give IB time to send us messages
        
#Create STP Sell order 5 pips below Low
        CONTRACT = create_contract(symbol, secType, exchange, exchange, 'USD')
        ORDER = make__short__order(action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        logger.debug('Contract built')
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit() #Primary Trade
        
 #Update CurrentPosition
        newCurPos = CurrentPositions[0] + 1
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + str(newCurPos) + " WHERE idRiskParameters='5'")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET EntryID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()

# create a profit take order of some kind
        logger.debug('riskreward is %s',RiskReward)
        Price = round(float(tLow[0]) - ((float(truncate(float(tHigh[0]),1))- float(truncate(float(tLow[0]),1))) * int(RiskReward[0])),1)
        logger.debug('Profit Price is %s',Price)
        Bracket = "Profit Target"
        OID = OID + 1
        idOrder = OID
        limit = 2
        ORDER = make__short__order(counter_action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, time.strftime("%m/%d/%Y"), time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        cnx.commit()#Profit Target 
        
                     
        query = ("UPDATE hasPosition SET ProfitID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        StopLossvalue = round(float(truncate(float(tHigh[0]),1)) + 0.2,1)
        logger.debug('StopLossValue %s',StopLossvalue)
        query = ("UPDATE hasPosition SET StopLossVal = " + str(StopLossvalue) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        Breakeven = round(float(truncate(float(tLow[0]),4)) - 0.2,1)
        logger.debug('Breakeven %s',Breakeven)
        query = ("UPDATE hasPosition SET Breakeven = " + str(Breakeven) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        
        logger.debug('Query is %s',type(float(tHigh[0])))
        logger.debug('Query is %s',type(float(truncate(float(tHigh[0]),4))))
        logger.debug('Query is %s',type(float(truncate(float(tLow[0]),4))))
        logger.debug('Query is %s',type(int(RiskReward[0])))
        logger.debug('Query is %s',type(float(BreakevenVal[0])))
        
        
        BreakevenTrigger = round(float(tLow[0]) -  ((float(truncate(float(tHigh[0]),1))- float(truncate(float(tLow[0]),1))) * (int(RiskReward[0])* float(BreakevenVal[0]))),1)
        logger.debug('BreakevenTrigger %s', BreakevenTrigger)
        query = ("UPDATE hasPosition SET BreakevenTrigger = " + str(BreakevenTrigger) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET StopQty = " + str(qty) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET direction = 'Short' WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s',query)
        cur.execute(query)
        cnx.commit()        
        conn.disconnect()
        
logger.debug('End BullBear %s%s', CCY1,CCY2)
