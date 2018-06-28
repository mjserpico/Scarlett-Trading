# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""
#import MySQLdb
import mysql.connector
import logging
import datetime
import datalink


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
logger.debug('Clear Prices')

#from ib.ext.Order import Order
#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass ,host=datalink.DB_Host, database=datalink.DB_Path)



cur = cnx.cursor()
cur.execute("delete from FUT_BB_ES where Open > 0")
cnx.commit()

cur = cnx.cursor()
cur.execute("delete from FUT_BB_E7 where Open > 0")
cnx.commit()



cur = cnx.cursor()
cur.execute("ALTER TABLE FUT_BB_ES AUTO_INCREMENT = 1")
cnx.commit()

cur = cnx.cursor()
cur.execute("ALTER TABLE FUT_BB_E7 AUTO_INCREMENT = 1")
cnx.commit()



