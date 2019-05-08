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
import math
import csv
global Flag
Flag = 0
CCY1 = "temp"
CCY2 = "OHLC"
yClose = 0
Table = 'DailyOHLC'
logging.basicConfig(filename='ALLDailyOHLC' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('ALLDailyOHLC' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('Starting DailyOHLC')


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def reply_handler(msg):
    #print(msg.value)
    logger.debug('In beginning of Reply Handler')
    print("Reply:", msg)
    test = msg.open
    test2 = msg.high
    test3 = msg.low
    test4 = msg.close
    test5 = msg.volume
    #Stock = msg.ticker
    logger.debug('test %s', test) 
    logger.debug('test5 %s', test5)
    global Flag 
    logger.debug('Flag %s', Flag) 
    #test5 - msg.volume
    logger.debug('In Reply Handler')
   
    if float(test) != -1:
            import time
            logger.debug('Valid Price Found (OPEN NOT -1)')
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            #cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')

            cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
            logger.debug('Connected to Database')
            cur = cnx.cursor()
            cur.execute("Insert Into "+ Table + """(Stock, Date, Open, High, Low, Close) values(%s,%s,%s,%s,%s,%s)""",(Ticker,time.strftime("%m/%d/%Y"),float(test),float(test2),float(test3),float(test4)))
            cnx.commit()
            logger.debug('Ran Insert Script')
                        

            today = datetime.date.today( )
            dayofweek = datetime.datetime.today().weekday()
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
            month = (str(0) + str(backdate.month))
            day = (str(0)+ str(backdate.day))
            backdate2 = (month[-2:] +"/"+ day[-2:] +"/"+str(backdate.year))
            logger.debug('First Date of Moving Average is %s', backdate2)

#Temporary Table for Security with Temp ID as key

            #Create temporary table tempOHLC3 as (Select * from DailyOHLC where Stock = 'AAPL') order by ID;            
            query = ("Create temporary table tempOHLC as (Select * from DailyOHLC where Stock =\'" + str(row[0]) + "\') order by Date;")
            logger.debug('Query is %s', query)
            cur.execute(query)
            #ALTER TABLE tempOHLC3 ADD tempID INT PRIMARY KEY AUTO_INCREMENT;
            query = ("ALTER TABLE tempOHLC ADD tempID INT PRIMARY KEY AUTO_INCREMENT;")
            logger.debug('Query is %s', query)
            cur.execute(query)
            #Select * from tempOHLC3;
            #query = ("Create temporary table tempOHLC as (Select * from DailyOHLC where Stock = " + str(row[0]) + ") order by Date;")
            #logger.debug('Query is %s', query)
            #cur.execute(query)

#Most recent OHLC for Stock on Main Table referenced from temp table.   Used for applying calculations to main table
            query = ("SELECT max(ID) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                IDmain = ID
                logger.debug('IDmain is %s', IDmain)

            query = ("SELECT max(tempID) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID1 = tempID
                logger.debug('ID1 is %s', ID1)
                
            query = ("SELECT (max(tempID)-20) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID2 = tempID
                logger.debug('ID1 is %s', ID1)
                logger.debug('ID2 is %s', ID2)
                
            query = ("SELECT (max(tempID)-1) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID3 = ID
                logger.debug('ID3 is %s', ID3)

#Pull ATR Length From RiskParameter Table
            query = ("Select RiskParametersValue from RiskParameters where RiskParametersName = 'ATRlength';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                atrlength = ID
                logger.debug('ID4 is %s', atrlength)
            
#ID for ATR length start point                
            query = ("SELECT (max(tempID)-" + str(atrlength[0]) + ") from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID4 = tempID
                logger.debug('ID4 is %s', ID4)
                
#Pull MovingAvg Length RiskParameter Table
            query = ("Select RiskParametersValue from RiskParameters where RiskParametersName = 'MovAvgLength';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                movavglength = ID
                logger.debug('mov avglength is %s', movavglength)
            
#ID for MovAvg length start point                
            query = ("SELECT (max(tempID)-" + str(movavglength[0]) + ") from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID5 = tempID
                logger.debug('ID5 is %s', ID5)
            
            query = ("SELECT (max(tempID)-10) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID10 = tempID
                logger.debug('ID10 is %s', ID10)
                
            query = ("SELECT (max(tempID)-30) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID30 = tempID
                logger.debug('ID30 is %s', ID30)
                
            query = ("SELECT (max(tempID)-60) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID60 = tempID
                logger.debug('ID60 is %s', ID60)
                
            query = ("SELECT (max(tempID)-90) from " + CCY1 + CCY2)
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (tempID) in cur:
                ID90 = tempID
                logger.debug('ID90 is %s', ID90)
   
            query = ("SELECT Close from " + CCY1 + CCY2 + " where tempID = " + str(ID3[0]) + ";")
            cur.execute(query)
            for (Close) in cur:
                yClose = Close
                logger.debug('yClose is %s', yClose[0])
                
            query = ("SELECT Close from " + CCY1 + CCY2 + " where tempID = " + str(ID1[0]) + ";")
            cur.execute(query)
            for (Close) in cur:
                tClose = Close
                logger.debug('tClose is %s', tClose[0])
                
#Interday Return
            CloseReturn = float(tClose[0])
            yCloseReturn = float(yClose[0])
            logger.debug('yClose is %s', yClose[0])
            logger.debug('Close is %s', tClose[0])
            returns = round(((CloseReturn / yCloseReturn) - 1) * 100,2)
            logger.debug('Return is %s', returns)
            
            query = ("UPDATE " + Table + " SET PercentReturn = " + str(returns) + " where ID = " + str(IDmain[0]) +";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()
            
# period Moving Average
            query = ("SELECT round(Avg(Close),2) as Avg from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID5[0]) + " AND " +  str(ID1[0]) + ";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (Avg) in cur:
                DailyMovAvg = Avg   #Final Moving Average Value
                logger.debug('MovAvg is %s', DailyMovAvg)
        
##Puts Moving Average Value in hasPosition Table for Reference with intraday strategies
            query = ("UPDATE hasPosition SET MovingAvgValue = " + str(DailyMovAvg[0]) + " where CCY =\'" + row[0] +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()
            
#True Range
            TR1 = (test2-test3)
            TR2 = abs(test2-float(yClose[0]))
            TR3 = abs(test3-float(yClose[0]))
            TR = truncate(max(TR1,TR2,TR3),4)
            print(TR)
            print(TR1)
            print(TR2)
            print(TR3)

            query = ("UPDATE "+ Table +" SET TrueRange = " + str(TR) + " where ID =\'" + str(IDmain[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()

#ATR Daily             
            query = ("SELECT round(Avg(TrueRange),2) as Avg from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID4[0]) + " AND " +  str(ID1[0]) + ";")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            for (Avg) in cur:
                ATRAvg = Avg   #Final Moving Average Value
                logger.debug('ATR is %s', ATRAvg)

##Puts ATR in hasPosition Table for Reference with intraday strategies
            query = ("UPDATE hasPosition SET ATRValue = " + str(ATRAvg[0]) + " where CCY =\'" + CCY1 + CCY2 +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            print(query)
            cnx.commit()


#Calculate 10D Vol       
            query = ("SELECT round(stddev(PercentReturn),2) as vol10 from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID10[0]) + " AND " +  str(ID1[0]) + ";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (vol10) in cur:
                tend = truncate((vol10[0] * math.sqrt(252)),2)  #Final Moving Average Value
                logger.debug('10d is %s', tend)

            query = ("UPDATE "+ Table +" SET tenvol = " + str(tend) + " where ID =\'" + str(ID1[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()



#Calculate 30D Vol       
            query = ("SELECT round(stddev(PercentReturn),2) as vol30 from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID30[0]) + " AND " +  str(ID1[0]) + ";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (vol30) in cur:
                thirtyd = truncate((vol30[0] * math.sqrt(252)),2)  #Final Moving Average Value
                logger.debug('30d is %s', thirtyd)

            query = ("UPDATE "+ Table +" SET thirtyvol = " + str(thirtyd) + " where ID =\'" + str(ID1[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()

#Calculate 60D Vol
            query = ("SELECT round(stddev(PercentReturn),2) as vol60 from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID60[0]) + " AND " +  str(ID1[0]) + ";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (vol60) in cur:
                sixtyd = truncate((vol60[0] * math.sqrt(252)),2)   #Final Moving Average Value
                logger.debug('sixtyd is %s', sixtyd)

            query = ("UPDATE "+ Table +" SET sixtyvol = " + str(sixtyd) + " where ID =\'" + str(ID1[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()


#Calculate 90D Vol
            query = ("SELECT round(stddev(PercentReturn),2) as vol90 from " + CCY1 + CCY2 + " where ID BETWEEN " +  str(ID90[0]) + " AND " +  str(ID1[0]) + ";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (vol90) in cur:
                ninetyd = truncate((vol90[0] * math.sqrt(252)),2)  #Final Moving Average Value
                logger.debug('ninetyd is %s', ninetyd)

            query = ("UPDATE "+ Table +" SET ninetyvol = " + str(ninetyd) + " where ID =\'" + str(ID1[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()
       
    Flag = 1
    logger.debug('Flag set to %s', Flag)
    print(Flag)
    return(Flag)

f = open('dow.csv')
csv_f = csv.reader(f)

for row in csv_f:
    global Ticker
    Ticker = row[0]
    exchange = row[1]
    logger.debug('Ticker is %s', row) 
    logger.debug('exchange is %s', exchange) 
    logger.debug('Flag set to %s', Flag)          
    conn = Connection.create(port=4002, clientId=999)
    conn.connect()
    logger.debug('Connecting to Server')
    time.sleep(1)
    conn.register(reply_handler,'HistoricalData')   #By registering "HistoricalData" --the Method name only --we can eliminate all the open order garbage
    logger.debug('Registered HistoricalData Reply Handler')
    time.sleep(1)
    qqq = Contract()  
    qqq.m_symbol = row[0]
    qqq.m_secType = 'STK'  
    qqq.m_exchange = 'SMART:' + row[1]
    qqq.m_currency = 'USD'
    logger.debug('Requesting historical data') 
    conn.reqHistoricalData(1, qqq, '', '1 D', '1 day', 'TRADES', 0, 1)
    logger.debug('Returned from Reply Handler')
    time.sleep(1) #give IB time to send us messages
    logger.debug('Disconnecting from Server')
    Flag = 0
    logger.debug('Flag is %s', Flag) 
    conn.disconnect()
    

logger.debug('Finished Daily OHLC')