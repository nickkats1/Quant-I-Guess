import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.config import load_config
import yfinance as yf
import numpy as np
from src.utils.logger import logger


class Var:
    def __init__(self,config):
        self.config = config
        self.stock_data = None

        
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
            
        returns = self.stock_data.pct_change().dropna()
        VaR = np.quantile(returns,0.05)
        logger.info(f'Returns from VaR.py : {returns.head()}')
        logger.info(f'Value at Risk: {Var}')
        print(returns)
        print(VaR)
        plt.figure(figsize=(10, 6))
        plt.hist(returns, bins=100, label="Returns Distribution", alpha=0.7)
        plt.axvline(VaR, color='r', linestyle='dashed', linewidth=2, label=f'VaR (5%): {VaR:.4f}')
        plt.title('Distribution of Returns and Value at Risk')
        plt.xlabel('Returns')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.show()






