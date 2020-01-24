import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }
MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6}
DAY_DATA = {'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please input city name. Options are "chicago", "new york city", or "washington": ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('City is invalid! Options are "chicago", "new york city", or "washington": ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please input month name. Options are "all", "january", "february", "march", "april", "may", "june": ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Month is invalid! Options are "all", "january", "february", "march", "april", "may", "june": ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please input day of week. Options are "all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday": ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Day is invalid! Options are "all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday": ').lower()
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Create day_of_week and month columns
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == MONTH_DATA[month]]      
        
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == DAY_DATA[day]]
    
    return df

#gets the name of the month or day
def get_name(dictionary,val):
    for key, value in dictionary.items():
        if val == value:
            return key

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: {}".format(get_name(MONTH_DATA,df['month'].mode().values[0]).capitalize()))

    # display the most common day of week
    print("The most common day of the week: {}".format(get_name(DAY_DATA,df['day_of_week'].mode().values[0]).capitalize()))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour: {}".format(str(df['start_hour'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {} ".format(df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print("The most common end station is: {}".format(df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " ==> " + df['End Station']
    print("The most common start and end station combo is: {}".format(df['routes'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("The total travel time is: {}".format(str(df['duration'].sum())))

    # display mean travel time
    print("The mean travel time is: {}".format(str(df['duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here are the counts of various user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print("Here are the genders:")
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print("The earliest birth year is: {}".format(str(int(df['Birth Year'].min()))))
        print("The latest birth year is: {}".format(str(int(df['Birth Year'].max()))))
        print("The most common birth year is: {}".format(str(int(df['Birth Year'].mode().values[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data"""
    start = 0
    end = 5
    display_raw = input("Do you want to see the raw data? (yes/no): ")
    
    while display_raw == "yes" or display_raw == "y":
        print(df.iloc[start:end])
        start += 5
        end += 5
        display_raw = input("Would you like to see more raw data? Enter yes or no.\n")
    
def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()