import threading
import time
import numpy as np
from sklearn.cluster import DBSCAN

# Global variables for data stream and control
data_stream = np.empty((0, 2))  # Initialize empty data stream
incoming_rate = 0.001  # Rate of incoming data (1ms)
max_data_points = 999999  # Maximum number of data points

data_counter = 0  # Counter to track the number of data points generated

# Function to continuously generate data
def generate_data():
    global data_stream, data_counter
    while True:
        # Generate new data (replace this with your data generation process)
        new_data = np.random.rand(10, 2)
        data_stream = np.concatenate((data_stream, new_data), axis=0)
        data_counter += 10  # Increment counter based on generated data size
        time.sleep(incoming_rate)

# Function for outlier detection using DBSCAN
def detect_outliers():
    global data_stream
    while True:
        if data_counter >= max_data_points and data_stream.shape[0] == 0:
            break  # Exit the loop if all data processed and no more data in stream

        if data_stream.shape[0] > 0:  # Perform outlier detection if data is available
            # Perform DBSCAN outlier detection on the current data stream
            dbscan = DBSCAN(eps=0.17, min_samples=5)  # Set parameters accordingly
            outliers = np.where(dbscan.fit_predict(data_stream) == -1)[0]

            print("Outlier indices:", outliers)
            print("Outlier data points:", data_stream[outliers])

        time.sleep(1)  # Adjust this delay as needed for outlier detection frequency

# Create and start threads for data generation and outlier detection
data_thread = threading.Thread(target=generate_data)
outlier_thread = threading.Thread(target=detect_outliers)

data_thread.start()
outlier_thread.start()

# Wait for both threads to complete
data_thread.join()
outlier_thread.join()

# When both threads finish, print a message and exit
print("Data processing complete. Exiting program.")
