import yfinance as yf
import pandas as pd
import numpy as np
import time
import os

def download_stock_data(ticker, start_date, end_date, max_retries=3, pause=1.0):
    """
    Download daily OHLC data using yfinance and return a DataFrame with a Close column.
    Adds defensive checks and retries.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
            # yf.download returns an empty DataFrame if ticker failed — handle that
            if df is None or df.empty:
                attempt += 1
                time.sleep(pause)
                continue
            
            # FIX: Handle MultiIndex columns - flatten the column structure
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Keep only Close and ensure it's a copy (avoid chained-assignment warnings)
            df = df[['Close']].copy()
            df.index = pd.to_datetime(df.index)
            # NOTE: keep trading days only (what yfinance returned).
            return df
        except Exception as e:
            # Sometimes yfinance returns malformed JSON or has network issues; retry a few times
            attempt += 1
            time.sleep(pause)
            last_exc = e
    # If we exit loop, either df was empty every time or we hit exception multiple times
    msg = f"Failed to download data for {ticker} after {max_retries} attempts."
    if 'last_exc' in locals():
        raise RuntimeError(msg + f" Last exception: {last_exc}")
    else:
        raise RuntimeError(msg + " The returned DataFrame was empty each attempt.")

def add_moving_averages(df, windows=[7, 14]):
    # operate on a copy to avoid chained-assignment warnings
    out = df.copy()
    for w in windows:
        out[f'MA_{w}'] = out['Close'].rolling(window=w, min_periods=1).mean()
    return out

def add_fake_sentiment(df, seed=42):
    out = df.copy()
    np.random.seed(seed)
    out['Sentiment'] = np.random.normal(0, 1, len(out))
    return out

def add_labels(df, threshold=0.0):
    """
    Create next-day Target label.
    threshold can be used to create a 'stay' zone, e.g. threshold=0.001 for 0.1% change.
    Returns a copy with columns Next_Close and Target (1 if next close > current + threshold, else 0).
    """
    out = df.copy()
    
    # Calculate next close first
    out['Next_Close'] = out['Close'].shift(-1)
    
    # Drop the last row which will have NaN for Next_Close
    out = out.iloc[:-1].copy()
    
    # Calculate the condition properly - use vectorized operations
    price_change = (out['Next_Close'] - out['Close']) / out['Close']
    out['Target'] = (price_change > threshold).astype(int)
    
    return out

if __name__ == "__main__":
    ticker = 'AMD'
    start_date = '2020-01-01'
    end_date = '2024-01-01'

    try:
        df = download_stock_data(ticker, start_date, end_date)
        print(f"✅ Downloaded {len(df)} rows for {ticker}")
        print(f"Initial columns: {df.columns.tolist()}")
        print(f"Column type: {type(df.columns)}")
    except RuntimeError as e:
        print("❌", e)
        raise

    df = add_moving_averages(df, windows=[7, 14])
    print(f"After moving averages: {df.columns.tolist()}")
    
    df = add_fake_sentiment(df)
    print(f"After sentiment: {df.columns.tolist()}")
    
    df = add_labels(df)
    print(f"After labels: {df.columns.tolist()}")
    print(f"Final shape: {df.shape}")

    # ensure target directory exists
    out_dir = os.path.join('..', 'data')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'mvp_dataset.csv')

    df.to_csv(out_path, index=True)
    print("✅ MVP dataset saved to", out_path)
    print(f"\nFirst few rows:")
    print(df.head(10))
    print(f"\nLast few rows:")
    print(df.tail(5))