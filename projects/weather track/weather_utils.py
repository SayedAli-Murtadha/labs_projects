import pandas as pd
import os
import uuid
from datetime import date, datetime, timedelta

# Define the file name 
CSV_FILE = 'weather_data.csv'

# Global variables 
records = []
DataFrame_records = 0 

def initialize_data():
    """
    Checks if the CSV file exists. If not, creates one and populates it with 
    dummy data so we can test the statistics and display functions.
    Done by SayedAli
    """
    if not os.path.exists(CSV_FILE):
        
        dummy_data = {
            'Date': ['06-25-2022', '06-26-2023', '06-27-2021', '06-28-2023', '06-29-2026'],
            'Temperature': [35.0, 38.5, 34.0, 40.0, 39.0],
            'Conditions': ['Sunny', 'Sunny', 'Cloudy', 'Sunny', 'Rainy'],
            'Humidity': [40, 45, 60, 35, 70],
            'Wind_Speed': [15, 20, 10, 25, 5]
        }
        df = pd.DataFrame(dummy_data)
        df.to_csv(CSV_FILE, index=False)
        print("--> Created new weather_data.csv file with sample data for testing.")
    else:
        print("--> Existing weather data loaded successfully.")

def display_menu():
    """Displays the main menu options to the user.
    Done by Sayedali"""
    print("\n  WEATHER TRACKER MENU  ")
    print("1. Record a new weather observation")
    print("2. View weather statistics")
    print("3. Search observations by date")
    print("4. View all observations")
    print("5. View Record-Breaking Tempratures")
    print("6. Exit Application")

def record_observation():
    """
    After user chose to record a new observation, he is permitted to input 
    date with 1 cycle for error and then setting todays date.
    Done by Qaem
    """
    print("\n[ Recording a New Observation ]")
    
    global DataFrame_records
    
    observation_date = input("Input the date of the observation in (MM-DD-YYYY): ")
    try:
        if not observation_date:
            raise ValueError  # if user inputs nothing
        observation_date = datetime.strptime(observation_date, "%m-%d-%Y").date()
    except ValueError:
        print("Invalid input. You have 1 more attempt before proceeding to today's date.")
        observation_date = input("Input the date of the observation in (MM-DD-YYYY): ").strip()
        try:
            if not observation_date:
                raise ValueError
            observation_date = datetime.strptime(observation_date, "%m-%d-%Y").date()
        except ValueError:
            observation_date = datetime.now().date()
            print(f"Invalid format entered again. Proceeding with default date of today: {observation_date.strftime('%m-%d-%Y')}")
            
    # Temperature input to make sure user inputs a float/integer
    while True:
        temperature = input('Input the temperature in (Degrees Celsius): ')
        if not temperature:
            print("Temperature cannot be empty. Please enter a value (float/integer).")
            continue
        try:
            temperature = float(temperature)
            break
        except ValueError:
            print("Invalid input. Please enter a valid value for temperature.")
            
    # Weather condition Input to make sure user inputs one of the 4 possible weather conditions
    valid_conditions = ['sunny', 'cloudy', 'rainy', 'snowy']
    while True:
        condition = input('Input the weather condition (Sunny, Cloudy, Rainy, Snowy): ').strip().lower()
        if not condition:
            print("Condition cannot be empty. Please enter a value.")
            continue
        if condition in valid_conditions:
            break
        else:
            print("Invalid condition. Please type one of these: Sunny, Cloudy, Rainy, Snowy.")
    
    # Humidity input to make sure user inputs a valid input between 1-100
    while True:
        humidity = input('Input the humidity percentage: ')
        if not humidity:
            print('Humidity cannot be empty please enter a value between 1 & 100.')
            continue
        if humidity.isdigit() and 1 <= int(humidity) <= 100:
            break
        else:
            print('Invalid input. Please enter a valid value for humidity (1 - 100).')

    # Wind Speed input to make sure user inputs a float/integer
    while True:
        wind_speed = input('Input the wind speed in (km/h): ')
        if not wind_speed:
            print("Wind speed cannot be empty. Please enter a value.")
            continue
        try:
            wind_speed = float(wind_speed)
            break
        except ValueError:
            print("Invalid input. Please enter a valid value for wind speed (float/integer).")

    # Storing of the user inputs into a dictionary
    
    data = {
        'Date': observation_date.strftime("%m-%d-%Y"),
        'Temperature': temperature,
        'Conditions': condition.capitalize(),
        'Humidity': f"{humidity}%",
        'Wind_Speed': wind_speed,
    }
    
    # Appending to the existing CSV file so it's compatible with the rest of the application
    pd.DataFrame([data]).to_csv(CSV_FILE, mode='a', header=False, index=False)
    
    records.append(data)
    print('Observation Data successfully saved')

    DataFrame_records = pd.DataFrame(records)


