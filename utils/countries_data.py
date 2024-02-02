import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#load processed data
def read_processed_data():
    return pd.read_csv('./data/processed/zomato.csv', encoding='latin-1')


#helper function to plot
def plot_bar_graph(dataset, x_col,  y_col, type_of_agg, title, x_label, y_label):
  if type_of_agg == 'count' :
    grouped_df = (
        dataset.loc[:, [y_col, x_col]]
        .groupby(x_col)
        .count()
        .sort_values(y_col, ascending=False)
        .reset_index()
    )

  elif type_of_agg == 'nunique':
    grouped_df = (
        dataset.loc[:, [y_col, x_col]]
        .groupby(x_col)
        .nunique()
        .sort_values(y_col, ascending=False)
        .reset_index()
    )

  elif type_of_agg == 'm':
    grouped_df = (
        dataset
        .groupby(x_col)
        [[y_col]]
        .mean()
        .sort_values(y_col, ascending=False)
        .reset_index()
    )
  else:
    print('Not developed, ask for help.')

  if type_of_agg == 'count' or type_of_agg == 'nunique' :
    fig = px.bar(
        grouped_df,
        x=x_col,
        y=y_col,
        text=y_col,
        title=title,
        labels={
            x_col: x_label,
            y_col: y_label,
        },
    )

  elif type_of_agg == 'm':

    fig = px.bar(
        grouped_df,
        x=x_col,
        y=y_col,
        text=y_col,
        text_auto='.2f',
        title=title,
        labels={
            x_col: x_label,
            y_col: y_label,
        },
    )

  else:
    print('Not developed, ask for help.')

  return fig

########
# Plots
########

def countries_restaurants(countries):
    df = read_processed_data()
    df_filter = df.loc[df['country'].isin(countries), ['restaurant_id', 'country']]

    fig = plot_bar_graph(dataset=df_filter, x_col='country',  y_col='restaurant_id', type_of_agg='count',
                        title='How Many Registered Restaurants by Country',
                        x_label='Country', y_label='Number of Restaurants')

    return fig


def countries_cities(countries):
    df = read_processed_data()
    df_filter = df.loc[df['country'].isin(countries), ['city', 'country']]

    fig = plot_bar_graph(dataset=df_filter, x_col='country',  y_col='city', type_of_agg='nunique',
                        title='How Many Registered Cities by Country',
                        x_label='Country', y_label='Number of Cities')

    return fig

def countries_mean_votes(countries):
    df = read_processed_data()
    df_filter = df.loc[df['country'].isin(countries), ['aggregate_rating', 'country']]

    fig = plot_bar_graph(dataset=df_filter, x_col='country',  y_col='aggregate_rating', type_of_agg='m',
                        title='Which is the Average Rating by Country',
                        x_label='Country', y_label='Average Mean Rating')

    return fig

def countries_average_plate(countries):
    df = read_processed_data()
    df_filter = df.loc[df['country'].isin(countries), ['average_cost_for_two', 'country']]

    fig = plot_bar_graph(dataset=df_filter, x_col='country',  y_col='average_cost_for_two', type_of_agg='m',
               title='Average Cost for Two by Country',
               x_label='Country', y_label='Average Cost for Two')

    return fig


def countires_registered_reviews(countries):
    df = read_processed_data()
    df_filter = df.loc[df['country'].isin(countries), ['votes', 'country']]

    fig = plot_bar_graph(dataset=df_filter, x_col='country',  y_col='votes', type_of_agg='m',
               title='Mean Registered Reviews by Country',
               x_label='Country', y_label='Mean Registered Reviews')

    return fig