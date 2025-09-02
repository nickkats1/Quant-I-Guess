import statsmodels.api as sm
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from src.config import load_config


class Sim:
    def __init__(self,config,data=None):
        self.config = config
        self.data = data

    def fetch_data(self):
        """
        fetches data from yfinance consiting of only
        S&P500 and selected stock tickers from config
        """
        self.data = yf.download(tickers=self.config['sim_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.data = self.data.dropna()
        return self.data
    
    def single_index_model(self,output_dir="images/sim"):

        if self.data is None:
            self.data = self.fetch_data()

        stock_tickers = self.config['stock_tickers']
        sp500_ticker = self.config['sp500_ticker']
        risk_free_rate = self.config['risk_free_rate']

        # to turn the data into seperate frame for market returns and stock returns
        stock_data = self.data[stock_tickers]
        sp500_data = self.data[sp500_ticker]


        Market_Excess_Returns = sp500_data - self.config['risk_free_rate']

        for stock_ticker in stock_tickers:
            stock_data = self.data[stock_ticker]
            Excess_Returns = stock_data - risk_free_rate
            model = sm.OLS(endog=stock_data,exog=sm.add_constant(Market_Excess_Returns)).fit()
            print(f'Single Index Model for: {stock_ticker}')
            print(f'Excess Returns for Historical Stock Data: {Excess_Returns}')
            print(f'Market Excess Return: {Market_Excess_Returns}')
            print(model.summary())

            plt.figure(figsize=(12,6))
            sns.scatterplot(x=Market_Excess_Returns, y=Excess_Returns, label=stock_ticker)
            sns.lineplot(x=Market_Excess_Returns, y=model.fittedvalues, color='red', label='Security Market Line')
            plt.title(f'Single Index Model for {stock_ticker}')
            plt.xlabel('Market Excess Return')
            plt.ylabel(f'{stock_ticker} Excess Return')
            plt.legend()
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, f"single_index_model_{stock_ticker}.png"))
            plt.show()
            plt.close()