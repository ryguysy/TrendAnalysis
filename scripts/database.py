import sqlite3
import pandas as pd
import os

def connect_db():
    """Utility to connect to the database."""
    return sqlite3.connect('stock_data.db')

def create_database():
    # check if database file already exists
    if os.path.exists('stock_data.db'):
        print("Database already exists")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Create stock data table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_data (
                        ticker TEXT,
                        date TEXT,
                        open REAL,
                        high REAL,
                        low REAL,
                        close REAL,
                        volume INTEGER,
                        PRIMARY KEY (ticker, date)
                    )''')

    # Create options data table
    cursor.execute('''CREATE TABLE IF NOT EXISTS options_data (
                        ticker TEXT,
                        expiration_date TEXT,
                        strike_price REAL,
                        option_type TEXT,
                        last_price REAL,
                        bid REAL,
                        ask REAL,
                        volume INTEGER,
                        PRIMARY KEY (ticker, expiration_date, strike_price, option_type)
                    )''')

    conn.commit()
    conn.close()

def insert_stock_data(ticker, stock_data):
    """Insert or update stock data in the database."""
    if stock_data.empty:
        print(f"No stock data to insert for {ticker}.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        for index, row in stock_data.iterrows():
            cursor.execute('''INSERT OR REPLACE INTO stock_data (ticker, date, open, high, low, close, volume) 
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (ticker, index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting stock data: {e}")
    finally:
        conn.close()

def insert_options_data(ticker, expiration_date, options_data):
    """Insert or update options data in the database."""
    if options_data.calls.empty and options_data.puts.empty:
        print(f"No options data to insert for {ticker} on {expiration_date}.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        for _, row in options_data.calls.iterrows():
            cursor.execute('''INSERT OR REPLACE INTO options_data (ticker, expiration_date, strike_price, option_type, last_price, bid, ask, volume) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (ticker, expiration_date, row['strike'], 'call', row['lastPrice'], row['bid'], row['ask'], row['volume']))

        for _, row in options_data.puts.iterrows():
            cursor.execute('''INSERT OR REPLACE INTO options_data (ticker, expiration_date, strike_price, option_type, last_price, bid, ask, volume) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (ticker, expiration_date, row['strike'], 'put', row['lastPrice'], row['bid'], row['ask'], row['volume']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting options data: {e}")
    finally:
        conn.close()

def get_stock_data(ticker, start_date, end_date):
    """Fetch stock data from the database as a Pandas DataFrame."""
    conn = connect_db()

    query = '''
        SELECT * 
        FROM stock_data 
        WHERE ticker = ? AND date BETWEEN ? AND ?
    '''
    try:
        df = pd.read_sql_query(query, conn, params=(ticker, start_date, end_date))
    except sqlite3.Error as e:
        print(f"Error fetching stock data: {e}")
        df = pd.DataFrame()  # Return empty DataFrame on error
    finally:
        conn.close()
    return df

def get_options_data(ticker, expiration_date):
    """Fetch options data from the database as a Pandas DataFrame."""
    conn = connect_db()

    query = '''
        SELECT * 
        FROM options_data 
        WHERE ticker = ? AND expiration_date = ?
    '''
    try:
        df = pd.read_sql_query(query, conn, params=(ticker, expiration_date))
    except sqlite3.Error as e:
        print(f"Error fetching options data: {e}")
        df = pd.DataFrame()  # Return empty DataFrame on error
    finally:
        conn.close()
    return df