import streamlit as st
import utils.cuisines_data as cdt


def create_sidebar(df):
    '''
    Create a sidebar with filter option.

    Return: list of selected countries, how many top and cuisine list
    '''
    st.sidebar.markdown('## Filters')

    countries = st.sidebar.multiselect(
        'Choose Which Countries To Analyze:',
        df.loc[:, 'country'].unique().tolist(),
        default=['United Kingdom', 'Brazil', 'South Africa', 'UAE', 'Canada'],
    )

    top_n = st.sidebar.slider(
        'How Many Restaurants to Show:', 1, 20, 10
    )

    cuisines = st.sidebar.multiselect(
        'Which Cuisine Are You Looking For',
        df.loc[:, 'cuisines'].unique().tolist(),
        default=[
            'Contemporary',
            'Japanese',
            'Brazilian',
            'Arabian',
            'American',
            'Italian',
        ],
    )

    return list(countries), top_n, list(cuisines)


def main():
    st.set_page_config(page_title='Cuisines', page_icon=':knife_fork_plate:', layout='wide')
    st.markdown('# :knife_fork_plate: Cusines Report')
    st.markdown(f'## Best Restaurants Wich of the Main Cuisines:')

    #reading the data
    df = cdt.read_processed_data()
    countries, top_n, cuisines = create_sidebar(df)
    df_restaurants = cdt.top_restaurants(countries, cuisines, top_n)

    #creating metric topic
    cdt.write_metrics()

     # creating the visualizations - table
    st.markdown(f'## Top {top_n} Restaurants')
    df_restaurants = df_restaurants.iloc[:, 2:]
    st.dataframe(df_restaurants.set_index(df_restaurants.columns[0]))
  
    
    best, worst = st.columns(2)

    with best:
        fig = cdt.top_best_cuisines(countries, top_n)

        st.plotly_chart(fig, use_container_width=True)

    with worst:
        fig = cdt.top_worst_cuisines(countries, top_n)

        st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()