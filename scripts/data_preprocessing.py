import pandas as pd
from database import get_stock_data, get_options_data

def preprocess_stock_data(stock_df):
    """Clean and preprocess the stock DataFrame."""
    # Ensure the date column is in datetime format
    stock_df.index = pd.to_datetime(stock_df.index)
    
    # Example: Handle missing values
    stock_df.fillna(method='ffill', inplace=True)  # Forward fill

    add_moving_averages(stock_df)
    
    return stock_df

def preprocess_options_data(options_chain, expiration_date):
    """Clean and preprocess the options into DataFrame."""
    # Convert the call and put options data into DataFrames
    calls_df = options_chain.calls
    puts_df = options_chain.puts
    
    # Add 'type' column to indicate if it's a call or put option
    calls_df['option_type'] = 'call'
    puts_df['option_type'] = 'put'
    
    # Add the expiration date to both calls and puts DataFrames
    calls_df['expiration'] = expiration_date
    puts_df['expiration'] = expiration_date
    
    # Combine calls and puts into a single DataFrame
    combined_options_df = pd.concat([calls_df, puts_df], ignore_index=True)
    
    return combined_options_df

def calculate_greek(options_chain):
    '''
    Calculates the greeks of an option
    '''



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