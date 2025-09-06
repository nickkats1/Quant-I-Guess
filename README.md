# Quant-I-Guess
A bunch of finance stuff I remember from Economics.



### Portfolio Optimization
* Go watch this video. Listen to professors, not random youtubers who lie, say nothing and make stuff up and waste time(all of them do).
* I was taught this at uni, but this man in the link is very good at explaining the Efficient Frontier and everything with EF ect..
* Link:
[efficient_diversification_video](https://www.youtube.com/watch?v=wo7LR-evnmc&t=605s)

Watch Both Parts

#### Value at Risk and Conditional Value at Risk (CVar)

![var_es_portfolio](images/VaR-Cvar-EfficientDiversification.png)

Tail risk, kurtosis(greek like me!)
VaR is the maximum amount that can be lost during a certain period of time.
Expected shortfall is furter to the left compared to Value at Risk(VaR) and takes into the "tail risk" that var ignores

### Single Index Model

![apple_sim](images/sim/single_index_model_AAPL.png)
![Ford_sim](images/sim/single_index_model_F.png)
![mcdonalds_sim](images/sim/single_index_model_MCD.png)
![google_sim](images/sim/single_index_model_GOOGL.png)

```text
--- Single Index Model for: AAPL ---
Alpha (intercept): 0.000003
Beta (market sensitivity): 1.258999
R-squared: 0.5890
Residual Variance (Unsystematic Risk): 0.000131

Full regression summary:
                            OLS Regression Results                            
==============================================================================
Dep. Variable:           Asset_Excess   R-squared:                       0.589
Model:                            OLS   Adj. R-squared:                  0.589
Method:                 Least Squares   F-statistic:                     1681.
Date:                Sat, 06 Sep 2025   Prob (F-statistic):          9.92e-229
Time:                        06:38:22   Log-Likelihood:                 3586.2
No. Observations:                1175   AIC:                            -7168.
Df Residuals:                    1173   BIC:                            -7158.
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
=================================================================================
                    coef    std err          t      P>|t|      [0.025      0.975]
---------------------------------------------------------------------------------
const          2.574e-06      0.000      0.008      0.994      -0.001       0.001
Market_Excess     1.2590      0.031     41.001      0.000       1.199       1.319
==============================================================================
Omnibus:                      110.401   Durbin-Watson:                   1.824
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              664.923
Skew:                           0.152   Prob(JB):                    4.11e-145
Kurtosis:                       6.673   Cond. No.                         92.0
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
All of the Single Index models have the SP500 at the independent variable and the asset(stocks in this case)
as the dependent variable. Excess returns,ect
I did not add other more CAPM related things becuase I like Markowits

#### Efficient Diversification

* This is a contrained optimization problem with the weights being the asset classes.
You cannot just have risky weight Efficient Diversifcation, you do not put all of your eggs into one basket
















