import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def read_processed_data():
     return pd.read_csv('./data/processed/zomato.csv', encoding='latin-1')


def top_cuisines():
    df = read_processed_data()

    cuisines = {
        'Italian': '',
        "American": '',
        "Arabian": '',
        "Japanese": '',
        "Brazilian": '',
    }

    cols = [
        'restaurant_id',
        "restaurant_name",
        "country",
        "city",
        'cuisines',
        "average_cost_for_two",
        "currency",
        "aggregate_rating",
        'votes',
    ]

    for key in cuisines.keys():

        lines = df['cuisines'] == key

        cuisines[key] = (
            df.loc[lines, cols]
            .sort_values(["aggregate_rating", 'restaurant_id'], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines


def write_metrics():

    cuisines = top_cuisines()

    italian, american, arabian, japonese, brazilian = st.columns(len(cuisines))

    with italian:
        st.metric(
            label=f'Italian: {cuisines["Italian"]["restaurant_name"]}',
            value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
            help=f'''
            Country: {cuisines["Italian"]["country"]}\n
            City: {cuisines["Italian"]["city"]}\n
            Average Cost for two: {cuisines["Italian"]["average_cost_for_two"]} ({cuisines["Italian"]["currency"]})
            ''',
        )

    with american:
        st.metric(
            label=f'American: {cuisines["American"]["restaurant_name"]}',
            value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
            help=f'''
            Country: {cuisines["American"]["country"]}\n
            City: {cuisines["American"]["city"]}\n
            Average Cost for two: {cuisines["American"]["average_cost_for_two"]} ({cuisines["American"]["currency"]})
            ''',
        )

    with arabian:
        st.metric(
            label=f'Arabian: {cuisines["Arabian"]["restaurant_name"]}',
            value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
            help=f'''
            Country: {cuisines["Arabian"]["country"]}\n
            City: {cuisines["Arabian"]["city"]}\n
            Average Cost for two: {cuisines["Arabian"]["average_cost_for_two"]} ({cuisines["Arabian"]["currency"]})
            ''',
        )

    with japonese:
        st.metric(
            label=f'Japanese: {cuisines["Japanese"]["restaurant_name"]}',
            value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
            help=f'''
            Country: {cuisines["Japanese"]["country"]}\n
            City: {cuisines["Japanese"]["city"]}\n
            Average Cost for two: {cuisines["Japanese"]["average_cost_for_two"]} ({cuisines["Japanese"]["currency"]})
            ''',
        )

    with brazilian:
        st.metric(
            label=f'Brazilian: {cuisines["Brazilian"]["restaurant_name"]}',
            value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
            help=f'''
            Country: {cuisines["Brazilian"]["country"]}\n
            City: {cuisines["Brazilian"]["city"]}\n
            Average Cost for two: {cuisines["Brazilian"]["average_cost_for_two"]} ({cuisines["Brazilian"]["currency"]})
            ''',
        )

    return None


def top_restaurants(countries, cuisines, top_n):
    df = read_processed_data()

    cols = [
        'restaurant_id',
        "restaurant_name",
        "country",
        "city",
        'cuisines',
        "average_cost_for_two",
        "aggregate_rating",
        'votes',
    ]

    lines = (df['cuisines'].isin(cuisines)) & (df["country"].isin(countries))

    dataframe = df.loc[lines, cols].sort_values(
        ["aggregate_rating", 'restaurant_id'], ascending=[False, True]
    )

    return dataframe.head(top_n)


def top_best_cuisines(countries, top_n):
    df = read_processed_data()

    lines = df["country"].isin(countries)

    grouped_df = (
        df.loc[lines, ["aggregate_rating", 'cuisines']]
        .groupby('cuisines')
        .mean()
        .sort_values("aggregate_rating", ascending=False)
        .reset_index()
        .head(top_n)
    )

    fig = px.bar(
        grouped_df.head(top_n),
        x='cuisines',
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto='.2f',
        title=f'Top {top_n} Best Cuisines',
        labels={
            'cuisines': 'Cuisine',
            "aggregate_rating": 'Aggregate Rating',
        },
    )

    return fig


def top_worst_cuisines(countries, top_n):
    df = read_processed_data()

    lines = df["country"].isin(countries)

    grouped_df = (
        df.loc[lines, ["aggregate_rating", 'cuisines']]
        .groupby('cuisines')
        .mean()
        .sort_values("aggregate_rating", ascending=True)
        .reset_index()
        .head(top_n)
    )

    fig = px.bar(
        grouped_df.head(top_n),
        x='cuisines',
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto='.2f',
        title=f'Top {top_n} Worst Cuisines',
        labels={
            'cuisines': 'Cuisine',
            "aggregate_rating": 'Aggregate Rating',
        },
    )

    return fig