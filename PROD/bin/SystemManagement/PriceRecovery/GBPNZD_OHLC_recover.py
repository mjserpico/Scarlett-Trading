# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""
#import MySQLdb
from ib.opt import Connection
import time
from ib.ext.Contract import Contract
import mysql.connector
import datetime
from dateutil.parser import parse
from RecoverySettings import daysback
from RecoverySettings import strdaysback
#from ib.ext.Order import Order


CCY1 = "GBP"
CCY2 = "NZD"


def reply_handler(msg):
    #print(msg.value)
    print("Reply:", msg)
    test = msg.open
    test2 = msg.high
    test3 = msg.low
    test4 = msg.close
    test5 = msg.date
    
  
    dt = parse(str(test5))
    print(dt)
    # datetime.datetime(2010, 2, 15, 0, 0)
    print(dt.strftime('%m/%d/%Y'))
    newdate = dt.strftime('%m/%d/%Y')

##Convert Date to proper format and relative reference
#    if dayofweek == 0:  #if Today is Monday
#        yesterday = today - datetime.timedelta(days=3)  #Get Previous Wednesday                   
#        month = (str(0) + str(yesterday.month))
#        day = (str(0)+ str(yesterday.day))
#        yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
#        print(yesterday2)
#
#    else:
#        yesterday = today - datetime.timedelta(days=1) #Take 3 Days back                    
#        month = (str(0) + str(yesterday.month))
#        day = (str(0)+ str(yesterday.day))
#        yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
#        print("Yesterday was " + str(yesterday2))
#    
    
    
   
    if float(test) != -1:
            import time
             #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            cur = cnx.cursor()
            cur.execute("""Insert Into EURCHF (Date, Open, High, Low, Close) values(%s,%s,%s,%s,%s)""",(newdate,float(test),float(test2),float(test3),float(test4)))
            cnx.commit()

conn = Connection.create(port=4002, clientId=999)
conn.connect()
time.sleep(2)
conn.register(reply_handler,'HistoricalData')   #By registering "HistoricalData" --the Method name only --we can eliminate all the open order garbage
#conn.registerall(reply_handler)
time.sleep(3)




today = datetime.date.today( )
print("Today is " + str(today))
dayofweek = datetime.datetime.today().weekday()
print("Today is coded:" + str(dayofweek))

#0 is Monday, 1 tues 2 wed 3 thurs 4 fri 5 sat 6 sun

# 5 is Saturday

##Convert Date to proper format and relative reference
if dayofweek == 0:  #if Today is Monday
    yesterday = today - datetime.timedelta(days=daysback)  #Get 5 days back                   
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    print(yesterday2)

else:
    yesterday = today - datetime.timedelta(days=daysback) #Take 5 Day back from day of run   04/08 - 5 is  04/03    <<<<<<<**********                 
    month = (str(0) + str(yesterday.month))
    day = (str(0)+ str(yesterday.day))
    yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
    print("First Date to grab price is " + str(yesterday2))


#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cur = cnx.cursor()
query = ("SELECT ID from " + CCY1 + CCY2 + " where Date = \'" + yesterday2 + "\'")
print(query)
cur.execute(query)
for (ID) in cur:
    ID1 = ID

print("ID1 is " + str(ID1)) 
query = ("Delete from " + CCY1 + CCY2 + " where ID >= \"" + str(ID1[0]) + "\"")
cur.execute(query)
cnx.commit()

ID2 = int(ID1[0])
print(ID2)

query = ("ALTER TABLE " + CCY1 + CCY2 + " AUTO_INCREMENT =" + str(ID2))
print(query)
cur.execute(query)

cnx.commit()
#cur.execute("""Insert Into EURCHF (Date, Open, High, Low, Close) values(%s,%s,%s,%s,%s)""",(time.strftime("%m/%d/%Y"),float(test),float(test2),float(test3),float(test4)))
#cnx.commit()

qqq = Contract()  
qqq.m_symbol = 'EUR'  
qqq.m_secType = 'CASH'  
qqq.m_exchange = 'IDEALPRO'  
qqq.m_currency = 'CHF'  
conn.reqHistoricalData(1, qqq, '', strdaysback, '1 day', 'Midpoint', 1, 2)  #Market days 
time.sleep(1) #give IB time to send us messages
conn.disconnect()