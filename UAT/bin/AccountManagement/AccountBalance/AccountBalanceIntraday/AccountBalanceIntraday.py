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

logging.basicConfig(filename='pythonlogs\IntradayAccountBalance' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('IntradayAccountBalance' + str(datetime.date.today()) + '.txt')
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
    if float(test) < 500000:
            logger.debug('Account Value to be entered into database. %s', test)
            import time
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            #cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
            cur = cnx.cursor()
            cur.execute("""Insert Into IntraAccountBalance (Date, Balance) values(%s,%s)""",(time.strftime("%m/%d/%Y/%H"), float(test)))
            cnx.commit()
            logger.debug('Ran insert statement')
            global Flag
            Flag = 1
            logger.debug('Flag set to 1')

while Flag == 0:
    logger.debug('Connecting to Database')
    conn = Connection.create(port=4002, clientId=885)
    conn.register(reply_handler, 'AccountSummary')
    conn.connect()
    logger.debug('Connected to Database')
    conn.reqAccountSummary(1,'All','TotalCashValue')  
    logger.debug('Requested Account Summary')
    time.sleep(1) #give IB time to send us messages
    
conn.disconnect()
logger.debug('disconnected from IBController')
