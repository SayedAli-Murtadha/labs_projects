import pandas as pd
import os
from datetime import datetime

CSV_FILE = 'weather_data.csv'

def initialize_data():
    """Creates dummy data if CSV doesn't exist."""
    if not os.path.exists(CSV_FILE):
        dummy_data = {
            'Date': ['06-25-2022', '06-26-2023', '06-27-2021', '06-28-2023', '06-29-2026'],
            'Temperature': [35.0, 38.5, 34.0, 40.0, 39.0],
            'Conditions': ['Sunny', 'Sunny', 'Cloudy', 'Sunny', 'Rainy'],
            'Humidity': ['40%', '45%', '60%', '35%', '70%'],
            'Wind_Speed': [15.0, 20.0, 10.0, 25.0, 5.0]
        }
        pd.DataFrame(dummy_data).to_csv(CSV_FILE, index=False)

def get_all_data():
    """Helper to load the current CSV file."""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_observation(date_obj, temperature, condition, humidity, wind_speed):
    """Saves a new observation to the CSV."""
    data = {
        'Date': date_obj.strftime("%m-%d-%Y"),
        'Temperature': float(temperature),
        'Conditions': condition.capitalize(),
        'Humidity': f"{humidity}%",
        'Wind_Speed': float(wind_speed),
    }
    pd.DataFrame([data]).to_csv(CSV_FILE, mode='a', header=False, index=False)

def search_by_date_logic(search_date_obj):
    """Searches observations by a specific date."""
    df = get_all_data()
    if df.empty:
        return []
    
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y', errors='coerce').dt.date
    searched = df[df['Date'] == search_date_obj]
    return searched.to_dict('records')

def delete_observation(index_to_remove):
    """Removes an observation by its dataframe index."""
    df = get_all_data()
    if index_to_remove in df.index:
        df = df.drop(index=index_to_remove)
        df.to_csv(CSV_FILE, index=False)
        return True
    return False

def get_record_breaking():
    """Calculates outliers based on IQR."""
    df = get_all_data()
    if df.empty:
        return pd.DataFrame()
    
    q1 = df['Temperature'].quantile(0.25)
    q3 = df['Temperature'].quantile(0.75)
    iqr = q3 - q1
    lowest = q1 - (iqr * 1.5)
    highest = q3 + (iqr * 1.5)
    
    outliers = df[(df['Temperature'] < lowest) | (df['Temperature'] > highest)]
    return outliers