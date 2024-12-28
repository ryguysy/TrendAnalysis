import pandas as pd
from database import get_stock_data, get_options_data

def preprocess_stock_data(stock_df):
    """Clean and preprocess the stock DataFrame."""
    # Ensure the date column is in datetime format
    stock_df.index = pd.to_datetime(stock_df.index)
    
    # Example: Handle missing values
    stock_df.ffill()  # Forward fill

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





'''

post preprocessing

'''

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import re

def clean_post(post):
    """
    Cleans the post text by removing URLs, mentions, hashtags, emojis, and special characters.

    Args:
        post (str): The raw post text.

    Returns:
        str: The cleaned post text.
    """
    post = re.sub(r"http\S+|www\S+|https\S+", '', post, flags=re.MULTILINE)  # Remove URLs
    post = re.sub(r"@\w+|#\w+", '', post)  # Remove mentions and hashtags
    post = re.sub(r"[^a-zA-Z\s]", '', post)  # Remove special characters and emojis
    post = post.lower()  # Convert to lowercase
    return post.strip()

def analyze_sentiment(posts_df):
    """
    Performs sentiment analysis on a DataFrame of posts.

    Args:
        posts_df (pd.DataFrame): DataFrame with a 'text' column containing post texts.

    Returns:
        pd.DataFrame: The original DataFrame with added sentiment scores and labels.
    """
    sia = SentimentIntensityAnalyzer()

    # Clean the posts
    posts_df['cleaned_text'] = posts_df['text'].apply(clean_post)

    # Apply VADER for sentiment analysis
    posts_df['sentiment_score'] = posts_df['cleaned_text'].apply(lambda x: sia.polarity_scores(x)['compound'])

    # Add sentiment labels
    posts_df['sentiment_label'] = posts_df['sentiment_score'].apply(
        lambda score: 'positive' if score > 0.05 else ('negative' if score < -0.05 else 'neutral')
    )

    return posts_df

def aggregate_daily_sentiment(posts_df):
    """
    Aggregates sentiment metrics for a single day.

    Args:
        posts_df (pd.DataFrame): DataFrame with sentiment analysis results.

    Returns:
        dict: Dictionary of aggregated sentiment metrics (counts and averages).
    """
    total_posts = len(posts_df)
    positive_count = len(posts_df[posts_df['sentiment_label'] == 'positive'])
    neutral_count = len(posts_df[posts_df['sentiment_label'] == 'neutral'])
    negative_count = len(posts_df[posts_df['sentiment_label'] == 'negative'])

    avg_sentiment_score = posts_df['sentiment_score'].mean()

    return {
        'total_posts': total_posts,
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'avg_sentiment_score': avg_sentiment_score
    }