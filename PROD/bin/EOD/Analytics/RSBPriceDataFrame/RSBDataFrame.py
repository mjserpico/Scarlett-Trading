# -*- coding: utf-8 -*-
"""
RSB DataFrame 
This script will pull the OHLC values for the past 45 trading days for each of the read Ticker symbols
The script will format the values and export the csv daily for ingestion by downstream script to analyze data
"""
#Standard Python Libs
#import mysql.connector
#Standard Python Libs
import mysql.connector
import datetime
import logging
import sys
import time
import pandas as pd
import numpy as np
import os
import csv

#Scarlett Trading Lib
import datalink  #universal logins for environment
import DatabaseQueries as Qry

#IB Library
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 

#Quantopian Library
#import zipline as zl
#Variables
Flag = 0

logging.basicConfig(filename='RSBDataframe' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('RSBDataframe' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

def reply_handler(msg):
    #print(msg.value)
    print("Reply:", msg)
    logger.debug('In Reply Handler')
    Flag = 1
"""
create daily analytics folder
"""
##f = open('dow.csv')
#csv_f = csv.reader(f)
#for row in csv_f:
#    print(row)

data = pd.read_csv('dow.csv')
print(data)
conn = Connection.create(port=4002, clientId=999)
conn.connect()
logger.debug('Connecting to Server')
time.sleep(1)
conn.register(reply_handler,'HistoricalData')   #By registering "HistoricalData" --the Method name only --we can eliminate all the open order garbage
logger.debug('Registered HistoricalData Reply Handler')
    #conn.registerall(reply_handler)
time.sleep(1)

qqq = Contract()
qqq.m_symbol = 'SPY'
#qqq.m_localSymbol = 'ES'+ datalink.monthcode + '8' 
#qqq.ConId = 279555803
qqq.m_secType = 'STK'  
qqq.m_exchange = 'SMART' #NASDAQ defined as ISLAND by IB API  
qqq.m_currency = 'USD'
logger.debug('Requesting historical data') 
conn.reqHistoricalData(1, qqq, '', '1 D', '1 day', 'ASK', 0, 1)
logger.debug('Returned from Reply Handler')
time.sleep(1) #give IB time to send us messages
logger.debug('Disconnecting from Server')
conn.disconnect()
logger.debug('Finished RSB dataframe')