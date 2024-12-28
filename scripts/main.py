from database import create_database
from data_collection import save_stock_data_to_db, download_options_data, get_price, collect_posts
from analysis import calculate_put_credit_spread
from datetime import date

def main():
    create_database()  # Check and create DB only if it doesn't exist
    
    '''
    Gathering stock data
    '''
    ticker = 'SPY'
    start_date = '2015-01-01'
    end_date = '2024-01-01'
    today = '2027-01-15' #str(date.today())

    save_stock_data_to_db(ticker, start_date, end_date)  # Download and store data in DB

    option_chain = download_options_data(ticker, today)

    spread,strike,price = calculate_put_credit_spread(option_chain,get_price(ticker))

    print(f'strike: {strike}, price: {price}')
    print(spread)

    '''
    Gathering tweets
    '''

    posts_df = collect_posts(ticker,'2024-01-01',end_date)
    #Assuming you already have a DataFrame with a 'text' column
    #posts_df = pd.read_csv('../data/tweets.csv')  # Example: Loading tweets data

    # Perform sentiment analysis
    #posts_df = analyze_sentiment(posts_df)

    # Aggregate daily sentiment
    #daily_sentiment = aggregate_daily_sentiment(posts_df)

    # Save the processed tweets with sentiment
    #posts_df.to_csv('../data/processed_posts.csv', index=False)

    print("Sentiment analysis completed and saved.")

    # Print daily sentiment metrics
    #print(daily_sentiment)

if __name__ == "__main__":
    main()