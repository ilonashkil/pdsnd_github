import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Prompts the user to input:
    1. A city (Chicago, New York City, or Washington)
    2. A month (January through June, or "all")
    3. A day of the week (or "all")

    Returns:
        tuple: (city, month, day)
            city (str): Name of the city to analyze
            month (str): Name of the month to filter by, or "all"
            day (str): Name of the day of week to filter by, or "all"
    """
    MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    def get_valid_input(prompt, valid_options):
        while True:
            response = input(prompt).lower()
            if response in valid_options:
                return response
            print(f'Invalid input. Please enter one of: {", ".join(valid_options)}.')
    
    city = get_valid_input(
        'Would you like to see data for Chicago, New York City, or Washington?\n',
        CITY_DATA.keys()
    )
    
    month = get_valid_input(
        'Which month? January, February, March, April, May, June or "all"?\n',
        MONTHS
    )
    
    day = get_valid_input(
        'Which day? Please type a day of the week or "all".\n',
        DAYS
    )

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city to analyze
        month (str): Name of the month to filter by, or "all"
        day (str): Name of the day of week to filter by, or "all"

    Returns:
        pandas.DataFrame: Contains the filtered bikeshare data with additional columns:
            - 'month': Extracted month from Start Time
            - 'day_of_week': Extracted day name from Start Time
            - 'hour': Extracted hour from Start Time
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (pandas.DataFrame): Bikeshare data

    Prints:
        - Most common month
        - Most common day of week
        - Most common start hour
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    # display the most common day of week  
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df (pandas.DataFrame): Bikeshare data

    Prints:
        - Most commonly used start station
        - Most commonly used end station
        - Most frequent combination of start and end stations
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most common end station:', common_end)

    # display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + ' to ' + df['End Station']
    common_combo = df['Station Combo'].mode()[0]
    print('Most common station combination:', common_combo)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (pandas.DataFrame): Bikeshare data

    Prints:
        - Total travel time (in days, hours, minutes)
        - Mean travel time (in minutes)
        - Median travel time (in minutes)
        - Trip duration distribution summary
        - 90th percentile trip duration
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time and convert to days, hours, minutes
    total_seconds = df['Trip Duration'].sum()
    days = total_seconds // (24 * 3600)
    remaining = total_seconds % (24 * 3600)
    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    
    print(f'Total travel time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes')

    # Calculate and display various duration statistics
    mean_mins = df['Trip Duration'].mean() / 60
    median_mins = df['Trip Duration'].median() / 60
    percentile_90 = df['Trip Duration'].quantile(0.9) / 60
    
    print(f'Mean travel time: {mean_mins:.1f} minutes')
    print(f'Median travel time: {median_mins:.1f} minutes')
    print(f'90% of trips are shorter than: {percentile_90:.1f} minutes')

    # Display trip duration distribution
    print('\nTrip Duration Distribution:')
    duration_bins = [0, 10, 20, 30, 60, float('inf')]
    labels = ['0-10 mins', '10-20 mins', '20-30 mins', '30-60 mins', '60+ mins']
    df['duration_category'] = pd.cut(df['Trip Duration'] / 60, bins=duration_bins, labels=labels)
    distribution = df['duration_category'].value_counts().sort_index()
    
    for category, count in distribution.items():
        percentage = (count / len(df)) * 100
        print(f'{category}: {count} trips ({percentage:.1f}%)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df (pandas.DataFrame): Bikeshare data

    Prints:
        - Counts of user types
        - Counts of gender (if available)
        - Earliest, most recent, and most common birth year (if available)
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types 
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types)


    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:\n', gender_counts)
    else:
        print('Gender data not available for this city.')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth year:', earliest_birth)
        print('Most recent birth year:', most_recent_birth)
        print('Most common birth year:', most_common_birth)
    else:
        print('Birth year data not available for this city.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def additional_stats(df):
    """
    Displays additional interesting statistics about the bikeshare data.

    Args:
        df (pandas.DataFrame): Bikeshare data

    Prints:
        - Rush hour analysis (morning and evening trip counts)
        - Average trip duration by user type
        - Longest and shortest trip durations
        - Weekend vs weekday usage statistics
        - Most popular routes by time of day (Morning, Afternoon, Evening, Night)
    """
    print('\nCalculating Additional Statistics...\n')
    start_time = time.time()

    # Calculate rush hour statistics
    print('Rush Hour Analysis:')
    morning_rush = df[df['hour'].between(7, 9)]['hour'].count()
    evening_rush = df[df['hour'].between(16, 18)]['hour'].count()
    print(f'Morning rush hour (7-9 AM) trips: {morning_rush}')
    print(f'Evening rush hour (4-6 PM) trips: {evening_rush}')

    # Calculate average trip duration by user type
    print('\nAverage Trip Duration by User Type:')
    avg_duration = df.groupby('User Type')['Trip Duration'].mean().round(2)
    print(avg_duration)

    # Find the longest and shortest trips
    longest_trip = df['Trip Duration'].max() / 60  # Convert to minutes
    shortest_trip = df['Trip Duration'].min() / 60
    print(f'\nLongest trip: {longest_trip:.2f} minutes')
    print(f'Shortest trip: {shortest_trip:.2f} minutes')

    # Calculate weekend vs weekday usage
    df['is_weekend'] = df['day_of_week'].isin(['saturday', 'sunday'])
    weekend_trips = df[df['is_weekend']]['Start Time'].count()
    weekday_trips = df[~df['is_weekend']]['Start Time'].count()
    print(f'\nWeekend trips: {weekend_trips}')
    print(f'Weekday trips: {weekday_trips}')

    # Find most popular routes during different times of day
    df['time_of_day'] = pd.cut(df['hour'], 
                              bins=[0, 6, 12, 18, 24], 
                              labels=['Night', 'Morning', 'Afternoon', 'Evening'])
    
    print('\nMost Popular Routes by Time of Day:')
    for time_period in ['Morning', 'Afternoon', 'Evening', 'Night']:
        popular_route = df[df['time_of_day'] == time_period]['Station Combo'].mode().iloc[0]
        print(f'{time_period}: {popular_route}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """
    Main function to run the bikeshare data analysis program.
    
    Continuously prompts user for input to analyze bikeshare data
    until the user chooses to exit. For each iteration:
    1. Gets filter preferences from user
    2. Loads and filters the data
    3. Displays various statistical analyses
    4. Asks if user wants to restart
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        additional_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

