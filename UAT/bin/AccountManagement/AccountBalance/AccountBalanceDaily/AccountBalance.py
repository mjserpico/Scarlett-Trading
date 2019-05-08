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
import mysql.connector 
from ib.opt import Connection, message
import ib
import time
import logging
import datetime
import datalink  #universal logins for environment
Flag = 0

logging.basicConfig(filename='\AccountBalance' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('AccountBalance' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')


def reply_handler(msg):
    test = msg.value
    logger.debug('Message Value is %s', msg)
    if float(test) < 5000000:
            logger.debug('Account Value to be entered into database. %s', test)
            import time
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            #cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
            cur = cnx.cursor()
            cur.execute("""Insert Into AccountBalance (Date, Balance) values(%s,%s)""",(time.strftime("%m/%d/%Y"), float(test)))
            cnx.commit()
            logger.debug('Ran insert statement')
            global Flag
            Flag = 1
            print(Flag)
            logger.debug('Flag set to 1')
            
            
#Sharpe Ratio is always 1 on index 
            query = ("UPDATE AccountBalance SET SharpeRatio = '1' where ID =\'" + str(ID1[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()
            
#Max Drawdown of index            
            MaxDrawdown = 0
            #Find Max value since Jan 1
            query = ("Select max(Close) as Maximum from" + CCY1 + CCY2 + ";")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (Maximum) in cur:
                Maxval = Maximum  #Final Moving Average Value
                logger.debug('Maxval is %s', Maxval)
            
            #Find Min value since Jan 1 AFTER the MAX value
            query = ("select min(Close) as Minimum from" + CCY1 + CCY2 + " where ID > (select ID from" + CCY1 + CCY2 + "where Close = (Select max(Close) from " + CCY1 + CCY2 + "));")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (Minimum) in cur:
                Minval = Minimum  #Final Moving Average Value
                logger.debug('Minval is %s', Minval)
           
            MaxDrawdown = Maxval - Minval 

            query = ("UPDATE "+ Table +" SET MaxDrawdown = " + str(MaxDrawdown) + " where ID =\'" + str(ID1[0]) +"\';")
            logger.debug('Query is %s', query)
            print(query)
            cur.execute(query)
            cnx.commit()
                
            
            
while Flag == 0:
    logger.debug('Connecting to Database')
    conn = Connection.create(port=4002, clientId=888)
    conn.register(reply_handler, 'AccountSummary')
    conn.connect()
    logger.debug('Connected to Database')
    conn.reqAccountSummary(1,'All','NetLiquidation')  
    logger.debug('Requested Account Summary')
    time.sleep(1) #give IB time to send us messages
    
conn.disconnect()
logger.debug('disconnected from IBController')
