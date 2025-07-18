import yfinance as yf
from src.utils.config import load_config
import pandas as pd
from src.utils.logger import logger


def load_data(config):
    """Loads in Assets from yfinance from config.yaml and seperate dataframe for each asset class"""
    try:
        all_data = yf.download(tickers=config['all_tickers'],start=config['start_date'],end=config['end_date'])['Close']
        stocks = yf.download(tickers=config['stock_tickers'],start=config['start_date'],end=config['end_date'])['Close']
        etfs = yf.download(tickers=config['etf_tickers'],start=config['start_date'],end=config['end_date'])['Close']
        crypto = yf.download(tickers=config['crypto_tickers'],start=config['start_date'],end=config['end_date'])['Close']
        sp500 = yf.download(tickers=config['sp500_ticker'],start=config['start_date'],end=config['end_date'])['Close']
        sim_data = yf.download(tickers=config['sim_tickers'],start=config['start_date'],end=config['end_date'])['Close']
        all_data = all_data.dropna()
        stocks = stocks.dropna()
        etfs = etfs.dropna()
        crypto = crypto.dropna()
        sim_data = sim_data.dropna()
        return all_data,stocks,etfs,crypto,sp500,sim_data
    except Exception as e:
        raise e

if __name__ == "__main__":
    try:
        config = load_config()


        all_data, stocks, etfs, crypto, sp500, sim_data = load_data(config)

        all_data.to_csv("data/raw/portfolio.csv") 
        stocks.to_csv("data/raw/stocks.csv")
        etfs.to_csv("data/raw/etf.csv")
        crypto.to_csv("data/raw/crypto.csv")
        sp500.to_csv("data/raw/sp500.csv")
        sim_data.to_csv("data/raw/sim_data.csv")
        logger.info("Data successfully loaded and saved to data/")

    except Exception as e:
        logger.error(f"An error occurred in the main execution block: {e}") 