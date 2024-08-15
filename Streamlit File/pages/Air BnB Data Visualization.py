import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

st.title('Data Exploration')

@st.cache_data
def load_clean_data():
    return pd.read_csv('airbnb_clean.csv')

# Load the data
df = load_clean_data()

# Checkbox to show clean data
if st.checkbox('Show Clean data'):
    st.subheader('AirBnB Dataset Clean')
    st.write(df)

list_of_country = df['country'].unique().tolist()
list_of_country.insert(0, "All")

st.subheader('Scatterplot Price and Total Beds')

region_select = st.selectbox('Select region:', list_of_country)

@st.cache_data
def visualize_scatterplot(country):
    if country == 'All':
        fig = px.scatter(df, x = 'beds', y = 'price_fix', color = 'guests')
        st.plotly_chart(fig, theme = 'streamlit')
    else: 
        df_select = df[df['country'] == country]
        fig = px.scatter(df_select, x = 'beds', y = 'price_fix', color = 'guests')
        st.plotly_chart(fig, theme = 'streamlit')        

visualize_scatterplot(region_select)

st.subheader('Price Boxplot for Listing around the world')

@st.cache_data
def visualize_boxplot():
    # Identify the top 10 countries based on the number of listings
    top_countries = df['country'].value_counts().nlargest(10).index

    # Filter the DataFrame to include only the top 10 countries
    df_top_countries = df[df['country'].isin(top_countries)]

    tab1, tab2 = st.tabs(['By Rating', 'By Country'])
    with tab1:
        fig = px.box(df, x='rating', y='price_fix')
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    with tab2:
        fig = px.box(df_top_countries, x='country', y='price_fix')
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)

visualize_boxplot()