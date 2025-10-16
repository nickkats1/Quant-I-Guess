from src.config import load_config
import yfinance as yf
import pandas as pd




class LoadData:
    def __init__(self,config):
        self.config = config



    def fetch_data(self):
        """
        fetches 'combined assets' from yfinance api using ticker from .yaml
        """
        self.all_prices = yf.download(self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.all_prices = self.all_prices.dropna()
        self.all_prices.drop_duplicates(inplace=True)
        return self.all_prices
    
    def fetch_stock_data(self):
        """
        fetches stock data from yfinance api
        """
        self.stocks = yf.download(self.config['stock_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.stocks = self.stocks.dropna()
        self.stocks.drop_duplicates(inplace=True)
        return self.stocks
    
    def fetch_etf_data(self):
        """ fetches etf data from yfinance api"""
        self.etfs = yf.download(tickers=self.config['etf_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.etfs = self.etfs.dropna()
        self.etfs.drop_duplicates(inplace=True)
        return self.etfs
    
    def fetch_crypto_data(self):
        """
        fetches crypto data from yfinance api
        """
        self.crypto = yf.download(tickers=self.config['crypto_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.crypto = self.crypto.dropna()
        self.crypto.drop_duplicates(inplace=True)
        return self.crypto
    
    def fetch_sp500_data(self):
        """Fetches SP&500 data from yfinance api """
        self.sp500 = yf.download(tickers='^GSPC',start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.sp500 = self.sp500.dropna()
        self.sp500.drop_duplicates(inplace=True)
        return self.sp500
    
    def fetch_returns(self):
        """
        returns from 'all_prices'
        """
        self.returns = yf.download(tickers=self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.returns = self.returns.pct_change().dropna()
        return self.returns
    


