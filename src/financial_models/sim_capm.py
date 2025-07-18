import statsmodels.api as sm
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from src.utils.config import load_config

class Sim:
    def __init__(self,config,df=None):
        self.config = config
        self.df = df
        
    def get_data(self):
        """Loads in stock data from yfinance, but with SP500. I use 'sim_assets from config.yaml to make this easier"""
        tickers = self.config['sim_tickers']
        self.df = yf.download(tickers,start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.df = self.df.dropna()
        return self.df
    
    
    def single_index_model(self,output_dir="images/sim"):
        """Converts sp500 and stock classes to frame for CAPM single index model"""
        if self.df is None:
            self.get_data()
        
        #stock and sp500 tickers for frame
        stock_tickers = self.config['stock_tickers']
        sp500_ticker = self.config['sp500_ticker']
        risk_free_rate = self.config['risk_free_rate']
        
        # to turn the data into seperate frame for market returns and stock returns
        stock_data = self.df[stock_tickers]
        sp500_data = self.df[sp500_ticker]
        
        
        Market_Excess_Returns = sp500_data - self.config['risk_free_rate']
        for stock_ticker in stock_tickers:
            stock_data = self.df[stock_ticker]
            Excess_Returns = stock_data - risk_free_rate
            model = sm.OLS(endog=stock_data,exog=sm.add_constant(Market_Excess_Returns)).fit()
            print(f'Single Index Model for: {stock_ticker}')
            print(f'Excess Returns for Historical Stock Data: {Excess_Returns}')
            print(f'Market Excess Return: {Market_Excess_Returns}')
            print(model.summary())
            
        
            plt.figure(figsize=(10,6))
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




if __name__ == "__main__":
    config = load_config()
    sig_obj = Sim(config)
    sig_obj.get_data()
    sig_obj.single_index_model()

