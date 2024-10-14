## Model Selection
Since K-Means clustering effectively groups users according to numerical characteristics like availability, location, and skill levels, we decided to use it. The model effectively divides users into discrete study groups and is unsupervised.

## Model Training
1. Preprocess the data by normalizing numerical values and encoding categorical features.
2. Determine the ideal number of clusters ({k`) using the Elbow Method and Silhouette Score.
3. Use `k=75` to train the K-Means model (based on the Elbow Method).

## Assessment
The model was assessed using:
To ascertain how accurately the clusters represent the data points, use the **Sum of Squared Errors (SSE)**.
- **Silhouette Score**: To gauge how far apart clusters are.
**Variance**: To ascertain how each cluster's datapoints vary

## Findings: 
The average variance within clusters was roughly 0.20, suggesting that users in each cluster were reasonably similar.
