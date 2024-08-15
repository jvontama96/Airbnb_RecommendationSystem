import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Weigthed Rating Recommendation System')

st.markdown(""" Recommendation system in here based on Weighted Rating from User Country and Price Preference
             not by user booking history""")

df = pd.read_csv('airbnb_clean.csv')

df['country'] = df['country'].str.lower()

# Calculate C (mean rating across all listings)
C = df['rating'].mean()

# Calculate m (minimum number of reviews required to be listed)
m = df['reviews'].quantile(0.9)

# Filter listings that qualify (have reviews >= m)
q_listings = df.copy().loc[df['reviews'] >= m]
print(q_listings.shape)

# Define the weighted rating function
def weighted_rating(x, m=m, C=C):
    v = x['reviews']
    R = x['rating']
    return (v / (v + m) * R) + (m / (m + v) * C)

# Calculate the score for qualified listings
q_listings['score'] = q_listings.apply(weighted_rating, axis=1)

# Sort listings by score
q_listings = q_listings.sort_values('score', ascending=False)

# Input widgets
country_input = st.text_input('Enter country:').strip().lower()
min_price = st.number_input('Enter minimum price:', min_value=0, value=0)
max_price = st.number_input('Enter maximum price:', min_value=0, value=300)

# Filter DataFrame based on inputs
filtered_listings = q_listings[q_listings['country'].str.lower() == country_input]
filtered_listings = filtered_listings[(filtered_listings['price_fix'] >= min_price) & (filtered_listings['price_fix'] <= max_price)]

# Show the filtered DataFrame with specified columns
if not filtered_listings.empty:
    top_listings = filtered_listings[['name', 'reviews', 'rating', 'price_fix']].head(10)
    st.write(top_listings)
else:
    st.write("No listings found for the specified criteria.")