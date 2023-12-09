import matplotlib.pyplot as plt
from sklearn.datasets import make_circles 
import numpy as np

import sys
sys.path.append('DenStream')
from DenStream import DenStream

# Generate circular data
X, _ = make_circles(n_samples=1500, noise=0.05, random_state=42, factor=0.5)

# Introduce noisy data (outliers)
outlier = np.array([[1.5, 2.0]])  # Define your outlier coordinates here
X = np.concatenate([X, outlier])

# Initialize DenStream
denstream = DenStream(lambd=0.1, eps=0.2, beta=0.5, mu=3)

# Prepare the plot
plt.figure(figsize=(8, 6))

batch_size = 5
batch_points = []

# Stream data and calculate clusters in batches
for i, point in enumerate(X):
    batch_points.append(point)
    
    # If the batch is complete or it's the last point
    if len(batch_points) == batch_size or i == len(X) - 1:
        # Partially fit the DenStream model with the accumulated batch
        tmpPs = np.array(batch_points)
        # print(tmpPs,tmpPs.shape)
        denstream.partial_fit(tmpPs)
        
        # Calculate clusters for the entire batch
        clusters = denstream.fit_predict(tmpPs)
        
        # Plot the points with their respective cluster labels
        for j, batch_point in enumerate(batch_points):
            cluster = clusters[j]
            if cluster == -1:
                plt.scatter(batch_point[0], batch_point[1], color='black', marker='x')
            else:
                plt.scatter(batch_point[0], batch_point[1], color=plt.cm.tab10(cluster))
        
        # Reset batch_points after processing the batch
        batch_points = []

plt.title('DenStream Clustering for Circular Data with Outliers (Batch Update)')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
