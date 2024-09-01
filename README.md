<h1 align="center">Recommendation System Based on Weighted Rating, Content-Based Filtering, and Clustering Model for Airbnb</h1>

<p align="center">
This project focuses on developing a recommendation system for Airbnb listings using a combination of weighted ratings, content-based filtering, and clustering models. The goal is to offer personalized recommendations based on user preferences and listing characteristics. Additionally, a Streamlit simulation has been created to allow for interactive exploration of the recommendations.
</p>

<h2>Overview</h2>

<p>
The recommendation system is built using various techniques to ensure the best possible recommendations for users. The approach includes:
</p>
<ul>
  <li><b>Weighted Rating:</b> Accounts for both the number of reviews and the average rating to rank listings.</li>
  <li><b>Content-Based Filtering:</b> Recommends listings similar to those the user has shown interest in.</li>
  <li><b>Clustering Model:</b> Groups listings using KMeans clustering to recommend similar options within a cluster.</li>
  <li><b>Streamlit Simulation:</b> Provides an interactive platform to explore scatter plots, box plots, and recommendations based on user preferences for country, price, and rating.</li>
</ul>

<h2>Methodology</h2>

<h3>1. Data Preprocessing</h3>
<ul>
  <li><b>Cleaning:</b> Handling missing values, outliers, and irrelevant features to prepare the data for analysis.</li>
  <li><b>Encoding:</b> Converting categorical variables into numerical values using techniques such as one-hot encoding.</li>
  <li><b>Feature Engineering:</b> Creating new features like <code>family_suitability</code>, <code>safety</code>, and <code>natural_condition</code> to enhance the recommendation system.</li>
</ul>

<a href="https://github.com/jvontama96/Airbnb_RecommendationSystem/tree/main/EDA_Image" target="_blank">
<h3>2. Exploratory Data Analysis (EDA)</h3>
<ul>
  <li><b>Visualization:</b> Analyzing the distribution of key variables (<code>price_fix</code>, <code>rating</code>, <code>reviews</code>) using scatter plots, box plots, and bar charts.</li>
  <li><b>Correlation Analysis:</b> Identifying relationships between features to inform model development.</li>
</ul>

<h3>3. Weighted Rating</h3>
<ul>
  <li><b>Calculation:</b> Developing a formula to weigh ratings based on the number of reviews, ensuring that listings with more reviews are ranked more accurately.</li>
  <li><b>Application:</b> Using this weighted rating to influence the recommendation process.</li>
</ul>

<h3>4. Content-Based Filtering</h3>
<ul>
  <li><b>Similarity Calculation:</b> Measuring similarity between listings based on features, allowing for the recommendation of similar listings.</li>
  <li><b>User Preference Matching:</b> Tailoring recommendations to match user preferences for specific features, such as country and price.</li>
</ul>

<h3>5. Data Engineering</h3>
<ul>
  <li><b>Feature Creation:</b> Developing features specifically for clustering, such as aggregated scores for <code>family_suitability</code>.</li>
  <li><b>Normalization:</b> Preparing data for clustering by scaling and normalizing features.</li>
</ul>

<h3>6. Parameter Tuning</h3>
<ul>
  <li><b>Elbow Method:</b> Identifying the optimal number of clusters by analyzing the sum of squared distances.</li>
  <li><b>Silhouette Analysis:</b> Validating the consistency of clusters to ensure meaningful groupings.</li>
</ul>

<h3>7. KMeans Clustering Recommendation System</h3>
<ul>
  <li><b>Clustering:</b> Implementing KMeans to group listings into clusters based on their features.</li>
  <li><b>Cluster-Based Recommendations:</b> Providing recommendations from within the same cluster to ensure relevance to user preferences.</li>
</ul>

<h3>8. Result and Evaluation</h3>
<ul>
  <li><b>Cluster Distribution Comparison:</b> Analyzing the distribution of clusters in user data versus recommended listings to assess relevance.</li>
  <li><b>Price Comparison:</b> Comparing the price distribution between user data and recommended listings to ensure alignment with user budgets.</li>
  <li><b>Country Comparison:</b> Evaluating the consistency of country preferences between user data and recommendations.</li>
</ul>

<h2>Streamlit Simulation: <a href="https://github.com/jvontama96/AirBnB_RecommendationSystem/tree/main/Streamlit%20File">GitHub Repository</a></h2>

<p>
A Streamlit application was created to allow users to interactively explore:
</p>
<ul>
  <li><b>Scatter Plots:</b> Visualize relationships between features such as beds, price, and rating.</li>
  <li><b>Box Plots:</b> Analyze the distribution of prices, ratings, and other features.</li>
  <li><b>Recommendation Simulation:</b> Simulate recommendations based on user preferences for country, price, and rating.</li>
</ul>

<h2>How to Use</h2>

<ol>
  <li><b>Clone the Repository:</b></li>
</ol>
<pre>
<code>git clone https://github.com/yourusername/Airbnb_RecommendationSystem.git</code>
</pre>

<ol start="2">
  <li><b>Install Dependencies:</b></li>
</ol>
<pre>
<code>pip install -r requirements.txt</code>
</pre>

<ol start="3">
  <li><b>Run the Streamlit Application:</b></li>
</ol>
<pre>
<code>streamlit run opening.py</code>
</pre>

<p>
Use the Streamlit app to explore data and generate personalized recommendations interactively.
</p>
