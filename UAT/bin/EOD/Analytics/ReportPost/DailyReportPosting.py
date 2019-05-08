# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 23:18:34 2018

@author: Michael
"""

from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import datetime
import logging
import sys
import time
import pandas as pd
import numpy as np
import mysql.connector
import datalink  #universal logins for environment
import locale
locale.setlocale( locale.LC_ALL, '' )
'English_United States.1252'
#locale.currency( 188518982.18 )
'$188518982.18'
#locale.currency( 188518982.18, grouping=True )
'$188,518,982.18'

logging.basicConfig(filename='DailyReportPost' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('DailyReportPost' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

url = r"http://www.scarletttradingreports.com"
table = 'Reports'
page = urlopen(url)
soup = BeautifulSoup(page.read(),"lxml")
#print(soup.prettify())

#New values
global todaydate
global todayAccountBalance
todaydate = 0
todayAccountBalance = 1
todayDailyReturns = 0
todayYTDReturns = 0
todaySharpeRatio = 0
todayMaxDrawdown = 0
todayBenchmarkClose = 0
RiskFreeRate = 2.75
Acct = 30000   #Jan 1 balance
SPY =  249.92   #Jan 1 Price

#f = open('index.html')
cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
logger.debug('Connected to Database')

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def Calc():
    
#    <td style=\"width: 92px;\">" + str(todayAccountBalance) + "</td>
#    <td style="width: 92px;"></td>
#    <td style="width: 92px;"></td>
#    <td style="width: 92px;">1</td>
#    <td style="width: 10px;">1</td>
#    <td style="width: 92px;"><span style="background-color: #ffcc00;">&nbsp;</span></td>
#    <td style="width: 92px;"><span style="background-color: #ffcc00;">&nbsp;</span></td>
#    <td style="width: 92px;"><span style="background-color: #ffcc00;">&nbsp;</span></td>
#    <td style="width: 92px;"><span style="background-color: #ffcc00;">&nbsp;</span></td>
#    <td style="width: 300px;"><span style="background-color: #ffcc00;">&nbsp;</span></td>
    original_tag = soup.tbody
    print(original_tag)
    tag = soup.new_tag("tr")
    #original_tag.append(tag)
    print(original_tag)
    print(type(original_tag))
    
#Today's Date
    todaydate = datetime.date.today()
    logger.debug('Date is %s', todaydate)
    rowDate = str(todaydate)
    tag2 = soup.new_tag("td")
    tag2.string = rowDate
    tag.append(tag2)
    
#Today's Account Balance
    query = ("Select Balance from AccountBalance t inner join (SELECT MAX(date) as max_date FROM AccountBalance) a on a.max_date = t.date")
    cur.execute(query)
    for (Balance) in cur:
        todayAccountBalance = Balance 
        logger.debug('Balance is %s', todayAccountBalance)
        print(type(todayAccountBalance[0]))
        bal2= float(todayAccountBalance[0])
        bal3 = locale.currency(bal2, grouping=True)
        print(bal3)
    tag3 = soup.new_tag("td")
    tag3['style'] = 'color: #0000ff'
    tag3.string = bal3
    tag.append(tag3)
    original_tag.append(tag)
    
#Today's DailyReturns    
    query = ("Select Balance from AccountBalance t inner join (SELECT (MAX(ID)-1) as max_date FROM AccountBalance) a on a.max_date = t.ID")
    logger.debug('Query is %s', query)
    cur.execute(query)
    
    for (Balance) in cur:
        yestBalance = Balance 
        logger.debug('YestBalance is %s', yestBalance)
    
    todayDailyReturns = (((float(todayAccountBalance[0]) - float(yestBalance[0])) / float(yestBalance[0]))) * 100    
    DailyReturn2 = truncate(todayDailyReturns,2)
    
    tag4 = soup.new_tag("td")
    tag4.string = str(DailyReturn2)
    tag.append(tag4)
    original_tag.append(tag)

#YTD Balance
    todayYTDReturns = (((float(todayAccountBalance[0]) - float(Acct)) / float(Acct))) * 100
    YTDReturn2= truncate(todayYTDReturns,2)   
    tag5 = soup.new_tag("td")
    tag5.string = str(YTDReturn2)
    tag.append(tag5)
    original_tag.append(tag)

#Sharpe Ratio   
    tag6 = soup.new_tag("td")
    tag6.string = "TBD"
    tag.append(tag6)
    original_tag.append(tag)


#Max Drawdown    
    tag7 = soup.new_tag("td")
    tag7.string = "TBD"
    tag.append(tag7)
    original_tag.append(tag)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Benchmark Close   
    query = ("Select Close from SPY where Id = (Select max(Id) from SPY)")
    cur.execute(query)
    for (Close) in cur:
        benchmarkVal = Close 
        logger.debug('todayBalance is %s', benchmarkVal)
    tag8 = soup.new_tag("td")
    tag8['style'] = 'color: #ff9900'
    tag8['width'] = '92px'
    tag8.string = benchmarkVal[0]
    tag.append(tag8)
    original_tag.append(tag)

#Daily Returns
    query = ("Select Close from SPY where Id = (Select max(Id)-1 from SPY);")
    cur.execute(query)
    for (Close) in cur:
        yestBenchmark = Close 
        logger.debug('YestBalance is %s', yestBenchmark)
    yestbenchmarkReturns = (((float(benchmarkVal[0]) - float(yestBenchmark[0])) / float(yestBenchmark[0]))) * 100    
    print(yestbenchmarkReturns)
    benchmarkReturn2 = truncate(yestbenchmarkReturns,2)
    
    tag9 = soup.new_tag("td")
    tag9.string = benchmarkReturn2[0]
    tag.append(tag9)
    original_tag.append(tag)

#YTD returns
    todaybenchYTDReturns = (((float(benchmarkVal[0]) - float(SPY)) / float(SPY))) * 100
    YTDbenchReturn2= truncate(todaybenchYTDReturns,2)      
    tag10 = soup.new_tag("td")
    tag10.string = YTDbenchReturn2
    tag.append(tag10)
    original_tag.append(tag)

#Sharpe Ratio  
    tag11 = soup.new_tag("td")
    tag11.string = "TBD"
    tag.append(tag11)
    original_tag.append(tag)

#MaxDrawdown 
    tag12 = soup.new_tag("td")
    tag12.string = "TBD"
    tag.append(tag12)
    original_tag.append(tag)

#Trades 
    tag13 = soup.new_tag("td")
    tag13.string = "TBD"
    tag.append(tag13)
    original_tag.append(tag)   
    print(original_tag)

    


def writetoServer():
##drop new index.html in folder
   with open('C:\Domains\scarletttradingreports.com\wwwroot\index.html', 'w') as f:
    f.write(str(soup))
    f.close()

logger.debug('Run Calc')
Calc()
logger.debug('done Calc')
writetoServer()
