import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = ''
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        city = input("Which city do you want to get the data from, Chicago, New York City, or Washington?\n")
        print('Please check the city or the format you entered!\n')

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input("Which month do you want to filter by, January, February, March, April, May, June, or all (no filter)?\n").lower()
        print('Please check the month or the format you entered!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = -1
    while int(day) not in range(0,7):
        day = int(input("Which day, or all (no filter)? Please enter your response as integer (e.g. 0=Monday)\n"))
        print('Please check the day or the format you entered!\n')

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
    print('\nLoading data...\n')
    df = pd.read_csv(CITY_DATA[city])

    # convert start time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day from start time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    # filter by month
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    if month != 'all':
        df = df[df['month'] == months[month]]

    # filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    # display the most common day of week
    day_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    popular_day_index = df['day_of_week'].mode()[0]
    popular_day = day_of_week[popular_day_index]
    print(f"\nMost Popular Day: {popular_day}")

    # display the most common start hour

    # extract hour
    df['hour'] = df['Start Time'].dt.hour
    popular_start = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_start}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")

    # display the most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station: {common_end_station}")

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    comb = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {comb}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()

    # finds duration in minutes and seconds
    minute, second = divmod(total_duration, 60)
    
    # finds duration in hour and minutes
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    # finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    # this filter prints the time if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"The types of users by number are :\n{user_type}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are :\n{gender}")
    except:
        print("\nThere is no 'Gender' column in the file.")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no 'Birth Year' column in this file.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to display data per user's request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city when user requested it.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    RESPONSE_LIST = ['yes', 'no']
    res = ''
    # counter variable store row index
    counter = 0
    while res not in RESPONSE_LIST:
        print("\nDo you want to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        res = input().lower()

        if res == "yes":
            print(df.head())
        elif res not in RESPONSE_LIST:
            print("\nPlease check your input again.")
            print("\nRestarting...\n")

    # ask user if want to view data again
    while res == 'yes':
        counter += 5
        res = input("Do you want to view more raw data?").lower()
        # If user wants, this displays next 5 rows of data
        if res == "yes":
            print(df[counter:counter+5])
        else:
            break

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
