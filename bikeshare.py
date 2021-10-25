import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
print('Hello there! Let\'s explore some US bikeshare data!\n')

def get_filters():

    #Asks user to specify a city, month, and day to analyze and filter data accordingly.
    """
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # This is to get user input for city (chicago, new york city, washington).
    # And to check user's input validity
    while True:
        city = input('Please choose city:\nChicago, New York City or Washington\n')
        city = city.lower()
        if city in ['chicago','new york city','washington']:
            break
        else:
                print('Sorry! City\'s data is not available\nPlease try again\n')

    # This is to get user input for Months and to check user's input validity
    while True:
        month = input('Please select Month for filteration:\n\'from January to June\' or just type \'all\' for all months data\n')
        month = month.lower()
        months = ['all','january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            break
        else:
            print('Sorry! Month\'s data is not available\nPlease try again\n')

    # This is to get user input for Months and to check user's input validity
    while True:
        day=input('Please select day for filteration or just type \'all\' for all days selection\n')
        day=day.lower()
        days = ['all','sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday']
        if day in days:
            break
        else:
            print('Sorry! Entered day is not correct\nPlease try again\n')

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
    #read data from CSV file based on user's selection
    df = pd.read_csv(CITY_DATA[city])
    # To replace NaN values with the previous values in the column
    df.fillna(method = 'ffill', axis = 0, inplace=True)
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #Month filtering
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    # To show raw data as per user's selected data
    for i in range(0,df.shape[0],5):
        show=input("Do you want to show raw data as per your selection ? Enter yes or no.\n")
        if show.lower()=='yes':
            filter_message=('Filters selected by user are for\nCity: {}, Month: {}, Weekday: {}\n')
            print(filter_message.format(city.title(),month,day.title()))
            print(df.iloc[i:i+5,1:])

        else:
            print('\nMoving on to calculation stats ----->')
            break
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Popular Month:', months[popular_month-1].title())

    #Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day of the week:', popular_day)

    #Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # Display most frequent combination of start station and end station trip
    combination=df.groupby(['Start Station'])['End Station'].value_counts()
    print('Combination counts of start station and end station:\n',combination)
    print('\nWith most frequent combination of:\n',df.groupby(['Start Station'])['End Station'].value_counts().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_hhh=str(total_travel_time//3600) #to caluclate how many hours in the total trip duration
    total_mmm=str((total_travel_time%3600)//60) #to caluclate how many remaining minutes in the total trip duration
    total_sss=str((total_travel_time%3600)%60) #to caluclate how many remaining seconds in the total trip duration
    total_travel_time_result_message=["{} hours {} mins {} seconds".format(total_hhh, total_mmm, total_sss)]
    print('Total Travel Time as per user\'s selected data:')
    print(total_travel_time_result_message)

    # Display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    avg_hhh=str(average_travel_time//3600) #to caluclate how many hours in the average trip duration
    avg_mmm=str((average_travel_time%3600)//60) #to caluclate how many remaining minutes in the average trip duration
    avg_sss=str((average_travel_time%3600)%60) #to caluclate how many remaining seconds in the average trip duration
    average_travel_time_result_message=["{} hours {} mins {} seconds".format(avg_hhh, avg_mmm, avg_sss)]
    print('\nAverage Travel Time as per user\'s selected data:')
    print(average_travel_time_result_message)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of Users Types as per selected data:\n',user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Classification of users genders as per selected data:\n',gender)
    else:
        print('\n<<< Sorry! Gender data is not available for this city >>>\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year= df['Birth Year'].min()
        earliest_age = 2021-earliest_year
        earliest_gender =df[df['Birth Year'] == earliest_year]['Gender'].mode()[0]
        print('\nThe earliest (oldest) users\' year of birth as per selected data: ', earliest_year)
        print('With the age of: ',earliest_age)
        print('and of the gender majority of: ',earliest_gender)

        youngest_year=df['Birth Year'].max()
        youngest_age=2021-youngest_year
        youngest_gender = df[df['Birth Year'] == youngest_year]['Gender'].mode()[0]
        print('\nThe youngest users\' year of birth as per selected data: ', youngest_year)
        print('With the age of: ',youngest_age)
        print('and of the gender majority of: ',youngest_gender)

        common_birth_year = df['Birth Year'].mode()[0]
        common_age=2021-common_birth_year
        common_gender = df[df['Birth Year'] == common_birth_year]['Gender'].mode()[0]
        print('\nThe most common users\' year of birth as per selected data: ', common_birth_year)
        print('With the age of: ',common_age)
        print('and of the gender majority of: ',common_gender)
    else:
        print('\n<<< Sorry! Birth Year data is not available for this city >>>')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
