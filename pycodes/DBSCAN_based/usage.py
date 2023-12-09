from method import OutlierDetectionDBSCAN
import numpy as np
from sklearn.datasets import make_blobs

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys
import os
parent_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent_dir)
from visualizer_outliers import visualize_clusters_outliers


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

##################### secion 1
# Generating data with two clusters and some outliers
data, _ = make_blobs(n_samples=20, centers=[[0, 0, 0], [4, 4, 4]], cluster_std=1, random_state=42)
outliers = np.random.uniform(low=-10, high=10, size=(10, 3))  # Ten outliers spread across the space

# Combining clusters and outliers into a single dataset
data_stream = np.vstack([data, outliers])


##################### secion 2 
# Example usage:
outlier_detector = OutlierDetectionDBSCAN(eps=50, min_samples=3)

# Simulate a data stream using the generated data
for data_point in data_stream:
    outlier_detector.handle_new_data(data_point)

# Get the detected outliers
detected_outliers = outlier_detector.get_detected_outliers()

# Print the detected outliers
print("Detected outliers:")
for i, outlier in enumerate(detected_outliers):
    print(f"Outlier {i + 1}: {outlier}")




















# Use the visualize_clusters_outliers function with your data and detected outliers
visualize_clusters_outliers(data, detected_outliers)
