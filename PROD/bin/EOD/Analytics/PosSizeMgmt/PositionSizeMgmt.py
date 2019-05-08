import mysql.connector 
from ib.opt import Connection, message
import ib
import time
import logging
import datetime
import datalink  #universal logins for environment
import csv

Flag = 0
test = 0

logging.basicConfig(filename='PositionSize' + str(datetime.date.today()) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('PositionSize' + str(datetime.date.today()) + '.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('****************************************************')

def reply_handler(msg):
    global test
    test = msg.value
    logger.debug('Message Value is %s', msg)
    global Flag
    Flag = 1
    print(Flag)
    logger.debug('Flag set to 1')

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

while Flag == 0:
    logger.debug('Connecting to Database')
    conn = Connection.create(port=4002, clientId=888)
    conn.register(reply_handler, 'AccountSummary')
    conn.connect()
    logger.debug('Connected to Database')
    conn.reqAccountSummary(1,'All','NetLiquidation')  
    logger.debug('Requested Account Summary')
    time.sleep(1) #give IB time to send us messages

cnx = mysql.connector.connect(user=datalink.DB_User, password=datalink.DB_Pass,host=datalink.DB_Host, database=datalink.DB_Path)
cur = cnx.cursor()
query = ("Select RiskParametersValue from RiskParameters where RiskParametersName = 'RiskPerPosition';")
logger.debug('Query is %s', query)
cur.execute(query)
for (RiskParametersValue) in cur:
    RiskPerPosition = RiskParametersValue
    logger.debug('RiskPerPosition is %s', RiskPerPosition)

logger.debug('Cash Value is %s', type(test[0]))
logger.debug('RiskPErPosition is %s', type(RiskPerPosition[0]))
TotalDollarValue  = float(test) * RiskPerPosition[0]
logger.debug('TotalDollarValue is %s', TotalDollarValue)

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

#Take stop loss range / totaldollarvlue    

    query = ("Select StopLossVal from hasPosition where CCY = \'" + Ticker[0] + "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    for (StopLossVal) in cur:
        StopVal = StopLossVal
        logger.debug('StopLoss Vale is %s', StopVal)
      
    Shares = float(TotalDollarValue) / float(StopVal[0])
    Shares2 = abs(int(round(Shares)))
    logger.debug('Shares is %s', Shares2)  
    
    query = ("UPDATE hasPosition SET StopQty = \'" + str(Shares2) + "\' where CCY =\'" + Ticker[0] + "\';")
    logger.debug('Query is %s', query)
    cur.execute(query)
    cnx.commit()
            
conn.disconnect()
logger.debug('disconnected from IBController')