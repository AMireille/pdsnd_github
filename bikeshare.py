"""
This script aim to analyse bikeshare statistical information 
for three USA cities being Chicago,New york city and Washington.
"""
import pandas as pd
import numpy as np
import time

# The dictionary below includes files corresponding to each of the city
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def filter_func(filt):
    """
    This function is receiving an input as either city or month or day.
    It request the further input related to the previous input and
    check if it is one of the available data then return it for further process.
    If the new inputs are not available,it request for new entry.
    """
        
    if (filt=='city'):
        inputs=(input("Which city would like to analyse? chicago,washington or new york city?: ")).lower()
        while(inputs not in (CITY_DATA.keys())):
            print('The name provided is not available, please check and try again')
            inputs=(input("Which city would like to analyse? chicago,washington or new york city?: ")).lower()
    elif (filt=='month'):
        inputs=int(input("which month would you like to analyse,choose the number:\n 1.January\n 2.February\n 3.March\n 4.April\n 5.May\n 6.June\n 7.July\n 8.August\n 9.September\n 10.Octobe\n 11.November\n 12.December\n"))
        while(inputs not in [1,2,3,4,5,6,7,8,9,10,11,12]):
            print('The choice you have made is not available. please check and try again.')
            inputs=int(input("which month would you like analyse,choose the number:\n 1.January\n 2.February\n 3.March\n 4.April\n 5.May\n 6.June\n 7.July\n 8.August\n 9.September\n 10.October\n 11.November\n 12.December\n"))
    elif(filt=='day'):
        inputs=(input("which day of the week would like to analyse:'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday': ")).title()
        while(inputs not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']):
            print('The choice you have made is not available. please check and try again.')
            inputs=(input("which day of the week would like to analyse:'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday': ")).title()
    return inputs 

def get_filters():

    
    """"
    Receive the city and type of filters to be used  for analysis.
    
    Returns:
    * city : string in lower case
    * month: integer 
    * day: string in title case
    if one of the filter is not applied a string 'all' is returned.
    
    """
    #Start by declaring default value for the month and day filters
    month='all'
    day='all'
    # Get the city to be analysed
    print("Time to analyse statistical data of some US city bikeshare. Let's start")
    city=filter_func('city')
    print()
    print("Now that the city chosen is {}, let check other filters to use.".format(city))
    filters=(input("Would like to filter by month,day,all or none: ")).lower()
    if (filters=='month'):
        month=filter_func('month')
    elif(filters=='day'):
        day=filter_func('day')
    elif(filters=='all'):
        month=filter_func('month')
        day=filter_func('day')
    return city,month,day
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (integer) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and/or day
    """
    if(city =='new york city'):
        file='new_york_city.csv'
    else:
        file=city +'.csv'
    df=pd.read_csv(file)

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['days']= df['Start Time'].dt.day_name()
    df['months']=df['Start Time'].dt.month
    df['hour']=df['Start Time'].dt.hour
    
    if (month!='all' and day!='all'):
        df=df[(df['months']==month)& (df['days']==day)]

    elif (month!='all' and day=='all'):
        df=df[(df['months']==month)]
    elif(month=='all' and day!='all'):
        df=df[(df['days']==day)]
        
    return df
def display_data(df):
    """"
    Display 5 new rows of data at a time until the user enter 'no'.
    
    args:
    df-filtered data
    """
    view_data = (input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')).lower()
    start_loc = 0
    while (view_data=='yes'):
        if((start_loc+5)< len(df)):
            print(df.iloc[start_loc:(start_loc+5)])
            start_loc += 5
            view_data = (input("Do you wish to continue to see other 5 rows of individual trip data?:")).lower()
        elif((start_loc+5)==len(df)):
            print(df.iloc[start_loc:(start_loc+5)])
            print("Rows are over.Continue to the next step.")
            break
        else:
            print("There are no remaining 5 unviewed rows remaining but here are the remaining rows:")
            print(df.iloc[start_loc:])
            print("Now that you have explored all rows,continue to the next step.")
            break
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
    df: filtered dataframe
    """

    print('\nCalculating The Most Frequent Times of Travel:\n')
    start_time = time.time()

    # display the most common month
    month=['none','January','February','March','April','May','June',
           'July','August','September','October','November','December']
    #print("see:",df['months'].mode())
    if(len(df['months'].mode())==1):
        print("The most common month is",month[df['months'].mode()[0]])
    else:
        print("The most common month are:",end=" ")
        for nber in range(len(df['months'].mode())):
            print(month[df['months'].mode()[nber]],end=",")
        print()

    # Display the most common day of week
    print("The most common day of the week is:",df['days'].mode()[0])

    # Display the most common start hour

    if(len(df['hour'].mode())==1):
        print("The most common start hour is",df['hour'].mode()[0])
    else:
        print("The most common start hours are:")
        for nber in range(len(df['hour'].mode())):
            print("{}. {}".format((nber+1),df['hour'].mode()[nber]))
        print()
    #print("The most common start hours are\n",df['Start Time'].mode())
    #print("len:",len(df['Start Time'].mode()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
    df- filtered dataframe
    """
    print('\nCalculating The Most Popular Stations and Trip\n')
    start_time = time.time()

    # Display most commonly used start station
    if(len(df['Start Station'].mode())==1):
        print("The most common start station is",df['Start Station'].mode()[0])
    else:
        print("The most common start stations are:",end=" ")
        for nber in range(len(df['Start Station'].mode())):
            print(df['Start Station'].mode()[nber],end=",")
        print()

    # Display most commonly used end station
    if(len(df['End Station'].mode())==1):
        print("The most common end station is",df['End Station'].mode()[0])
    else:
        print("The most common end stations are:",end=" ")
        for nber in range(len(df['End Station'].mode())):
            print(df['End Station'].mode()[nber],end=",")
        print()
    #print("The most common end station is",df['End Station'].mode())
    #Display most frequent combination of start station and end station trip
    print("The most combination of start station and end station is {} and {}".format(df[['Start Station','End Station']].mode()['Start Station'][0],
                                                                                     df[['Start Station','End Station']].mode()['End Station'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    args:
    df-filtered dataframe
    """

    print('\nCalculating Trip Duration:\n')
    start_time = time.time()

    #Display total travel time
    print("The total travel time is",df['Trip Duration'].sum())

    #Display mean travel time
    print("The average travel time is",df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    args:
    df-filtered dataframe
    """

    print('\nCalculating User Statistics:\n')
    start_time = time.time()

    #Display counts of user types
    print("User types counts are:\n",df['User Type'].value_counts())
    print()
    if ('Gender' in df.columns):
        # Display counts of gender
        print("User gender counts are:\n",df['Gender'].value_counts())
        print()
        #Display earliest, most recent, and most common year of birth
        print("The earliest year of birth is:",int(min(df["Birth Year"])))
        print("The most recent year of birth is:",int(max(df["Birth Year"])))
        print("The most common year of birth is:",int(df["Birth Year"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # The following condition will let know the user that the filters applied lead to an empty dataframe.
        if (df.empty):
            print("There are no data corresponding to the filters you applied.")
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            display_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                print("The analysis is over. Thank you!!")
                break
            
                



if __name__ == "__main__":
	main()
