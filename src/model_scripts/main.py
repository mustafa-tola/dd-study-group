# main.py

import asyncio
from data_loader import DataLoader
from clustering import KMeansClustering
from visualization import Visualizer
from utils import Utils

async def main():
    # Initialize DataLoader
    processor = DataLoader("../data/data.csv")
    
    # Preprocess and split the data
    X_train, X_test = await processor.split_data()
    
    # Initialize KMeansClustering
    cluster_processor = KMeansClustering(processor.data)
    
    # Perform Elbow Method and Silhouette Analysis
    cluster_processor.elbow_method(k_max=100)  # Elbow method is synchronous
    await cluster_processor.silhouette_analysis(k_max=100)  # Silhouette analysis
    
    # Perform KMeans clustering
    k_optimal = 75  # Based on analysis
    arr = await cluster_processor.kmeans_clustering(X_train, k_optimal)
    
    # Visualize clusters
    visualizer = Visualizer(arr[1])
    await visualizer.visualize_clusters()
    
    # Save the results
    await Utils.save_to_csv(arr[1], "../data/output.csv")

    #Save the model
    await Utils.save_model(arr[0],"../model/model.joblib")

# Run the main function
asyncio.run(main())
