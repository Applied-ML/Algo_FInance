Residual Momentum among other financial (long-term) indicators will be used for specific ticker performance relative to general market behaviour.
Fama-French factors aren't utilized within residual momentum strategy in this case, I assume results wont be as different, can be added in the future.
Universe of stocks contains 1000+ tickers of US-Based companies.
Top 1%-2% is used for a given month of trading.
Within that selected portion, XGBoost (optimized via PSO or SA) is used predict if the 'Close' Price for the stock the following day will be higher or lower, then to long/short respectively.
TCNs are used to futher semient the daily prediction from XGBoost by performing live minutely forecasting of the selected stocks for that day and checking if executing a position is appropriate.
More markers need to be added..
