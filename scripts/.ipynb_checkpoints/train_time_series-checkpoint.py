import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import pickle

def train_arima_model(df, order=(5, 1, 0)):
    """
    Trains an ARIMA model on the stock data.

    Args:
    df (pd.DataFrame): The stock data DataFrame with 'Close' price column.
    order (tuple): The (p, d, q) order of the ARIMA model.

    Returns:
    ARIMA: The trained ARIMA model.
    """
    model = ARIMA(df['Close'], order=order)
    model_fit = model.fit()
    return model_fit

if __name__ == "__main__":
    # Load the preprocessed stock data
    df = pd.read_csv('../data/preprocessed_stock_data.csv', index_col='Date', parse_dates=True)

    # Train the ARIMA model
    arima_model = train_arima_model(df)

    # Save the trained ARIMA model
    with open('../models/arima_model.pkl', 'wb') as f:
        pickle.dump(arima_model, f)

    print("ARIMA model saved to ../models/arima_model.pkl")