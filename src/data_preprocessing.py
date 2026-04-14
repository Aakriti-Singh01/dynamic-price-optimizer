def clean_input_data(df):
    """
    Minimal cleaning for input data (used in app)
    """
    df = df.copy()

    # Fill missing safely
    df['CompetitionDistance'] = df['CompetitionDistance'].fillna(50000)

    return df