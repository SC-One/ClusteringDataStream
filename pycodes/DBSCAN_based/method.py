from sklearn.cluster import DBSCAN
import numpy as np

class OutlierDetectionDBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.clusterer = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        self.outliers = []

    def handle_new_data(self, new_data):
        labels = self.clusterer.fit_predict(np.array([new_data]))
        if labels[0] == -1:  # DBSCAN assigns outliers as -1
            self.outliers.append(new_data)

    def get_detected_outliers(self):
        return self.outliers
