import threading
import time
import numpy as np
from sklearn.ensemble import IsolationForest

# Global variables for data stream and control
data_stream = np.empty((0, 2))  # Initialize empty data stream
incoming_rate = 0.100  # Rate of incoming data generation (1ms)
detection_rate = 1.0  # Rate of outlier detection (16ms)
max_data_points = 20  # Maximum number of data points

data_counter = 0  # Counter to track the number of data points generated

# Function to continuously generate data (higher rate)
def generate_data():
    global data_stream, data_counter
    while data_counter < max_data_points:
        # Generate new data (replace this with your data generation process)
        new_data = np.random.rand(10, 2)
        data_stream = np.concatenate((data_stream, new_data), axis=0)
        data_counter += 10  # Increment counter based on generated data size
        time.sleep(incoming_rate)

# Function for outlier detection at a lower rate
def detect_outliers():
    global data_stream
    while True:
        if data_counter >= max_data_points and data_stream.shape[0] == 0:
            print("jhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            break  # Exit the loop if all data processed and no more data in stream

        if data_stream.shape[0] > 0:  # Perform outlier detection if data is available
            # Perform outlier detection using Isolation Forest
            isolation_forest = IsolationForest(n_estimators=100, contamination=0.05)  # Adjust parameters
            outlier_prediction = isolation_forest.fit_predict(data_stream)

            outliers = np.where(outlier_prediction == -1)[0]

            print("Outlier indices:", outliers)
            print("Outlier data points:", data_stream[outliers])
            print("size of outliers: ",len(outliers))
            print("size of data_stream: ",len(data_stream))
            print("---------------------------")
            print("data_counter: ",data_counter)
            print("data_stream.shape: ",data_stream.shape)

            # Clear processed data after outlier detection
            data_stream = np.delete(data_stream, outliers, axis=0)

        time.sleep(detection_rate)  # Adjust this delay for outlier detection frequency

# Create and start threads for data generation and outlier detection
data_thread = threading.Thread(target=generate_data)
outlier_thread = threading.Thread(target=detect_outliers)

data_thread.start()
outlier_thread.start()

# Wait for the data generation thread to complete
data_thread.join()

# Wait for the outlier detection thread to complete
outlier_thread.join()

# When both threads finish, print a message and exit
print("Data processing complete. Exiting program.")
