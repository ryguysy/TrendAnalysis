import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import pickle

def prepare_lstm_data(df, lookback=60):
    """
    Prepares the stock data for LSTM model training.
    
    Args:
    df (pd.DataFrame): The stock data DataFrame.
    lookback (int): The number of days to look back for LSTM input.

    Returns:
    np.array: The feature data for LSTM.
    np.array: The target data for LSTM.
    """
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

    X_train, y_train = [], []
    for i in range(lookback, len(scaled_data)):
        X_train.append(scaled_data[i-lookback:i, 0])
        y_train.append(scaled_data[i, 0])
    
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    
    return X_train, y_train, scaler

def build_lstm_model(input_shape):
    """
    Builds an LSTM model for stock price prediction.
    
    Args:
    input_shape (tuple): The shape of the LSTM input data.

    Returns:
    Sequential: The LSTM model.
    """
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

if __name__ == "__main__":
    # Load preprocessed data
    df = pd.read_csv('../data/preprocessed_stock_data.csv', index_col='Date', parse_dates=True)

    # Prepare data for LSTM
    X_train, y_train, scaler = prepare_lstm_data(df)

    # Build and train LSTM model
    lstm_model = build_lstm_model((X_train.shape[1], 1))
    lstm_model.fit(X_train, y_train, batch_size=1, epochs=1)

    # Save the trained LSTM model
    lstm_model.save('../models/lstm_model.h5')

    # Save the scaler for future use (for scaling test data)
    with open('../models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print("LSTM model and scaler saved to ../models/")