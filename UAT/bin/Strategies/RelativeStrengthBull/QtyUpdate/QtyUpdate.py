from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection
from datetime import timedelta
import mysql.connector
import datetime
import logging
import datalink  #universal logins for environment
import time
import csv

today = datetime.date.today( )

logging.basicConfig(filename='QtyUpdate' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('QtyUpdate' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')
logger.debug('time is %s', datetime.datetime.now().strftime("%I:%M%p"))


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
limit = 1
Strategy = "RelativeStrengthBull"
Status = "Submitted"
pos = ""
directionTrade = ""
timer = datetime.datetime.now().strftime("%I:%M%p")
logger.debug('Current Time is %s', timer)
masteraccount = datalink.DB_Account
inPos = 0
masteraccount = 'DU1240329'
global inPosAPI
inPosAPI = 0
logger.debug('inPosAPI is %s', inPosAPI)
global inorderAPI
inorderAPI = 0
logger.debug('inorderAPI is %s', inorderAPI)
global inStopAPI
inStopAPI = 0
logger.debug('inStopAPI is %s', inStopAPI)
global inProfitAPI
inProfitAPI = 0
logger.debug('inProfitAPI is %s', inProfitAPI)
global Order_entry
Order_entry = 0
logger.debug('order_entry is %s', Order_entry)
global Order_stop
Order_stop = 0
logger.debug('order_stop is %s', Order_stop)
global Order_profit
Order_profit = 0
logger.debug('order_profit is %s', Order_profit)

def reply_handler(msg):
    #Resets and Assumes Position is 0 until confirmed in IF statement for specific Stock 
    logger.debug('Beginning of Reply Handler') 
    test0 = msg
    acct = 'DU1240329'
    global pos
    pos = msg.pos 
    global con
    con = msg.contract
    conTicker = msg.contract.m_symbol
    logger.debug('Pos Mgmt %s', pos)
    logger.debug('Pos Mgmt %s', acct)
    logger.debug('Ticker to match %s', Ticker[0])
    logger.debug('con %s', con)
    logger.debug('conTicker %s', conTicker)
    if acct == 'DU1240329':
        #logger.debug('Reply handler %s', test0)
        logger.debug('ccy1 Symbol with position is %s', con.m_symbol)
        logger.debug('Ticker %s', Ticker[0])
        logger.debug('ccy2 Currency with position is %s', con.m_currency)
        logger.debug('Contract is %s', con.m_secType)
        logger.debug('Position is %s', pos)  
        if(conTicker == Ticker[0] and (pos != 0) and (con.m_secType == "STK")):
            logger.debug('In Position')
            global inPosAPI
            inPosAPI = 1
            
            query = ("UPDATE hasPosition SET StopQty = \'" + str(pos) + "\' where CCY =\'" + Ticker[0] + "\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()
                    
            logger.debug('inPos flag is %s', inPosAPI)
            logger.debug('Ticker is %s', Ticker[0])
            return inPosAPI
        logger.debug('inPos flag after IF %s', inPosAPI)
    logger.debug('inPos flag at end of reply handler %s', inPosAPI)

#def reply_handler_Orders(msg):
#    #Resets and Assumes Position is 0 until confirmed in IF statement for specific Stock 
#    logger.debug('Beginning of Order Handler') 
#    test0 = msg
#    acct = 'DU1240329' 
#    global con
#    con = msg.contract
#    orderinfo = msg.order
#    APIorderID = msg.order.m_orderId
#    APIstatus = msg.orderState.m_status
#    global Order_entry
#    logger.debug('EntryID from DB %s', Order_entry)
#    logger.debug('EntryID from API %s', APIorderID)
#    logger.debug('Order status from API %s', APIstatus)
#    logger.debug('Pos Mgmt %s', acct)
#    logger.debug('Ticker %s', Ticker[0])
#    logger.debug('Order info object %s', orderinfo)
#    logger.debug('Order info action %s', orderinfo.m_action)
#        #order.Action+", "+order.OrderType
#    if acct == 'DU1240329':
#        logger.debug('Order handler %s', test0)
#        logger.debug('Order Symbol with position is %s', con.m_symbol)
#        logger.debug('Order Currency with position is %s', con.m_currency)
#        logger.debug('Contract is %s', con.m_secType)  
#        #If Entry Order Filled and no order is filled, return flag
#        if((con.m_symbol == Ticker[0]) and (con.m_secType == "STK") and (APIorderID[0] == Order_entry[0]) and (APIstatus[0] == "Filled") and EntryPending == 0): #First time order will be filled
#            logger.debug('In Order')
#            global inorderAPI
#            inorderAPI = 1
#            logger.debug('inorder flag is %s', inorderAPI)
#            return inorderAPI
#        #if Order had been filled previously and now Stop ID is filled then return Flag
#        if((con.m_symbol == Ticker[0]) and (con.m_secType == "STK") and (APIorderID[0] == Order_stop[0]) and (APIstatus[0] == "Filled") and EntryPending == 1): #First time order will be filled
#            logger.debug('In Order')
#            global inStopAPI
#            inStopAPI = 1
#            logger.debug('inorder flag is %s', inStopAPI)
#            return inStopAPI
#        #if Order had been filled previously and now Prodit Id is filled then return flag
#        if((con.m_symbol == Ticker[0]) and (con.m_secType == "STK") and (APIorderID[0] == Order_profit[0]) and (APIstatus[0] == "Filled") and EntryPending == 1): #First time order will be filled
#            logger.debug('In Order')
#            global inProfitAPI
#            inProfitAPI = 1
#            logger.debug('in Profit flag is %s', inProfitAPI)
#            return inProfitAPI
#    logger.debug('in Order flag at end of reply handler %s', inorderAPI)
#        
#def reply_handler_contract(msg):
#    test0 = msg
#    logger.debug('Reply Handler Contract is %s', test0) 
#    
#    
#def reply_handler_Status(msg):
#    test0 = msg
#    order_status = msg.status
#    order_Identify = msg.orderId
#    logger.debug('reply handler status %s', test0)
#    logger.debug('Order status %s', order_status)
#    logger.debug('Order Identification %s', order_Identify)
#    logger.debug('Order Identification %s', type(order_Identify))
#    
#    if(order_Identify == int(Order_stop[0])):
#        global stop_api_id
#        stop_api_id = order_Identify
#        logger.debug('Stop API ID is %s', stop_api_id)
#    
#    if(order_Identify == int(Order_profit[0])):
#        global profit_api_id
#        profit_api_id = order_Identify
#        logger.debug('Profit API ID is %s', profit_api_id)
#        
#    if(order_Identify == int(Order_entry[0])):
#        global entry_api_id
#        entry_api_id = order_Identify
#        logger.debug('Entry API ID is %s', entry_api_id)
            
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


#Profit target function for Sell Profit Orders (Long Trades)
#def make_profit_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
#        order = Order()
#        order.m_action = action
#        order.m_totalQuantity = qty
#        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
#        profitPrice = float(EntryPriceVal[0]) + (float(ATRValueVal[0]) * float(ProfitATRmultipleVal[0]))
#        logger.debug('profit price is %s', profitPrice)
#        profitPrice2 = truncate(profitPrice,2)
#        order.m_lmtPrice  = truncate((float(profitPrice2)), 2)
#        logger.debug('Profit Target LMT Order Price is is %s', order.m_lmtPrice)
#        order.m_orderType = 'LMT'
#        order.m_triggerMethod = 4
#        order.m_account = masteraccount
#        order.m_outsideRth = True
#        order.m_transmit = transmit
#        
#        logger.debug('transmitted profit order')
#        return order    
#
#def make_trail(action, qty, limit = None, transmit=True):
#        logger.debug('In TRAIL STOP function')
#        order = Order()
#        order.m_action = action
#        order.m_ocaGroup = 1
#        order.ocaType = 1
#        logger.debug('Order action %s', order.m_action) 
#        order.m_totalQuantity = qty
#        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
#        logger.debug('Limit value is %s', limit)
#        order.m_orderType = 'TRAIL'
#        order.m_outsideRth = True
#        order.m_triggerMethod = 4
#        logger.debug('entryprice is %s', float(EntryPriceVal[0]))
#        logger.debug('ATRValue is %s', float(ATRValueVal[0]))
#        logger.debug('StopATRMultiple is %s', StopATRMultipleVal[0])
#        stopPrice = float(EntryPriceVal[0]) - (float(ATRValueVal[0]) * float(StopATRMultipleVal[0]))
#        logger.debug('stop price is %s', stopPrice)
#        stopPrice2 = truncate(stopPrice,2)
#        logger.debug('stop price is %s', stopPrice2)
#        order.m_lmtPrice  = truncate(float(stopPrice2),2)
#        logger.debug('In SEll action. TRAIL price is %s', order.m_lmtPrice)
#        order.m_auxPrice = stopPrice2;
#        order.m_account = masteraccount
#        logger.debug('In Buy action. AUX Price price is %s', stopPrice2)
#        logger.debug('In Buy action. account is %s', order.m_account)
#        # Important that we only send the order when all children are formed.
#        order.m_transmit = transmit
#
#        return order

yesterday = datetime.date.today() - timedelta(1)
f = open('C:/Program Files/Serpico/bin/relativestrengthrank' + str(yesterday) +'.csv')
#f = open('relativestrengthrank' + str(yesterday) +'.csv')
csv_f = csv.reader(f)

for row in csv_f:
    Ticker = row   
    logger.debug('STARTING NEW LOOP WITH NEW Ticker %s', Ticker)
    logger.debug('Connecting to database')
    cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
    cur = cnx.cursor()
    logger.debug('Connected to database')
               
    #Main code
    logger.debug('Connecting to IBController')
    conn = Connection.create(port=4002, clientId=999)
    conn.connect() 
    time.sleep(1)
    logger.debug('Connected to IBController')
    
#Register REply Handlers to do actual checking of Order Status
    conn.register(reply_handler, 'Position')
    logger.debug('register reply handler')
    conn.register(reply_handler_Orders) 
    #conn.register(reply_handler_Status, 'OrderStatus')
       
#Get Entry ID, Profit ID and STop ID from hasposition table to compare against API results

#    query = ("SELECT EntryID from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (EntryID) in cur:
#        Order_entry = EntryID
#    logger.debug('Order_entry is %s', Order_entry)   
#    
#    query = ("SELECT StopID from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (StopID) in cur:
#        Order_stop = StopID
#    logger.debug('Order_stop is %s', Order_stop)  
#    
#    query = ("SELECT ProfitID from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (ProfitID) in cur:
#        Order_profit = ProfitID
#    logger.debug('Order_profit is %s', Order_profit) 
#    
#    query = ("SELECT EntryPending from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (EntryPending) in cur:
#        Order_position = EntryPending
    #logger.debug('Position API is at MAIN code BEFORE%s', inPosAPI)
    inPosAPI = 0
    logger.debug('inPosAPI is %s', inPosAPI)
    conn.reqPositions() # will find the order if it was filled 
    #logger.debug('Position API is at MAIN code AFTER %s', inPosAPI)
    #time.sleep(1)
    #logger.debug('Open Orders is next')
    #conn.reqAllOpenOrders() # will find the order if it's open
    #logger.debug('Open Orders requested')
    
    
#    qqq = Contract()
#    qqq.m_symbol = Ticker[0]  
#    qqq.m_secType = 'STK'  
#    qqq.m_exchange = 'SMART'
#    qqq.m_primary_exch = 'ARCA'
#    qqq.m_currency = 'USD' 
#    time.sleep(1)
#          
#           
#    #Calculate yesterday's date
#    #Find today's date and Day of the week
#    today = datetime.date.today( )
#    logger.debug('Today is %s', today)
#    dayofweek = datetime.datetime.today().weekday()
#    logger.debug('Day of the week %s', dayofweek)
#    today2 = str(today)
#    logger.debug('Position API is at MAIN code LATER is %s', inPosAPI)
#    Date = datetime.date.today()
#    yesterday = Date #Take 1 Day back                    
#    month = (str(0) + str(yesterday.month))
#    day = (str(0)+ str(yesterday.day))
#    yesterday3 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
#    logger.debug('Todays date is %s', yesterday3)
#    Date = yesterday3
#    
#    timer = datetime.datetime.now().strftime("%I:%M%p")
#    logger.debug('time is %s',timer)#placeholder for Orders. Use when intraday strategies go into effect
    
    ##Convert Date to proper format and relative reference
#    if dayofweek == 0:  #if Today is Monday
#        yesterday = today - datetime.timedelta(days=3)  #Get Previous Wednesday                   
#        month = (str(0) + str(yesterday.month))
#        day = (str(0)+ str(yesterday.day))
#        yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
#        logger.debug('Yesterday is %s', yesterday2)  
#    
#    else:
#        yesterday = today - datetime.timedelta(days=1) #Take 3 Days back                    
#        month = (str(0) + str(yesterday.month))
#        day = (str(0)+ str(yesterday.day))
#        yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
#        logger.debug('Yesterday is %s', yesterday2) 
    
    
#    query = ("SELECT EntryPending from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (EntryPending) in cur:
#        EntryPend = EntryPending
#        
#    logger.debug('EntryPend is %s', EntryPend[0])
#    
#    query = ("SELECT EntryID from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (EntryID) in cur:
#        orderEntry = EntryID
#        
#    logger.debug('EntryPend is %s', EntryPend[0])
# 
#    query = ("SELECT StopLossFlag from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (StopLossFlag) in cur:
#        curStopLossFlag = StopLossFlag
#        
#    query = ("SELECT ProfitTarget from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (ProfitTarget) in cur:
#        curprofitFlag = ProfitTarget
#
#    query = ("SELECT EntryPrice from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (EntryPrice) in cur:
#        EntryPriceVal = EntryPrice
#        
#    query = ("SELECT ATRValue from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (ATRValue) in cur:
#        ATRValueVal = ATRValue
        
#    query = ("SELECT StopQty from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (StopQty) in cur:
#        StopQtyVal = StopQty
#        
#    query = ("SELECT ProfitATRMultiple from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (ProfitATRmultiple) in cur:
#        ProfitATRmultipleVal = ProfitATRmultiple
#        
#    query = ("SELECT StopATRMultiple from hasPosition where CCY =\'" + Ticker[0] +"\';")
#    logger.debug('query is %s', query)
#    cur.execute(query)
#    for (StopATRMultiple) in cur:
#        StopATRMultipleVal = StopATRMultiple
#    
#    query = ("SELECT max(idOrders) from Orders;")
#    cur.execute(query)
#    for (idOrders) in cur:
#        OID = idOrders
#        logger.debug('OLD Order ID is %s', OID)
    
#    logger.debug('EntryPending is %s', EntryPend[0])
#    logger.debug('StopLossFlag is %s', curStopLossFlag[0])
#    logger.debug('Order profit is %s', Order_profit)
#    logger.debug('Stop Order is %s', Order_stop)
#    logger.debug('ProfitFlag is %s', curprofitFlag[0])
#    logger.debug('API knows pos is %s', inPosAPI)
#    logger.debug('Ticker is %s', Ticker[0])
#    logger.debug('EntryPendingTYPE is %s', type(EntryPend[0]))
#    logger.debug('StopLossFlagTYPE is %s', type(curStopLossFlag[0]))
#    logger.debug('ProfitTYPE is %s', type(curprofitFlag[0]))
#    logger.debug('inPosAPI is %s', type(inPosAPI))
#    logger.debug('Order profit is %s', type(Order_profit))
#    logger.debug('Stop Order is %s', type(Order_stop))
#    logger.debug('WHERE I THINK IT DIES ')

###Create Stop Loss order & Profit Target Order after Order has been filled via API
#    if (int(curStopLossFlag[0]) == 0 and int(EntryPend[0]) == 1 and inPosAPI == 1):
#            # create a stop loss order, and THEN transmit(set transmit to true) the entire order by placing this last child order(note inTWS it looks like a tree with parent order and two sub orders inside)
#        logger.debug('Identified Entry Order Has Been Filled')
#        logger.debug('The WINNER is %s', Ticker[0])
#        logger.debug('Identif')
#        Bracketstop = "Stop Loss"
#        Bracketprofit  ="ProfitTarget"
#        
#        OIDstop = OID[0] + 1
#        OIDprofit = OIDstop + 1
#        
#        logger.debug('Incremented Order ID for stop loss %s', OIDstop)
#        
#        logger.debug('EntryPriceVal[0] is %s', EntryPriceVal[0])
#        logger.debug('EntryPriceVal[0]TYPE is %s', type(EntryPriceVal[0]))
#        
#        logger.debug('ATRValueVal[0 is %s', ATRValueVal[0])
#        logger.debug('ATRValueVal[0 is %s', type(ATRValueVal[0]))
#        
#        logger.debug('StopMultiple[0 is %s', StopATRMultipleVal[0])
#        logger.debug('StopMultipleTYPE is %s', type(StopATRMultipleVal[0]))
#        
#        logger.debug('ProfitMultiple is %s', ProfitATRmultipleVal[0])
#        logger.debug('ProfitMultipleTYPE is %s', type(ProfitATRmultipleVal[0]))
#        
#        stopPrice = float(EntryPriceVal[0]) - (float(ATRValueVal[0]) * float(StopATRMultipleVal[0]))
#        logger.debug('stop price is %s', stopPrice)
#        stopPrice2 = truncate(stopPrice,2)
#        
#        profitPrice = float(EntryPriceVal[0]) + (float(ATRValueVal[0]) * float(ProfitATRmultipleVal[0]))
#        logger.debug('profit price is %s', profitPrice)
#        profitPrice2 = truncate(profitPrice,2)
#        
#        PosSize = int(StopQtyVal[0])
#        TriggerID = orderEntry[0]
#        
#        logger.debug('stopPrice final %s', stopPrice2)
#        logger.debug('Profit price final %s', profitPrice2)
#        logger.debug('Pos Size %s', PosSize)
#        logger.debug('TriggerID %s', TriggerID)
#        
#        #StopLoss
#        CONTRACT = create_contract(Ticker[0], 'STK', 'SMART', 'ARCA', 'USD')
#        ORDER = make_trail('Sell', PosSize, limit, transmit=True)
#        conn.placeOrder(OIDstop, CONTRACT, ORDER)
#        logger.debug('Long stop order placed')
#        
#        logger.debug('Stop id order %s', OIDstop)
#        logger.debug('order type %s', type(OIDstop))
#        
#        logger.debug('Profi id order %s', OIDprofit)
#        logger.debug('order type %s', type(OIDprofit))
#        
#        logger.debug('entry id order %s', idOrders)
#        logger.debug('order type %s', type(idOrders))
#        
#        logger.debug('Trigger ID %s', TriggerID)
#        logger.debug('trigger type %s', type(TriggerID))
#        
#        logger.debug('Date %s', Date)
#        logger.debug('DAte type %s', type(Date))
#        
#        logger.debug('Time %s', time)
#        logger.debug('time type %s', type(time))
#                
#        logger.debug('Size %s', PosSize)
#        logger.debug('Size type %s', type(PosSize))
#        
##Universal Changes bc of Order Fill           
#        query = ("UPDATE hasPosition SET Position = " + "1" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        logger.debug('POSITION Set to 1.  No More positions should be taken')
#        cur.execute(query)
#        cnx.commit()
#        
#        query = ("UPDATE Orders SET Status = \'" + "Filled" + "\' where idOrders = " + str(orderEntry[0]) + ";")
#        logger.debug('Query is %s', query)
#        cur.execute(query)
#        cnx.commit()
#
#        query = ("UPDATE hasPosition SET EntryPending = " + "0" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        logger.debug('Entry Pending Set to 0')
#        cur.execute(query)
#        cnx.commit()       
#       
#        logger.debug('Stop id order %s', OIDstop)
#        logger.debug('order type %s', type(OIDstop))
#        
#        logger.debug('today %s', today2)
#        logger.debug('today %s', type(today2))
#        
#        logger.debug('ticker %s', Ticker[0])
#        logger.debug('ticker %s', type(Ticker[0]))
#        
#        logger.debug('entry id order %s', idOrders)
#        logger.debug('order type %s', type(idOrders))
#        
#        logger.debug('Trigger ID %s', TriggerID)
#        logger.debug('trigger type %s', type(TriggerID))
#        
#        logger.debug('Date %s', Date)
#        logger.debug('DAte type %s', type(Date))
#        
#        logger.debug('Timer %s', timer)
#        logger.debug('timer type %s', type(timer))
#                
#        logger.debug('Size %s', PosSize)
#        logger.debug('Size type %s', type(PosSize))
#        
#        logger.debug('strategy %s', str(Strategy))
#        logger.debug('strategy type %s', type(str(Strategy)))
#                
#        logger.debug('str(Bracketstop) %s', str(Bracketstop))
#        logger.debug('str(Bracketstop) type %s', type(str(Bracketstop)))
#        
##Stop Loss        
#        query = ("UPDATE hasPosition SET StopLossFlag = " + "1" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        logger.debug('POSITION Set to 1.  No More positions should be taken')
#        cur.execute(query)
#        cnx.commit()
#    
#        query = ("UPDATE hasPosition SET StopID = " + str(OIDstop) + " WHERE CCY =\'" + Ticker[0] +"\';")
#        cur.execute(query)
#        cnx.commit()
#           
#        #query =("Insert Into Orders (idOrders, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status, Size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(OIDstop), str(today2), str(timer), str(Ticker[0]), str(TriggerID), str(stopPrice2), str(Strategy), str(Bracketstop), str(Status), str(PosSize)))
#        cur.execute("""Insert Into Orders (idOrders, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status, Size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(str(OIDstop), today2, timer, Ticker[0], TriggerID, stopPrice2, Strategy, Bracketstop, Status, str(PosSize)))
#        logger.debug('Query is %s', query)
#        logger.debug('Query type %s', type(query))
#        #cur.execute(query[0])
#        cnx.commit() 
#
###Profit Target
#        CONTRACT = create_contract(Ticker[0], 'STK', 'SMART', 'ARCA', 'USD')
#        ORDER = make_profit_order('Sell', PosSize, limit, transmit=True)
#        conn.placeOrder(OIDprofit, CONTRACT, ORDER)
#        logger.debug('Profit Target order placed')
#        
#        #query =("Insert Into Orders (idOrders, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status, Size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",  (str(OIDprofit), today2, timer, Ticker, TriggerID, profitPrice2, Strategy, Bracketprofit, Status, str(PosSize)))
#        cur.execute("""Insert Into Orders (idOrders, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status, Size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(str(OIDprofit), today2, timer, Ticker[0], TriggerID, profitPrice2, Strategy, Bracketprofit, Status, str(PosSize)))
#        #logger.debug('Query is %s', query)
#        #cur.execute(query)
#        cnx.commit() #Profit Target
#            
#        query = ("UPDATE hasPosition SET ProfitTarget = " + "1" + " where CCY = \'" + Ticker[0] + "\'")
#        logger.debug('Query is %s', query)
#        logger.debug('POSITION Set to 1.  No More positions should be taken')
#        cur.execute(query)
#        cnx.commit()
#    
#        query = ("UPDATE hasPosition SET ProfitID = " + str(OIDprofit) + " WHERE CCY =\'" + Ticker[0] +"\';")
#        cur.execute(query)
#        cnx.commit()
#    
#        
#    if (int(curStopLossFlag[0]) == 1 and int(EntryPend[0]) == 0 and inPosAPI == 0 and int(Order_stop[0]) > 0):
#        logger.debug('Profit Target order placed')
#        
#    if (int(curprofitFlag[0]) == 1 and int(EntryPend[0]) == 0 and inPosAPI == 0 and int(Order_profit[0]) > 0):
#        logger.debug('Profit Target order placed')
        
        
        
    conn.disconnect()
    time.sleep(1)
#    logger.debug('EntryPending is %s', EntryPend[0])
#    logger.debug('StopLossFlag is %s', curStopLossFlag[0])
#    logger.debug('ProfitFlag is %s', curprofitFlag[0])
#    logger.debug('API knows pos is %s', inPosAPI)
#    logger.debug('Ticker is %s', Ticker[0])
#    logger.debug('EntryPendingTYPE is %s', type(EntryPend[0]))
#    logger.debug('StopLossFlagTYPE is %s', type(curStopLossFlag[0]))
#    logger.debug('ProfitTYPE is %s', type(curprofitFlag[0]))
#    logger.debug('inPosAPI is %s', type(inPosAPI))
#    logger.debug('Past All IF statements')
logger.debug('Disconnected from IBController')
logger.debug('END POS MGMT SCRIPT :-!')