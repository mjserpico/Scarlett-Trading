# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""
#import MySQLdb
from ib.opt import Connection
import time
import datetime
from ib.ext.Contract import Contract
import mysql.connector
#from ib.ext.Order import Order

def reply_handler(msg):
    #print(msg.value)
    print("Reply:", msg)
    test = msg.open
    test2 = msg.high
    test3 = msg.low
    test4 = msg.close
    test5 = msg.date
    

     
    if float(test) != -1:
        
            today = test5
            print("Today is " + str(today))
            timeing = datetime.datetime.now().time()
            print(type(timeing))
            str(timeing)
            print(type(timeing))
            print(timeing)
##Convert Date to proper format and relative reference
      #if Today is Monday
            today2 = datetime.datetime.strptime(test5, '%Y%m%d').strftime('%m/%d/%y')
            print("Final date is " + str(today2))
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            cur = cnx.cursor()
            cur.execute("""Insert Into wUSDMXN (Date, Open, High, Low, Close) values(%s,%s,%s,%s,%s)""",(str(today2),float(test),float(test2),float(test3),float(test4)))
            cnx.commit()

conn = Connection.create(port=4002, clientId=999)
conn.connect()
time.sleep(2)
conn.register(reply_handler,'HistoricalData')   #By registering "HistoricalData" --the Method name only --we can eliminate all the open order garbage
#conn.registerall(reply_handler)
time.sleep(3)

qqq = Contract()  
qqq.m_symbol = 'USD'  
qqq.m_secType = 'CASH'  
qqq.m_exchange = 'IDEALPRO'  
qqq.m_currency = 'MXN'  
conn.reqHistoricalData(1, qqq, '', '1 W', '1 week', 'Midpoint', 1, 2) 
time.sleep(1) #give IB time to send us messages
conn.disconnect()