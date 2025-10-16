import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
from src.config import load_config
import numpy as np
from pypfopt import expected_returns
import os
import yfinance as yf
from src.data_acquisition.download_data import LoadData
from src.logger import logger


class Sim:
    def __init__(self,config):
        self.config = config
        
        
    def get_data(self):
        """ fetch data from data ingestion """
        # combined data
        self.data = pd.read_csv(self.config['all_data_path'],delimiter=",")
        return self.data
    
    
    def get_market_data(self):
        """ Market Data is the SP500 """
        try:
            # ticker for sp500
            sp500_ticker = self.config['sp500_ticker']
            # all assets ticker
            all_prices = self.get_data()
            self.sp500_data = all_prices[sp500_ticker]
            return self.sp500_data
        except FileNotFoundError as e:
            logger.error(f"Could not find file: {e}")
            raise None
        
        
    def get_returns(self):
        """ Returns from Sp500 and combined assets """
        try:
            self.Market_Returns = self.sp500_data.pct_change().dropna()
            self.returns = self.data.pct_change().dropna()
        except Exception as e:
            logger.exception(f"Error loading data: {e}")
            raise e
        
    def single_index_model(self,output_dir="images/sim/"):

        #tickers to turn data into correct frame

        sp500_ticker = self.config['sp500_ticker']
        tickers = self.config['combined_assets']
        risk_free_rate = self.config['risk_free_rate']

        # sp500 data
        self.sp500_data = self.data[sp500_ticker]
        # Market Returns(sp500) and Market Excess Returns
        market_returns = self.sp500_data.pct_change().dropna()
        market_excess_returns = self.sp500_data.pct_change().dropna()

        #market index risk is of the sp500(variance(sp500))
        market_index_risk = np.var(market_returns)
        print(f'Market Index Risk: {market_index_risk}')




        # alphas, betas, total risk, covariance, market index risk,firm specific risk,product of betas
        alphas = {}
        betas = {}
        error_terms = {}
        adjusted_betas = {}
        firm_specific_risks = {}
        systematic_risks = {}
        total_risks = {}
        risk_premiums = {}
        Expected_Returns = {}
    







        for ticker in tickers:
            asset_data = self.data[ticker]
            returns = asset_data.pct_change().dropna()
            Excess_Returns = asset_data.pct_change().dropna() - risk_free_rate
            print(f'Returns for: {ticker}, {returns}')
            print(f'Excess Returns: {Excess_Returns}')
            print(f'Market Returns: {sp500_ticker},{market_returns};----- Market Excess Returns: {market_excess_returns}')



            model = sm.OLS(exog=sm.add_constant(market_returns),endog=returns).fit()
            

            # alpha, beta, error-term (e), firm-specific risk(variance(e)), market risk(variance of sp500 in this case).
            # risk premium: E(R) - Rf
            alpha = model.params.const
            beta = model.params.iloc[1]
            residuals = model.resid
            




            #adjusted beta: 2/3 * beta + 1/3 * 1
            adj_beta = (2/3) * beta + (1/3) * 1


            # Systematic risk is (Beta**2) * Market Index Risk (defined above)
            systematic_risk = (beta**2) * market_index_risk

            #  firm-specific risk is the variance of the "Unanticipated surpises" (the variance of the residuals for the asset)
            firm_specific_risk = np.var(residuals)

            # total risk = systematic Risk + Firm Specific Risk
            total_risk = systematic_risk + firm_specific_risk






            alphas[ticker] = alpha
            betas[ticker] = beta
            error_terms[ticker] = residuals
            adjusted_betas[ticker] = adj_beta
            systematic_risks[ticker] = systematic_risk
            firm_specific_risks[ticker] = firm_specific_risk
            total_risks[ticker] = total_risk

            print(f'Alpha Value: {alpha:.4f}')
            print(f'Beta Value: {beta:.4f}')
            print(f'Adjusted Beta: {adj_beta:4f}')
            print(f'Firm Specific Risk: {firm_specific_risk:.4f}')
            print(f'Systematic Risk: {systematic_risk:.4f}')
            print(f'Total Risk: {total_risk}')
            print(f'Error Term: {residuals}')

            


        

            # E(r) -> The Expected Return using pyportfolio & Risk Premiun = E(r) - rf 
            Expected_Return = expected_returns.mean_historical_return(asset_data)
            risk_premium = Expected_Return - risk_free_rate

            Expected_Returns[ticker] = Expected_Return
            risk_premiums[ticker] = risk_premium
            

            
            # for the individual betas and alphas

            print(f'ANOVA Table: {model.summary()}')
            print(f'R2 Score: {model.rsquared*100:.2f}')
            print(f'Expected Return: {Expected_Return}')
            
            
            plt.figure(figsize=(12,6))
            sns.scatterplot(x=market_returns, y=returns, label=ticker)
            sns.lineplot(x=market_returns, y=model.fittedvalues, color='red', label='Security Market Line')
                
            plt.title(f'Single Index Model for {ticker}')
            plt.xlabel('Market Excess Return')
            plt.ylabel(f'{ticker} Excess Return')
            plt.legend()
            plt.show()





