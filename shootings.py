from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np


def get_data():
    """
    get_data uses Kaggle's API to fetch the required dataset.
    """
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file('zusmani/us-mass-shootings-last-50-years', 'Mass Shootings Dataset Ver 5.csv')


def main():
    # get_data()
    raw_dataframe = pd.read_csv('Mass%20Shootings%20Dataset%20Ver%205.csv', sep=',', encoding='latin-1')
    df_shootings = raw_dataframe.copy()
    '''
     Deleted:
     1) S# Column - abundant column
     2) Incident Area Column - Interested state-wise
     3) Open/Close Location - Not relevant
     4) Summary - too long and not relevant
     5) Title - same as 4
     6) Employeed Y/N - Not much data
     7) Employed at - same as 6
    '''
    df_shootings = df_shootings.drop(['S#', 'Incident Area', 'Open/Close Location',
                                      'Target', 'Summary', 'Title', 'Employeed (Y/N)', 'Employed at'],
                                     axis=1)
    '''
    Fixing Date type object
    '''
    # Checkpoint - Date
    df_shootings_mod = df_shootings.copy()
    df_shootings_mod['Date'] = pd.to_datetime(df_shootings_mod['Date'], format='%m/%d/%Y')

    '''
    Get a list of year of each incident and add it to the modded dataframe.
    '''
    list_year = []
    for row in range(df_shootings_mod.shape[0]):
        list_year.append(df_shootings_mod['Date'][row].year)

    df_shootings_mod['Year Value'] = list_year

    '''
    Combine domestic dispute + domestic disputer
    replaced nan with unknown
    '''
    # Checkpoint - Cause
    df_shootings_cause = df_shootings_mod.copy()

    df_shootings_cause['Cause'].replace('domestic disputer', 'domestic dispute', inplace=True)
    df_shootings_cause['Cause'].replace(np.nan, 'unknown', inplace=True)

    # Checkpoint - Total Victims
    df_shootings_total_victims = df_shootings_cause.copy()
    df_shootings_total_victims.rename({'Total victims': 'Total Victims'}, axis=1, inplace=True)

    '''
    nan changed to 0
    converted from float to int
    '''
    df_shootings_total_victims['Policeman Killed'].replace(np.nan, 0.0, inplace=True)
    df_shootings_total_victims['Policeman Killed'] = df_shootings_total_victims['Policeman Killed'].apply(np.int64)

    # Checkpoint - Age
    df_shootings_age = df_shootings_total_victims.copy()
    df_shootings_age['Age'].replace(np.nan, -1, inplace=True)
    df_shootings_age['Age'].replace('0', -1, inplace=True)

    # Checkpoint - Mental Health Issues
    df_shootings_mental = df_shootings_age.copy()
    mental_dict = {'Unknown': 'Unclear', 'unknown': 'Unclear'}
    df_shootings_mental['Mental Health Issues'].replace(mental_dict,
                                                        regex=True,
                                                        inplace=True)

    # Checkpoint - Race
    df_shootings_race = df_shootings_mental.copy()
    race_dict = {np.nan: "Unknown", "Other": "Unknown", "Black American or African American": "Black",
                 "White American or European American": "White", "Asian American": "Asian",
                 "Some other race": "Unknown",
                 "Two or more races": "Mixed", "Black American or African American/Unknown": "Black",
                 "White American or European American/Some other Race": "White",
                 "Native American or Alaska Native": "Native American",
                 "white": "White", "black": "Black", "Asian American/Some other race": "Asian"}
    df_shootings_race['Race'].replace(race_dict, inplace=True)

    # Checkpoint - Gender
    df_shootings_gender = df_shootings_race.copy()
    gender_dict = {"M": "Male", "M/F": "Unknown", "Male/Female": "Unknown"}
    df_shootings_gender['Gender'].replace(gender_dict, inplace=True)

    # Checkpoint
    df_shootings_final = df_shootings_gender.copy()
    df_shootings_final.insert(0, 'City', df_shootings_final['Location'].str.split(',', expand=True)[0])
    df_shootings_final.insert(1, 'State', df_shootings_final['Location'].str.split(',', expand=True)[1])
    df_shootings_final.drop('Location', inplace=True, axis=1)

    # Create processed CSV file
    df_shootings_final.to_csv("us_shootings_processed.csv", sep=',')


if __name__ == '__main__':
    main()
