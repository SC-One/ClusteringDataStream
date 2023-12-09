import numpy as np
from collections import defaultdict, deque
from scipy.spatial.distance import cdist

class DataStreamClustering:
    def __init__(self, threshold, density_coefficient):
        self.threshold = threshold
        self.density_coefficient = density_coefficient
        self.data_collection = []  # Store the data collection
        self.cluster_set = []  # Store the clusters
        self.adj_table_1 = defaultdict(list)  # Adjacency Table 1
        self.adj_table_2 = defaultdict(int)  # Adjacency Table 2

    def initialize(self):
        # Step 1: Initialize the data collection (if needed)
        pass

    def calculate_nearest_neighbor_distance(self, data_object):
        # Step 3: Calculate the average distance of the nearest neighbor of the data object
        distances = cdist([data_object], self.data_collection).flatten()
        nearest_neighbor_distance = np.mean(np.sort(distances)[1:6])  # Considering 5 nearest neighbors
        return nearest_neighbor_distance

    def calculate_density_factor(self):
        # Step 4: Set the density factor (for example, median distance)
        distances = cdist(self.data_collection, self.data_collection)
        np.fill_diagonal(distances, np.inf)
        self.density_factor = np.median(np.min(distances, axis=1))

    def calculate_average_distance_within_cluster(self, cluster):
        # Step 5: Calculate the average distance within the cluster
        cluster_distances = cdist(cluster, cluster)
        np.fill_diagonal(cluster_distances, np.inf)
        avg_distance_cluster = np.mean(np.min(cluster_distances, axis=1))
        return avg_distance_cluster

    def initialize_outliers_array(self):
        # Step 6: Initialize the array of outliers
        self.outliers = []

    def traverse_using_tree_structure(self, data_object):
        # Step 7: Traversal using tree structure
        distances = cdist([data_object], self.data_collection).flatten()
        nearest_neighbors_indices = np.argsort(distances)[:6]  # Considering 5 nearest neighbors
        self.adj_table_1[tuple(data_object)] = [tuple(self.data_collection[i]) for i in nearest_neighbors_indices]
        self.adj_table_2[tuple(data_object)] = len(nearest_neighbors_indices) - 1

    def breadth_first_search(self, data_object):
        # Step 9: Use breadth-first search to traverse connected branches
        visited = set()
        queue = deque([tuple(data_object)])
        while queue:
            current = queue.popleft()
            visited.add(current)
            for neighbor in self.adj_table_1[current]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)  # Ensure the neighbor is marked as visited

    def calculate_shared_nearest_neighbor_density(self):
        # Step 8: Traverse the adjacent table 2, calculate the shared nearest neighbor density
        for data_point, nn_count in self.adj_table_2.items():
            shared_density = 0
            for neighbor in self.adj_table_1[data_point]:
                if self.adj_table_2[tuple(neighbor)] >= 2:  # Considering neighbors with at least 2 nearest neighbors
                    shared_density += 1
            self.adj_table_2[data_point] = shared_density

    def add_to_cluster(self, data_object):
        # Step 10: Add data object to cluster if conditions are met
        if self.adj_table_2[tuple(data_object)] > self.threshold:
            self.cluster_set.append(data_object)

    def handle_new_data(self, new_data):
        # Step 11: Handle new incoming data
        self.data_collection.append(new_data)
        self.calculate_shared_nearest_neighbor_density()
        self.traverse_using_tree_structure(new_data)
        self.breadth_first_search(new_data)
        self.add_to_cluster(new_data)

    # just a method to test:
    def run(self):
        # Main loop to simulate data stream
        while True:
            new_data = np.random.rand(3)  # Replace this with actual new data
            self.handle_new_data(new_data)
            # Perform other operations or break loop based on your requirements
