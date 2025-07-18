from pypfopt import risk_models,expected_returns,EfficientFrontier
from src.utils.config import load_config
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from src.utils.logger import logger



class EfficientDiversification:
    def __init__(self,config):
        self.config = config
        self.all_prices = None #all assets combined
        self.mu = None # expected returns using pyportfolio
        self.S = None # Risk(Vol) through pyportfolio
        self.ef = None # Efficient Frontier using pyportfolio
        self.weights = None # weights
        self.perf = None #portfolio Performance
        
    def load_data(self):
        """Loads in data from yfinance using config.yaml"""
        self.all_prices = yf.download(tickers=self.config['all_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.all_prices = self.all_prices.dropna()
        return self.all_prices   
    
    def eval_returns(self):
        """
        The pct change for each asset(returns). This is not the same
        as 'Expected Returns'
        """
        if self.all_prices is None:
            self.load_data()
            
     
        returns = self.all_prices.pct_change().dropna()
        logger.info(f'Returns from full portfolio: {returns.head()}')
        print(f'Returns: {returns}')
        return returns
    
    
    def portfolio_metrics(self):
        """
        (mu) -> Expected Returns (using pyportfolio)
        (S) -> Risk(Volatility);
        (Ef) -> Efficient Frontier;
        Most people(probably everyone honestly) wants to minimize risk in some way
        and Maximize some gain(this is everything in life)
        So, you want to maximize utility st. Budget Contraint; or
        Maximize returns given the risk st. the Weights......
        Or, Maximize Efficiency st limitations of hardware, ect.
        """
        if self.all_prices is None:
            self.load_data()
            if self.all_prices is None:
                return
            
        self.mu = expected_returns.mean_historical_return(self.all_prices)
        self.S = risk_models.sample_cov(self.all_prices)
        self.ef = EfficientFrontier(self.mu,self.S)
        logger.info("Portfolio Metrics(Expected Returns, S) has been calculated")
        
    def optimizing_portfolio(self,target_risk=None,target_return=None):
        """Optimizing Returns based on Efficient Frontier and Weights(there are four)"""
        if self.mu is None or self.S is None:
            self.portfolio_metrics()
            
        self.ef = EfficientFrontier(self.mu,self.S)
        
        if target_risk is not None:
            self.weights = self.ef.efficient_risk(target_risk)
            
        elif target_return is not None:
            self.weights = self.ef.efficient_return(target_return)
        
        else:
            self.weights = self.ef.max_sharpe() # default, this is what will be used more than likely.
            
        
        self.weights = self.ef.clean_weights()
        
        expected_annual_return, annual_volatility, sharpe_ratio = self.ef.portfolio_performance(verbose=False)
        self.perf = {
            "Expected Annual Return":expected_annual_return,
            "Annual Volatility":annual_volatility,
            "Sharpe Ratio":sharpe_ratio
        }
        logger.info("Expected Annual Returns, Annual Volatiliy,and Sharpe Ratio")
        return self.weights,self.perf


if __name__ == "__main__":
    config = load_config()
    ef_obj = EfficientDiversification(config)
    ef_obj.load_data()
