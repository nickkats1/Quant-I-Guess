from src.config import load_config
from src.data_acquisition.download_data import LoadData
from src.financial_models.portfolio_optimization import EfficientDiversification
from src.financial_models.VaR import Var
from src.financial_models.sim import Sim


if __name__ == "__main__":
    config =load_config()
    
    # Load data config
    load_data_config = LoadData(config)
    
    # fetch all prices
    load_data_config.fetch_stock_data()
    
    # Value at Risk Config
    var_config = Var(config)
    var_config.load_data()
    # VaR and CVaR
    var_config.get_var()
    var_config.get_cvar()
    var_config.plot_returns()
    
    # Efficient Diversification config
    ef_config = EfficientDiversification(config)
    ef_config.fetch_data()
    ef_config.get_portfolio_returns()
    ef_config.portfolio_metrics()
    ef_config.weights
    ef_config.mu
    ef_config.S
    
    # single index model config
    sim_config = Sim(config)
    sim_config.get_data()
    # sp&500 data

    sim_config.get_market_data()
    sim_config.single_index_model()
