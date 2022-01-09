from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np

'''
Task : 1) Which state has the most shooting incidents
2) Employed/Unemployed
3) Race Distribution
4) Reason for shooting
'''


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
    print(df_shootings_mental.columns)

    vals_to_replace = {'Unknown': 'Unclear', 'unknown': 'Unclear'}
    df_shootings_mental['Mental Health Issues'].replace(vals_to_replace,
                                                        regex=True,
                                                        inplace=True)

    print(df_shootings_mental['Race'].unique())
    print(df_shootings_mental['Gender'].unique())

if __name__ == '__main__':
    main()
