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
logger.debug('Starting SpreadTrader %s', Product[count])

x=1
y=2
z=3

list1=[2.34,4.346,4.234]

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Basis")

sheet1.write(0, 0, "Display")
sheet1.write(1, 0, "Dominance")
sheet1.write(2, 0, "Test")

sheet1.write(0, 1, x)
sheet1.write(1, 1, y)
sheet1.write(2, 1, z)

sheet1.write(4, 0, "Stimulus Time")
sheet1.write(4, 1, "Reaction Time")

i=4

for n in list1:
    i = i+1
    sheet1.write(i, 0, n)



book.save("Basis.xls")
