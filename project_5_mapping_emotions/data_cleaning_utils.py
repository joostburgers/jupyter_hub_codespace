"""
Data Cleaning Utilities for Digital Studies Project 4
====================================================

This module contains utility functions for cleaning and standardizing 
institution data with proper data types and fallback values.

Author: Digital Studies Course
Date: November 2025
"""

import pandas as pd


def clean_institution_dataframe(df):
    """
    Clean and standardize institution data with proper data types and fallback values.
    
    This function performs comprehensive data cleaning including:
    - Converting columns to appropriate data types (strings, dates, floats, booleans)
    - Applying fallback values for empty revised location columns
    - Setting default values for tracking columns
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to clean and standardize. Should contain institution location data
        with columns like: school_name, unique_id, date, sentences, roberta_compound,
        place, latitude, longitude, revised_place, revised_latitude, revised_longitude,
        place_type, false_positive, checked_by
        
    Returns:
    --------
    pandas.DataFrame
        Cleaned DataFrame with standardized data types and fallback values applied.
        The original DataFrame is not modified (a copy is returned).
        
    Example:
    --------
    >>> import pandas as pd
    >>> from data_cleaning_utils import clean_institution_dataframe
    >>> 
    >>> # Load raw data
    >>> df_raw = pd.read_csv('group_data_packets/group_1/python/GMU_processed.csv')
    >>> 
    >>> # Clean the data
    >>> df_clean = clean_institution_dataframe(df_raw)
    >>> 
    >>> # Use the cleaned data for analysis
    >>> print(df_clean.dtypes)
    """
    # Create a copy to avoid modifying the original
    df_cleaned = df.copy()
    
    # String columns (using StringDtype for better handling of missing values)
    string_columns = ['school_name', 'unique_id', 'sentences', 'place', 'revised_place', 'place_type', 'checked_by']
    for col in string_columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].astype(pd.StringDtype())
    
    # Date column
    if 'date' in df_cleaned.columns:
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')
    
    # Float columns
    float_columns = ['roberta_compound', 'latitude', 'longitude', 'revised_latitude', 'revised_longitude']
    for col in float_columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
    
    # Boolean column
    if 'false_positive' in df_cleaned.columns:
        df_cleaned['false_positive'] = df_cleaned['false_positive'].astype('boolean')
    
    # Apply fallback values for empty columns
    # If revised_place is empty, fill with place
    if 'revised_place' in df_cleaned.columns and 'place' in df_cleaned.columns:
        df_cleaned['revised_place'] = df_cleaned['revised_place'].fillna(df_cleaned['place'])
    
    # If revised_latitude is empty, use latitude
    if 'revised_latitude' in df_cleaned.columns and 'latitude' in df_cleaned.columns:
        df_cleaned['revised_latitude'] = df_cleaned['revised_latitude'].fillna(df_cleaned['latitude'])
    
    # If revised_longitude is empty, use longitude
    if 'revised_longitude' in df_cleaned.columns and 'longitude' in df_cleaned.columns:
        df_cleaned['revised_longitude'] = df_cleaned['revised_longitude'].fillna(df_cleaned['longitude'])
    
    # If place_type is empty, set to "Unknown"
    if 'place_type' in df_cleaned.columns:
        df_cleaned['place_type'] = df_cleaned['place_type'].fillna("Unknown")
    
    # If checked_by is empty, set to "Not Checked"
    if 'checked_by' in df_cleaned.columns:
        df_cleaned['checked_by'] = df_cleaned['checked_by'].fillna("Not Checked")
    
    print("DataFrame cleaned successfully!")
    
    return df_cleaned


def get_data_type_summary(df):
    """
    Get a summary of data types in the DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to analyze
        
    Returns:
    --------
    pandas.Series
        Series containing data type information for each column
    """
    return df.dtypes


def get_null_value_summary(df):
    """
    Get a summary of null values in the DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to analyze
        
    Returns:
    --------
    pandas.Series
        Series containing null value counts for each column
    """
    null_counts = df.isnull().sum()
    return null_counts[null_counts > 0] if null_counts.sum() > 0 else pd.Series([], dtype='int64')