def search_by_date():
    """After user chose to search by date, he is permitted to input a date
    Done by Qaed"""
    print("\n[ Search Observations by Date ]")
    search_date=input(f'Input a date to search for in (MM-DD-YYYY): ')
    try:
        if not search_date:
            raise ValueError  #if user inputs nothing
        search_date = datetime.strptime(search_date, "%m-%d-%Y").date()
    except ValueError:
        print(f'Invalid date format or empty. Please enter a date with format MM-DD-YYYY')
        return
        
    # Read from CSV and convert to dict format seamlessly identical to the dummy_data logic
    try:
        df = pd.read_csv(CSV_FILE)
        # We transform the Date column back to datetime.date objects for precise matching logic
        df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y', errors='coerce').dt.date
        dataset = df.to_dict('records')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        dataset = []

    searched_records=[]

    for i in dataset:
        if i['Date'] == search_date:
           searched_records.append(i) 

    if searched_records:
        print(f'Found observations for {search_date}')
        for j in searched_records:
            print(f"Condition:{j['Conditions']} ")
            print(f"Temp:{j['Temperature']}°C")
            print(f"Humidity:{j['Humidity']}")
            print(f"Wind Speed:{j['Wind_Speed']} km/h")
    else:
        print(f'No observation found for the date: {search_date}')
    
