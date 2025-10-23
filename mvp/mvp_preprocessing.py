import yfinance as yf
import pandas as pd
import numpy as np

def download_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df[['Close']]
    df.index = pd.to_datetime(df.index)
    df = df.asfreq('B')
    return df

def add_moving_averages(df, windows=[7, 14]):
    for w in windows:
        df[f'MA_{w}'] = df['Close'].rolling(window=w).mean()
    return df

def add_fake_sentiment(df):
    # Replace this later with your Reddit/Twitter sentiment aggregation
    np.random.seed(42)
    df['Sentiment'] = np.random.normal(0, 1, len(df))
    return df

def add_labels(df):
    df['Next_Close'] = df['Close'].shift(-1)
    df['Target'] = np.where(df['Next_Close'] > df['Close'], 1, 0)  # 1 = increase, 0 = decrease/stay
    df.dropna(inplace=True)
    return df

if __name__ == "__main__":
    ticker = 'AMD'
    start_date = '2020-01-01'
    end_date = '2024-01-01'

    df = download_stock_data(ticker, start_date, end_date)
    df = add_moving_averages(df)
    df = add_fake_sentiment(df)
    df = add_labels(df)

    df.to_csv('../data/mvp_dataset.csv')
    print("✅ MVP dataset saved to ../data/mvp_dataset.csv")
    print(df.head())
