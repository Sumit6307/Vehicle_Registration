import pandas as pd
import numpy as np

def load_category_data():
    df = pd.read_csv('data/category_registrations.csv')
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    # Map vehicle_category to 2W/3W/4W (dummy data already uses 2W/3W/4W)
    df['category'] = df['vehicle_category']  # No mapping needed for dummy data
    df = df[df['category'].isin(['2W', '3W', '4W'])]
    # Handle non-finite values in year and month
    df = df.dropna(subset=['year', 'month'])  # Drop rows with NaN
    df = df[~df['year'].isin([np.inf, -np.inf])]  # Drop rows with inf
    df = df[~df['month'].isin([np.inf, -np.inf])]
    # Convert year and month to integers
    df['year'] = df['year'].astype(float).astype(int)  # Handle float to int
    df['month'] = df['month'].astype(float).astype(int)
    # Ensure month is between 1 and 12
    df = df[df['month'].between(1, 12)]
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-01')
    return df

def load_manufacturer_data():
    df = pd.read_csv('data/manufacturer_registrations.csv')
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    # Handle non-finite values in year and month
    df = df.dropna(subset=['year', 'month'])  # Drop rows with NaN
    df = df[~df['year'].isin([np.inf, -np.inf])]  # Drop rows with inf
    df = df[~df['month'].isin([np.inf, -np.inf])]
    # Convert year and month to integers
    df['year'] = df['year'].astype(float).astype(int)  # Handle float to int
    df['month'] = df['month'].astype(float).astype(int)
    # Ensure month is between 1 and 12
    df = df[df['month'].between(1, 12)]
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-01')
    return df

def calculate_growth(df, group_by_col, time_level='Y'):
    if time_level == 'Y':
        freq = 'Y'
    elif time_level == 'Q':
        freq = 'Q'
    else:
        raise ValueError("Invalid time_level")
    
    agg = df.groupby([pd.Grouper(key='date', freq=freq), group_by_col])['registrations'].sum().reset_index()
    agg = agg.sort_values(['date', group_by_col])
    agg['previous'] = agg.groupby(group_by_col)['registrations'].shift(1)
    agg['growth'] = ((agg['registrations'] - agg['previous']) / agg['previous']) * 100
    agg = agg.dropna()
    return agg