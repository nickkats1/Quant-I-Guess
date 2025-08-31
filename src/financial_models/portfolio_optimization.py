import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from src.config import load_config
import numpy as np

class EfficientDiversification:
    def __init__(self,config):
        self.config = config
        self.all_prices = None #all assets combined
        self.mu = None # expected returns using pyportfolio
        self.S = None # Risk(Vol) through pyportfolio
        self.ef = None # Efficient Frontier using pyportfolio
        self.weights = None # weights
        self.performance = None # portfolio performance
        
    def load_data(self):
        """Loads in data from yfinance using config.yaml"""
        self.all_prices = yf.download(tickers=self.config['combined_assets'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.all_prices = self.all_prices.dropna()
        return self.all_prices   
    
    def eval_returns(self):
        """
        The pct change for each asset(returns). This is not the same
        as 'Expected Returns'
        """

        returns = self.all_prices.pct_change().dropna()
        print(f'Returns: {returns}')
        return returns
    
    
    def portfolio_metrics(self):
        """
        args:
            (mu) -> Expected Returns (using pyportfolio)
            (S) -> Risk(Volatility);
            (Ef) -> Efficient Frontier;
        """

        if self.all_prices is None:
            self.load_data()
            if self.all_prices is None:
                return
            
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



