import asyncio
import websockets
import json
import numpy as np
from sklearn.datasets import make_circles


import sys
sys.path.append('DenStream')
from DenStream import DenStream


async def handle_client(websocket, path):
    
    X, ____ = make_circles(n_samples=0, noise=0.05, random_state=42, factor=0.5) 
    denstream = DenStream(lambd=0.1, eps=0.35, beta=0.5, mu=5) # change eps please in the class to demonstrate outliers ...
    BATCH_SIZE_TOPROCESS = 10

    accumulated_points = [] 
    accumulated_point_ids = [] 

    while True: 
        message = await websocket.recv()
        
        data = json.loads(message)
        
        
        point_id = data.get("id")
        point = data.get("point")
        accumulated_points.append(point)
        accumulated_point_ids.append(point_id)
        
        structuredPoint = np.array([[point[0], point[1]]])  # Define your outlier coordinates here
        X = np.concatenate([X, structuredPoint])
        
        # If enough points are accumulated, perform clustering and send back cluster labels
        if len(accumulated_points) == BATCH_SIZE_TOPROCESS:
            batch_points = []
            # X, _ = make_circles(n_samples=BATCH_SIZE_TOPROCESS, noise=0.05, random_state=42, factor=0.5) # uncomment to test!
            for i, t_p in enumerate(X):
                batch_points.append(t_p)

            # print(len(batch_points), BATCH_SIZE_TOPROCESS, len(X))
            # Convert accumulated points to numpy array
            tmpPoints = np.array(batch_points)
            
            # print(tmpPoints,tmpPoints.shape)
            # Partially fit the DenStream model with the accumulated batch
            denstream.partial_fit(tmpPoints)
            
            # Calculate clusters for the entire batch
            clusters = denstream.fit_predict(tmpPoints)
            
            responses = []
            # print("clusters size: ", len(clusters) , len(accumulated_points))
            for j, batch_point in enumerate(accumulated_points):
                cluster = int(clusters[j])
                response = {
                    "id": accumulated_point_ids[j],  # Update IDs for each point
                    "point": accumulated_points[j],
                    "cluster": cluster  # Send cluster label
                } 
                # print(json.dumps(response))
                responses.append(response)
            # print(len(response)) 
            # Send the cluster information back to the client for each point
            for resp in responses:
                await websocket.send(json.dumps(resp))
            # print("send invoked: ")

            # Reset accumulated points for the next batch
            accumulated_points = []
            accumulated_point_ids = []
            X, _ = make_circles(n_samples=0, noise=0.05, random_state=42, factor=0.5)

async def start_server():
    server = await websockets.serve(handle_client, "localhost", 57777)
    await server.wait_closed()

async def main():
    await start_server()

asyncio.run(main())
