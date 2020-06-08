# python bikeshare.py
import time
import pandas as pd
import numpy as np
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city
    city = input('Which city would you like to explore? Chicago, New York City or Washington? \n')
    if city.lower() not in ['chicago', 'new your city', 'washington']:
        city = input('You have to explore one of the following: Chicago, New York City or Washington. \n')

    # TO DO: get user input for month (all, january, february, ... , june)
    global month
    month = input('Which month would you like to explore? All, January, February, March, April, May or June? \n')
    if month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('You have to explore one of the following: All, January, February, March, April, May or June. \n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    global day
    day = input(
        'Which day would you like to explore? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? \n')
    if day.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input(
            'You have to explore one of the following: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. \n')

    print('-' * 40)
    return city.lower(), month.lower(), day.lower()


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month != 'all':
        most_common_month = df['month'].mode()[0]
        print('The most common month: ', most_common_month)

    # TO DO: display the most common day of week
    if day != 'all':
        mc_day_of_week = df['day_of_week'].mode()[0]
        print('The most common day: ', mc_day_of_week)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    mc_hour = df['hour'].mode()[0]
    print('The most common start hour: ', mc_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().sort_index(ascending=False).head(1)
    print('The most common start station:\n', start_station)

    # TO DO: display most commonly used end station
    common_endst = df['End Station'].value_counts().sort_index(ascending=False).head(1)
    print('The most commonly used end station:\n', common_endst)

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_concat'] = df['Start Station'] + " - " + df['End Station']
    common_start_end = df['start_end_concat'].value_counts().sort_index(ascending=False).head(1)
    print('The most frequent combination of start station and end station trip:\n', common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_t = df['Trip Duration'].sum()
    print('The total travel time: ', int(tot_t), ' seconds')

    # TO DO: display mean travel time
    mean_t = df['Trip Duration'].mean()
    print('The mean travel time: ', int(mean_t), ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print('The types of users:\n', user_types)

    # TO DO: Display counts of gender
    if city == 'washington':
        print('\nThere is no data about gender distribution\n')
    else:
        gend_c = df['Gender'].value_counts()
        print('\nThe gender distribution:\n', gend_c)

    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nThere is no data about the year of birth\n')


    else:
        earliest_birth = df.groupby(['Birth Year'])['Birth Year'].min().min()
        recent_birth = df.groupby(['Birth Year'])['Birth Year'].max().max()
        common_birth = df['Birth Year'].value_counts().sort_index(ascending=False).head(1)
        print('\nThe earliest year of birth:\n', int(earliest_birth))
        print('\nThe most recent year of birth:\n', int(recent_birth))
        print('\nThe most common year of birth:\n', common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # raw data
        raw = input('Would you like to see raw bikeshare data? '
                    'Enter yes or no: ').lower()
        df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        rows = 5
        while raw == 'yes':
            print(json.dumps(df.head(rows).to_dict('index'), indent=1))
            raw = input('Would you like to see more '
                        'bikeshare data? Enter yes or no: ').lower()
            rows += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
