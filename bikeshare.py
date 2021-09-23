"Script by Andrew Bean"
"Date: 9/21/2021"
"Bikeshare database - Project 2"
"Udacity - Intro to Data Science with Python"

import time
import pandas as pd
import numpy as np
import datetime as dt
import click

CITY_DATA = {'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv'}
MONTH = ('january', 'february', 'march', 'april', 'may', 'june')
DAY = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday')

def decision(prompt, choices=('y', 'n')):
    "Check to see if user input is valid"
    
    while True:
        choice = input(prompt).lower().strip()
        
        # close the program
        if choice == 'end':
            raise SystemExit
        
        # one choice
        elif ',' not in choice:
            if choice in choices:
                break
        
        # multiple choices
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break
        prompt = ("\nThere was an error. Please try again:\n>")
    return choice

def get_filters():
    "Prompt user to input cities, filters, months, and weekdays. Returns strings."
    
    print('Hello! Let\'s explore some US bikeshare data!')
    print('To exit at any time, type end.\n')
    while True:
        city = decision("\nWhich city or cities are you interested in: New York City, Chicago or Washington? Please use commas if more than one.\n>", CITY_DATA.keys())
        month = decision("\nWhich month or months would you like to explore (Jan-Jun)? Please use commas if more than one.\n>", MONTH)
        day = decision("\nWhich weekday(s) do you wish to filter by? Please use commas if more than one.\n>", DAY)
        
        # confirmation
        confirm_prompt = decision("\nPlease confirm your choice of filter.\n\n City(ies): {}\n Month(s): {}\n Weekday(s): {}\n\n [y] Yes\n [n] No\n\n>".format(city, month, day))
        if confirm_prompt == 'y':
            break
        else:
            print("\nError, please try again.")
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    "Load data dependent on user-chosen filters for cities, months, and weekdays. All arguements are strings. Returns Pandas dataframe."
    
    print("\nYour choices have been entered. The program is now loading.")
    start_time = time.time()
    
    # filtering the data
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        
        # data reorganization
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time','Trip Duration', 'Start Station','End Station', 'User Type', 'Gender','Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])
    
    # stat columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    
    # month and weekday filter
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (MONTH.index(month)+1)], month))
    else:
        df = df[df['Month'] == (MONTH.index(month)+1)]
    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]
    print("\nDuration:{} seconds.".format((time.time() - start_time)))
    print('-'*40)
    return df

def time_stats(df):
    "Shows statistics for most common times of travel"
    
    print('\nStatistics on the most frequent times of travel...\n')
    start_time = time.time()
    
    # month
    most_common_month = df['Month'].mode()[0]
    print('The month with most travel is: ' + str(MONTH[most_common_month-1]).title() + '.')
    
    # weekday
    most_common_day = df['Weekday'].mode()[0]
    print('The most common weekday is: ' + str(most_common_day) + '.')
    
    # hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' + str(most_common_hour) + '.')
    print("\nDuration:{} seconds.".format((time.time() - start_time)))
    print('-'*40)

def station_stats(df):
    "Shows statistics for most common stations and trip."
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # most common start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " + most_common_start_station)
    
    # most common end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common end station is: " + most_common_end_station)
    
    # most common combo of start and end station
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("The most common combination of start-end stations is " + most_common_start_end_combination)
    print("\nDuration:{} seconds.".format((time.time() - start_time)))
    print('-'*40)

def trip_duration_stats(df):
    "Shows statistics for trip duration as average and total."
    
    print('\nCalculating duration of trip...\n')
    start_time = time.time()
    
    # travel time - total
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) + 'd ' + str(int((total_travel_time % 86400)//3600)) + 'h ' + str(int(((total_travel_time % 86400) % 3600)//60)) + 'm ' + str(int(((total_travel_time % 86400) % 3600) % 60)) + 's')
    print('The total travel time is : ' + total_travel_time + '.')
    
    # travel time - average
    avg_travel_time = df['Trip Duration'].mean()
    avg_travel_time = (str(int(avg_travel_time//60)) + 'm ' + str(int(avg_travel_time % 60)) + 's')
    print("The average travel time is : " + avg_travel_time + ".")
    print("\nDuration:{} seconds.".format((time.time() - start_time)))
    print('-'*40)

def user_stats(df, city):
    "Shows bikeshare user statistics."
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # user types
    user_types = df['User Type'].value_counts().to_string()
    print("User type distribution:")
    print(user_types)
    
    # gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nGender distribution:")
        print(gender_distribution)
    except KeyError:
        print("No data exists for user genders for {}.".format(city.title()))
    
    # birth years
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nThe oldest bikerider was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("The youngest bikerider was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("The mmajority of bikeriders were born in: " + most_common_birth_year)
    except:
        print("No data exists for birth year of {}.".format(city.title()))
    print("\nDuration:{} seconds.".format((time.time() - start_time)))
    print('-'*40)

def data(df, pause):
    "Displays 5 rows of data at a time."
    
    print("\nDisplaying raw data.")
    
    # if the user paused
    if pause > 0:
        last_place = decision("\nWould you like to continue where you left off? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            pause = 0
    
    # column sort
    if pause == 0:
        sort_df = decision("\nPlease choose how you wish to sort the data. Hit Enter to view unsorted.\n \n [st] Start Time\n [et] End Time\n [td] Trip Duration\n [ss] Start Station\n [es] End Station\n\n>", ('st', 'et', 'td', 'ss', 'es', ''))
        as_de = decision("\nDo you wish to sort ascensing or descending? \n [a] Ascending\n [d] Descending \n\n>", ('a', 'd'))
        if as_de == 'a':
            as_de = True
        elif as_de == 'd':
            as_de = False
        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=as_de)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=as_de)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=as_de)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=as_de)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=as_de)
        elif sort_df == '':
            pass
    
    # prompt for 5 lines of data
    while True:
        for i in range(pause, len(df.index)):
            print("\n")
            print(df.iloc[pause:pause+5].to_string())
            print("\n")
            pause += 5
            if decision("Would you like to display more data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break
    return pause

def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        pause = 0
        while True:
            select_data = decision("\nWhich data would you like to view?\n\n [ts] Time Stats\n [ss] Station Stats\n [tds] Trip Duration Stats\n [us] User Stats\n [rd] Display Raw Data\n [r] Restart\n\n>", ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                pause = data(df, pause)
            elif select_data == 'r':
                break
        restart = decision("\nRestart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()