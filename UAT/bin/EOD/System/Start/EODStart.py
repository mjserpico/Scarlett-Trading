# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 15:00:13 2017

@author: Michael
"""

import mysql.connector
import time
import datetime
import smtplib
import datalink

messagetext = "text"

def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message,login, password,smtpserver='smtp.gmail.com:587'):
    print(message)
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()

#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')    
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass, host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()

#query = ("Select Balance from AccountBalance t inner join (SELECT MAX(date) as max_date FROM AccountBalance) a on a.max_date = t.date")
#cur.execute(query)
#for (Balance) in cur:
#    bal = Balance
#    print(bal)    
#
#    
#query = ("SELECT CCY, direction FROM hasPosition where Count > 0;")
#cur.execute(query)
#for (CCY) in cur:
#    ccyval = CCY[0]
#    dirvalue = CCY[1]
#    print(dirvalue)
#    print(ccyval)  
#    


messagetext = "PROD EOD Running"
subjecttext = "PROD EOD Running"
message = 'Subject: {}\n\n{}'.format(subjecttext, messagetext) + "\n" #+  str(CCY)
    
sendemail(from_addr    = ['michael.serpico@scarletttrading.com'], 
          to_addr_list = ['michael.serpico@scarletttrading.com'],
          cc_addr_list = ['michael.serpico@scarletttrading.com'], 
          subject      = subjecttext, 
          message      = message, 
          login        = 'michael.serpico@scarletttrading.com', 
          password     = '@99Mz6SayF')
