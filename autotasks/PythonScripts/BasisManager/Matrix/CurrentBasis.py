# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 17:00:49 2017

@author: Michael
"""

import xlwt
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection 
import mysql.connector
import time
import datetime
import logging
import numpy
import datalink  #universal logins for environment

logging.basicConfig(filename='pythonlogs\SpreadTrader' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('SpreadTrader' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')
#logger.debug('Starting Current Basis Calculation for %s', Product[count])

Product = ["M6A",-1]
Title = "Today's Basis Matrix"
HisTitle = "Average Basis Matrix"
VarTitle = "Deviation from Average"

F="F"
G="G"
H="H"
I="I"
J="J"
K="K"
M="M"
N="N"
Q="Q"
U="U"
V="V"
X="X"
Z="Z"

#z=3

list1=[2.34,4.346,4.234]

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet(Product[0])

cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass ,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
query = ("SELECT Close FROM SERPDB01.Z where Product = 'M6E';")
logger.debug('Query is %s', query)
cur.execute(query)
for (Close) in cur:
    CloseTest = Close
    print(CloseTest)
    print(type(CloseTest))
    list(CloseTest)
    print(type(CloseTest))
#puts results to a list ????
#list(cnx.cursor.fetchall())

"""
CURRENT BASIS FOR TODAY's CLOSE
"""


#ROWs TITLE  (Row, COLUMN)

sheet1.write(0, 0, Title)
sheet1.write(3, 0, F)
sheet1.write(4, 0, G)
sheet1.write(5, 0, H)
sheet1.write(6, 0, I)
sheet1.write(7, 0, J)
sheet1.write(8, 0, K)
sheet1.write(9, 0, M)
sheet1.write(10, 0, N)
sheet1.write(11, 0, Q)
sheet1.write(12, 0, U)
sheet1.write(13, 0, V)
sheet1.write(14, 0, X)
sheet1.write(15, 0, Z)

#COLUMN TITLE

sheet1.write(3, 2, F)
sheet1.write(3, 3, G)
sheet1.write(3, 4, H)
sheet1.write(3, 5, I)
sheet1.write(3, 6, J)
sheet1.write(3, 7, K)
sheet1.write(3, 8, M)
sheet1.write(3, 9, N)
sheet1.write(3, 10, Q)
sheet1.write(3, 11, U)
sheet1.write(3, 12, V)
sheet1.write(3, 13, X)
sheet1.write(3, 14, Z)
#sheet1.write(2, 1, z)

"""
HISTORICAL AVERAGE BASIS FOR  CLOSE

"""

sheet1.write(0, 0, HisTitle)
sheet1.write(3, 0, F)
sheet1.write(4, 0, G)
sheet1.write(5, 0, H)
sheet1.write(6, 0, I)
sheet1.write(7, 0, J)
sheet1.write(8, 0, K)
sheet1.write(9, 0, M)
sheet1.write(10, 0, N)
sheet1.write(11, 0, Q)
sheet1.write(12, 0, U)
sheet1.write(13, 0, V)
sheet1.write(14, 0, X)
sheet1.write(15, 0, Z)

#COLUMN TITLE

sheet1.write(3, 2, F)
sheet1.write(3, 0, G)
sheet1.write(3, 0, H)
sheet1.write(3, 0, I)
sheet1.write(3, 0, J)
sheet1.write(3, 0, K)
sheet1.write(3, 0, M)
sheet1.write(3, 0, N)
sheet1.write(3, 0, Q)
sheet1.write(3, 0, U)
sheet1.write(3, 0, V)
sheet1.write(3, 0, X)
sheet1.write(3, 0, Z)

"""
VARIANCE BASIS FOR  CLOSE.  Anything +/- 2 Standard Deviations will trade to to revert basis to mean

"""

sheet1.write(17, 0, VarTitle)
sheet1.write(18, 0, F)
sheet1.write(19, 0, G)
sheet1.write(20, 0, H)
sheet1.write(21, 0, I)
sheet1.write(22, 0, J)
sheet1.write(23, 0, K)
sheet1.write(24, 0, M)
sheet1.write(25, 0, N)
sheet1.write(26, 0, Q)
sheet1.write(27, 0, U)
sheet1.write(28, 0, V)
sheet1.write(29, 0, X)
sheet1.write(30, 0, Z)

#COLUMN TITLE

sheet1.write(3, 2, F)
sheet1.write(3, 0, G)
sheet1.write(3, 0, H)
sheet1.write(3, 0, I)
sheet1.write(3, 0, J)
sheet1.write(3, 0, K)
sheet1.write(3, 0, M)
sheet1.write(3, 0, N)
sheet1.write(3, 0, Q)
sheet1.write(3, 0, U)
sheet1.write(3, 0, V)
sheet1.write(3, 0, X)
sheet1.write(3, 0, Z)
#Subtract old value
#average = ((average * nbValues) - value) / (nbValues - 1);

#Add Today's Value
#average = average + ((value - average) / nbValues)
#Loops to input values
i=4

for n in list1:
    i = i+1
    sheet1.write(i, 0, n)

book.save('CurrentBasis' + str(datetime.date.today()) + '.xls')