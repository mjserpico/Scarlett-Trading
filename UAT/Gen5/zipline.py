from zipline import pipeline
from zipline.pipeline.factors import *
import math as math
import numpy as np
import quandl
from zipline.api import (
    attach_pipeline,
    date_rules,
    order_target_percent,
    pipeline_output,
    record,
    schedule_function,
)
#https://docs.quandl.com/docs/parameters-2#section-times-series-parameters
# See options for parameters
#from quantopian.research import run_pipeline

quandl.ApiConfig.api_key = "yoTEFmM_iXvFy7sMyBDw"
data = quandl.get('NASDAQOMX/XQC', start_date='2019-05-08', end_date='2019-05-08')
print(data)

def initialize(context):
    pipe = Pipeline()
    attach_pipeline(pipe, 'pipeline_tutorial')
    _50ma = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=50)
    _200ma = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=200)
    vwap_10 = VWAP(window_length=10)
    my_volatility_from_daily = Volatility_Daily_Annual()
    pipe.add(_50ma, '_50ma')
    pipe.add(_200ma, '_200ma')
    pipe.add(_50ma/_200ma, 'ma_ratio')
    pipe.add(vwap_10, 'vwap_10')
    pipe.add(my_volatility_from_daily, 'my_volatility_from_daily')
    pipe.set_screen(_50ma/_200ma > 1.0)
    

def before_trading_start(context, data):
    output = pipeline_output('pipeline_tutorial')
    context.my_universe = output.sort('ma_ratio', ascending=False).iloc[:100]
    #update_universe(context.my_universe.index)


def handle_data(context, data):
    #log.info("\n" + str(context.my_universe.head()))
    #log.info("\n" + str(len(context.my_universe)))
    pass


class Volatility_Daily_Annual(CustomFactor): 
    
    inputs = [USEquityPricing.close]  
    window_length = 20  
    
    def compute(self, today, assets, out, close):  
        
        # [0:-1] is needed to remove last close since diff is one element shorter 
        daily_returns = np.diff(close, axis = 0) / close[0:-1] 
        out[:] = daily_returns.std(axis = 0) * math.sqrt(252)
        
def volatility_example():
    
    my_volatility_from_daily = Volatility_Daily_Annual()
    
    return Pipeline(
        columns = {
            'annual volatility from daily': my_volatility_from_daily,
            },
        )
#results = run_pipeline(volatility_example(), '2016-03-01', '2016-03-01')
#results.sort('annual volatility from daily')