from src.config import load_config
import yfinance as yf
import pandas as pd




class LoadData:
    def __init__(self,config):
        self.config = config



    def fetch_data(self):
        """
        fetches data from yfinance given the selected asset class
        """
        self.prices = yf.download(self.config['combined_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.prices = self.prices.reset_index()
        self.prices['Date'] = pd.to_datetime(self.prices['Date'])
        self.prices = self.prices.set_index('Date')
        self.prices = self.prices.dropna()
        self.prices.drop_duplicates(inplace=True)
        return self.prices
    
    def fetch_stock_data(self):
        """
        same as before but only stocks
        """
        self.stocks = yf.download(self.config['stock_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.stocks = self.stocks.dropna()
        self.stocks.drop_duplicates(inplace=True)
        return self.stocks
    
    def fetch_etf_data(self):
        """etf"""
        self.etfs = yf.download(tickers=self.config['etf_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.etfs = self.etfs.dropna()
        self.etfs.drop_duplicates(inplace=True)
        return self.etfs
    
    def fetch_crypto_data(self):
        """
        fetches crypto data from yfinance
        """
        self.crypto = yf.download(tickers=self.config['crypto_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.crypto = self.crypto.dropna()
        self.crypto.drop_duplicates(inplace=True)
        return self.crypto
    
    def fetch_sp500_data(self):
        """Fetches market data from market"""
        self.sp500 = yf.download(tickers="^GSPC",start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.sp500 = self.sp500.dropna()
        self.sp500.drop_duplicates(inplace=True)
        return self.sp500
    
    def fetch_returns(self):
        """
        Fetches returns from combined assets
        """
        self.returns = yf.download(tickers=self.config['combined_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.returns = self.returns.pct_change().dropna()
        return self.returns



if __name__ == "__main__":
    config = load_config()
    data_config = LoadData(config)
