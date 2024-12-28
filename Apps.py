import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import joblib 
from PIL import Image
from sklearn.ensemble import RandomForestRegressor



# Set custom style for green minimalist theme with watermark
st.markdown(
    """
    <style>
        .apps-title {
            font-size: 24px;
            font-weight: normal;
            color: red;
            background-color: transparent;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        .tab-title {
            font-size: 20px;          
            font-weight: bold;        
            color: white;             
            background-color: #ff4d4d; 
            padding: 15px 20px;  
            border-radius: 8px;       
            text-align: left;       
            margin-bottom: 20px;      
            word-wrap: break-word;    
        }
        .tab-subtitle {
            font-size: 16px;             /* Slightly smaller font size than the title */
            font-weight: normal;         /* Normal font weight to distinguish from the bold title */
            color: #ffffff;              /* White color for text */
            background-color: #28a745;   /* Muted blue for the subtitle background */
            padding: 10px 15px;          /* Padding for spacing */
            border-radius: 6px;          /* Rounded corners */
            text-align: left;            /* Align text to the left */
            margin-bottom: 15px;         /* Space below the subtitle */
            word-wrap: break-word;       /* Wrap long words */
        }
        .tab-description {
            font-size: 16px;
            color: var(--text-color, #555); /* Fallback for light mode */
            margin-bottom: 20px;
            text-align: justify;
        }

        .container {
            margin: 20px 0;
            text-align: center;
        }
    
    </style>
    """,
    unsafe_allow_html=True,
)


# Create a horizontal tab navigation bar
tabs = st.tabs(["Home", "Booking", "Recommendations", "History and Performance", "New Listing"])

