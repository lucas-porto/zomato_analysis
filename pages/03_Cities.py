import streamlit as st    
import utils.cities_data as cdt

def create_sidebar(dataframe):
    '''
    Create a sidebar with filter option.

    Return: list of selected countries
    '''
    st.sidebar.markdown('## Filters')

    countries =  st.sidebar.multiselect(
        'Choose Which Countries To Analyze:',
        dataframe.loc[:, 'country'].unique().tolist(),
        default=['United Kingdom', 'Brazil', 'South Africa', 'UAE', 'Canada'],
    )
    return list(countries)

def main():
    st.set_page_config(page_title='Cities', page_icon=':city_sunset:', layout='wide')
    st.markdown('# :city_sunset: Cities Report')
        
    #reading the data
    df = cdt.read_processed_data()
    countries = create_sidebar(df)

    # creating the visualizations
    fig = cdt.top_cities_restaurants(countries)
    st.plotly_chart(fig, use_container_width=True)

    top_, worst_ = st.columns(2)
    with top_:
        fig = cdt.top_bests_restaurants(countries)

        st.plotly_chart(fig, use_container_width=True)

    with worst_:
        fig = cdt.top_worsts_restaurants(countries)

        st.plotly_chart(fig, use_container_width=True)

    fig = cdt.top_cusines_restaurants(countries)
    st.plotly_chart(fig, use_container_width=True)

    return None

if __name__ == '__main__':
    main()