def create_location_counts(df, minimum_count=1, place_type_filter=None):
    """
    Group locations by revised_place and count occurrences with optional filtering.
    
    This function aggregates location data by place name and applies optional filters
    for minimum occurrence count and place type categories.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing location data with revised_place, revised_latitude, 
        revised_longitude, and place_type columns
    minimum_count : int, default=1
        Minimum number of occurrences required to include a location
    place_type_filter : list or None, default=None
        List of place types to include (e.g., ['State', 'City', 'University'])
        If None, includes all place types
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with columns: revised_place, count, revised_latitude, 
        revised_longitude, place_type
        
    Example:
    --------
    >>> # Get all locations
    >>> all_locations = create_location_counts(df)
    >>> 
    >>> # Get only frequent locations
    >>> frequent = create_location_counts(df, minimum_count=4)
    >>> 
    >>> # Get only states
    >>> states = create_location_counts(df, place_type_filter=['State'])
    >>> 
    >>> # Get frequent states
    >>> frequent_states = create_location_counts(df, minimum_count=4, place_type_filter=['State'])
    """
    # Group by place and count occurrences
    place_counts = (
        df.groupby("revised_place")
        .agg({
            "revised_place": "count",  # Count occurrences
            "revised_latitude": "first",  # Take first latitude for each place
            "revised_longitude": "first",  # Take first longitude for each place
            "place_type": "first",  # Take first place type
        })
        .rename(columns={"revised_place": "count"})
    )
    
    # Reset index to make 'revised_place' a regular column
    place_counts = place_counts.reset_index()
    
    # Remove places with missing coordinates
    place_counts = place_counts.dropna(subset=["revised_latitude", "revised_longitude"])
    
    # Filter by minimum count
    if minimum_count > 1:
        place_counts = place_counts[place_counts['count'] >= minimum_count]
    
    # Filter by place type if specified
    if place_type_filter is not None:
        place_counts = place_counts[place_counts['place_type'].isin(place_type_filter)]
    
    return place_counts


def create_location_sentiment(df, minimum_count=1, place_type_filter=None):
    """
    Group locations by revised_place and calculate average sentiment with counts.
    
    This function aggregates location data by place name, calculates average sentiment
    scores, and applies optional filters for minimum occurrence count and place type.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing location data with revised_place, revised_latitude, 
        revised_longitude, place_type, and roberta_compound columns
    minimum_count : int, default=1
        Minimum number of occurrences required to include a location
    place_type_filter : list or None, default=None
        List of place types to include (e.g., ['State', 'City', 'University'])
        If None, includes all place types
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with columns: revised_place, count, avg_sentiment, revised_latitude, 
        revised_longitude, place_type
        
    Example:
    --------
    >>> # Get all locations with sentiment
    >>> all_sentiment = create_location_sentiment(df)
    >>> 
    >>> # Get only frequent locations with sentiment
    >>> frequent_sentiment = create_location_sentiment(df, minimum_count=4)
    >>> 
    >>> # Get only states with sentiment
    >>> state_sentiment = create_location_sentiment(df, place_type_filter=['State'])
    >>> 
    >>> # Get frequent states with sentiment
    >>> frequent_state_sentiment = create_location_sentiment(df, minimum_count=4, place_type_filter=['State'])
    """
    # Group by place and calculate counts and average sentiment
    place_sentiment = (
        df.groupby("revised_place")
        .agg({
            "revised_place": "count",  # Count occurrences
            "roberta_compound": "mean",  # Average sentiment
            "revised_latitude": "first",  # Take first latitude for each place
            "revised_longitude": "first",  # Take first longitude for each place
            "place_type": "first",  # Take first place type
        })
        .rename(columns={"revised_place": "count", "roberta_compound": "avg_sentiment"})
        .round({"avg_sentiment": 4})  # Round sentiment to 4 decimal places
    )
    
    # Reset index to make 'revised_place' a regular column
    place_sentiment = place_sentiment.reset_index()
    
    # Remove places with missing coordinates or sentiment
    place_sentiment = place_sentiment.dropna(subset=["revised_latitude", "revised_longitude", "avg_sentiment"])
    
    # Filter by minimum count
    if minimum_count > 1:
        place_sentiment = place_sentiment[place_sentiment['count'] >= minimum_count]
    
    # Filter by place type if specified
    if place_type_filter is not None:
        place_sentiment = place_sentiment[place_sentiment['place_type'].isin(place_type_filter)]
    
    return place_sentiment


