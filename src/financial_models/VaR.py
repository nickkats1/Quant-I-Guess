import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import load_config
import yfinance as yf
import numpy as np
from src.logger import logger


class Var:
    def __init__(self,config):
        self.config = config
        self.stock_data = None
        self.returns = None
        self.var = None
        self.cvar = None

        
    def load_data(self):
        """
        Loads in data from yfinance
        """
        self.stock_data = yf.download(self.config['stock_tickers'],start=self.config['start_date'],end=self.config['end_date'])['Close']
        self.stock_data = self.stock_data.dropna()
        return self.stock_data
    
    def get_returns(self):
        if self.stock_data is None:
            self.load_data()
            
        self.returns = self.stock_data.pct_change().dropna()
        return self.returns
    
    def get_var(self,ci=0.95):
        """
        value at risk
        """
        if self.stock_data is None:
            self.load_data()

        self.value_at_risk = np.percentile(self.returns,(1 - ci)*100)
        return self.value_at_risk
    
    def get_cvar(self,ci=0.95):
        """
        Conditional Value at Risk
        """
        if self.stock_data is None:
            self.load_data()


        tail_risk = self.returns[self.returns < self.value_at_risk]
        self.cvar = np.mean(tail_risk)
        return self.cvar
    
    def plot_returns(self):
        """
        Args:
          plots VaR, Returns, and cvar
          """
        if self.stock_data is None:
            self.load_data()
        print(f' Returns: {self.returns}')
        print(f'Value at Risk: {self.value_at_risk}')
        print(f'Conditional Value at Risk: {self.cvar:.4}%')
        plt.figure(figsize=(10, 6))
        plt.hist(self.returns, bins=100, label="Returns Distribution", alpha=0.7)
        plt.axvline(self.value_at_risk, color='r', linestyle='dashed', linewidth=2, label=f'VaR (5%): {self.value_at_risk:.4f}')
        plt.axvline(x=self.cvar, color='green', linestyle='--', label=f'CVaR ({self.cvar:.4f}%)')
        plt.title('Distribution of Returns and Value at Risk')
        plt.xlabel('Returns')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.show()



