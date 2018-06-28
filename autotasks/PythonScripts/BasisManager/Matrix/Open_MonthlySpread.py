# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 17:00:49 2017
Monthly Rollover Trade
Ecery month @ Rollover Date -1, Buy frontmonth contract and sell the out month as the basis converges.  Close spread prior to expiration
Rollover Date =  Thursday before expiration Friday (8 days prior)   We take trade Wednesday morning before rollover
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
import datalink  #universal logins for environment
#,"M6B","ES","M6E"
Product = ["M6A","MCD","E7","ZC","M6B","ES","M6E",-1]
masteraccount = datalink.DB_Account
count = 0
symbol = ""
exchange = "Globex"
secType = "FUT"
logging.basicConfig(filename='pythonlogs\SpreadTrader' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('SpreadTrader' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')
logger.debug('Starting SpreadTrader %s', Product[count])

def reply_handler(msg):
    #test = msg.value
    logger.debug('Reply Handler %s', msg)
    
def create_contract(symbol, sec_type, exch, prim_exch, month, curr):
    logger.debug('symbol %s', symbol)
    logger.debug('sec_type %s', sec_type)
    logger.debug('exch %s', exch)
    logger.debug('prim_exch %s', prim_exch)
    logger.debug('month %s', month[0])
    logger.debug('curr %s', curr)
    
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_localSymbol = str(symbol) + str(month[0]) + "7";
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    logger.debug('Contract created')
    return contract
    
    
# limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None)
def make_leg1_order(action, qty):
        logger.debug('action %s', action[0])
        logger.debug('qty %s', qty[0])
        order = Order()
        order.m_action = str(action[0])
        order.m_totalQuantity = int(qty[0])
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        order.m_orderType = 'MKT'
        order.m_account = masteraccount
        order.m_transmit = True
        return order    
        
def make_leg2_order(action, qty):
        logger.debug('action %s', action)
        logger.debug('qty %s', qty)
        order = Order()
        order.m_action = str(action[0])
        order.m_totalQuantity = int(qty[0])
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        order.m_orderType = 'MKT'
        order.m_account = masteraccount
        order.m_transmit = True
        return order   
        
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connected To Database')

while Product[count] != -1:            
    logger.debug('Product set to %s', Product[count])
    time.sleep(1)
    today = datetime.date.today( )
    Date = today
    time = datetime.datetime.now().strftime("%I:%M%p")
    logger.debug('Time is %s', time)
    #placeholder for Orders. Use when intraday strategies go into effect
    Currency = Product[count]
    Price = 'MKT'
    Strategy = "MonthlyBasisRoll"
    Bracket = "Leg1"
    Status = "Filled"
    
    
    #conn.registerall(reply_handler)
    symbol = Product[count]
    query = ("SELECT Leg1_Month from RolloverExpiry where Product =\'" + str(Product[count])+ "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (Leg1_Month) in cur:
        Leg1month = Leg1_Month

    logger.debug('Leg1_month is %s', Leg1month) 

    query = ("SELECT Leg2_Month from RolloverExpiry where Product =\'" + str(Product[count]) + "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (Leg2_Month) in cur:
        Leg2month = Leg2_Month

    logger.debug('Leg2_month is %s', Leg2month) 

    query = ("SELECT Leg1_Action from RolloverExpiry where Product =\'" + str(Product[count])+ "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (Leg1_Action) in cur:
        Leg1Action = Leg1_Action

    logger.debug('Leg1_action is %s', Leg1Action) 

    query = ("SELECT Leg2_Action from RolloverExpiry where Product =\'" + str(Product[count]) + "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (Leg2_Action) in cur:
        Leg2Action = Leg2_Action

    logger.debug('Leg2_Action is %s', Leg2Action) 

    query = ("SELECT Quantity from RolloverExpiry where Product =\'" + Product[count]+ "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (Quantity) in cur:
        Qty = Quantity

    logger.debug('Leg2_Action is %s', Leg2Action)     

    query = ("SELECT max(idOrder) from Orders;")
    cur.execute(query)
    for (idOrder) in cur:
        OID = int(idOrder[0]) + 1
        logger.debug('Order ID for next trade is %s', OID)

    logger.debug('Connecting to Server')
    conn = Connection.create(port=4002, clientId=999)
    conn.connect()
    conn.registerAll(reply_handler)

    parentId = OID
    TriggerID = OID  #Groups Parent and Child orders to single parent order ID
    
#LEG1
    CONTRACT = create_contract(symbol, secType, exchange, exchange, Leg1month, 'USD')
    logger.debug('Back From contract function')
    ORDER = make_leg1_order(Leg1Action, Quantity)
    logger.debug('Back from Order Function')
    conn.placeOrder(OID, CONTRACT, ORDER)
    logger.debug('Order Placed')

    cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(OID, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
    cnx.commit() #Leg1
    
    query = ("SELECT max(idOrder) from Orders;")
    cur.execute(query)
    for (idOrder) in cur:
        OID = int(idOrder[0]) + 1
        logger.debug('Order ID for next trade is %s', OID)
#LEG2
    CONTRACT = create_contract(symbol, secType, exchange, exchange, Leg2month, 'USD')
    logger.debug('Back From contract function')
    ORDER = make_leg2_order(Leg2Action, Quantity)
    logger.debug('Back from Order Function')
    conn.placeOrder(OID, CONTRACT, ORDER)
    logger.debug('Order Placed')
    
    Bracket = "Leg2"
    
    cur.execute("""Insert Into Orders (idOrder, Date, Time, Currency, TriggerID, Price, Strategy, Bracket, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(OID, Date, time, Currency, TriggerID, Price, Strategy, Bracket, Status))
    cnx.commit() #Leg1
    
    count = count + 1
conn.disconnect()