import yfinance as yf
from database import insert_stock_data, insert_options_data
from data_preprocessing import preprocess_stock_data, preprocess_options_data

def get_price(ticker):

    return yf.Ticker(ticker).info.get('currentPrice')


def download_stock_data(ticker, start_date, end_date):
    # Use yfinance to download stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def download_options_data(ticker, expiration_date):
    # Use yfinance to get options data
    ticker_obj = yf.Ticker(ticker)
    options_chain = ticker_obj.option_chain(expiration_date)
    return preprocess_options_data(options_chain,expiration_date)

def save_stock_data_to_db(ticker, start_date, end_date):
    """Download, preprocess, and save stock data to the database."""
    raw_stock_data = download_stock_data(ticker, start_date, end_date)
    if not raw_stock_data.empty:
        preprocessed_stock_data = preprocess_stock_data(raw_stock_data)
        insert_stock_data(ticker, preprocessed_stock_data)  # Save preprocessed data

def save_options_data_to_db(ticker, expiration_date):
    """Download, preprocess, and save options data to the database."""
    raw_options_chain = download_options_data(ticker, expiration_date)
    if raw_options_chain:
        preprocessed_options_data = preprocess_options_data(raw_options_chain,expiration_date)
        if preprocessed_options_data is not None:
            insert_options_data(ticker, expiration_date, preprocessed_options_data)  # Save preprocessed data