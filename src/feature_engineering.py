import pandas as pd


def create_features(df):
    """
    Create only required features for prediction
    """

    df = df.copy()

    # Example: Month extraction if Date provided
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month

    return df