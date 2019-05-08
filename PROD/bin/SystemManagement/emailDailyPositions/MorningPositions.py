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
import smtplib
import datalink  #universal logins for environment
Flag = 0

logging.basicConfig(filename='emailDailyPositions' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('emailDailyPositions' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')
test = 0
messagetext = ""
messagetext2 ="Morning Orders \n"
def reply_handler_Orders(msg):
    orderinfo = msg.order
    con = msg.contract
    logger.debug('Message Value is %s', orderinfo)
    logger.debug('Message con is %s', con)
    if float(test) < 5000000:
     #         logger.debug('Account Value to be entered into database. %s', test)
      #      import time
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
            #cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
            #cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
            #cur = cnx.cursor()
#            cur.execute("""Insert Into AccountBalance (Date, Balance) values(%s,%s)""",(time.strftime("%m/%d/%Y"), float(test)))
#            cnx.commit()
#            logger.debug('Ran insert statement')
            global Flag
            Flag = 1
            print(Flag)
            logger.debug('Flag set to 1')
            #query = ("UPDATE RiskParameters SET RiskParametersValue='1' WHERE idRiskParameters='8';")
            #logger.debug('Query is %s', query)
            #print(query)
            #cur.execute(query)
            #cnx.commit()
            
            #for (RiskParametersValue) in cur:
            #    bal = RiskParametersValue 
            #    logger.debug('Balance is %s', bal)
            global messagetext2
            messagetext = con.m_symbol + "         " + str(orderinfo.m_totalQuantity) + "         " + str(orderinfo.m_auxPrice)+ "\n"
            messagetext2 += messagetext
    


def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message,login, password,smtpserver='smtp.gmail.com:587'):
    logger.debug(message)
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    logger.debug('Email sent')                    

           
while Flag == 0:
    logger.debug('Connecting to Database')
    conn = Connection.create(port=4002, clientId=999)
    conn.register(reply_handler_Orders, 'OpenOrder') 
    conn.connect()
    logger.debug('Connected to Database')
    conn.reqAllOpenOrders() # will find the order if it's open
    #conn.reqAccountSummary(1,'All','NetLiquidation')  
    logger.debug('Requested All Open orders')
    time.sleep(1) #give IB time to send us messages

subjecttext = "Morning Orders " + time.strftime("%m/%d/%Y")
message = 'Subject: {}\n\n{}'.format(subjecttext, messagetext2) + "\n" #+  str(CCY)
sendemail(from_addr    = ['michael.serpico@scarletttrading.com'], to_addr_list = ['michael.serpico@scarletttrading.com'], cc_addr_list = ['michael.serpico@scarletttrading.com'], subject = subjecttext, message = message, login = 'michael.serpico@scarletttrading.com', password = '@99Mz6SayF')
logger.debug('Email function called')   
conn.disconnect()
logger.debug('disconnected from IBController')