def view_statistics():
    """
    Calculates and displays min, max, avg temperatures, and common conditions.
    Done by SayedAli
    """
    print("\n[  Weather Statistics ]")
    
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print("   Error: The weather_data.csv file is missing. Please restart the app.")
        return
    except pd.errors.EmptyDataError:
        print("   Error: The file is empty.")
        return

    required_columns = ['Date', 'Temperature', 'Conditions']
    for col in required_columns:
        if col not in df.columns:
            print(f"  Error: Missing '{col}' column in the dataset.")
            return
            
    # Convert dates and extract Year/Month
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month   
    
    # 1. FILTER BY MONTH 
    try:
        ask_input = input("Do you want to filter by month? (y/n): ")
        if ask_input.strip().lower() == "y":
            month_input = int(input("What month? (1-12): "))
            if not (1 <= month_input <= 12):
                print("Not a valid month, showing everything instead.")
            else:
                df = df[df['Month'] == month_input]
                print(f"Filtering the data based on the specified month! ({month_input})")
    except ValueError:
        print("  Invalid input. Showing all months instead.")

    if df.empty:
        print("  No weather records found matching your criteria.")
        return          
        
    def print_stats(data_frame, title):
        if data_frame.empty:
            return None
            
        avg_temp = data_frame['Temperature'].mean()
        max_temp = data_frame['Temperature'].max()
        min_temp = data_frame['Temperature'].min()
        
        modes = data_frame['Conditions'].mode()
        if not modes.empty:
            common_cond = modes[0]
        else:
            common_cond = 'Unknown'
            
        print(f"\n--- {title} ---")
        print(f"  Average Temp:      {avg_temp:.2f}°")
        print(f"  Max Temperature:   {max_temp:.2f}°")
        print(f"  Min Temperature:   {min_temp:.2f}°")
        print(f"  Common Conditions: {common_cond}")
        
        return avg_temp 
        
    # Calling the function so users actually see the general stats!
    print_stats(df, "Current Filtered Summary")

    #  2. COMPARE YEARS
    # Safe conversion to standard Python integers
    available_years = sorted(int(y) for y in df['Year'].dropna().unique())
    
    # Ask user 
    compare_input = input(f"\nCompare a year against previous years? Available: {available_years}\n(y/n or enter year directly): ").strip().lower()
    
    target_year = None
    
    # If the user bypasses y/n and types the year directly
    if compare_input.isdigit():
        target_year = int(compare_input)
    # If the user properly answers 'y' or 'yes'
    elif compare_input.startswith('y'):
        try:
            target_year = int(input("Enter the target year: "))
        except ValueError:
            print("  Invalid number entered.")
            
    if target_year is not None:
        if target_year in available_years:
            compare_df = df[df['Year'] <= target_year].copy()
            
            compare_df['Period'] = compare_df['Year'].apply(lambda y: f"{target_year}" if y == target_year else "Previous Years")
            
            stats_table = compare_df.groupby('Period')['Temperature'].agg(['mean', 'max', 'min']).round(2)
            
            print(f"\n[ Temperature Comparison for {target_year} vs Previous ]")
            print(stats_table)
            
        else:
            print("  Year not found in dataset. Showing overall stats instead.")
            print("\n[ Overall Statistics ]")
            print(df['Temperature'].agg(['mean', 'max', 'min']).round(2))
    else:
        print("\n[ Overall Statistics ]")
        # Simple command to just show stats if they don't want to compare
        print(df['Temperature'].agg(['mean', 'max', 'min']).round(2))
        
def view_all_observations():
    """
    Displays the entire dataset of weather observations.
    Done by Qaed
    """
    print("\n[  All Weather Observations ]\n")
    df = pd.read_csv(CSV_FILE)
    
    if df.empty:
        print(" No data available. Please record an observation first.")
    else:
        print(df.to_string())
        
        remove_input = input("\ninput the index number you would like to remove from the observation list (Press Enter if you dont want to remove any data): ")
        if not remove_input:
            print('Remove cancelled')
            return
        
        try:
            remove_index = int(remove_input)
            if remove_index not in df.index:
                raise ValueError
            
            df = df.drop(index=remove_index)
            df.to_csv(CSV_FILE, index=False)
            print("The selected observation data has been removed")
        except ValueError:
            print('invalid index entered, no data is removed')

def Record_breaking():
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print(" No data available. Please record an observation first.")
    else:
        target_column = 'Temperature'
        q1 = df['Temperature'].quantile(0.25)
        q3 = df['Temperature'].quantile(0.75)
        iqr = q3 - q1
        lowest = q1 - (iqr * 1.5)
        highest = q3 + (iqr * 1.5)
        outliers = df[(df['Temperature'] < lowest) | (df['Temperature'] > highest)]
        
        if outliers.empty:
            print("There are no outliers!")
        else:
            print(outliers)

#  MAIN APP LOOP 

def run_app():
    """
    Main function to run the Weather Tracker application.
    Done by SayedAli
    """
    initialize_data()
    
    while True:
        display_menu()
        user_choice = input("Please select an option (1-6): ").strip()
        
        if user_choice == '1':
            record_observation()
        elif user_choice == '2':
            view_statistics()
        elif user_choice == '3':
            search_by_date()
        elif user_choice == '4':
            view_all_observations()
        elif user_choice == '5':
            Record_breaking()
        elif user_choice == '6':
            print("\n Exiting Weather Tracker. Have a great day! ")
            break
        else:
            print("\n Invalid selection. Please type a number between 1 and 6.")
