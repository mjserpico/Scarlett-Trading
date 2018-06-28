# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""
import mysql.connector
from ib.opt import Connection
from ib.ext.Contract import Contract
import time
import logging
import datetime
import datalink  #universal logins for environment


logging.basicConfig(filename='pythonlogs\BBPricing' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('BBPricing' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

CCY1 = 'E'
CCY2 = 'C'
Table = 'FUT_BB_6E'

logger.debug('Starting'+ CCY1 + CCY2)


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def reply_handler(msg):
    #print(msg.value)
    print("Reply:", msg)
    logger.debug('Reply is %s',msg)
    test = msg.open
    test2 = msg.high
    test3 = msg.low
    test4 = msg.close
    test5 = msg.date

 
   
    if float(test) != -1:
            logger.debug('Valid Price Found OPEN NOT negative one')
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            #cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
            logger.debug('Connected to Database')
            cur = cnx.cursor()
            cur.execute("Insert Into " + Table + " (Date, Open, High, Low, Close) values(%s,%s,%s,%s,%s)",(test5,truncate(float(test),4),truncate(float(test2),4),truncate(float(test3),4),truncate(float(test4),4)))
            cnx.commit()
            logger.debug('Ran Insert Script')
            
conn = Connection.create(port=4002, clientId=999)
conn.connect()
logger.debug('Connecting to Server')
time.sleep(1)
conn.register(reply_handler,'HistoricalData')   #By registering "HistoricalData" --the Method name only --we can eliminate all the open order garbage
logger.debug('Registered HistoricalData Reply Handler')
#conn.registerall(reply_handler)
time.sleep(1)

qqq = Contract()
qqq.m_symbol = CCY1+CCY2 
qqq.m_localSymbol = CCY1+CCY2 + datalink.monthcode + "7"; 
qqq.m_secType = 'FUT'  
qqq.m_exchange = 'GLOBEX'  
qqq.m_currency = 'USD'
qqq.m_expiry = datalink.exp_quarter; 
logger.debug('Requesting historical data') 
conn.reqHistoricalData(6, qqq, '', '60 S', '5 mins', 'ASK', 0, 1) 
logger.debug('Returned from Reply Handler')
time.sleep(1) #give IB time to send us messages
logger.debug('Disconnecting from Server')
conn.disconnect()

time.sleep(1)
logger.debug('Start Bollinger Band Calculation')
#Store BollingerBand Values
logger.debug('Connecting to Database again')
#cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
query = ("Select round(stddev(Close),5) as StdDev from " + Table + " where ID BETWEEN ((SELECT MAX(ID) as max_ID FROM " + Table + ")-20) and (SELECT MAX(ID) as max_ID FROM " + Table + ");")
cur = cnx.cursor()
cur.execute(query)
logger.debug('ran select statement to get prices for calc')
for (StdDev) in cur:
    tStdDev = StdDev   
    logger.debug('Got StdDev. %s', tStdDev)

    
query = ("SELECT MAX(ID) as maxID FROM " + Table + "")
cur = cnx.cursor()
cur.execute(query)
for (maxID) in cur:
    maximumID = maxID   
    logger.debug('Got Max ID. %s', maximumID)
    
    
if maximumID[0] > 20:    
        logger.debug('Over 20 entries, can now print BB')
        query = ("Select round(Avg(Close),5) as Average from " + Table + " where ID BETWEEN ((SELECT MAX(ID) as max_ID FROM " + Table + ")-20) and (SELECT MAX(ID) as max_ID FROM " + Table + ");")
        logger.debug('Query is . %s', query)
        cur = cnx.cursor()
        cur.execute(query)
        logger.debug('Past query')
        for (Average) in cur:
            logger.debug('In For Loop')
            logger.debug('Average is %s', Average)
            logger.debug('Average is %s', type(Average))
            BBAverage = truncate(Average[0],4)  
            logger.debug('BBAverage is %s', BBAverage)
            logger.debug('BBAverage is %s', type(BBAverage))
            
        logger.debug('Out of For Loop')
        logger.debug('tStdDev[0] is %s', tStdDev[0])
        logger.debug('tStdDev[0] is %s', type(tStdDev[0]))
        tUpperBand = truncate((float(BBAverage)  + (2 * float(tStdDev[0]))),4)
        logger.debug('BBAverage is %s', BBAverage)
        logger.debug('BBAverage is %s', type(BBAverage))
        logger.debug('std dev 2 is %s', (2 * float(tStdDev[0])))
        logger.debug('tUpperBand %s', tUpperBand)
        tLowerBand = truncate((float(BBAverage)  - (2 * float(tStdDev[0]))),4)
        logger.debug('Upper is . %s', tUpperBand)
        logger.debug('Lower is . %s', tLowerBand)
        BBAverage = truncate(BBAverage,4)
        
        query = ("Update " + Table + " set UpperBand = " + str(tUpperBand) + ", LowerBand = " + str(tLowerBand) + ", MidLine = " + str(BBAverage) + " where ID = " + str(maximumID[0]) + ";") 
        logger.debug('Query is %s', query)
        cur.execute(query)
        cnx.commit()
        
logger.debug('&&&&&&&&&&& END &&&&&&&&& Band Calculation')