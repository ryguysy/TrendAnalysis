import yfinance as yf
from database import insert_stock_data, insert_options_data
from data_preprocessing import preprocess_stock_data, preprocess_options_data

'''

Methods for gathering Stock data

'''

def get_price(ticker):

    data = yf.Ticker(ticker).history(period="1d", interval="1m")
    return data["Close"].iloc[-1]


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
'''

Methods for gathering reddit posts

'''

import praw
import pandas as pd


def collect_posts(ticker, start_date, end_date, max_results=10):
    # Set up Reddit API credentials
    reddit = praw.Reddit(
        client_id='0U2AHMjW3xj8TaG1FIwDww',
        client_secret='Ae0EyU-bCxEl8FVyMlnq9ctWWoUzMg',
        user_agent='myTrendProjectBot v1.0'
    )

    # Define the subreddit and how many posts to fetch
    subreddit = 'wallstreetbets'

    # Initialize lists to hold post and comment data
    posts = []

   # Scrape posts and comments from the specified subreddit
    for submission in reddit.subreddit(subreddit).hot(limit=max_results):
        # Post data
        post_data = {
            'title': submission.title,
            'url': submission.url,
            'upvotes': submission.score,
            'author': submission.author.name if submission.author else None,
            'created_at': submission.created_utc,
            'body': submission.selftext,  # Body of the post (text content)
        }

        # Get comments for the post
        submission.comments.replace_more(limit=0)  # Remove "More comments" to get all comments
        comments = [comment.body for comment in submission.comments.list()]  # List of comment bodies

        # Add the comments as part of the post data
        post_data['comments'] = comments

        posts.append(post_data)

    # Convert the list of posts into a pandas DataFrame
    df = pd.DataFrame(posts)

    print(df.head())

    return df