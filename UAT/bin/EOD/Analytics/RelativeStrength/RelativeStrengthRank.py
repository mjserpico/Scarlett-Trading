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
#Quantopian Library
#import zipline as zl 

logging.basicConfig(filename='RelativeStrengthRank' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
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

print("Relative Strength Rank")



# Need to print out top 5 choices and format them for trades

cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
logger.debug('Connected to Database')
cur = cnx.cursor()

query = ("Select CCY, RelativeStrength from hasPosition where RelativeStrength > 2 ORDER BY RelativeStrength ASC LIMIT 50;")
logger.debug('Query is %s', query)
cur.execute(query)
result = cur.fetchall()
final_result = [list(i) for i in result]
print(final_result)
final_result.sort(reverse=True)
print(final_result)

with open('C:/Program Files/Serpico/bin/relativestrengthrank' + str(datetime.date.today()) +'.csv', 'w', newline ='') as f:
    writer = csv.writer(f)
    for val in final_result:
        writer.writerow(val)
        
