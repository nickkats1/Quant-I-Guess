import pytest
import pandas as pd
from src.financial_models.portfolio_optimization import EfficientDiversification


@pytest.fixture(scope="module")
def sample_config():
    config = {
        'all_tickers': ['AAPL','NVDA','MSFT','GOOGL','META','TSLA','SPY','IVV','VTI','QQQ','VUG','BND','BTC-USD','XPR-USD','ADA-USD','SOL-USD','DAI-USD','MATIC-USD'],
        'start_date': '2020-10-10',
        'end_date': '2025-07-17',
    }
    return config


@pytest.fixture(scope="module")
def efficient_diversification_instance(sample_config):
    return EfficientDiversification(sample_config)



def test_efficient_frontier_instance(efficient_diversification_instance):
    assert efficient_diversification_instance is not None


def test_load_data(efficient_diversification_instance):
    prices = efficient_diversification_instance.load_data()
    prices = prices.dropna()
    assert prices is not None
    assert isinstance(prices, pd.DataFrame)
    assert not prices.empty
    assert not prices.columns.empty
