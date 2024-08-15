import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('AirBnB Across The world Listing Data')

# Cache the data loading function
@st.cache_data
def load_data():
    return pd.read_csv("airbnb.csv")

# Load the data
df = load_data()

# Checkbox to show raw data
if st.checkbox('Show raw data'):
    st.subheader('AirBnB Dataset')
    st.write(df)