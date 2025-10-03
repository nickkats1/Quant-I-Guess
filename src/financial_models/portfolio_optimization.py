import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from src.config import load_config
import numpy as np
from pypfopt import expected_returns,EfficientFrontier,risk_models
from pypfopt.discrete_allocation import DiscreteAllocation,get_latest_prices
from src.financial_models.VaR import Var

class EfficientDiversification:
    def __init__(self,config):
        self.config = config


        
    def fetch_data(self) -> pd.DataFrame:
        """Loads in data from yfinance using config.yaml"""
        try:
            self.all_prices = yf.download(tickers=self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
            self.all_prices = self.all_prices.dropna()
            self.all_prices.drop_duplicates(inplace=True)
            return self.all_prices
        except Exception as e:
            raise e 
        
    
    def get_portfolio_returns(self) -> pd.DataFrame:
        """ returns from portfolio from yfinance download """
        try:
            self.returns = self.all_prices.pct_change().dropna()
            return self.returns
        except Exception as e:
            raise e
        

    
    
    def portfolio_metrics(self):
        """
        args:
            (mu) -> Expected Returns (using pyportfolio)
            (S) -> Risk(Volatility);
            (Ef) -> Efficient Frontier;
        """


        self.mu = expected_returns.mean_historical_return(self.all_prices)
        self.S = risk_models.sample_cov(self.all_prices)
        self.ef = EfficientFrontier(self.mu,self.S)
            

        self.weights = self.ef.max_sharpe()
        self.weights = self.ef.clean_weights()


            
        expected_annual_return, annual_volatility, sharpe_ratio = self.ef.portfolio_performance(verbose=True)
        self.performance = {
            "Expected Annual Return":expected_annual_return,
            "Annual Volatility":annual_volatility,
            "Sharpe Ratio":sharpe_ratio
        }
        return self.weights,self.performance



if __name__ == "__main__":
    config = load_config()
    ef_obj = EfficientDiversification(config)


