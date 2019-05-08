# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:16:43 2017

@author: Michael
"""
#import MySQLdb
import mysql.connector
#from ib.ext.Order import Order
            #cnx = mysql.connector.connect(user='mjserpico', password='UrzE8B66',host="scar01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SCAR01')
cnx = mysql.connector.connect(user='Scarlett01', password='scar01lett',host="serpdb01.cqxmc7cib5oh.us-east-1.rds.amazonaws.com", database='SERPDB01')
cur = cnx.cursor()
cur.execute("delete from BB_EURUSD where Open > 0")
cnx.commit()

cur = cnx.cursor()
cur.execute("delete from BB_GBPUSD where Open > 0")
cnx.commit()

cur = cnx.cursor()
cur.execute("delete from BB_USDCHF where Open > 0")
cnx.commit()

cur = cnx.cursor()
cur.execute("delete from BB_USDJPY where Open > 0")
cnx.commit()

cur = cnx.cursor()
cur.execute("ALTER TABLE BB_EURUSD AUTO_INCREMENT = 1")
cnx.commit()

cur = cnx.cursor()
cur.execute("ALTER TABLE BB_GBPUSD AUTO_INCREMENT = 1")
cnx.commit()

cur = cnx.cursor()
cur.execute("ALTER TABLE BB_USDCHF AUTO_INCREMENT = 1")
cnx.commit()

cur = cnx.cursor()
cur.execute("ALTER TABLE BB_USDJPY AUTO_INCREMENT = 1")
cnx.commit()

cur = cnx.cursor()
cur.execute("delete from Orders where idOrder > 0")
cnx.commit()

cur = cnx.cursor()
cur.execute("ALTER TABLE Orders AUTO_INCREMENT = 1")
cnx.commit()

#cur = cnx.cursor()
#cur.execute("INSERT INTO Orders (`idOrder`) VALUES ('1');")
#cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set Count = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set StopLossVal = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set StopQuantity = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set direction = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set Count = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set StopLossVal = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set StopQty = 0 where StopQty > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set direction = "" where direction != "";")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update hasPosition set BB_DailyMovingAvgValue = 0 where Count > 0;")
cnx.commit()

cur = cnx.cursor()
cur.execute("Update RiskParameters set RiskParametersValue = 0 where idRiskParameters = 5;")
cnx.commit()