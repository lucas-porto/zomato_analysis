import pandas as pd

from .process_data import preparing_data


def restaurants_qt(dataframe):
    return dataframe.restaurant_id.shape[0]


def countries_qt(dataframe):
    return dataframe.country.nunique()


def cities_qt(dataframe):
    return dataframe.city.nunique()


def ratings_qt(dataframe):
    return dataframe.votes.sum()


def cuisines_qt(dataframe):
    return dataframe.cuisines.nunique()