import pandas as pd
import re
import numpy as np

def check_is_nan(value):
    if pd.isnull(value) or value == "":
        return np.nan

def clean_price(price_str):
    """
    Cleaning the price to display as a numeric value instead of string.

    Args:
        price_str: str
            string representation of the price
    Returns:
        Float: Numerical value of the price
    """
    check_is_nan(price_str)

    clean = re.sub(r'[$,\s]', '', str(price_str))
    try:
        return float(clean)
    except:
        return np.nan

def clean_numeric_field(value):
    """
    convert other numeric string fields to numeric values

    Args:
        value (str): string value of the field

    returns:
        float: numeric value of the field or NaN if invalid
    """
    check_is_nan(value)
    cleaned = re.sub(r'[$,\s]', '', str(value))
    try:
        return float(cleaned)
    except ValueError:
        return np.nan
def clean_year_built(year_built):
    """
    Validate and clean the year build column

    Args:
        year_str: String representation of the year built


    Returns:
        Int: valid year built or NaN
    """
    check_is_nan(year_built)
    try:
        year = int(year_built)
        if year <= 1800 <= year <= current_year +2:
            return year
            "This is to verify that it is a reasonable year"
        return np.nan
    except ValueError:
        return np.nan

def clea_lot_size(lot_size_str):
    """
    Clean the lot size field to return numeric value in square feet

    Args:
        lot_size_str: str
            string representation of the lot size

    Returns:
        Float: Numeric value of the lot size in square feet
    """
    check_is_nan(lot_size_str)

    lot_size_str = str(lot_size_str).lower().strip()

    numbers = re.findall(r'[\d.]+', lot_size_str)
    if not numbers:
        return np.nan

    value = float(numbers[0])

    if 'ac' in lot_size_str or 'acre' in lot_size_str:
        return lot_size_str
    elif 'sq' in lot_size_str or 'ft' in lot_size_str:
        "an acre is 4350"
        return value /43560
    else:
        return value
        "We're assuming acres if there is not unit specified"

def clean_garage(garage_str):
    """
    Extracting the number of garages

    Args:
        garage_str: string representation of the garage

    Returns:
        int: number of garages or 0 if none/invalid
    """
    check_is_nan(garage_str)

    numbers = re.findall(r'\d+', str(garage_str))
    if numbers:
        return int(numbers[0])
    return 0

def remove_agent(agent_str):
    pd.drop(columns=[agent_str], inplace=True)
    return pd

def clean_address(address_str):
    """
    Standardize the address column

    Args:
        address_str: String representation of the address

    Returns:
        str: cleaned address string
    """
    check_is_nan(address_str)

    cleaned = re.sub(r'\s+', ' ', str(address_str)).strip()
    cleaned = re.sub(r',\s*,', ',', cleaned)
    cleaned = cleaned.strip(',').strip()

    return cleaned


def clean_city(city_str):
    check_is_nan(city_str)
    return city_str.lower().strip()

def clean_housing_data(df):
    """
    Applying all the clenaing functions to the dataframe

    Args:
        df: pandas DataFrame with the raw housing data

    Returns:
        Pandas DataFrame with cleaned data
    """

    df_clean = df.copy()
    if 'agent' in df_clean.columns:
        df_clean = remove_agent(df_clean)
    if 'price' in df_clean.columns:
        df_clean['price'] = df_clean['price'].apply(clean_price)
    if 'year_built' in df_clean.columns:
        df_clean['year_built'] = df_clean['year_built'].apply(clean_year_built)
    if 'lot_size' in df_clean.columns:
        df_clean['lot_size'] = df_clean['lot_size'].apply(clea_lot_size)
    if 'garage' in df_clean.columns:
        df_clean['garage'] = df_clean['garage'].apply(clean_garage)
    if 'address' in df_clean.columns:
        df_clean['address'] = df_clean['address'].apply(clean_address)
    if 'city' in df_clean.columns:
        df_clean['city'] = df_clean['city'].apply(clean_city)
    return df_clean

def remove_duplicates(df, subset=['mls_number']):
    """
    Remove duplicate entries from the dataframe using the MLS number as the unique identifier

    Args:
        df: Pandas DataFrame with housing data

    Returns:
        Pandas DataFrame: DataFrame with duplicates removed
    """

    return df.drop_duplicates(subset=subset, keep='first')

def remove_invalid_entries(df):
    """
    Remove rows with critical missing data


    Args:
        df: Pandas DataFrame with housing data

    Returns:
        pandas DataFrame: DataFrame with invalid entries removed
    """

    critical_fields = ['mls','price','address']

    for field in critical_fields:
        df = df[df[field].notna()]
        if field == 'price':
            df = df[df['price'] > 0]
    return df

def get_cleaned_data(max_listings=5, cities=None, output='pandas'):
    """
    Get housing data and do cleaning automatically


    Args:
        max_listings (int) Maximum number of listings to fetch
        cities List of cities to fetch to scrape (None = all cities)
        output = pandas or csv


    Returns:
        Pandas or CSV DataFrame: Cleaned housing data
    """
    from utah_housing_stat286.core import get_data

    df_raw = get_data(max_listings=max_listings, cities=cities, output='pandas')

    df_clean = clean_housing_data(df_raw)
    df_clean = remove_invalid_entries(df_clean)
    df_clean = remove_duplicates(df_clean)

    if output == 'pandas':
        return df_clean
    elif output == 'csv':
        df_clean.to_csv("utah_housing_data_cleaned.csv",index=False)
        return "Data saved to utah_housing_data_cleaned.csv"
    else:
        raise ValueError("Invalid output option. Choose 'pandas' or 'csv'.")







