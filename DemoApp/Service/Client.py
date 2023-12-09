import asyncio
import websockets
import json
import matplotlib.pyplot as plt
import random
import time

async def send_points(websocket):
    idNumber = 1  # 0 reserved by Heydar
    while True:
        # Generating random points in a rectangle area (change as needed)
        point = {
            "id": idNumber,
            "point": [random.uniform(5, 7), random.uniform(5, 7)]
        }
        idNumber += 1
        msg = json.dumps(point)
        # print("before sending message:", msg)
        # Sending the random point to the server
        await websocket.send(msg)
        # print("await send invoked")
        await asyncio.sleep(0.2)  # Sleep for 0.2 seconds before sending the next point (200ms)

async def receive_results(websocket):
    while True:
        # Receiving cluster information from the server
        response = await websocket.recv()
        # print("await recv invoked")
        data = json.loads(response)
        # print("clusterLabels data: ", data)
        
        # Plotting points with their clusters
        cluster = data["cluster"]
        x, y = data["point"]
        
        if (-1 == cluster):
            plt.scatter(x, y, color='black', marker='x' , s=250, linewidths=6)
        else:
            plt.scatter(x, y, color='C' + str(cluster % 10))
        plt.pause(0.01)  # Update the plot

        # Redraw the plot to reflect the changes
        plt.draw()

        # Add a slight delay between points for visualization purposes
        await asyncio.sleep(0.1)


async def main():
    uri = "ws://localhost:57777"  # Change this to your server URI
    async with websockets.connect(uri) as websocket:
        sender_task = asyncio.create_task(send_points(websocket))
        receiver_task = asyncio.create_task(receive_results(websocket))
        await asyncio.gather(sender_task, receiver_task)

if __name__ == "__main__":
    plt.title('DenStream Clustering for Circular Data with Outliers (Batch Update)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ion()  # Turn on interactive mode for plotting
    plt.show()
    asyncio.run(main())
