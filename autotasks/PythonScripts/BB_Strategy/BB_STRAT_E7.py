# -*- coding: utf-8 -*-
"""
@author: Michael
"""
#
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 
import mysql.connector
import datetime
import logging
import sys
import datalink  #universal logins for environment

logging.basicConfig(filename='pythonlogs\BBSTRATEGY' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('BBSTRATEGY' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

#Variables Imported From Database
#totalRiskPercent = 0.0
#riskPerPosition = 0.0
#currentPositions = 0.0
profitTarget = 0.0
stopLoss = 0.0
AcctBalanceBasis = 0.0
MaxPositions = 0
CurrentPositions = 0
#RiskRewardRatio = 0
MovingAvg = 0
CCY1 = 'E'
CCY2 = '7'
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
logger.debug('Starting BB_STRAT %s %s', CCY1,CCY2)


#TWS Async Reply handler
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


        #bracket order function for Short Trades
def make__short__order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Short Order Function')
        logger.debug('Limit Value is %s', limit)
        if limit == 2: # Profit Target
            logger.debug('In Limit is 2 subfunction')
            if action == 'BUY':
                logger.debug('In Profit Order Subfunction')
                #logger.debug('Profit Pips is: %s', ProfitPips)
                profitlimitprice = truncate((float(tLow[0]) - 0.0060), 4)
                #logger.debug('Risk Reward Ratio is: %s', RiskRewardRatio)
                logger.debug('Limit Price: %s', profitlimitprice)
                order.m_lmtPrice  = profitlimitprice
                order.m_orderType = 'LMT'
                order.m_account = masteraccount
                order.m_transmit = transmit
            order.m_transmit = transmit
            logger.debug('transmitted order')
        elif limit == 1:
            logger.debug('In Limit is 1 subfunction')
       	# ENTRY   A simple stop order
            order.m_orderType = 'MIT'
#            if action == 'BUY':
#                logger.debug('In Buy subfunction')
#                #logger.debug('Profit Pips is: %s', ProfitPips)
#                #logger.debug('Risk Reward Ratio is: %s', RiskRewardRatio)
#                order.m_lmtPrice  = (float(tLow[0]) - 0.0002)
#                stopPrice = truncate((float(tLow[0]) - 0.0002),4)   #Stop Order -- Entry Price
#                logger.debug('STP Price: %s', stopPrice)
#                
#                order.m_auxPrice = stopPrice
#                #order.m_parentId = parentId
#                order.m_account = masteraccount
#                order.m_transmit = transmit

            if action == 'SELL':
                logger.debug('In Sell subfunction')
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                lmtPrice = truncate((float(tLow[0]) - 0.0005),4)
                logger.debug('Buy Stop Limit"Limit" Price or better to buy %s', lmtPrice)
                order.m_lmtPrice  = lmtPrice
                stopPrice = truncate((float(tLow[0]) - 0.0002),4)
                logger.debug('Stop Price: %s', stopPrice)
                order.m_auxPrice = stopPrice;
                
                order.m_triggerMethod = 4
                order.m_parentId = parentId
                order.m_account = masteraccount
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit
        logger.debug('transmitted order')
        return order    

#Bracket Order function for Long Trades
def make_long_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Long Order Function')
        logger.debug('Limit Value is %s', limit)
        if limit == 2:  #Profit Target 
            if action == 'SELL':
                #logger.debug('Profit Pips is %s', ProfitPips)
                order.m_lmtPrice  = truncate((float(tHigh[0]) + 0.0060), 4)
                logger.debug('In Profit Target section of make long order')
                logger.debug('Profit Target Limit Order Price is is %s', order.m_lmtPrice)
                #logger.debug('Risk Reward Ratio is %s', RiskRewardRatio)
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
            order.m_orderType = 'MIT'
            logger.debug('In Long Order Function when Limit is 1')
            logger.debug('Action is %s', action)
            if action == 'BUY':
            	# Rounding is due to FX, we cannot create an order with bad price, and FX book increments at 0.00005 only!
                #order.m_lmtPrice  = limit - int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                logger.debug('In Buy action')
                lmtPrice = truncate((float(tHigh[0]) + 0.0005),4)
                logger.debug('Buy Stop Limit"Limit" Price or better to buy %s', lmtPrice)
                order.m_lmtPrice  = lmtPrice
                stopPrice = truncate((float(tHigh[0]) + 0.0002),4)
                logger.debug('Buy Stop Limit"Stop" Price to fire a buy order %s', stopPrice)
                order.m_auxPrice = stopPrice;
               
                order.m_triggerMethod = 4
                order.m_parentId = parentId
                order.m_account = masteraccount
                logger.debug('Buy Upper Limit Price %s', order.m_lmtPrice)
                logger.debug('Buy Upper Limit Type %s', type(order.m_lmtPrice))
                logger.debug('Stop Entry Trigger Price %s ', stopPrice)
                logger.debug('Stop Entry Trigger Type %s ', type(stopPrice))
                logger.debug('Parent ID %s', order.m_parentId)
                logger.debug('Account is %s', order.m_account)
#            elif action == 'SELL':
#                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
#                logger.debug('In Sell action')
#                order.m_lmtPrice  = truncate((float(tHigh[0]) + 0.0002),4)
#                stopPrice = truncate((float(tHigh[0]) + 0.0002),4)
#                order.m_auxPrice = stopPrice;
#                order.m_parentId = parentId
#                order.m_account = masteraccount
#                logger.debug('SEll Entry Price %s', order.m_lmtPrice)
#                logger.debug('Stop loss buy Price %s ', stopPrice)
#                logger.debug('Assigned Stop Price %s ', order.m_auxPrice)
#                logger.debug('Parent ID %s', order.m_parentId)
#                logger.debug('Account is %s', order.m_account)
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
    contract.m_currency = 'USD'
    return contract
    logger.debug('Contract created')
    
    
#Main Function of code
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
#cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connecting To Database')
##Quick checks for Trade Eligibility
query = ("SELECT Count from hasPosition where CCY =\'" + CCY1 + CCY2+"\';")
cur.execute(query)
for (Count) in cur:
    hasPosition = Count
    logger.debug('Has Position is %s', hasPosition)

 
if hasPosition[0] == '1':
    logger.debug('Has Position is 1. Now exiting')
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
    
#query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 15")
#cur.execute(query)
#for (RiskParametersValue) in cur:
#    MaxPositions = RiskParametersValue
#    logger.debug('Max Positions is %s', MaxPositions)
# 
#  
#if MaxPositions[0] == 4:
#    logger.debug('Max Position is 4. Now exiting')
#    sys.exit(1)    
#
#   
#Risk Parameter Values
#
#
#TotalRiskPercent -- DO NOT NEED FOR BB
#query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 1")
#cur.execute(query)
#for (RiskParametersValue) in cur:
#    totalRiskPercent = RiskParametersValue
#
#print(totalRiskPercent)  

#RiskPerPosition

query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 18")
cur.execute(query)
for (RiskParametersValue) in cur:
    stopPips = RiskParametersValue

logger.debug('Stop Loss pips is %s', stopPips)
  
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 13")
cur.execute(query)
for (RiskParametersValue) in cur:
    ProfitTargPips = RiskParametersValue

logger.debug('Profit Target Pips is %s', ProfitTargPips)
logger.debug('Profit Target Pips type is %s', type(ProfitTargPips))
  
#
#query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 11")
#cur.execute(query)
#for (RiskParametersValue) in cur:
#    riskPerPosition = RiskParametersValue
#
#logger.debug('Risk Per Position is %s', riskPerPosition)
  
#AcctBalanceBasis
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 12")
cur.execute(query)
for (RiskParametersValue) in cur:
    AcctBalanceBasis = RiskParametersValue

logger.debug('AcctBalanceBasis is %s', AcctBalanceBasis)

query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 20")
cur.execute(query)
for (RiskParametersValue) in cur:
    BB_SizeMultiplier = RiskParametersValue

logger.debug('BB_SizeMultiplier is %s', BB_SizeMultiplier)
#MaxPositions
#query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 4")
#cur.execute(query)
#for (RiskParametersValue) in cur:
#    MaxPositions = RiskParametersValue
#
#print(MaxPositions)  

#CurrentPositions
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 16")
cur.execute(query)
for (RiskParametersValue) in cur:
    CurrentPositions = RiskParametersValue

logger.debug('CurrentPositions is %s', CurrentPositions)

#RiskRewardRatio
#query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 17")
#cur.execute(query)
#for (RiskParametersValue) in cur:
#    RiskRewardRatio = RiskParametersValue
#
#logger.debug('RiskRewardRatio is %s', RiskRewardRatio)

#stoploss
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 18")
cur.execute(query)
for (RiskParametersValue) in cur:
    stopLoss = RiskParametersValue

logger.debug('stopLoss is %s', stopLoss)

#profittarget
query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 13")
cur.execute(query)
for (RiskParametersValue) in cur:
    profitTarget = RiskParametersValue

logger.debug('profitTarget is %s', profitTarget)  

#MovingAvg From Daily
query = ("SELECT BB_STRATMovingAvgValue from hasPosition WHERE CCY =\'" + CCY1 + CCY2+"\';")
cur.execute(query)
for (BB_STRATMovingAvgValue) in cur:
    MovAvg = BB_STRATMovingAvgValue
    
logger.debug('MovAvg is %s', MovAvg) 

#Today's OHLC value

query = ("SELECT max(ID) from FUT_BB_" + CCY1+CCY2+ ";")
logger.debug('MAX ID Query is %s', query) 
cur.execute(query)
for (ID) in cur:
    BB_ID = ID
logger.debug('ID for time period is %s', BB_ID) 

# '" + str(int(BB_ID)) + "\';"
query = ("SELECT Open from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
logger.debug('query for time period is %s', query) 
cur.execute(query)
for (Open) in cur:
    tOpen = Open 
logger.debug('tOpen for time period is %s', tOpen) 

query = ("SELECT High from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
cur.execute(query)
for (High) in cur:
    tHigh = High

logger.debug('tHigh for time period is %s', tHigh) 

query = ("SELECT Low from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
cur.execute(query)
for (Low) in cur:
   tLow = Low

logger.debug('tLow for time period is %s', tLow)  

query = ("SELECT Close from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
cur.execute(query)
for (Close) in cur:
    tClose = Close

logger.debug('tClose for time period is %s', tClose) 

query = ("SELECT UpperBand from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
cur.execute(query)
for (UpperBand) in cur:
    tUpperBand = UpperBand

logger.debug('tUpperBand for time period is %s', tUpperBand)
 
query = ("SELECT LowerBand from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
cur.execute(query)
for (LowerBand) in cur:
    tLowerBand = LowerBand

logger.debug('tLowerBand for time period is %s', tLowerBand)  

query = ("SELECT MidLine from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(BB_ID[0]) + ";")
cur.execute(query)
for (MidLine) in cur:
    tMidLine = MidLine

logger.debug('tMidLine for time period is %s', tMidLine)   

#Calculate yesterday's date
#Find today's date and Day of the week
today = datetime.date.today( )
logger.debug('Today is %s', today)  
dayofweek = datetime.datetime.today().weekday()



##Convert Date to proper format and relative reference
if dayofweek == 0:  #if Today is Monday
    yesterday = today - datetime.timedelta(days=3)  #Get Friday                   
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Previous Trading day was %s', yesterday2)  

else:
    yesterday = today - datetime.timedelta(days=1) #Take 1 Day back                    
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    logger.debug('Previous trading day was %s', yesterday2)

#Yesterday's OHLC value

query = ("SELECT (max(ID)-1) from FUT_BB_" + CCY1+CCY2+ ";")
logger.debug('Max Id - 1 %s', query)  
cur.execute(query)
for (ID) in cur:
    yBB_ID = ID
    logger.debug('ID for Last trading period--5 minutes ago-- was %s', yBB_ID)

query = ("SELECT Open from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (Open) in cur:
    yOpen = Open

logger.debug('yOpen for last time period was %s', yOpen)  

query = ("SELECT High from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (High) in cur:
    yHigh = High

logger.debug('yHigh for last time period was %s', yHigh)  

query = ("SELECT Low from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (Low) in cur:
    yLow = Low

logger.debug('yLow for last time period was %s', yLow)  

query = ("SELECT Close from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (Close) in cur:
    yClose = Close

logger.debug('yClose for last time period was %s', yClose)

query = ("SELECT UpperBand from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (UpperBand) in cur:
    yUpperBand = UpperBand

logger.debug('yUpperBand for last time period was %s', yUpperBand) 
 
query = ("SELECT LowerBand from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (LowerBand) in cur:
    yLowerBand = LowerBand

logger.debug('yLowerBand for last time period was %s', yLowerBand)  

query = ("SELECT MidLine from FUT_BB_" + CCY1 + CCY2 + " where ID = " + str(yBB_ID[0]) + ";")
logger.debug('query is %s', query)
cur.execute(query)
for (MidLine) in cur:
    yMidLine = MidLine

logger.debug('yMidLine for last time period was %s', yMidLine) 

query = ("SELECT BBEntryPending from hasPosition where CCY =\'" + CCY1 + CCY2 +"\';")
logger.debug('query is %s', query)
cur.execute(query)
for (BBEntryPending) in cur:
    EntryPend = BBEntryPending

logger.debug('BBEntry Pending is %s', EntryPend) 

# Order ID Management
# Pull Last OID from Database and set OID to that plus 1
query = ("SELECT max(idOrder) from Orders;")
logger.debug('Max Order query is %s', query) 
cur.execute(query)
for (idOrder) in cur:
    OID = int(idOrder[0]) + 1
logger.debug('Order Id for next trade is %s', OID) 

###Position Size Calculation
#logger.debug('$$$ Position Size Calculation $$$') 
#DollarLoss = AcctBalanceBasis[0] * riskPerPosition[0]
#logger.debug('Dollar Loss permitted is is %s', DollarLoss)  # allowable Dollar loss per trade
logger.debug('Today High is %s', tHigh) 
logger.debug('Today Low is %s', tLow) 

StopLossPips = int(round((float(tHigh[0]) - float(tLow[0]))*10000,0))  # Stop Loss Pips for Position Sizing ratio
logger.debug('Stop Loss Pips is %s', StopLossPips) 
#PositionSize = (10000 * BB_SizeMultiplier[0])   # Position Size to Take
PositionSize = 1
logger.debug('Position Size for trade is %s', PositionSize)
#ProfitPips = (StopLossPips * int(RiskRewardRatio[0]))
#logger.debug('Profit Pips is %s', ProfitPips)
#amountProfit = 10000*ProfitPips
#print(amountProfit)

##Strategy Logic
logger.debug('STRATEGY LOGIC !!!!!!')
logger.debug('Current Position is %s', CurrentPositions)
if (CurrentPositions[0] < 1000000):  ##Removes Positions limits for BB Strat
    logger.debug('There is an available position slot for %s%s',CCY1,CCY2)
    symbol   = CCY1+CCY2
    symbol2 = CCY2
    secType  = 'FUT'
    exchange = 'GLOBEX'
    action   = 'BUY'
    counter_action = 'SELL'
    idOrder = int(OID)
    qty = int(PositionSize)
    limit = 1 
    Date = today
    #time = "6:00"  #placeholder for Orders. Use when intraday strategies go into effect
    Currency = CCY1+CCY2
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    Price = float(truncate(float(tHigh[0]),4)) + 0.0002  #Entry Price
    Strategy = "BB_STRAT"
    Bracket = "Entry"
    Status = "Submitted"
    parentId = OID
    #RiskReward = RiskRewardRatio

#LONG TRADES
    logger.debug('Checking for Longs')
    logger.debug('tCLose is %s', float(tClose[0]))
    logger.debug('MovAvg is %s', float(MovAvg[0]))
    logger.debug('yClose is %s', float(yClose[0]))
    logger.debug('yOpen is %s', float(yOpen[0]))
    logger.debug('tOpen is %s', float(tOpen[0]))
    logger.debug('yLow is %s', float(yLow[0]))
    logger.debug('tMidline is %s', float(tMidLine[0]))
    logger.debug('yLowerBand is %s', yLowerBand[0])
    logger.debug('Current Position is %s', CurrentPositions)
    logger.debug('Checking for Long trade entry')
    
#LONGS    
    if (float(EntryPend[0]) == 0 and float(tClose[0]) > float(MovAvg[0]) and float(yClose[0]) < float(yOpen[0]) and float(tClose[0]) > float(tOpen[0]) and float(yLow[0]) < float(yLowerBand[0])): #float(tClose[0]) > float(MovAvg[0]) and float(yClose[0]) < float(yOpen[0]) and float(tClose[0]) > float(tOpen[0]) and float(yLow[0]) < float(yLowerBand[0])):
        logger.debug('Valid Long Entry Found')
        #TWS Connection
        conn = Connection.create(port=4002, clientId=999)
        conn.registerAll(reply_handler)
        conn.connect()
        logger.debug('Connected to Database')
        #time.sleep(1) #give IB time to send us messages
        
        #Create entry pending in hasPosition Table
        query = ("UPDATE hasPosition SET BBEntryPending = " + "1" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        #Order Query 
        #amount = round(float(truncate(float(tHigh[0]),4)) + 0.0005,4)  # Stop Price for Long trades
        idOrder = int(OID)
        
        
        
        Date = today
        yesterday = Date #Take 1 Day back                    
        month = (str(0) + str(yesterday.month))
        day = (str(0)+ str(yesterday.day))
        yesterday3 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
        logger.debug('Todays date is %s', yesterday3)
        Date = yesterday3
        
        
        time = datetime.datetime.now().strftime("%I:%M%p")
        logger.debug('time is %s',time)#placeholder for Orders. Use when intraday strategies go into effect
        
        Currency = CCY1+CCY2
        TriggerID = OID
        Price = round(float(truncate(float(tHigh[0]),4)) + 0.0002,4)
        Strategy = "BBSTRAT"
        Bracket = "Entry"
        Status = "Submitted"
        qty = int(PositionSize)
        limit = 1   #tick mark to set up limit
        logger.debug('Quantity %s ',  qty)
        action   = 'BUY'
        counter_action = 'SELL'
        
#Create ENTRY Stp Buy Order 2 pips above High
        CONTRACT = create_contract(symbol, secType, exchange, exchange, symbol2)
        ORDER = make_long_order(action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        logger.debug('Contract Created')
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

        
        #, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status , Date, time, Currency, str(TriggerID), str(Price), Strategy, Bracket, Status)
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        logger.debug('Order query is %s',query)
        #cur.execute(query)
        cnx.commit() #Primary Trade
        logger.debug('Order added to database')
        
        query = ("UPDATE hasPosition SET BB_EntryID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('hasPosition query is %s',query)
        cur.execute(query)
        cnx.commit()
        logger.debug('hasPosition Entry ID set to %s ', OID)
        
        query = ("UPDATE hasPosition SET BB_EntryPrice = " + str(Price) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('hasPosition query is %s',query)
        cur.execute(query)
        cnx.commit()
        logger.debug('hasPosition Entry Price set to %s ', Price)

# create a PROFIT take order of some kind
        limit = 2
        logger.debug('profitTarget PIPS %s ', profitTarget[0])

       
      
#       Bracket = "Profit Target"
#        OID = OID + 1
#        idOrder = OID
#        logger.debug('idOrder is %s ', idOrder)
 #REMOVE PROFIT TARGET IN STRAT AND MOVE TO POSMGTM AS PART OF OCA WITH STOP LOSS       
        #ORDER = make_long_order(counter_action, qty, limit, parentId=OID, transmit=True)
        #conn.placeOrder(OID, CONTRACT, ORDER)
        #logger.debug('Order Placed %s ', ORDER)
        Price = truncate((float(tHigh[0]) + 0.0060),4) # Keep this to ensure Orders shows proper Profit Target
        #cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        #cur.execute(query)
        #cnx.commit() #Profit Target
        #logger.debug('Profit target entered into Order Table')
        
#        query = ("UPDATE hasPosition SET BB_ProfitID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
#        logger.debug('query is %s ', query)
#        cur.execute(query)
#        cnx.commit()
#        logger.debug('HasPosition table set ProfitID to %s', OID)

        #Add Profit Price to Has Positions Table
        query = ("UPDATE hasPosition SET BB_ProfitPrice = " + str(Price) + " WHERE CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('query is %s ', query)
        cur.execute(query)
        cnx.commit()
        logger.debug('HasPosition table set ProfitPrice to %s', str(Price))

        #Update CurrentPosition
        newCurPos = CurrentPositions[0] + 1
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + str(newCurPos) + " WHERE idRiskParameters='5'")
        cur.execute(query)
        cnx.commit()
        logger.debug('RiskParameters set to %s', newCurPos)
        
#Put STOPLOSS Value in hasPosition Table as Placeholder
        StopLossvalue = truncate(min((float(tLow[0]) - 0.0002),(float(tHigh[0]) - 0.001)),4)  # Stop Price
        query = ("UPDATE hasPosition SET BB_StopLossVal = " + str(StopLossvalue) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('hasPosition query is %s',query)
        cur.execute(query)
        cnx.commit()
        logger.debug('Stop Loss Value set to %s', StopLossvalue)
        
        query = ("UPDATE hasPosition SET BB_StopQty = " + str(qty) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        logger.debug('hasPosition query is %s',query)
        cnx.commit()
        logger.debug('Stop Loss Quantity set to %s', qty)
        
        query = ("UPDATE hasPosition SET BB_direction = 'Long' WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        logger.debug('hasPosition query is %s',query)
        cnx.commit()       
        logger.debug('Direction set to Long')
        
        conn.disconnect()
        logger.debug('Database disconnected')
        
#        ##Update Orders Table
#        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
#        cnx.commit()#Stop Loss
   
#SHORT TRADES 
    logger.debug('Past Long Function') 
    action   = 'SELL'
    counter_action = 'BUY'
    idOrder = int(OID)
    qty = int(PositionSize)
    limit = 1 
    Date = today
    time = datetime.datetime.now().strftime("%I:%M%p")
    logger.debug('time is %s',time)
    Currency = CCY1+CCY2
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    Price = round(float(truncate(float(tLow[0]),4)) - 0.0002,4)
    Strategy = "BB_STRAT"
    Bracket = "Entry"
    Status = "Submitted"
    parentId = OID
    #RiskReward = RiskRewardRatio
    logger.debug('Checking Short value') 
    logger.debug('tCLose is %s', float(tClose[0]))
    logger.debug('MovAvg is %s', float(MovAvg[0]))
    logger.debug('yClose is %s', float(yClose[0]))
    logger.debug('yOpen is %s', float(yOpen[0]))
    logger.debug('tOpen is %s', float(tOpen[0]))
    logger.debug('yLow is %s', float(yLow[0]))
    logger.debug('yUpperBand is %s', yUpperBand[0])
    logger.debug('Current Position is %s', CurrentPositions)
    logger.debug('Checking for SHORT trade entry')
    if (float(EntryPend[0]) == 0 and float(tClose[0]) < float(MovAvg[0]) and float(yClose[0]) > float(yOpen[0]) and float(tClose[0]) < float(tOpen[0]) and float(yHigh[0]) > float(yUpperBand[0])): #float(tClose[0]) > float(MovAvg[0]) and float(yClose[0]) < float(yOpen[0]) and float(tClose[0]) > float(tOpen[0]) and float(yLow[0]) < float(yLowerBand[0])):
        logger.debug('Valid ShortEntry Found')
        #TWS Connection
        conn = Connection.create(port=4002, clientId=999)
        conn.registerAll(reply_handler)
        conn.connect()
        logger.debug('Connected to database')
        #time.sleep(1) #give IB time to send us messages
        
        #Create entry pending in hasPosition Table
        query = ("UPDATE hasPosition SET BBEntryPending = " + "1" + " where CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
#Create STP Sell order 5 pips below Low
        CONTRACT = create_contract(symbol, secType, exchange, exchange, symbol2)
        ORDER = make__short__order(action, qty, limit, transmit=True)
        conn.placeOrder(OID, CONTRACT, ORDER)
        logger.debug('Order placed for short')
        
        cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status)) 
        cnx.commit() #Primary Trade
        
 #Update CurrentPosition
        newCurPos = CurrentPositions[0] + 1
        logger.debug('New Current Position is %s', newCurPos)
        query = ("UPDATE RiskParameters SET RiskParametersValue= " + str(newCurPos) + " WHERE idRiskParameters='5'")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
        query = ("UPDATE hasPosition SET BB_EntryID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()

        query = ("UPDATE hasPosition SET BB_EntryPrice = " + str(Price) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        logger.debug('hasPosition query is %s',query)
        cur.execute(query)
        cnx.commit()
        logger.debug('hasPosition Entry Price set to %s ', Price)
        
# create a profit take order of some kind
        #logger.debug('RiskReward is %s', RiskReward)
        Price = truncate((float(tLow[0]) - 0.0060),4)
        logger.debug(Price)
#        Bracket = "Profit Target"
#        OID = OID + 1
#        idOrder = OID
        limit = 2
        #ORDER = make__short__order(counter_action, qty, limit, transmit=True)
        #conn.placeOrder(OID, CONTRACT, ORDER)
        
        #cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(idOrder, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
        #cnx.commit()#Profit Target 
        
        query = ("UPDATE hasPosition SET BB_ProfitPrice = " + str(Price) + " WHERE CCY =\'" + CCY1 + CCY2 +"\';")
        logger.debug('query is %s ', query)
        cur.execute(query)
        cnx.commit()
        logger.debug('HasPosition table set ProfitPrice to %s', str(Price))
        
        query = ("UPDATE hasPosition SET BB_ProfitID = " + str(OID) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        cnx.commit()
        logger.debug('HasPosition table set ProfitID to %s', OID)
        
        StopLossvalue = truncate(max((float(tHigh[0]) + 0.0002),(float(tLow[0]) + 0.001)),4) #Either 2 pips above the High or 10 pips from the low, whichever is more
        query = ("UPDATE hasPosition SET BB_StopLossVal = " + str(StopLossvalue) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        logger.debug('hasPosition query is %s',query)
        cnx.commit()
        logger.debug('Stop Loss Value set to %s', StopLossvalue)
        
        query = ("UPDATE hasPosition SET BB_StopQty = " + str(qty) + " WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        logger.debug('hasPosition query is %s',query)
        cnx.commit()
        logger.debug('Stop Loss Quantity set to %s', qty)
        
        query = ("UPDATE hasPosition SET BB_direction = 'Short' WHERE CCY =\'" + CCY1 + CCY2+"\';")
        cur.execute(query)
        logger.debug('hasPosition query is %s',query)
        cnx.commit() 
        logger.debug('Direction set to Short')
         
        conn.disconnect()
        logger.debug('Database disconnected')
        
logging.debug('Past Short function')
logging.debug('%%%%%%%%%%%%%% END STRATEGY %s%s',CCY1,CCY2)