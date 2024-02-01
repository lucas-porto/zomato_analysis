import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#load processed data
def read_processed_data():
    return pd.read_csv('./data/processed/zomato.csv', encoding='latin-1')

## Plots Functions
def top_cities_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df['country'].isin(countries), ['restaurant_id', 'country', 'city']]
        .groupby(['country', 'city'])
        .count()
        .sort_values(['restaurant_id', 'city'], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(10),
        x='city',
        y='restaurant_id',
        text='restaurant_id',
        color='country',
        title='Top 10 Cities With Registered Restaurants',
        labels={
            'city': 'Cities',
            'restaurant_id': 'Number of Restaurants',
            'country': 'Country',
        },
    )

    return fig


def top_bests_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[
                ((df['aggregate_rating'] >= 4) & (df['country'].isin(countries))),
                ['restaurant_id', 'country', 'city']
                ]
        .groupby(['country', 'city'])
        .count()
        .sort_values(['restaurant_id', 'city'], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x='city',
        y='restaurant_id',
        text='restaurant_id',
        color='country',
        title='Top 7 Cities Boasting Restaurants with Ratings Exceeding 4',
        labels={
            'city': 'Cities',
            'restaurant_id': 'Number of Restaurants',
            'country': 'Country',
        },
    )

    return fig


def top_worsts_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[
                ((df['aggregate_rating']  <= 2.5) & (df['country'].isin(countries))),
                ['restaurant_id', 'country', 'city']
                ]
        .groupby(['country', 'city'])
        .count()
        .sort_values(['restaurant_id', 'city'], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x='city',
        y='restaurant_id',
        text='restaurant_id',
        color='country',
        title='Top 7 Cities Boasting Restaurants with Ratings Bellow 2.5',
        labels={
            'city': 'Cities',
            'restaurant_id': 'Number of Restaurants',
            'country': 'Country',
        },
    )

    return fig

def top_cusines_restaurants(countries):
    df = read_processed_data()

    grouped_df = (
        df.loc[df['country'].isin(countries), ['cuisines', 'country', 'city']]
        .groupby(['country', 'city'])
        .count()
        .sort_values(['cuisines', 'city'], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(10),
        x='city',
        y='cuisines',
        text='cuisines',
        color='country',
        title='Top 10 Cities With Registered Restaurants With Most Variable Cuisines',
        labels={
            'cuisines': 'Cusines',
            'city': 'City',
            'country': 'Country',
        },
    )

    return fig