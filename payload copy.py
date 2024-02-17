import asyncio
import websockets
import cv2
import base64
import time

# Function to read frames from video device, encode as base64, and send over WebSocket
async def send_frames():
    # Open the video capture device (0 for default camera)
    cap = cv2.VideoCapture(0)

    # Create WebSocket connection
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            # Read frame from video device
            ret, frame = cap.read()
            if not ret:
                break

            # Encode frame as JPEG and then as base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)

            # Send base64-encoded frame over WebSocket
            await websocket.send(jpg_as_text)
            
            time.sleep(1)

    # Release the video capture device
    cap.release()

# Main function to run the event loop
async def main():
    await send_frames()

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
