import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def validate_input(prompt, options):
    """
    Asks user for input, and checks it is valid
    
    Args:
        (str) prompt to display to user 
        (array of str) options for valid user input

    Returns:
        (str) the validated user input 
    """

    while True:
        selection = input(prompt).lower()
        if selection in options:
            print("")
            return selection
        else:
            print("\nInvalid input.  Please select from the following options:")
            print(options)
            print("")
        


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
    city = validate_input("Please enter the city you want to filter for: ", list(CITY_DATA.keys()))

    # get user input for month (all, "january, february, ... , june)
    month = validate_input("Please enter the month you want to filter for (or 'all'): ", ["january", "february", "march", "april", "may", "june", "all"])
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = validate_input("Please enter the day of the week you want to filter for (or 'all'): ", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"])

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
    
    # Get filepath to CSV
    csv_path = './' + CITY_DATA[city]

    # Import the data and do initial cleanup
    df = pd.read_csv(csv_path, index_col=0)
    df.sort_index(axis=0, inplace=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')

    # extract month and day of week from Start Time to create new columns
    df['start_hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek #Note this counts up from Monday = 0 to Sunday = 6.

    # Create new column including the start and end station combinaton
    df["Station Combination"] = df["Start Station"] + " / " + df["End Station"]

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_no = MONTHS.index(month) + 1
        df = df[df['month']==month_no]

    # filter by day if applicable
    if day != 'all':
        # use the index of the months list to get the corresponding int
        day_no = DAYS.index(day.title())
        df = df[df['day_of_week']==day_no]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is:')
    print(MONTHS[df['month'].mode()[0] -1 ])
    print("")

    # display the most common day of week
    print('The most common day of the week is:')
    print(DAYS[df['day_of_week'].mode()[0]])
    print("")

    # display the most common start hour
    print('The most common start hour is:')
    print(df['start_hour'].mode()[0])
    print("")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is:')
    print(df['Start Station'].mode()[0])
    print("")

    # display most commonly used end station
    print('The most commonly used end station is:')
    print(df['End Station'].mode()[0])
    print("")

    # display most frequent combination of start station and end station trip
    print('The most common start / end station combination is:')
    print(df['Station Combination'].mode()[0])
    print("")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time for all journeys is:')
    print(str(df['Trip Duration'].sum()) + ' seconds')
    print("")

    # display mean travel time
    print('The mean travel time across journeys is:')
    print(str(df['Trip Duration'].mean()) + ' seconds')
    print("")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The breakdown of user types is:')
    print(df.groupby(['User Type'])['User Type'].count())
    print("")

    # Display counts of gender (if present in the dataset)
    if 'Gender' in df:
        print('The breakdown of user gender is:')
        print(df.groupby(['Gender'])['Gender'].count())
        print("")
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
        print("")


    # Display earliest, most recent, and most common year of birth (if present in the dataset)
    if 'Birth Year' in df:
        print("The minimum, maximum and most common birth years for users are:")
        print(str(df["Birth Year"].min()))
        print(str(df["Birth Year"].max()))
        print(str(df["Birth Year"].mode()[0]))
        print("")
    else:
        print('Birth year stats cannot be calculated because birth year does not appear in the dataframe')
        print("")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = validate_input('\nWould you like to restart? Enter yes or no.\n', ['yes', 'no'])
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
