from database import create_database
from data_collection import save_stock_data_to_db, download_options_data, get_price
from analysis import calculate_put_credit_spread
from datetime import date

def main():
    create_database()  # Check and create DB only if it doesn't exist
    
    # Example: Download and save stock data
    ticker = 'SPY'
    start_date = '2015-01-01'
    end_date = '2024-01-01'
    today = str(date.today())

    save_stock_data_to_db(ticker, start_date, end_date)  # Download and store data in DB

    option_chain = download_options_data(ticker, today)

    spread = calculate_put_credit_spread(calculate_put_credit_spread,get_price(ticker))

    print(spread)

if __name__ == "__main__":
    main()