# Home Tab
with tabs[0]:

    # Title for the app
    st.image("banner.png")
    
    # Short Description
    st.markdown(
        """
        <div class="tab-description">
         Hotel Booking Apps based on Airbnb data to simulate a Recommendation System using a K-means clustering model 
         and predict prices for new listings using Random Forest model, recommending the optimal price 
         range to hotel owners for their newly input listings.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Recommendation Flow Chart
    st.markdown(
        """
        <div class="tab-subtitle">
            Recommendation Flow Chart
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("recommendation.png", caption="Step-by-step Recommendation Process", use_container_width=True)

    # New Listing Flow Chart
    st.markdown(
        """
        <div class="tab-subtitle">
            New Listing Flow Chart
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("price.png", caption="Process for Adding New Listings", use_container_width=True)

    

df = pd.read_csv('new_airbnb.csv')

# Set custom style for slider and button
st.markdown(
    """
    <style>
        .slider-label {
            font-weight: bold;
            color: #555;
        }
        .stcolumns {
            margin: 10px 0;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Booking Page
with tabs[1]:
    # Title
    st.markdown(
        """
        <div class="tab-title">
            Where Would You Like to Stay?
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Organize inputs and sliders into two columns
    col1, col2 = st.columns(2)

    # Input fields in the first column
    with col1:
        st.markdown('<div class="slider-label">Location:</div>', unsafe_allow_html=True)
        country_input = st.selectbox(
            'Select a location',
            options=df['country'].unique(),
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Guests:</div>', unsafe_allow_html=True)
        num_guests = st.number_input(
            'Enter the number of guests',
            min_value=1, max_value=16, value=1,
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Min Price:</div>', unsafe_allow_html=True)
        min_price = st.number_input(
            'Enter the minimum price',
            min_value=0, max_value=65000, value=0, step=50,
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Max Price:</div>', unsafe_allow_html=True)
        max_price = st.number_input(
            'Enter the maximum price',
            min_value=min_price, max_value=65000, value=65000, step=50,
            label_visibility="collapsed"
        )

    # Sliders in the second column
    with col2:
        st.markdown('<div class="slider-label">Price Range:</div>', unsafe_allow_html=True)
        price_range = st.slider(
            'Select a price range',
            50, 65000, (min_price, max_price), step=50,
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Family Suitability Level:</div>', unsafe_allow_html=True)
        family_suitability_input = st.select_slider(
            'Choose family suitability level',
            options=['Basic', 'Comfortable', 'Family-friendly'], value='Basic',
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Safety Level:</div>', unsafe_allow_html=True)
        safety_input = st.select_slider(
            'Choose safety level',
            options=['Standard', 'Enhanced', 'High-Security'], value='Standard',
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Natural Condition Level:</div>', unsafe_allow_html=True)
        natural_condition_input = st.select_slider(
            'Choose natural condition level',
            options=['Minimal', 'Scenic', 'Nature-Rich'], value='Minimal',
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Work Suitability Level:</div>', unsafe_allow_html=True)
        work_suitability_input = st.select_slider(
            'Choose work suitability level',
            options=['Basic', 'Enhanced', 'Professional'], value='Basic',
            label_visibility="collapsed"
        )

    # Update inputs based on slider adjustments
    min_price, max_price = price_range
    st.session_state['country_input'] = country_input
    st.session_state['min_price'] = min_price
    st.session_state['max_price'] = max_price
    st.session_state['price_range'] = min_price, max_price

    # Convert slider labels to corresponding values
    family_suitability_values = {
        'Basic': random.choice([0]),
        'Comfortable': random.choice([1, 2]),
        'Family-friendly': random.choice([3, 4, 5]),
    }[family_suitability_input]

    safety_values = {
        'Standard': random.choice([0]),
        'Enhanced': random.choice([1]),
        'High-Security': random.choice([2, 3, 4, 5, 6, 7]),
    }[safety_input]

    natural_condition_values = {
        'Minimal': 0,
        'Scenic': random.choice([1]),
        'Nature-Rich': random.choice([2, 3]),
    }[natural_condition_input]

    work_suitability_values = {
        'Basic': 0,
        'Enhanced': 1,
        'Professional': random.choice([2, 3]),
    }[work_suitability_input]

  # Filter DataFrame based on base conditions (country, price, guests)
    filtered_listings = df[
        (df['country'].str.replace(" ", "").str.lower() == country_input.replace(" ", "").lower()) &
        (df['price_fix'] >= min_price) & (df['price_fix'] <= max_price) &
        (df['guests'] >= num_guests)
    ]

    filtered_listings = filtered_listings.copy() 
    # Calculate the absolute differences between the amenities preferences and the listings
    filtered_listings['family_diff'] = np.abs(filtered_listings['family_suitability'] - family_suitability_values)
    filtered_listings['safety_diff'] = np.abs(filtered_listings['safety'] - safety_values)
    filtered_listings['natural_diff'] = np.abs(filtered_listings['natural_condition'] - natural_condition_values)
    filtered_listings['work_diff'] = np.abs(filtered_listings['work_suitability'] - work_suitability_values)

    # Add scoring for partial matches based on user preferences
    filtered_listings['match_score'] = (
        (1 - (filtered_listings['family_diff'] / 5)) * 0.25 +
        (1 - (filtered_listings['safety_diff'] / 7)) * 0.25 +
        (1 - (filtered_listings['natural_diff'] / 3)) * 0.25 +
        (1 - (filtered_listings['work_diff'] / 3)) * 0.25
    )


    # Overall weighted score (adding importance for rating & reviews)
    filtered_listings['weighted_score'] = (
        filtered_listings['match_score'] * 0.6 +  # 60% importance for preference match
        (filtered_listings['rating'] / 5) * 0.3 +  # 30% for rating (normalized to 0-1)
        (filtered_listings['reviews'] / filtered_listings['reviews'].max()) * 0.1  # 10% for reviews
    )

    # Sorting state: initialize session variables for sorting if they don't exist
    if 'sort_by' not in st.session_state:
        st.session_state['sort_by'] = 'weighted_score'
        st.session_state['ascending'] = False

    # Sorting function
    def sort_data(dataframe, column, ascending):
        return dataframe.sort_values(by=column, ascending=ascending)

    # Sort based on user selection
    sorted_listings = sort_data(filtered_listings, st.session_state['sort_by'], st.session_state['ascending'])

    # Select the top 10 listings after sorting
    top_listings = sorted_listings.head(10)

    
    # Check if there are no listings based on user preferences
    if top_listings.empty:
        st.write("Sorry, no listings match your preferences at this time.")
    else:
        # Initialize user_data in session state if it doesn't exist
        if 'user_data' not in st.session_state:
            st.session_state['user_data'] = pd.DataFrame(columns=top_listings.columns)

    # Sample feature mappings
    feature_mappings = {
        'natural_condition': {0: 'Urban Vibes', 1: 'Tranquil Escape', 2: 'Nature Immersion', 3: 'Wilderness Haven'},
        'safety': {0: 'Basic Security', 1: 'Safe Haven', 2: 'Fortified', 3: 'Shielded Sanctuary', 4: 'Maximum Protection',
                5: 'Maximum Protection', 6: 'Maximum Protection', 7: 'Maximum Protection'},
        'work_suitability': {0: 'Casual Workspace', 1: 'Work-Friendly', 2: 'Productivity Hub', 3: 'Executive Suite'},
        'family_suitability': {0: 'Cozy Retreat', 1: 'Child-Friendly', 2: 'Child-Friendly', 3: 'Family Paradise',
                            4: 'Family Paradise', 5: 'Family Paradise'}
    }
    # Add sort functionality
    sort_options = ['Name', 'Guests', 'Price', 'Rating', 'Reviews']
    sort_columns = {
        'Name': 'name',
        'Guests': 'guests',
        'Price': 'price_fix',
        'Rating': 'rating',
        'Reviews': 'reviews'
    }
 
    # Search bar for hotel name
    st.markdown('<div class="slider-label">Search By Name:</div>', unsafe_allow_html=True)
    search_term = st.text_input("Search By Name:", label_visibility="collapsed")

    if search_term:
        top_listings = top_listings[top_listings['name'].str.contains(search_term, case=False, na=False)]

    # Sort dropdown
    sort_by = st.selectbox("Sort By:", options=sort_options, index=0)
    ascending = st.checkbox("Sort Ascending", value=True)
    top_listings = top_listings.sort_values(by=sort_columns[sort_by], ascending=ascending)
    
    # Placeholder for booking success messages
    booking_success_placeholder = st.empty()

    # Display listings
    for index, row in top_listings.iterrows():
        with st.container():
            st.markdown(f"<h3 style='font-weight: bold; font-size: 22px;'>{row['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px;'>Price: <strong>${row['price_fix']}/night</strong></p>", unsafe_allow_html=True)

            stars = "★" * row['rating'] + "☆" * (5 - row['rating'])
            st.markdown(f"<p style='font-size: 18px;'>Rating: <span style='color: gold;'>{stars}</span> | Reviews: {row['reviews']} | Guests: {row['guests']}</p>", unsafe_allow_html=True)

            family_suitability = feature_mappings['family_suitability'][row['family_suitability']]
            natural_condition = feature_mappings['natural_condition'][row['natural_condition']]
            work_suitability = feature_mappings['work_suitability'][row['work_suitability']]
            safety = feature_mappings['safety'][row['safety']]

            st.markdown(
                f"<p style='font-size: 18px;'>" \
                f"{family_suitability} | {natural_condition} | {work_suitability} | {safety}</p>",
                unsafe_allow_html=True
            )

            if st.button(f'Book', key=f'book_{index}'):
                st.session_state['user_data'] = pd.concat([st.session_state.get('user_data', pd.DataFrame()), row.to_frame().T], ignore_index=True)
                booking_success_placeholder.success(f"Booking successful for {row['name']}!")

            st.markdown("<hr>", unsafe_allow_html=True)


# Second page content

# Load your data
df = pd.read_csv('new_airbnb.csv')

# Drop columns not needed for clustering
new_df = df.drop(columns=['id', 'name', 'host_id', 'country', 'studios', 'checkin', 'checkout', 'toilets', 'price_fix', 'rating', 'reviews'])

common_columns = ['bathrooms', 'beds', 'guests', 'bedrooms',
                'family_suitability', 'safety',
                'natural_condition', 'work_suitability']

# Load the saved KMeans model
kmeans = joblib.load('kmeans_model.pkl')

# Perform clustering
kmeans = KMeans(n_clusters=5, random_state=100, n_init=10)
cluster = kmeans.fit_predict(new_df[common_columns])

# Add the cluster labels to the original dataframe
df['cluster'] = cluster

# Rename the dataframe with clusters as 'merged_df'
merged_df = df.copy()

# Define function to find similar listings in the same cluster
def recommend_for_user(user_data_entry, merged_df, country, min_price, max_price):
    user_cluster = merged_df[
        (merged_df['family_suitability'] == user_data_entry['family_suitability']) &
        (merged_df['safety'] == user_data_entry['safety']) &
        (merged_df['natural_condition'] == user_data_entry['natural_condition']) &
        (merged_df['work_suitability'] == user_data_entry['work_suitability'])
    ]['cluster'].unique()

    # Filter listings in the same cluster and within the price range
    recommendations = merged_df[
        (merged_df['cluster'].isin(user_cluster)) &
        (merged_df['country'].str.lower().str.strip() == country) &
        (merged_df['price_fix'].between(min_price, max_price))
    ]

    return recommendations.drop_duplicates(subset='id')

# Sort function
def sort_recommendations(recommendations, column, ascending):
    return recommendations.sort_values(by=column, ascending=ascending)

# Second page content
with tabs[2]:

    st.markdown(
        """
        <div class="tab-title">
            Recommendation For You!
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Retrieve country and price range inputs from the first tab
    country_input = st.session_state['country_input'].lower().strip()
    min_price, max_price = st.session_state['price_range']

    # Initialize sorting state for recommendations
    if 'recommend_sort_by' not in st.session_state:
        st.session_state['recommend_sort_by'] = 'reviews'  # Default sort by reviews
        st.session_state['recommend_ascending'] = False

     # Add sort functionality
    sort_options = ['Name', 'Guests', 'Price', 'Rating', 'Reviews']
    sort_columns = {
        'Name': 'name',
        'Guests': 'guests',
        'Price': 'price_fix',
        'Rating': 'rating',
        'Reviews': 'reviews'
    }

    # Ensure user_data exists in session state
    if not st.session_state['user_data'].empty:
        user_data = st.session_state['user_data']

        all_recommendations = []

        # Generate recommendations for each user entry
        for _, user_data_entry in user_data.iterrows():
            recommendations = recommend_for_user(user_data_entry, merged_df, country_input, min_price, max_price)
            all_recommendations.append(recommendations)

        # Combine recommendations and ensure at least 10 unique listings
        all_recommendations_df = pd.concat(all_recommendations).drop_duplicates(subset='id').head(10)

        # Apply sorting to the final recommendations
        sorted_recommendations = sort_recommendations(
            all_recommendations_df,
            column=st.session_state['recommend_sort_by'],
            ascending=st.session_state['recommend_ascending']
        )

        # Sort dropdown
        sort_by = st.selectbox("Sort By:", options=sort_options, index=0, key='recommendation')
        ascending = st.checkbox("Sort Ascending", value=True, key='recommendation_sort')
        sorted_recommendations = sorted_recommendations.sort_values(by=sort_columns[sort_by], ascending=ascending)

        # Placeholder for booking success messages
        booking_success_placeholder = st.empty()

        # Display listings
        for index, row in sorted_recommendations.iterrows():
            with st.container():
                st.markdown(f"<h3 style='font-weight: bold; font-size: 22px;'>{row['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 18px;'>Price: <strong>${row['price_fix']}/night</strong></p>", unsafe_allow_html=True)

                stars = "★" * row['rating'] + "☆" * (5 - row['rating'])
                st.markdown(f"<p style='font-size: 18px;'>Rating: <span style='color: gold;'>{stars}</span> | Reviews: {row['reviews']} | Guests: {row['guests']}</p>", unsafe_allow_html=True)

                family_suitability = feature_mappings['family_suitability'][row['family_suitability']]
                natural_condition = feature_mappings['natural_condition'][row['natural_condition']]
                work_suitability = feature_mappings['work_suitability'][row['work_suitability']]
                safety = feature_mappings['safety'][row['safety']]

                st.markdown(
                    f"<p style='font-size: 18px;'>" \
                    f"{family_suitability} | {natural_condition} | {work_suitability} | {safety}</p>",
                    unsafe_allow_html=True
                )

                if st.button(f'Book', key=f'book_{index}_{row["name"]}'):
                    st.session_state['user_data'] = pd.concat([st.session_state.get('user_data', pd.DataFrame()), row.to_frame().T], ignore_index=True)
                    booking_success_placeholder.success(f"Booking successful for {row['name']}!")

                st.markdown("<hr>", unsafe_allow_html=True)



# In the second tab
with tabs[3]:
    st.markdown(
        """
        <div class="tab-subtitle">
            Booking History
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Merge user_data with cluster information from merged_df on 'id'
    #if not st.session_state['user_data'].empty:
    if 'user_data' in st.session_state and not st.session_state['user_data'].empty:    
        # Perform the initial merge
        user_data_2 = pd.merge(st.session_state['user_data'], merged_df[['id', 'cluster']], on='id', how='left')
    
        # Check if 'cluster_y' column exists and rename it to 'cluster'
        if 'cluster_y' in user_data_2.columns:
            user_data_2 = user_data_2.rename(columns={'cluster_y': 'cluster'})

        # Store the merged data in session state
        st.session_state['user_data_2'] = user_data_2

        # Display the full DataFrame if available
        if 'user_data_2' in st.session_state and not st.session_state['user_data_2'].empty:

            # Define the columns to display
            display_columns = ['name', 'guests', 'reviews', 'rating', 'price_fix', 'country']

            # Create a subset DataFrame
            user_data_display = st.session_state['user_data_2'][display_columns].copy()
            user_data_display.columns = ['Name', 'Guests Capacity', 'Reviews', 'Rating', 'Price', 'Country']
            user_data_display['Price'] = user_data_display['Price'].apply(lambda x: f"${int(x)}")
            user_data_display = user_data_display.reset_index(drop=True)

            # Display the subset DataFrame
            st.dataframe(user_data_display.sort_values(by='Name').reset_index(drop=True),
            use_container_width=True)

        
        all_recommendations = []

        # Generate recommendations for each user entry
        for _, user_data_entry in user_data_2.iterrows():
            recommendations = recommend_for_user(user_data_entry, merged_df, country_input, min_price, max_price)
            all_recommendations.append(recommendations)

        # Combine recommendations and ensure at least 10 unique listings
        all_recommendations_df = pd.concat(all_recommendations).drop_duplicates(subset='id').head(10)

        # Apply sorting to the final recommendations
        sorted_recommendations = sort_recommendations(
            all_recommendations_df,
            column=st.session_state['recommend_sort_by'],
            ascending=st.session_state['recommend_ascending']
        )

        ## Cluster Comparison
        # Data for the first pie chart
        cluster_counts_recommendations = sorted_recommendations['cluster'].value_counts()
        labels_recommendations = cluster_counts_recommendations.index
        values_recommendations = cluster_counts_recommendations.values

        # Data for the second pie chart
        cluster_counts_user_data = user_data_2['cluster'].value_counts()
        labels_user_data = cluster_counts_user_data.index
        values_user_data = cluster_counts_user_data.values

        st.markdown(
            """
            <div class="tab-subtitle">
                Cluster Comparison
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="tab-description">
            Compare the percentage of cluster categories between user bookings and recommendations 
            to evaluate the accuracy of the recommendations.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Create the second donut chart: Cluster Distribution in User Booking History
        fig1 = go.Figure(
            data=[
                go.Pie(
                    labels=labels_user_data,
                    values=values_user_data,
                    textinfo="percent+label",
                    insidetextorientation="radial",
                    hole=0.4,  # Add hole for donut style
                )
            ]
        )
        fig1.update_layout(
            title=dict(
                text="Cluster Distribution in User Booking History",  # Title text
                font=dict(size=14, color="black"),
                x=0.5,  # Center the title horizontally
                xanchor='center',  # Ensure text alignment
                yanchor='top',  # Align above the chart
            ),
            legend_title_text="Cluster Type",  # Add legend title
            showlegend=True,
        )

        # Create the first donut chart: Cluster Distribution in Recommendations
        fig2 = go.Figure(
            data=[
                go.Pie(
                    labels=labels_recommendations,
                    values=values_recommendations,
                    textinfo="percent+label",
                    insidetextorientation="radial",
                    hole=0.4,  # Add hole for donut style
                )
            ]
        )
        fig2.update_layout(
            title=dict(
                text="Cluster Distribution in Recommendations",  # Title text
                font=dict(size=14, color="black"),
                x=0.5,  # Center the title horizontally
                xanchor='center',  # Ensure text alignment
                yanchor='top',  # Align above the chart
            ),
            legend_title_text="Cluster Type",  # Add legend title
            showlegend=True,
        )


        # Display side-by-side interactive donut charts
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.plotly_chart(fig2, use_container_width=True)

        ## Feature Comparison
        # Feature mappings
        feature_mappings = {
            'natural_condition': {0: 'Minimal', 1: 'Scenic', 2: 'Nature-Rich', 3: 'Nature-Rich'},
            'safety': {0: 'Standard', 1: 'Enhanced', 2: 'High-Security', 3: 'High-Security', 4: 'High-Security',
                    5: 'High-Security', 6: 'High-Security', 7: 'High-Security'},
            'work_suitability': {0: 'Basic', 1: 'Enhanced', 2: 'Professional', 3: 'Professional'},
            'family_suitability': {0: 'Basic', 1: 'Comfortable', 2: 'Comfortable', 3: 'Family-friendly',
                                4: 'Family-friendly', 5: 'Family-friendly'}
        }

        def plot_feature_comparison(feature):
            # Map numeric values to category names
            user_data_2[f'{feature}_name'] = user_data_2[feature].map(feature_mappings[feature])
            sorted_recommendations[f'{feature}_name'] = sorted_recommendations[feature].map(feature_mappings[feature])

            # Count occurrences of each category
            user_counts = user_data_2[f'{feature}_name'].value_counts().sort_index()
            recommendation_counts = sorted_recommendations[f'{feature}_name'].value_counts().sort_index()

            # Combine counts into a DataFrame
            comparison_df = pd.DataFrame({
                'User Data': user_counts,
                'Recommendations': recommendation_counts
            }).fillna(0)

            # Reset the index and rename the column
            comparison_df = comparison_df.reset_index()
            comparison_df.rename(columns={f'{feature}_name': 'Feature Level'}, inplace=True)

            # Add total and percentage calculations
            comparison_df['Total'] = comparison_df['User Data'] + comparison_df['Recommendations']
            comparison_df['User Percentage'] = (comparison_df['User Data'] / comparison_df['Total'] * 100).fillna(0)
            comparison_df['Recommendation Percentage'] = (comparison_df['Recommendations'] / comparison_df['Total'] * 100).fillna(0)

            # Plotting
            sns.set_style("whitegrid")
            plt.figure(figsize=(8, 5))

            # Plot stacked bars
            bars1 = plt.bar(
                comparison_df['Feature Level'], 
                comparison_df['User Percentage'], 
                label='User Data', 
                color='#3498db', 
                edgecolor='white', 
                width=0.6
            )
            bars2 = plt.bar(
                comparison_df['Feature Level'], 
                comparison_df['Recommendation Percentage'], 
                bottom=comparison_df['User Percentage'], 
                label='Recommendations', 
                color='#2ecc71', 
                edgecolor='white', 
                width=0.6
            )

            # Add value labels to User Data bars
            for bar, percentage, count in zip(
                bars1, 
                comparison_df['User Percentage'], 
                comparison_df['User Data']
            ):
                plt.text(
                    bar.get_x() + bar.get_width() / 2, 
                    bar.get_height() / 2, 
                    f'{percentage:.1f}%\n({int(count)})', 
                    ha='center', 
                    va='center', 
                    color='white', 
                    fontsize=10
                )

            # Add value labels to Recommendations bars
            for bar, percentage, count in zip(
                bars2, 
                comparison_df['Recommendation Percentage'], 
                comparison_df['Recommendations']
            ):
                plt.text(
                    bar.get_x() + bar.get_width() / 2, 
                    bar.get_height() / 2 + bar.get_y(), 
                    f'{percentage:.1f}%\n({int(count)})', 
                    ha='center', 
                    va='center', 
                    color='white', 
                    fontsize=10
                )

            # Add title and labels
            plt.title(f'{feature.replace("_", " ").title()} Comparison', fontsize=14, weight='bold')
            plt.xlabel(f'{feature.replace("_", " ").title()} Levels', fontsize=12)
            plt.ylabel('Percentage (%)', fontsize=12)
            plt.xticks(fontsize=10)
            plt.legend(title='', fontsize=10)
            sns.despine(left=True, bottom=True)
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(plt)
                
        # Streamlit UI for the feature comparison
        st.markdown(
            """
            <div class="tab-subtitle">
                Feature Comparison: User VS Recommendation
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="tab-description">
            Analyze the alignment between user preferences and recommendations by examining the distribution of Family Suitability, Safety, Natural Condition, and Work Suitability. 
            These factors play a critical role in determining amenities, facilities, and overall ambiance.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Dropdown for feature selection
        feature_choice = st.selectbox(
            'Select the feature:',
            options=['natural_condition', 'safety', 'work_suitability', 'family_suitability'],
            format_func=lambda x: x.replace("_", " ").title()
        )

        # Plot the selected feature comparison
        plot_feature_comparison(feature_choice)

        ###Price Comparison
        st.markdown(
            """
            <div class="tab-subtitle">
                Price Comparison
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="tab-description">
            Compare the price distribution in the user booking history with the recommendations to evaluate how accurately 
            the price distribution in the recommendations represents the user booking history.
            </div>
            """,
            unsafe_allow_html=True,
        )

        
        # Extract price data for user booking history and recommendations
        user_prices = user_data_2['price_fix']
        recommendation_prices = sorted_recommendations['price_fix']
        
        # Create a box plot for user booking history prices
        user_price_fig = go.Figure(
            data=[
                go.Box(
                    y=user_prices,
                    name="User Booking History",
                    marker=dict(color='lightblue'),
                )
            ]
        )
        user_price_fig.update_layout(
            title=dict(
                text="Price Distribution in User Booking History",
                font=dict(size=16, color="black"),
                x=0.5,
                xanchor='center',
                yanchor='top',
            ),
            yaxis_title="Price",
            showlegend=False,
        )

        # Create a box plot for recommendation prices
        recommendation_price_fig = go.Figure(
            data=[
                go.Box(
                    y=recommendation_prices,
                    name="Recommendations",
                    marker=dict(color='salmon'),
                )
            ]
        )
        recommendation_price_fig.update_layout(
            title=dict(
                text="Price Distribution in Recommendations",
                font=dict(size=16, color="black"),
                x=0.5,
                xanchor='center',
                yanchor='top',
            ),
            yaxis_title="Price",
            showlegend=False,
        )

        # Display the two box plots side by side
        col3, col4 = st.columns(2)

        with col3:
            st.plotly_chart(user_price_fig, use_container_width=True)

        with col4:
            st.plotly_chart(recommendation_price_fig, use_container_width=True)

        
        ###Countries History
        st.markdown(
            """
            <div class="tab-subtitle">
                Country Booking History
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="tab-description">
            Display the countries where the user has previously booked hotels.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Extract country data and count bookings per country
        country_counts = user_data_2['country'].value_counts()
        country_labels = country_counts.index
        country_values = country_counts.values
        
        # Create a bar chart for country booking history
        country_fig = go.Figure(
            data=[go.Bar(
                x=country_labels,
                y=country_values,
                text=country_values,
                textposition='outside',  # Text outside the bars for better visibility
                marker=dict(
                    color='royalblue',  # Change color to a more vibrant shade
                    line=dict(color='black', width=1)  # Add a border around the bars
                ),
            )],
            layout=dict(
                xaxis_title="Country",  # X-axis title
                yaxis_title="Number of Bookings",  # Y-axis title
                showlegend=False,
                xaxis=dict(
                    tickangle=45,  # Rotate the x-axis labels for better readability
                    tickfont=dict(size=12, color='black'),  # Set font size and color for x-axis ticks
                    showgrid=False,  # Remove x-axis grid lines for a cleaner look
                ),
                yaxis=dict(
                    tick0=0,  # Start the ticks from 0
                    dtick=2,  # Set the tick interval to 2 for better spacing
                    tickfont=dict(size=12, color='black'),  # Set font size and color for y-axis ticks
                    showgrid=True,  # Keep y-axis grid lines for better readability
                    gridcolor='lightgray'  # Set grid color to a subtle shade
                ),
                plot_bgcolor='white',  # Set the background color of the plot 
                margin=dict(l=40, r=40, t=20, b=60),  # Adjust the margins to fit the labels
            )
        )
        # Display the bar chart below the donut charts
        st.plotly_chart(country_fig, use_container_width=True)


    else:
        st.write("No booking history available to display cluster analysis.")

#user input
with tabs[4]:

    df  = pd.read_csv("new_airbnb.csv")

    # Load the RF model
    model = joblib.load('rf_price.pkl')

    # Load the dataset
    df_predict  = df.copy()

    # Apply log transformation to reduce skewness
    df_predict['price_fix'] = np.log1p(df_predict['price_fix'])
    
    # Handle outliers using log transformation
    skewed_features = ['reviews','safety']
    skewed_features_2 = ['bedrooms','beds','bathrooms','price_fix','guests']
    for feature in skewed_features:
        df_predict[feature] = np.log1p(df_predict[feature])

    # Function to handle outliers based on quantiles
    def handle_outliers_quantile(df_predict, feature, lower_percentile=0.05, upper_percentile=0.95):
        lower_bound =  df_predict[feature].quantile(lower_percentile)
        upper_bound =  df_predict[feature].quantile(upper_percentile)
        df_predict[feature] = np.where(df_predict[feature] < lower_bound, lower_bound, df_predict[feature])
        df_predict[feature] = np.where(df_predict[feature] > upper_bound, upper_bound, df_predict[feature])
    for feature in skewed_features_2 :
        handle_outliers_quantile(df_predict, feature)

    # Reverse log transformation and scale the values back to the original range
    df_predict['price_fix'] = np.expm1(df_predict['price_fix'])

    # Optional: Apply a scaling factor to normalize the values further (if needed)
    scaling_factor = 10  # Ensure price_fix is scaled to hundreds
    df_predict['price_fix'] = df_predict['price_fix'] / scaling_factor
   
    # Calculate the mean price for each country
    country_price_median = df_predict.groupby('country')['price_fix'].median()

    # Map the mean price to the country column
    df_predict['country_encoded'] = df_predict['country'].map(country_price_median).astype(int)

    # Define the encodings for checkin and checkout times
    checkin_encoding = {'Not specified': 0, 'Early Morning': 1, 'Early Afternoon': 2, 'Flexible': 3}
    checkout_encoding = {'Not specified': 0, 'Early Morning': 1, 'Early Afternoon': 2}

    # Streamlit Page
    st.markdown(
        """
        <div class="tab-title">
           Register Your Property!
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Organize inputs and sliders into two columns
    col1, col2 = st.columns(2)

    # Input fields in the first column
    with col1:
        st.markdown('<div class="slider-label">Name of Listing:</div>', unsafe_allow_html=True)
        name = st.text_input(
            'Enter the name of the listing',
            label_visibility="collapsed",
        )

        st.markdown('<div class="slider-label">Location:</div>', unsafe_allow_html=True)
        country_input = st.selectbox(
            'Select a location',
            options=df['country'].unique(),
            label_visibility="collapsed",
            key='country_input_selectbox'
        )

        st.markdown('<div class="slider-label">Number of Guests:</div>', unsafe_allow_html=True)
        guests = st.number_input(
            'Enter the number of guests',
            min_value=1, max_value=20, value=1, step=1,
            label_visibility="collapsed",
            key='num_guests_input'
        )

        st.markdown('<div class="slider-label">Number of Beds:</div>', unsafe_allow_html=True)
        beds = st.number_input(
            'Enter the number of beds',
            min_value=0, max_value=10, value=1, step=1,
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Number of Toilets:</div>', unsafe_allow_html=True)
        toilets = st.number_input(
            'Enter the number of toilets',
            min_value=0, max_value=10, value=1, step=1,
            label_visibility="collapsed"
        )

        st.markdown('<div class="slider-label">Check-in Time:</div>', unsafe_allow_html=True)
        checkin = st.selectbox(
            'Select check-in time',
            options=list(checkin_encoding.keys()),
            label_visibility="collapsed"
        )

    # Sliders in the second column
    with col2:
        st.markdown('<div class="slider-label">Family Suitability Level:</div>', unsafe_allow_html=True)
        family_suitability = st.select_slider(
            'Choose family suitability level',
            options=['Basic', 'Comfortable', 'Family-friendly'], value='Basic',
            label_visibility="collapsed",
            key='family_slider'
        )

        st.markdown('<div class="slider-label">Safety Level:</div>', unsafe_allow_html=True)
        safety = st.select_slider(
            'Choose safety level',
            options=['Standard', 'Enhanced', 'High-Security'], value='Standard',
            label_visibility="collapsed",
            key='safety_slider'
        )

        st.markdown('<div class="slider-label">Natural Condition Level:</div>', unsafe_allow_html=True)
        natural_condition = st.select_slider(
            'Choose natural condition level',
            options=['Minimal', 'Scenic', 'Nature-Rich'], value='Minimal',
            label_visibility="collapsed",
            key='natural_condition_slider'
        )

        st.markdown('<div class="slider-label">Work Suitability Level:</div>', unsafe_allow_html=True)
        work_suitability = st.select_slider(
            'Choose work suitability level',
            options=['Basic', 'Enhanced', 'Professional'], value='Basic',
            label_visibility="collapsed",
             key='work_suitability_slider'
        )

        st.markdown('<div class="slider-label">Check-out Time:</div>', unsafe_allow_html=True)
        checkout = st.selectbox(
            'Select check-out time',
            options=list(checkout_encoding.keys()),
            label_visibility="collapsed"
        )
        
    # Dynamically fetch the encoded value for the selected country
    country_encoded_input = (
        df_predict[df_predict['country'] == country_input]['country_encoded'].iloc[0]
        if country_input in df_predict['country'].values else 0
    )
    # Map slider values
    family_suitability_values = {'Basic': 0, 'Comfortable': random.choice([1, 2]), 'Family-friendly': random.choice([3, 4, 5])}[family_suitability]
    safety_values = {'Standard': 0, 'Enhanced': 1, 'High-Security': random.choice([2, 3, 4, 5, 6, 7])}[safety]
    natural_condition_values = {'Minimal': 0, 'Scenic': 1, 'Nature-Rich': random.choice([2, 3])}[natural_condition]
    work_suitability_values = {'Basic': 0, 'Enhanced': 1, 'Professional': random.choice([2, 3])}[work_suitability]

    # Prepare the new input as a DataFrame
    new_data = pd.DataFrame({
        'guests': [guests],                  # 2. guests
        'toilets': [toilets],                # 3. toilets
        'studios': [0],                      # 4. studios (default value)
        'family_suitability': [family_suitability_values],  # 5. family_suitability
        'safety': [safety_values],           # 6. safety
        'natural_condition': [natural_condition_values],  # 7. natural_condition
        'work_suitability': [work_suitability_values],  # 8. work_suitability
        'country_encoded': [country_encoded_input]  # 9. country_encoded
    })

    # Ensure generated ID does not exist in the DataFrame
    def generate_unique_id(df, column, start, end, is_integer=True):
        while True:
            new_id = random.randint(start, end) if is_integer else random.uniform(start, end)
            if new_id not in df[column].values:
                return new_id

    # Assuming `df` is your DataFrame
    id_new = generate_unique_id(df, 'id', 10000, 99999, is_integer=True)
    host_id_new = generate_unique_id(df, 'host_id', 1000, 9999, is_integer=False)

    # Encode checkin and checkout times
    checkin_encoded = checkin_encoding[checkin]
    checkout_encoded = checkout_encoding[checkout]

    # Predict recommended price
    recommended_price = model.predict(new_data).flatten()[0] 

 
    st.markdown(
    f'<p style="font-size: 18px; font-family: sans-serif; color: green; text-align: left;">Recommended Price ${recommended_price:.2f}</p>',
    unsafe_allow_html=True      
    )
    # Input price
    price_fix = st.number_input("Set your price", key="price_input_key")  # Add unique key to avoid DuplicateWidgetID

    # Add to DataFrame
    if st.button("Submit Listing"):
        new_listing = {
            "id": id_new,
            "name": name,
            "rating": 0,
            "reviews": 0,
            "bathrooms": toilets,
            "beds": beds,
            "guests": guests,
            "toilets": toilets,
            "bedrooms": beds,
            "studios": 0,
            "checkin": checkin_encoded,
            "checkout": checkout_encoded,
            "host_id": host_id_new,
            "country": country_input,
            "family_suitability": family_suitability_values,
            "price_fix": price_fix,
            "safety": safety_values,
            "natural_condition": natural_condition_values,
            "work_suitability": work_suitability_values,
        }
        # Update the session state with the new listing
        if 'df' not in st.session_state:
            st.session_state['df'] = df  # Initialize session state with the main dataframe if not already present

        # Append the new listing to the session DataFrame
        st.session_state['df'] = pd.concat([st.session_state['df'], pd.DataFrame([new_listing])], ignore_index=True)
        
        # Save the updated DataFrame to CSV
        st.session_state['df'].to_csv('new_airbnb.csv', index=False)

        st.success("Listing added successfully!")

st.markdown(
    """
    <style>
        .footer {
            font-size: 16px;
            font-weight: bold;
            color: #28a745; /* Green color */
            text-align: left;
            margin-top: 20px;
        }
    </style>
    <div class="footer">
        Created by Jevon Sianipar
    </div>
    """,
    unsafe_allow_html=True,
) 
