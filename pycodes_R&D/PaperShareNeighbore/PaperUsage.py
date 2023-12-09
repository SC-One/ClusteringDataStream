from PaperImpl import DataStreamClustering
import numpy as np

# Creating a meaningful dataset with two clusters and outliers
np.random.seed(42)  # For reproducibility
cluster1 = np.random.normal(loc=0, scale=1, size=(10, 3))  # First cluster around (0, 0, 0)
cluster2 = np.random.normal(loc=4, scale=1, size=(10, 3))  # Second cluster around (4, 4, 4)
outliers = np.random.uniform(low=-10, high=10, size=(3, 3))  # Three outliers

# Combine clusters and outliers into a single dataset
data_stream = np.vstack([cluster1, cluster2, outliers])

# Create an instance of DataStreamClustering
threshold_value = 3  # Adjust as needed
density_coefficient_value = 0.5  # Adjust as needed

clustering_algorithm = DataStreamClustering(threshold_value, density_coefficient_value)

# Simulate a data stream with the generated meaningful data
for data_point in data_stream:
    clustering_algorithm.handle_new_data(data_point)

# Get the resulting clusters
resulting_clusters = clustering_algorithm.cluster_set

# Print the resulting clusters
for i, cluster in enumerate(resulting_clusters):
    print(f"Cluster {i + 1}: {cluster}")
