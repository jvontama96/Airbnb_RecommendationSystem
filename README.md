Recommendation System Based on Weighted Rating, Content-Based Filtering, and Clustering Model for Airbnb
This project focuses on developing a recommendation system for Airbnb listings using a combination of weighted ratings, content-based filtering, and clustering models. The goal is to offer personalized recommendations based on user preferences and listing characteristics. Additionally, a Streamlit simulation has been created to allow for interactive exploration of the recommendations.

Overview
The recommendation system is built using various techniques to ensure the best possible recommendations for users. The approach includes:

Weighted Rating: Accounts for both the number of reviews and the average rating to rank listings.
Content-Based Filtering: Recommends listings similar to those the user has shown interest in.
Clustering Model: Groups listings using KMeans clustering to recommend similar options within a cluster.
Streamlit Simulation: Provides an interactive platform to explore scatter plots, box plots, and recommendations based on user preferences for country, price, and rating.
Methodology
1. Data Preprocessing
Cleaning: Handling missing values, outliers, and irrelevant features to prepare the data for analysis.
Encoding: Converting categorical variables into numerical values using techniques such as one-hot encoding.
Feature Engineering: Creating new features like family_suitability, safety, and natural_condition to enhance the recommendation system.
2. Exploratory Data Analysis (EDA)
Visualization: Analyzing the distribution of key variables (price_fix, rating, reviews) using scatter plots, box plots, and bar charts.
Correlation Analysis: Identifying relationships between features to inform model development.
3. Weighted Rating
Calculation: Developing a formula to weigh ratings based on the number of reviews, ensuring that listings with more reviews are ranked more accurately.
Application: Using this weighted rating to influence the recommendation process.
4. Content-Based Filtering
Similarity Calculation: Measuring similarity between listings based on features, allowing for the recommendation of similar listings.
User Preference Matching: Tailoring recommendations to match user preferences for specific features, such as country and price.
5. Data Engineering
Feature Creation: Developing features specifically for clustering, such as aggregated scores for family_suitability.
Normalization: Preparing data for clustering by scaling and normalizing features.
6. Parameter Tuning
Elbow Method: Identifying the optimal number of clusters by analyzing the sum of squared distances.
Silhouette Analysis: Validating the consistency of clusters to ensure meaningful groupings.
7. KMeans Clustering Recommendation System
Clustering: Implementing KMeans to group listings into clusters based on their features.
Cluster-Based Recommendations: Providing recommendations from within the same cluster to ensure relevance to user preferences.
8. Evaluation
Cluster Distribution Comparison: Analyzing the distribution of clusters in user data versus recommended listings to assess relevance.
Price Comparison: Comparing the price distribution between user data and recommended listings to ensure alignment with user budgets.
Country Comparison: Evaluating the consistency of country preferences between user data and recommendations.
Streamlit Simulation
A Streamlit application was created to allow users to interactively explore:

Scatter Plots: Visualize relationships between features such as beds, price, and rating.
Box Plots: Analyze the distribution of prices, ratings, and other features.
Recommendation Simulation: Simulate recommendations based on user preferences for country, price, and rating.
How to Use
Clone the Repository:

bash

git clone https://github.com/yourusername/airbnb-recommendation-system.git
Install Dependencies:

bash

pip install -r requirements.txt
Run the Streamlit Application:

bash

streamlit run opening.py
Use the Streamlit app to explore data and generate personalized recommendations interactively.
