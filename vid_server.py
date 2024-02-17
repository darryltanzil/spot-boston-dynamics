import asyncio
import websockets
import base64
import cv2
import numpy as np

# Function to decode base64 image data and display it using OpenCV
def display_image(base64_str):
    # Decode base64 string to bytes
    img_bytes = base64.b64decode(base64_str)

    # Convert bytes to numpy array
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)

    # Decode image array using OpenCV
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Display image
    cv2.imshow('Frame', img)
    cv2.waitKey(1)  # Adjust according to your refresh rate

# WebSocket server handler
async def server(websocket, path):
    while True:
        try:
            # Receive base64-encoded JPEG image
            base64_str = await websocket.recv()

            # Display the image
            display_image(base64_str)

        except websockets.exceptions.ConnectionClosedError:
            print("Client disconnected")
            break

# Start the WebSocket server
start_server = websockets.serve(server, "localhost", 8765)

print("WebSockets video server starting", flush=True)
asyncio.get_event_loop().run_until_complete(start_server)

print("WebSockets video server running", flush=True)
asyncio.get_event_loop().run_forever()
