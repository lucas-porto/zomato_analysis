import streamlit as st    
import utils.countries_data as cdt

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
    st.set_page_config(page_title='Countries', page_icon=':earth_americas:', layout='wide')
    st.markdown('# :earth_americas: Country Report')

    #reading the data
    df = cdt.read_processed_data()
    countries = create_sidebar(df)

    # creating the visualizations
    fig = cdt.countries_restaurants(countries)
    st.plotly_chart(fig, use_container_width=True)

    fig = cdt.countries_cities(countries)
    st.plotly_chart(fig, use_container_width=True)

    fig = cdt.countires_registered_reviews(countries)
    st.plotly_chart(fig, use_container_width=True)

    fig = cdt.countries_mean_votes(countries)
    st.plotly_chart(fig, use_container_width=True)


#    plate_price_, votes_ = st.columns(2)
    
#    with plate_price_:
#        fig = cdt.countires_registered_reviews(countries)

#        st.plotly_chart(fig, use_container_width=True)

#    with votes_:
#        fig = cdt.countries_mean_votes(countries)

#        st.plotly_chart(fig, use_container_width=True)
    
    return None

if __name__ == '__main__':
    main()