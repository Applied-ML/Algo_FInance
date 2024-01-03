import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class resMomentum:
    def __init__(self,look_back_period,holding_period):
        self.look_back_period = look_back_period
        self.holding_period = holding_period
        self.start_date = '2020-01-01'
        self.end_date = datetime.today().strftime('%Y-%m-%d')
        self.risk_free_rate = yf.Ticker('^IRX').info['previousClose']/12/100
        self.index_symbol = '^GSPC'

    def getRankings(self,stock_prices):
        stock_prices.index = pd.to_datetime(stock_prices.index)
        monthly_returns = stock_prices.resample('M').ffill().pct_change()
        market_returns = yf.download('^GSPC',start=self.start_date,end=self.end_date)['Adj Close'].resample('M').ffill().pct_change()
        excess_returns = monthly_returns[stock_prices.columns].subtract(market_returns, axis=0)


        ranking_period_end = monthly_returns.index[-self.holding_period - 1]
        ranking_period_start = ranking_period_end - pd.DateOffset(months=self.look_back_period)
        residual_momentum = excess_returns.loc[ranking_period_start:ranking_period_end].mean()
        ranked_stocks = residual_momentum.sort_values(ascending=False).index[:5]
        holding_returns = monthly_returns.loc[ranking_period_end:, ranked_stocks].mean(axis=1)
        cumulative_returns = (1 + holding_returns).cumprod() - 1

        return ranked_stocks,holding_returns,cumulative_returns




        



