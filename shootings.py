from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np

pd.set_option('display.width', 320)
np.set_printoptions(linewidth=320)
pd.set_option('display.max_columns', 20)


# TODO : 1) Fix Gender
# TODO : 2) Fix Unemployed
# TODO : 3) Remove rows without location (Latitude + Longitude)
# TODO : 4) Change date to proper form
# TODO : 5) Change nan -> unknown


def get_data():
    """
    get_data uses Kaggle's API to fetch the required dataset.
    """
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file('zusmani/us-mass-shootings-last-50-years', 'Mass Shootings Dataset Ver 5.csv')


if __name__ == '__main__':
    # get_data()
    raw_dataframe = pd.read_csv('Mass%20Shootings%20Dataset%20Ver%205.csv', sep=',', encoding='latin-1')
    df_shootings = raw_dataframe.copy()
    # print(df_shootings.head())
    # print(df_shootings.describe())
    # print(df_shootings.nunique())
    print(df_shootings.loc[:1])
