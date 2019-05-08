# -*- coding: utf-8 -*-
"""
Created on Sat Mar 04 15:00:13 2017

@author: Michael
"""

import mysql.connector
import datetime
import smtplib
import logging
import datalink  #universal logins for environment

messagetext = "text"


logging.basicConfig(filename='pythonlogs\EmailSummary' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('EmailSummary' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')



def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message,login, password,smtpserver='smtp.gmail.com:587'):
    logger.debug(message)
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    logger.debug('Email sent')

#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')    
#cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()

query = ("Select Balance from IntraAccountBalance t inner join (SELECT MAX(date) as max_date FROM IntraAccountBalance) a on a.max_date = t.date")
cur.execute(query)
for (Balance) in cur:
    bal = Balance 
    logger.debug('Balance is %s', bal)

messagetext = "PROD Intraday Account Balance is  \n" + str(Balance[0])
subjecttext = "PROD Intraday Account Summary"
message = 'Subject: {}\n\n{}'.format(subjecttext, messagetext) + "\n" #+  str(CCY)
    
sendemail(from_addr    = ['michael.serpico@scarletttrading.com'], 
          to_addr_list = ['michael.serpico@scarletttrading.com'],
          cc_addr_list = ['michael.serpico@scarletttrading.com'], 
          subject      = subjecttext, 
          message      = message, 
          login        = 'michael.serpico@scarletttrading.com', 
          password     = '@99Mz6SayF')
logger.debug('Email function called')