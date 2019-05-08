# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:33:05 2018

@author: Michael
"""

def error_handler(msg):
    """Handles the capturing of error messages"""
    print(msg)
    logger.debug('Error Reply: %s', msg)
    

#TWS Async Reply handler
def reply_handler(msg):
    #test = msg.value
    print(msg)
    logger.debug('Reply: %s', msg)
    

def reply_handler_price(msg):
    #print(msg.value)
    logger.debug('In Price Reply Handler')
    print("Reply:", msg)
    global o
    global h
    global l
    global c
    o = msg.open
    logger.debug('open now %s', o)
    logger.debug('high now %s', h)
    logger.debug('low now %s', l)
    logger.debug('close now %s', c)
    #test5 - msg.volume
    if float(o) != -1:
        global Flag
        Flag = 1
        h = msg.high
        l = msg.low
        c = msg.close
        logger.debug('Flag set to 1')