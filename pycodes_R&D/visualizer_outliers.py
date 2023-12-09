import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to visualize clusters and outliers
def visualize_clusters_outliers(data, outliers):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c='blue', label='Clusters')
    ax.scatter(np.array(outliers)[:, 0], np.array(outliers)[:, 1], np.array(outliers)[:, 2], c='red', marker='x', label='Detected Outliers')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.title('Detected Outliers with Clusters')
    plt.show()
