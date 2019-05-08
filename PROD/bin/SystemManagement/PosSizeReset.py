# -*- coding: utf-8 -*-
"""
Created on Sat May 13 07:14:45 2017

@author: Michael
"""

import mysql.connector
import datetime
import logging
import time

logging.basicConfig(filename='pythonlogs\MultiplierReset' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('MultiplierReset' + str(datetime.date.today()) + '.txt')
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

#cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01') 
cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cur = cnx.cursor()

query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 11")
logger.debug('Query is %s', query)
cur.execute(query)
for (RiskParametersValue) in cur:
    riskpercent = RiskParametersValue
logger.debug('Risk Per Position is %s', riskpercent)

query = ("SELECT RiskParametersValue from RiskParameters where idRiskParameters = 13")
logger.debug('Query is %s', query)
cur.execute(query)
for (RiskParametersValue) in cur:
    ProfitPips = RiskParametersValue
logger.debug('ProfitPips is %s', ProfitPips)

query = ("Select Balance from AccountBalance where Date = \"" + str(time.strftime("%m/%d/%Y")) + "\"" )
logger.debug('Query is %s', query)
cur.execute(query)
for (Balance) in cur:
    Balance2 = Balance
logger.debug('Balances is %s', Balance2)

multiplier = ((int(Balance2[0]) * riskpercent[0]) / ProfitPips[0])

query = ("UPDATE RiskParameters SET RiskParametersValue = " +  str(truncate(multiplier,4))  + " where idRiskParameters = 20")
logger.debug('Query is %s', query)
cur.execute(query)
logger.debug('hasPosition query is %s',query)
cnx.commit()       
logger.debug('Finished Position Size Re-calibration')