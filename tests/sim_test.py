import pytest
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
from src.utils.config import load_config
from src.financial_models.sim_capm import Sim


@pytest.fixture
def dummy_config():
    """Provides a dummy configuration for testing."""
    return {
        'sim_tickers': ['MSFT', '^GSPC'],
        'start_date': '2022-01-01',
        'end_date': '2022-01-31',
        'stock_tickers': ['MSFT'],
        'sp500_ticker': '^GSPC',
        'risk_free_rate': 0.01
    }

@pytest.fixture
def mock_yf_download():
    """Mocks yfinance.download to return a sample DataFrame."""
    mock_data = pd.DataFrame({
        'MSFT': [100, 102, 105, 103, 107],
        '^GSPC': [4000, 4050, 4100, 4080, 4120]
    }, index=pd.to_datetime(pd.date_range('2022-01-01', periods=5)))
    with patch('yfinance.download', return_value={'Close': mock_data}) as mock_download:
        yield mock_download

@pytest.fixture
def mock_sm_ols():
    """Mocks statsmodels.api.OLS to return a simplified mock model."""
    mock_model = MagicMock()
    mock_model.fittedvalues = pd.Series([101, 103, 106, 104, 108], 
                                         index=pd.to_datetime(pd.date_range('2022-01-01', periods=5)))
    mock_model.summary.return_value = "Mock OLS Summary"
    with patch('statsmodels.api.OLS', return_value=MagicMock(fit=lambda: mock_model)) as mock_ols:
        yield mock_ols

@pytest.fixture
def mock_plt_show_and_savefig(monkeypatch, tmp_path):
    """Mocks plt.show() and plt.savefig() to prevent actual plotting and manage temporary files."""
    def mock_show():
        pass

    def mock_savefig(filename, *args, **kwargs):
        pass

    monkeypatch.setattr(plt, "show", mock_show)
    monkeypatch.setattr(plt, "savefig", mock_savefig)


class TestSim:

    def test_get_data_loads_data(self, dummy_config, mock_yf_download):

        sim_instance = Sim(dummy_config)
        df = sim_instance.get_data()
        assert not df.empty
        assert isinstance(df, pd.DataFrame)
        assert 'MSFT' in df.columns
        assert '^GSPC' in df.columns
        mock_yf_download.assert_called_once_with(dummy_config['sim_tickers'],
                                                start=dummy_config['start_date'],
                                                end=dummy_config['end_date'])

    def test_single_index_model_performs_analysis_and_plots(self, dummy_config, 
                                                             mock_yf_download, 
                                                             mock_sm_ols,
                                                             mock_plt_show_and_savefig,
                                                             tmp_path):

        sim_instance = Sim(dummy_config)
        

        output_dir = tmp_path / "images/sim"
        sim_instance.single_index_model(output_dir=output_dir)


        mock_sm_ols.assert_called()
