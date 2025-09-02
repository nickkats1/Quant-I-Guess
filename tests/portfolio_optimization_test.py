import pytest
import pandas as pd
from unittest.mock import patch
from src.financial_models.portfolio_optimization import EfficientDiversification
from pypfopt import expected_returns, risk_models, EfficientFrontier



@pytest.fixture
def mock_prices():
    return pd.DataFrame({
        "AAPL": [100,101,102,103,104],
        "MSFT": [150,152,151,153,154],
        "ARKK": [130,128,125,122,125],
        "BNB-USD": [31,32,35,38,37],
        "BTC-USD": [23000,23001,23002,23003,23004],
        "DIA": [277,278,279,280,281],
        "EFA": [63,64,65,66,67],
        "ETH-USD":[583,584,585,586,587],
        "F":[11,12,13,14,15],
        "GM":[58,59,60,61,62],
        "GOOGL":[208,207,209,210,211],
        "IWM":[232,233,234,235,236],
        "LINK-USD":[23,24,25,26,27],
        "MCD":[311,312,313,314,315],
        "QQQ": [570,571,572,573,574],
        "SBUX":[85,86,87,88,89],
        "SOL-USD":[187,188,189,190,191],
        "SPY":[642,643,644,645,646],
        "STETH-USD":[4370,4371,4372,4373,4374],
        "TGT":[96,97,98,99,100],
        "TRX-USD":[0.34,0.35,0.36,0.37,0.38],
        "TSLA": [346,347,348,349,350],
        "USDC-USD": [1,2,3,4,5],
        "VOO":[590,591,592,593,594],
        "VTI":[316,317,318,319,320],
        "WMT": [96,97,98,99,100],
        "XLF":[53,54,55,56,57],
        "XLK": [261,262,263,264,265],
        "XRP-USD":[2,3,4,5,6]
    }, index=pd.to_datetime([
        "2022-01-01", "2022-01-02", "2022-01-03",
        "2022-01-04", "2022-01-05"
    ]))



@pytest.fixture
def efficient_diversification_instance():
    mock_config = {
        "combined_assets": ['AAPL', 'ARKK', 'BNB-USD', 'BTC-USD', 'DIA', 'EFA', 'ETH-USD',
       'F', 'GM', 'GOOGL', 'IWM', 'LINK-USD', 'MCD', 'MSFT', 'QQQ', 'SBUX',
       'SOL-USD', 'SPY', 'STETH-USD', 'TGT', 'TRX-USD', 'TSLA', 'USDC-USD',
       'USDT-USD', 'VOO', 'VTI', 'WMT', 'XLF', 'XLK', 'XRP-USD'],
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "risk_free_rate": 0.0092
    }
    return EfficientDiversification(mock_config)



@patch("src.financial_models.portfolio_optimization.yf.download")
def test_load_data_with_mock(mock_download, efficient_diversification_instance,mock_prices):


    
    close_prices = mock_prices.copy()


    mock_download.return_value = {
        "Close": close_prices
    }


    efficient_diversification_instance.load_data()

    pd.testing.assert_frame_equal(
        efficient_diversification_instance.all_prices,
        close_prices
    )






def test_load_returns_with_mock(efficient_diversification_instance, mock_prices):
    efficient_diversification_instance.all_prices = mock_prices

    returns = efficient_diversification_instance.eval_returns()

    assert isinstance(returns, pd.DataFrame)
    assert not returns.empty




def test_portfolio_metrics_with_mock(efficient_diversification_instance, mock_prices):
    efficient_diversification_instance.all_prices = mock_prices
    returns = efficient_diversification_instance.eval_returns()

    mu = expected_returns.mean_historical_return(returns)
    S = risk_models.sample_cov(returns)
    ef = EfficientFrontier(mu, S)

    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance(verbose=True)
    performance = {
        "Expected Annual Return": expected_annual_return,
        "Annual Volatility": annual_volatility,
        "Sharpe Ratio": sharpe_ratio
    }

    assert not mu.empty
    assert not S.empty
    assert isinstance(weights, dict)
    assert isinstance(cleaned_weights, dict)
    assert isinstance(performance, dict)
    assert abs(sum(cleaned_weights.values()) - 1.0) < 1e-4








        



