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
        all_prices = yf.download(self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        all_prices = all_prices.dropna()
        all_prices.drop_duplicates(inplace=True)
        all_prices.to_csv("data/raw/all_prices.csv",index="Date")
        return all_prices
    
    def fetch_stock_data(self):
        """
        same as before but only stocks
        """
        stocks = yf.download(self.config['stock_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        stocks = stocks.dropna()
        stocks.drop_duplicates(inplace=True)
        stocks.to_csv("data/raw/stocks.csv",index="Date")
        return stocks
    
    def fetch_etf_data(self):
        """etf"""
        etfs = yf.download(tickers=self.config['etf_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        etfs = etfs.dropna()
        etfs.drop_duplicates(inplace=True)
        etfs.to_csv("data/raw/etfs.csv",index="Date")
        return etfs
    
    def fetch_crypto_data(self):
        """
        fetches crypto data from yfinance
        """
        crypto = yf.download(tickers=self.config['crypto_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        crypto = crypto.dropna()
        crypto.drop_duplicates(inplace=True)
        crypto.to_csv("data/raw/crypto.csv",index="Date")
        return crypto
    
    def fetch_sp500_data(self):
        """Fetches market data from market"""
        sp500 = yf.download(tickers='^GSPC',start=self.config['start_date'],end=self.config['end_date'])['Close']
        sp500 = sp500.dropna()
        sp500.drop_duplicates(inplace=True)
        sp500.to_csv("data/raw/sp500.csv",index="Date")
        return sp500
    
    def fetch_returns(self):
        """
        Fetches returns from combined assets
        """
        returns = yf.download(tickers=self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        returns = returns.pct_change().dropna()
        returns.to_csv("data/processed/returns.csv",index="Date")
        return returns
    



if __name__ == "__main__":
    config = load_config()
    data_config = LoadData(config)
    stock_data = data_config.fetch_stock_data()
    crypto_data = data_config.fetch_crypto_data()
    etf_data = data_config.fetch_etf_data()
    data_combined = data_config.fetch_data()
    returns = data_config.fetch_returns()
    sp500_data = data_config.fetch_sp500_data()
