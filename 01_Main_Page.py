import pandas as pd
import streamlit as st

from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

from utils import general_data as gd
from utils.process_data import preparing_data

#Declared paths
RAW_FILE_PATH = f"./data/raw/zomato.csv"
RAW_FILE_PATH_SECCONDARY = f"./data/raw/Country-Code.csv"


def create_sidebar(dataframe):
    '''
    Function to generate the sidebar, 
    this will return a list of select countries.

    Output: list(selected_countries)
    '''

    st.sidebar.markdown('# Zomato APP')
    st.sidebar.markdown('## Helping Companies and Customers:')
    st.sidebar.markdown("""---""")

    img_path = './img/'
    image = Image.open(img_path + 'Zomato_logo.png')

    icon_, header_ = st.sidebar.columns([1,6], gap='small')
    icon_.image(image, width=40)
    header_.markdown('# Finding The Best')


    countries =  st.sidebar.multiselect(
        'Choose Which Countries To Analyze:',
        dataframe.loc[:, 'country'].unique().tolist(),
        default=['United Kingdom', 'Brazil', 'South Africa', 'UAE', 'Canada'],
    )

    st.sidebar.markdown('### The data used in this dashboard.')

    st.sidebar.download_button(
        label='Download',
        data=dataframe.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )

    return list(countries)

def create_map(dataframe):
    '''
    Function our main plot with the filters aplied of select countries.
    
    Output: map figure
    '''
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) for two"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)

    
def main():
    '''
    This function is the setup of main page, with built-in functions 
    to create sidebar and the main map.

    This is were our dataframe is generate and saved in our folder.
    '''
    #Config
    st.set_page_config(page_title="Home", page_icon="📊", layout="wide")

    #Data + Creating Sidebar
    df = preparing_data(RAW_FILE_PATH, RAW_FILE_PATH_SECCONDARY)
    selected_countries = create_sidebar(df)

    #Header
    st.markdown('# Zomato APP')
    st.markdown('## The Best APP to Find Your Next Favorite Restaurant!')
    st.markdown('### This are our biggest numbers:')

    #-------------------------------
    # BIG NUMBERS
    #-------------------------------

    restaurants_, countries_, cities_, ratings_, cuisines_ = st.columns(5)

    restaurants_.metric(
        'Registered Restaurants:',
        gd.restaurants_qt(df)
    )

    countries_.metric(
        'Resgistered Countries:',
        gd.countries_qt(df)
    )

    cities_.metric(
        'Registered Cities:',
        gd.cities_qt(df)
    )

    ratings_.metric(
        'How Many Votes:',
        gd.ratings_qt(df)
    )

    cuisines_.metric(
        'Different Cuisines:',
        gd.cuisines_qt(df)
    )

    #-------------------------------
    # MAP
    #-------------------------------

    map_df = df.loc[df["country"].isin(selected_countries), :]

    create_map(map_df)

    return None

if __name__ == '__main__':
    main()