def create_time_animation_data(df, window_months=3, minimum_count=2, place_type_filter=None):
    """
    Create time series data with cumulative counts and rolling average sentiment for animation.
    
    This function prepares location data for animated visualizations by creating monthly
    frames with cumulative mention counts and rolling average sentiment scores.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing location data with revised_place, revised_latitude, 
        revised_longitude, date, roberta_compound, and place_type columns
    window_months : int, default=3
        Number of months to use for rolling average sentiment calculation
    minimum_count : int, default=2
        Minimum cumulative count required to include a location in the animation
    place_type_filter : list or None, default=None
        List of place types to include (e.g., ['State', 'City', 'University'])
        If None, includes all place types
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with columns for animation: revised_place, cumulative_count, 
        roberta_compound, revised_latitude, revised_longitude, place_type,
        rolling_avg_sentiment, month, month_num
        
    Example:
    --------
    >>> # Create animation data with 3-month rolling sentiment
    >>> animation_data = create_time_animation_data(df)
    >>> 
    >>> # Create animation data with 6-month rolling sentiment and minimum count
    >>> animation_data_6m = create_time_animation_data(df, window_months=6, minimum_count=5)
    >>> 
    >>> # Create animation data for specific place types only
    >>> animation_states = create_time_animation_data(df, place_type_filter=['State', 'Country'])
    """
    # Ensure we have the required columns and clean data
    df_clean = df.dropna(subset=['revised_place', 'revised_latitude', 'revised_longitude', 'date', 'roberta_compound']).copy()
    
    # Convert date to datetime if not already
    df_clean.loc[:, 'date'] = pd.to_datetime(df_clean['date'])
    
    # Create year-month for grouping
    df_clean.loc[:, 'year_month'] = df_clean['date'].dt.to_period('M')
    
    # Get all unique places and months
    places = df_clean['revised_place'].unique()
    months = sorted(df_clean['year_month'].unique())
    
    # Create animation frames
    animation_data = []
    
    for i, current_month in enumerate(months):
        # Get data up to current month (cumulative)
        cumulative_data = df_clean[df_clean['year_month'] <= current_month]
        
        # Group by place for cumulative counts
        place_stats = cumulative_data.groupby('revised_place').agg({
            'revised_place': 'count',
            'roberta_compound': 'mean',
            'revised_latitude': 'first',
            'revised_longitude': 'first',
            'place_type': 'first'
        }).rename(columns={'revised_place': 'cumulative_count'})
        
        # Calculate rolling average sentiment (last N months)
        start_window = max(0, i - window_months + 1)
        window_months_list = months[start_window:i+1]
        
        rolling_data = df_clean[df_clean['year_month'].isin(window_months_list)]
        rolling_sentiment = rolling_data.groupby('revised_place')['roberta_compound'].mean()
        
        # Convert to DataFrame for easier handling
        place_stats_df = place_stats.reset_index()
        
        # Map rolling sentiment to places
        place_stats_df['rolling_avg_sentiment'] = place_stats_df['revised_place'].map(rolling_sentiment)
        
        # Fill NaN values with the cumulative average sentiment
        mask = place_stats_df['rolling_avg_sentiment'].isna()
        place_stats_df.loc[mask, 'rolling_avg_sentiment'] = place_stats_df.loc[mask, 'roberta_compound']
        
        # Add time information
        place_stats_df['month'] = str(current_month)
        place_stats_df['month_num'] = i
        
        # Only include places with minimum count
        place_stats_df = place_stats_df[place_stats_df['cumulative_count'] >= minimum_count]
        
        # Filter by place type if specified
        if place_type_filter is not None:
            place_stats_df = place_stats_df[place_stats_df['place_type'].isin(place_type_filter)]
        
        animation_data.append(place_stats_df)
    
    # Combine all frames
    if animation_data:
        animation_df = pd.concat(animation_data, ignore_index=True)
    else:
        # Return empty DataFrame with expected columns if no data
        animation_df = pd.DataFrame(columns=[
            'revised_place', 'cumulative_count', 'roberta_compound', 
            'revised_latitude', 'revised_longitude', 'place_type', 
            'rolling_avg_sentiment', 'month', 'month_num'
        ])
    
    return animation_df