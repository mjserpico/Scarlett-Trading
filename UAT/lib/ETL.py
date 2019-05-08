# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 21:16:21 2018

@author: Michael
"""

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def dateconversion():
##Convert Date to proper format and relative reference
    if dayofweek == 0:  #if Today is Monday
        yesterday = today - datetime.timedelta(days=3)  #Get Friday                   
        month = (str(0) + str(yesterday.month))
        day = (str(0)+ str(yesterday.day))
        yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
        logger.debug('Previous Trading day was %s', yesterday2)  
    else:
        yesterday = today - datetime.timedelta(days=1) #Take 1 Day back                    
        month = (str(0) + str(yesterday.month))
        day = (str(0)+ str(yesterday.day))
        yesterday2 = (month[-2:] +"/"+ day[-2:] +"/"+str(yesterday.year))
        logger.debug('Previous trading day was %s', yesterday2)