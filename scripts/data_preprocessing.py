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

    # Ensure the index is a DateTime index
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date', inplace=True)

    # Set the frequency to daily (or 'B' for business days)
    stock_data = stock_data.asfreq('B')

    
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
    ticker = 'AMD'
    start_date = '2015-01-01'
    end_date = '2024-01-01'

    stock_data = download_stock_data(ticker, start_date, end_date)
    stock_data = add_moving_averages(stock_data)
    
    # Save preprocessed data
    stock_data.to_csv(f'../data/{ticker}_data.csv')
    print(f"Data saved to ../data/{ticker}_data.csv")