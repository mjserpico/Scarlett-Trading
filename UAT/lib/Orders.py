# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 22:32:05 2018

@author: Michael
"""

def create_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_localSymbol = CCY1+CCY2 + datalink.monthcode + "8";
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = 'USD'
    return contract

def create_stock_symbol(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = 'USD'
    return contract

#Bracket Order function for Long Trades
def make_long_order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Long Order Function')
        logger.debug('Limit Value is %s', limit)
        if limit == 2:  #Profit Target   # Remove Profit Target for Daily Strat which will close at Market At EOD instead
#            if action == 'SELL':
#                #logger.debug('Profit Pips is %s', ProfitPips)
#                order.m_lmtPrice  = truncate((float(tHigh[0]) + 11.0), 2)
            logger.debug('In Profit Target section of make long order')
#                logger.debug('Profit Target Limit Order Price is is %s', order.m_lmtPrice)
#                #logger.debug('Risk Reward Ratio is %s', RiskRewardRatio)
#                order.m_orderType = 'LMT'
#                order.m_account = masteraccount
#                order.m_transmit = transmit
#            elif action == 'SELL':
#                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
#                order.m_lmtPrice  = float(truncate(float(tLow[0]),4)) - 0.0005
#                print("In Profit Take")
#                print(RiskRewardRatio)
#            order.m_transmit = transmit
        elif limit == 1:
       	# ENTRY   A simple stop order
            order.m_orderType = 'STP'
            order.m_outsideRth = True
            logger.debug('In Long Order Function when Limit is 1')
            logger.debug('Action is %s', action)
            if action == 'BUY':
            	# Rounding is due to FX, we cannot create an order with bad price, and FX book increments at 0.00005 only!
                #order.m_lmtPrice  = limit - int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                logger.debug('In Buy action')
                
                lmtPrice = truncate((float(tHigh[0]) + 1.50),2)
                logger.debug('Buy Stop Limit"Limit" Price or better to buy %s', lmtPrice)
                order.m_lmtPrice  = lmtPrice
                
                stopPrice = truncate((float(tHigh[0]) + 1.00),2)
                logger.debug('Buy Stop Limit"Stop" Price to fire a buy order %s', stopPrice)
                order.m_auxPrice = stopPrice;
               
                order.m_triggerMethod = 4
                order.m_parentId = parentId
                order.m_account = masteraccount
                logger.debug('Buy Upper Limit Price %s', order.m_lmtPrice)
                logger.debug('Buy Upper Limit Type %s', type(order.m_lmtPrice))
                logger.debug('Stop Entry Trigger Price %s ', stopPrice)
                logger.debug('Stop Entry Trigger Type %s ', type(stopPrice))
                logger.debug('Parent ID %s', order.m_parentId)
                logger.debug('Account is %s', order.m_account)
#            elif action == 'SELL':
#                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
#                logger.debug('In Sell action')
#                order.m_lmtPrice  = truncate((float(tHigh[0]) + 0.0002),4)
#                stopPrice = truncate((float(tHigh[0]) + 0.0002),4)
#                order.m_auxPrice = stopPrice;
#                order.m_parentId = parentId
#                order.m_account = masteraccount
#                logger.debug('SEll Entry Price %s', order.m_lmtPrice)
#                logger.debug('Stop loss buy Price %s ', stopPrice)
#                logger.debug('Assigned Stop Price %s ', order.m_auxPrice)
#                logger.debug('Parent ID %s', order.m_parentId)
#                logger.debug('Account is %s', order.m_account)
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit

        return order    
    
    
 def make__short__order(action, qty, limit = None, profit_take=None, training_stop_percent=None, transmit=True, parentId=None):
        order = Order()
        order.m_action = action
        order.m_totalQuantity = qty
        order.m_tif = "GTC"  #All orders are GTC by default with NO TIME LIMIT to auto cancel
        logger.debug('In Short Order Function')
        logger.debug('Limit Value is %s', limit)
        if limit == 2: # Profit Target
            logger.debug('In Limit is 2 subfunction')
#            if action == 'BUY':
#                logger.debug('In Profit Order Subfunction')
#                #logger.debug('Profit Pips is: %s', ProfitPips)
#                profitlimitprice = truncate((float(tLow[0]) - 11.0), 2)
#                #logger.debug('Risk Reward Ratio is: %s', RiskRewardRatio)
#                logger.debug('Limit Price: %s', profitlimitprice)
#                order.m_lmtPrice  = profitlimitprice
#                order.m_orderType = 'LMT'
#                order.m_account = masteraccount
#                order.m_transmit = transmit
#            order.m_transmit = transmit
#            logger.debug('transmitted order')
        elif limit == 1:
            logger.debug('In Limit is 1 subfunction')
       	# ENTRY   A simple stop order
            order.m_orderType = 'STP'
            order.m_outsideRth = True
#            if action == 'BUY':
#                logger.debug('In Buy subfunction')
#                #logger.debug('Profit Pips is: %s', ProfitPips)
#                #logger.debug('Risk Reward Ratio is: %s', RiskRewardRatio)
#                order.m_lmtPrice  = (float(tLow[0]) - 0.0002)
#                stopPrice = truncate((float(tLow[0]) - 0.0002),4)   #Stop Order -- Entry Price
#                logger.debug('STP Price: %s', stopPrice)
#                
#                order.m_auxPrice = stopPrice
#                #order.m_parentId = parentId
#                order.m_account = masteraccount
#                order.m_transmit = transmit

            if action == 'SELL':
                logger.debug('In Sell subfunction')
                #order.m_lmtPrice  = limit + int(np.around((limit*profit_take_percent)/100.0, 5)/0.00005)*0.00005
                
                lmtPrice = truncate((float(tLow[0]) - 1.50),2)
                logger.debug('Buy Stop Limit"Limit" Price or better to buy %s', lmtPrice)
                order.m_lmtPrice  = lmtPrice
                
                stopPrice = truncate((float(tLow[0]) - 1.00),2)
                logger.debug('Stop Price: %s', stopPrice)
                order.m_auxPrice = stopPrice;
                
                order.m_triggerMethod = 4
                order.m_parentId = parentId
                order.m_account = masteraccount
        # Important that we only send the order when all children are formed.
        order.m_transmit = transmit
        logger.debug('transmitted order')
        return order    