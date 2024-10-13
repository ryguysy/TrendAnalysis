import yfinance as yf
import pandas as pd

def download_stock_data(ticker, start_date, end_date):
    """
    Downloads historical stock data from Yahoo Finance for a given ticker symbol.
    
    Args:
    ticker (str): The stock ticker symbol (e.g., 'AAPL').
    start_date (str): The start date for downloading data (e.g., '2015-01-01').
    end_date (str): The end date for downloading data (e.g., '2024-01-01').

    Returns:
    pd.DataFrame: The historical stock data as a pandas DataFrame.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def add_moving_averages(df, window_short=50, window_long=200):
    """
    Adds moving averages to the stock data.

    Args:
    df (pd.DataFrame): The stock data DataFrame.
    window_short (int): The short window for the moving average (default: 50 days).
    window_long (int): The long window for the moving average (default: 200 days).

    Returns:
    pd.DataFrame: The DataFrame with added moving averages.
    """
    df[f'MA_{window_short}'] = df['Close'].rolling(window=window_short).mean()
    df[f'MA_{window_long}'] = df['Close'].rolling(window=window_long).mean()
    return df

if __name__ == "__main__":
    # Example usage
    ticker = 'AAPL'
    start_date = '2015-01-01'
    end_date = '2024-01-01'

    stock_data = download_stock_data(ticker, start_date, end_date)
    stock_data = add_moving_averages(stock_data)
    
    # Save preprocessed data
    stock_data.to_csv('../data/preprocessed_stock_data.csv')
    print("Data saved to ../data/preprocessed_stock_data.csv")