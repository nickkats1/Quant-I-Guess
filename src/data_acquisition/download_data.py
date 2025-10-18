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
        all_prices = yf.download(self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        all_prices = all_prices.dropna()
        all_prices.drop_duplicates(inplace=True)
        return all_prices
    
    def fetch_stock_data(self):
        """
        fetches stock data from yfinance api
        """
        stocks = yf.download(self.config['stock_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        stocks = stocks.dropna()
        stocks.drop_duplicates(inplace=True)
        return stocks
    
    def fetch_etf_data(self):
        """ fetches etf data from yfinance api"""
        etf = yf.download(tickers=self.config['etf_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        etf = etf.dropna()
        etf.drop_duplicates(inplace=True)
        return etf
    
    def fetch_crypto_data(self):
        """
        fetches crypto data from yfinance api
        """
        crypto = yf.download(tickers=self.config['crypto_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        crypto = crypto.dropna()
        crypto.drop_duplicates(inplace=True)
        return crypto
    
    def fetch_sp500_data(self):
        """Fetches SP&500 data from yfinance api """
        sp500 = yf.download(tickers='^GSPC',start=self.config['start_date'],end=self.config['end_date'])['Close']
        sp500 = sp500.dropna()
        sp500.drop_duplicates(inplace=True)
        return sp500
    
    def fetch_returns(self):
        """
        returns from 'all_prices'
        """
        returns = yf.download(tickers=self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        returns.to_csv(self.config['returns_path'])
        return returns



