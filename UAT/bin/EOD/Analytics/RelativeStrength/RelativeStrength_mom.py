# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:54:39 2018

@author: Michael
"""
#Standard Python Libs
import mysql.connector
import datetime
import logging
import sys
import time
import pandas as pd
import numpy as np
import os

#Scarlett Trading Lib
import datalink  #universal logins for environment
import DatabaseQueries as Qry

#IB Library
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 
import csv
import math
Flag = 0
Table = 'SPY'
yClose = 0
#Quantopian Library
#import zipline as zl 

logging.basicConfig(filename='\RelativeStrength' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('RelativeStrength' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

print("Relative Strength")
"""
Add csv file to daily analytics folder
"""
#Index
def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
logger.debug('Connected to Database')
cur = cnx.cursor()



f = open('dow.csv')
csv_f = csv.reader(f)

for row in csv_f:
            print(row)
            Ticker = row
        #SPY INDEX max ID
#            query = ("SELECT max(ID) from " + Table)
#            logger.debug('Query is %s', query)
#            cur.execute(query)
#            for (ID) in cur:
#                ID1 = ID
#                logger.debug('ID1 is %s', ID1)
         #Stock Max ID      
            query = ("SELECT max(ID) from " + Ticker[0])
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID2 = ID
                logger.debug('ID2 is %s', ID2)  
    
        #3 days back and 10 days back for Ticker        
                
            query = ("SELECT (max(ID)-3) from " + Ticker[0])
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID3Ticker = ID
                logger.debug('ID3Ticker is %s', ID3Ticker)
                
            query = ("SELECT (max(ID)-10) from " + Ticker[0])
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID10ticker = ID
                logger.debug('ID10ticker is %s', ID10ticker)

            
#Close from Days Back
            
            query = ("SELECT Close from " + Table + " where ID = " + str(ID3Ticker[0]) + ";")
            cur.execute(query)
            for (Close) in cur:
                tickerthreeClose = Close
                logger.debug('indexfiveClose is %s', tickerthreeClose[0])
                
            query = ("SELECT Close from " + Ticker[0] + " where ID = " + str(ID10ticker[0]) + ";")
            cur.execute(query)
            for (Close) in cur:
                tickertenClose = Close
                logger.debug('tickertenClose is %s', tickertenClose[0])

#Close from Most recent day

#            query = ("SELECT Close from " + Table + " where ID = " + str(ID1[0]) + ";")
#            cur.execute(query)
#            for (Close) in cur:
#                indexClose = Close
#                logger.debug('indexClose is %s', indexClose[0])
                
            query = ("SELECT Close from " + Ticker[0] + " where ID = " + str(ID2[0]) + ";")
            cur.execute(query)
            for (Close) in cur:
                tickerClose = Close
                logger.debug('tickerClose is %s', tickerClose[0])

#Calculate the Percent Return over 5 days for Index
            #returnsIdx = ((float(indexClose[0]) - float(indexfiveClose[0])) / float(indexfiveClose[0])*100)
            #returnsIdx2 = truncate(returnsIdx,2)
            #logger.debug('returnsIdx is %s', returnsIdx2)
#Calculate the Percent Return over 5 days for Ticker
#/ float(tickerfiveClose[0])*100)
            returnsStock3 = (float(tickerClose[0]) - float(tickerthreeClose[0])
            returnsStock10 = (float(tickerClose[0]) - float(tickertenClose[0])
            
            
#Relative Strength      
#            RelStr = float(returnsStock2) / float(returnsIdx2)
#            RelStr2 = truncate(RelStr,2)
#            logger.debug('RelStr2 is %s', RelStr2)  
            
            query = ("UPDATE hasPosition SET Mom3 = " + str(RelStr2) + " where CCY =\'" + Ticker[0] +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()        
            
            query = ("UPDATE hasPosition SET Mom10 = " + str(RelStr2) + " where CCY =\'" + Ticker[0] +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()  