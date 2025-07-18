import pytest
import pandas as pd
import numpy as np
import yfinance as yf
from unittest.mock import patch
from src.financial_models.VaR import Var


SAMPLE_CONFIG = {
    'stock_tickers': 'AAPL',
    'start_date': '2023-01-01',
    'end_date': '2023-01-10'
}


@pytest.fixture
def var_instance():
    """Fixture to create an instance of the Var class for testing."""
    return Var(SAMPLE_CONFIG)


def test_var_initialization(var_instance):
    """Test that the Var class is initialized correctly."""
    assert var_instance.config == SAMPLE_CONFIG
    assert var_instance.stock_data is None


@patch('yfinance.download')
def test_load_data(mock_download, var_instance):
    """Test the load_data method."""


    mock_data = pd.DataFrame({
        'Close': [150, 152, 155, 153, 156, 155, 158, 160, 159, 161]
    }, index=pd.to_datetime(pd.date_range(start=SAMPLE_CONFIG['start_date'], end=SAMPLE_CONFIG['end_date'])))
    mock_download.return_value = mock_data

    data = var_instance.load_data()

    assert isinstance(data, pd.Series)
    assert not data.empty
    assert var_instance.stock_data is not None


@patch('yfinance.download')
@patch('matplotlib.pyplot.show')
def test_get_returns(mock_show, mock_download, var_instance):
    """Test the get_returns method."""

    mock_data = pd.DataFrame({
        'Close': [150, 152, 155, 153, 156, 155, 158, 160, 159, 161]
    }, index=pd.to_datetime(pd.date_range(start=SAMPLE_CONFIG['start_date'], end=SAMPLE_CONFIG['end_date'])))
    mock_download.return_value = mock_data


    var_instance.get_returns()


    assert var_instance.stock_data is not None


    mock_show.assert_called_once()

    returns = var_instance.stock_data.pct_change().dropna()

    VaR = np.quantile(returns,0.05)
    assert VaR is not None











