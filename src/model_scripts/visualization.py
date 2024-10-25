# modules/visualization.py

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

class Visualizer:
    def __init__(self, X_train):
        self.X_train = X_train

    async def visualize_clusters(self):
        """Reduce dimensions and plot clusters asynchronously."""
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X_train.drop(columns=['Cluster'], inplace=False))

        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=self.X_train['Cluster'], cmap='viridis')
        plt.title('K-Means Clustering of Users')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.colorbar(label='Cluster')
        plt.show()
