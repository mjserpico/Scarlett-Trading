# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""
import mysql.connector
from ib.opt import Connection, message
from ib.ext.Contract import Contract
import time
import logging
import datetime
import datalink2  #universal logins for environment
Flag = 0
CCY1 = "H"
CCY2 = "E"
Table = 'HE'

logging.basicConfig(filename='pythonlogs\DailyOHLC' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('DailyOHLC' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('Starting HEDailyOHLC')


def reply_handler(msg):
    #print(msg.value)
    print("Reply:", msg)
    test = msg.open
    test2 = msg.high
    test3 = msg.low
    test4 = msg.close
    test5 = msg.volume
    logger.debug('test5 %s', test5) 
    #test5 - msg.volume
    logger.debug('In Reply Handler')
   
    if float(test) != -1:
            import time
            logger.debug('Valid Price Found (OPEN NOT -1)')
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            #cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            cnx = mysql.connector.connect(user=datalink2.DB_User, password=datalink2.DB_Pass,host=datalink2.DB_Host, database=datalink2.DB_Path)
            logger.debug('Connected to Database')
            cur = cnx.cursor()
            cur.execute("Insert Into "+ Table + """(Date, Open, High, Low, Close) values(%s,%s,%s,%s,%s)""",(time.strftime("%m/%d/%Y"),float(test),float(test2),float(test3),float(test4)))
            cnx.commit()
            logger.debug('Ran Insert Script')
            
            today = datetime.date.today( )
            print("Today is " + str(today))
            dayofweek = datetime.datetime.today().weekday()
            print(dayofweek)
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
            #MovingAverage Calculation
            #Step 1 Get earliest Date to calculate avg from
            #reformat date to DB convention first
            logger.debug('Today is still  %s', today)
            backdate = today - datetime.timedelta(days=13)
            logger.debug('Date shifted back 10 is %s', backdate)
            dayofweek = backdate.weekday()

            #Adjust for Saturdays and Sundays: No price data available.  
#            if dayofweek == 6:
#                backdate = today - datetime.timedelta(days = 9)
#            if dayofweek == 5:
#                backdate = today - datetime.timedelta(days = 8)
#    
            month = (str(0) + str(backdate.month))
            day = (str(0)+ str(backdate.day))
            backdate2 = (month[-2:] +"/"+ day[-2:] +"/"+str(backdate.year))
            logger.debug('First Date of BB Moving Average is %s', backdate2)

                    #Select ID from EURUSD where Date in ('12/19/2016', '02/07/2017');
                    #Select round(Avg(Close),5) from EURUSD where ID BETWEEN 3881 AND 3915;
#            query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \"" + yesterday2 + "\"")
#            logger.debug('Query is %s', query)
#            cur.execute(query)
#            for (ID) in cur:
#                ID1 = ID
#                logger.debug('BB ID1 is %s', ID1)
#    
#            query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \"" + backdate2 + "\"")
#            logger.debug('Query is %s', query)
#            cur.execute(query)
#            for (ID) in cur:
#                ID2 = ID
#                logger.debug('BB ID1 is %s', ID1)
#                logger.debug('BB ID2 is %s', ID2)

            query = ("SELECT max(ID) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID1 = ID
                logger.debug('BB ID1 is %s', ID1)
                
            query = ("SELECT (max(ID)-20) from " + CCY1 + CCY2)
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

            
            
            global Flag
            Flag = 1
            logger.debug('Flag set to 1')

while Flag == 0:            
    conn = Connection.create(port=4002, clientId=886)
    conn.connect()
    logger.debug('Connecting to Server')
    time.sleep(1)
    conn.register(reply_handler,'HistoricalData')   #By registering "HistoricalData" --the Method name only --we can eliminate all the open order garbage
    logger.debug('Registered HistoricalData Reply Handler')
    #conn.registerall(reply_handler)
    time.sleep(1)

    qqq = Contract()  
    qqq.m_symbol = 'HE'
    qqq.m_localSymbol = 'HE'+ datalink2.monthcode + '8' 
    #qqq.ConId = 279555803
    qqq.m_secType = 'FUT'  
    qqq.m_exchange = 'GLOBEX'  
    qqq.m_currency = 'USD'
    qqq.m_expiry = datalink2.exp_quarter;
    logger.debug('Requesting historical data') 
    conn.reqHistoricalData(1, qqq, '', '1 D', '1 day', 'ASK', 0, 1)
    logger.debug('Returned from Reply Handler')
    time.sleep(1) #give IB time to send us messages
    logger.debug('Disconnecting from Server')
    conn.disconnect()
logger.debug('Finished HE Daily OHLC')