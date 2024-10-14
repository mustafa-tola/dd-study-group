# Model Documentation

## Model Choice
We chose K-Means clustering because it efficiently groups users based on numerical features like availability, location, and skill levels. The model is unsupervised and works well for organizing users into distinct study groups.

## Training the Model
1. Preprocess the data by encoding categorical features and normalizing numeric values.
2. Use the Elbow Method and Silhouette Score to determine the optimal number of clusters (`k`).
3. Train the K-Means model using `k=75` (based on the Elbow Method).

## Evaluation
The model was evaluated using:
- **Sum of Squared Errors (SSE)**: To determine how well the clusters represent the data points.
- **Silhouette Score**: To measure the separation between clusters.
- **Variance**: To determine the variation in datapoints within each cluster

## Results
- The average variance within clusters was approximately 0.20, indicating reasonable similarity among users within each cluster.
