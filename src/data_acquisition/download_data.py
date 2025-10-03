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
        self.all_prices = yf.download(self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.all_prices = self.all_prices.dropna()
        self.all_prices.drop_duplicates(inplace=True)
        self.all_prices.to_csv("data/raw/all_prices.csv",index="Date")
        return self.all_prices
    
    def fetch_stock_data(self):
        """
        same as before but only stocks
        """
        self.stocks = yf.download(self.config['stock_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.stocks = self.stocks.dropna()
        self.stocks.drop_duplicates(inplace=True)
        self.stocks.to_csv("data/raw/stocks.csv",index="Date")
        return self.stocks
    
    def fetch_etf_data(self):
        """etf"""
        self.etfs = yf.download(tickers=self.config['etf_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.etfs = self.etfs.dropna()
        self.etfs.drop_duplicates(inplace=True)
        self.etfs.to_csv("data/raw/etfs.csv",index="Date")
        return self.etfs
    
    def fetch_crypto_data(self):
        """
        fetches crypto data from yfinance
        """
        self.crypto = yf.download(tickers=self.config['crypto_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.crypto = self.crypto.dropna()
        self.crypto.drop_duplicates(inplace=True)
        self.crypto.to_csv("data/raw/crypto.csv",index="Date")
        return self.crypto
    
    def fetch_sp500_data(self):
        """Fetches market data from market"""
        self.sp500 = yf.download(tickers='^GSPC',start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.sp500 = self.sp500.dropna()
        self.sp500.drop_duplicates(inplace=True)
        self.sp500.to_csv("data/raw/sp500.csv",index="Date")
        return self.sp500
    
    def fetch_returns(self):
        """
        Fetches returns from combined assets
        """
        self.returns = yf.download(tickers=self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.returns = self.returns.pct_change().dropna()
        self.returns.to_csv("data/processed/returns.csv",index="Date")
        return self.returns
    



if __name__ == "__main__":
    config = load_config()
    data_config = LoadData(config)
    stock_data = data_config.fetch_stock_data()
    crypto_data = data_config.fetch_crypto_data()
    etf_data = data_config.fetch_etf_data()
    data_combined = data_config.fetch_data()
    returns = data_config.fetch_returns()
    sp500_data = data_config.fetch_sp500_data()