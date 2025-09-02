import pytest
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
from src.financial_models.sim import Sim

@pytest.fixture
def dummy_config():
    return {
        'sim_tickers': ['AAPL', 'MSFT', 'GOOGL', 'META', 'TSLA', 'TGT', 'GM', 'VZ', 'T', '^GSPC'],
        'stock_tickers': ['MSFT'], 
        'start_date': '2020-10-10',
        'end_date': '2025-08-30',
        'sp500_ticker': '^GSPC',
        'risk_free_rate': 0.0092
    }

@pytest.fixture
def mock_yf_download_data():
    dates = pd.date_range('2022-01-01', periods=5)
    mock_data = pd.DataFrame({
        ('Close', 'MSFT'): [100, 102, 105, 103, 107],
        ('Close', '^GSPC'): [4000, 4050, 4100, 4080, 4120],
        ('Adj Close', 'MSFT'): [98, 100, 103, 101, 105],
        ('Adj Close', '^GSPC'): [3950, 4000, 4050, 4030, 4070]
    }, index=dates)
    mock_data.columns = pd.MultiIndex.from_tuples(mock_data.columns, names=['Attributes', 'Symbols'])

    with patch('yfinance.download', return_value=mock_data) as mock_download:
        yield mock_download

@pytest.fixture
def mock_sm_ols():
    mock_model = MagicMock()
    mock_model.fittedvalues = pd.Series([101, 103, 106, 104, 108], 
                                         index=pd.date_range('2022-01-01', periods=5))
    mock_model.summary.return_value = "Mock OLS Summary"
    mock_fit = MagicMock(return_value=mock_model)

    with patch('statsmodels.api.OLS', return_value=MagicMock(fit=mock_fit)) as mock_ols:
        yield mock_ols

@pytest.fixture
def mock_plt_show_and_savefig(monkeypatch, tmp_path):
    def mock_show():
        pass

    def mock_savefig(filename, *args, **kwargs):
        full_path = tmp_path / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.touch()

    monkeypatch.setattr(plt, "show", mock_show)
    monkeypatch.setattr(plt, "savefig", mock_savefig)

class TestSim:

    def test_get_data_loads_data(self, dummy_config, mock_yf_download_data):
        sim_instance = Sim(dummy_config)
        data = sim_instance.fetch_data()

        assert not data.empty
        assert isinstance(data, pd.DataFrame)
        assert 'MSFT' in data.columns
        assert '^GSPC' in data.columns

        mock_yf_download_data.assert_called_once_with(
            tickers=dummy_config['sim_tickers'],
            start=dummy_config['start_date'],
            end=dummy_config['end_date']
        )

    def test_single_index_model_performs_analysis_and_plots(self, dummy_config,
                                                             mock_yf_download_data,
                                                             mock_sm_ols,
                                                             mock_plt_show_and_savefig,
                                                             tmp_path):
        sim_instance = Sim(dummy_config)
        output_dir = tmp_path / "images/sim"
        sim_instance.single_index_model(output_dir=output_dir)

        mock_sm_ols.return_value.fit.assert_called_once()

        expected_file = output_dir / "single_index_model_MSFT.png"
        assert expected_file.exists()

