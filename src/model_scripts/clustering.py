# modules/clustering.py

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import asyncio
from concurrent.futures import ThreadPoolExecutor

class KMeansClustering:
    def __init__(self, data):
        self.data = data

    def elbow_method(self, k_max=100):
        """Perform KMeans clustering and plot the Elbow curve."""
        sse = []
        k_range = range(1, k_max)

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(self.data)
            sse.append(kmeans.inertia_)

        plt.plot(k_range, sse, "bx-")
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Sum of squared errors (SSE)')
        plt.title('Elbow Method for Optimal k')
        plt.show()

    async def silhouette_analysis(self, k_max=100):
        """Run silhouette analysis to find the optimal number of clusters asynchronously."""
        range_n_clusters = range(2, k_max)
        silhouette_avg = []

        # Using a ThreadPoolExecutor for the CPU-bound KMeans task
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            for num_clusters in range_n_clusters:
                kmeans = KMeans(n_clusters=num_clusters)
                await loop.run_in_executor(executor, kmeans.fit, self.data)
                cluster_labels = kmeans.labels_
                silhouette_avg.append(silhouette_score(self.data, cluster_labels))

        plt.plot(range_n_clusters, silhouette_avg, "bx-")
        plt.xlabel("Values of K")
        plt.ylabel("Silhouette score")
        plt.title("Silhouette Analysis for Optimal k")
        plt.show()

    async def kmeans_clustering(self, X_train, k_optimal):
        """Perform KMeans clustering asynchronously with threading."""
        kmeans = KMeans(n_clusters=k_optimal, random_state=42)
        
        # Using a thread to run KMeans fitting as it can be CPU-bound
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            X_train['Cluster'] = await loop.run_in_executor(executor, kmeans.fit_predict, X_train)

        print("Cluster Assignment Preview:")
        print(X_train['Cluster'].head())

        return [kmeans,X_train]
