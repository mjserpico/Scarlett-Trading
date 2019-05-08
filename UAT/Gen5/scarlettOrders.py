#IBAPi default libraries
from ib.ext.Contract import Contract
from ib.ext.EWrapper import EWrapper
from ib.ext.EClientSocket import EClientSocket
from ib.ext.EReader import EReader
from ib.opt import Connection

#Default Python Libraries
from threading import Thread
import queue
import mysql.connector
from datetime import timedelta
import datetime
import logging
import sys
import time
import pandas as pd
import numpy as np
import os
import csv

#Scarlett Trading Libraries
import datalink   #universal login

def make_long_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty[0]
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        order.m_orderType = 'STP'
        lmtPrice = float(truncate((float(gap_close) + (float(ATRentrymultiple[0])*float(ATRVal[0]))),2))
        order.m_lmtPrice  = lmtPrice
        stopPrice = float(truncate((float(gap_close) + (float(ATRentrymultiple[0])*float(ATRVal[0]))),2))
        logger.debug('stop price type is %s', type(stopPrice))
        order.m_auxPrice = stopPrice
        order.m_triggerMethod = 3
        order.m_parentId = parentId
        order.m_account = masteraccount
        order.m_transmit = transmit
        return order    
    
def make_sell_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty[0]
        logger.debug('qty is %s', qty[0])
        logger.debug('qty type is %s', type(qty))
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Sell Order Function')
        logger.debug('Limit Value is %s', limit)
       	# ENTRY   A simple stop order
        order.m_orderType = 'MKT'
        order.m_outsideRth = True
        order.m_sweepToFill = 1
        logger.debug('In Sell Order Function when Limit is 1')
        logger.debug('Action is %s', action)
     #order.m_lmtPrice  = limit - int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005               
        #order.m_triggerMethod = 4
        order.m_parentId = parentId
        order.m_account = masteraccount
        order.m_transmit = transmit
        return order    