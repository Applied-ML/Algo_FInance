import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
class getData:

    
    def __init__(self):
        self.start_date = '2020-01-01'
        self.end_date = datetime.today().strftime('%Y-%m-%d')
        
       
        
    def dataLoad(self,tickerList,interval):
        df = pd.DataFrame()
        for ticker in tickerList:
            print(ticker)
            temp = yf.download(ticker,start = self.start_date,end = self.end_date,interval=interval)['Adj Close']
            temp.name = ticker
            df = pd.concat([df,temp],axis=1)
        return df 
