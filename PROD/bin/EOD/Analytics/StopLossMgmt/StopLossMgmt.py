# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 22:53:28 2018

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
import csv
import math

#Scarlett Trading Lib
import datalink  #universal logins for environment
import DatabaseQueries as Qry

#IB Library
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 

#Quantopian Library
#import zipline as zl

logging.basicConfig(filename='StopLossCalculation' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('StopLossCalculation' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

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
            query = ("SELECT max(ID) from " + Ticker[0])
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID1 = ID
                logger.debug('ID1 is %s', ID1)
                
            query = ("SELECT (max(ID)-5) from " + Ticker[0])
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (ID) in cur:
                ID3 = ID
                logger.debug('ID3 is %s', ID3)
                
                
            query = ("SELECT ATRValue from hasPosition where CCY =\'" + Ticker[0] +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (TrueRange) in cur:
                ATR = TrueRange   #Final Moving Average Value
                logger.debug('ATR is %s', ATR)
                logger.debug('ATR is %s', type(ATR[0]))

##StopLoss Range based on ATR value and multiple of it                
            query = ("Select RiskParametersValue from RiskParameters where RiskParametersName = 'StopATRmultiple';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (RiskParametersValue) in cur:
                ATRmultiple = RiskParametersValue   #Final Moving Average Value
                logger.debug('ATRmultiple is %s', ATRmultiple)
                logger.debug('ATRmultiple is %s', type(ATRmultiple[0]))
                
            
            StopLoss = float(ATR[0]) * float(ATRmultiple[0])
            StopLoss2 = truncate(StopLoss,2)
            query = ("UPDATE hasPosition SET StopLossVal = " + str(StopLoss2) + " where CCY =\'" + Ticker[0] +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()
            
##Profit Target range based on ATR value and multiple of it
            query = ("Select RiskParametersValue from RiskParameters where RiskParametersName = 'ProfitATRmultiple';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            for (RiskParametersValue) in cur:
                ProfitATRmultiple = RiskParametersValue   #Final Moving Average Value
                logger.debug('ATRmultiple is %s', ProfitATRmultiple)
                logger.debug('ATRmultiple is %s', type(ProfitATRmultiple[0]))
                
            
            Profit = float(ATR[0]) * float(ProfitATRmultiple[0])
            Profit2 = truncate(Profit,2)
            query = ("UPDATE hasPosition SET ProfitTargetVal = " + str(Profit2) + " where CCY =\'" + Ticker[0] +"\';")
            logger.debug('Query is %s', query)
            cur.execute(query)
            cnx.commit()           