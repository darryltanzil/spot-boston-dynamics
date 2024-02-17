#!/usr/bin/env python

import asyncio
import websockets
import os
import cv2
import base64
import numpy as np
import time

async def echo(websocket, path):
    async def move_right():
        print("Moving Right")

    # Function to move left
    async def move_left():
        print("Moving Left")

    # Function to move up
    async def move_up():
        print("Moving Up")

    # Function to move down
    async def move_down():
        print("Moving Down")

    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Function to detect face position and call corresponding movement functions
    async def detect_face_and_move(frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Get the center of the frame
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        
        for (x, y, w, h) in faces:
            # Calculate the center of the detected face
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            
            # Check the position of the face relative to the center of the frame
            if face_center_x < center_x - 75: # Face too far left
                await move_left()
            elif face_center_x > center_x + 75: # Face too far right
                await move_right()
            elif face_center_y < center_y - 75: # Face too far up
                await move_up()
            elif face_center_y > center_y + 75: # Face too far down
                await move_down()
            else:
                print("OK")

    hello = await websocket.recv()
    while True:
        await websocket.send("[CAM]")
        # Get image back from client as base64 encoded jpeg, and display it using cv2
        base64_str = await websocket.recv()
        # print(base64_str)
        if base64_str == "[ERROR]":
            print("Error receiving frame")
            continue
        img_bytes = base64.b64decode(base64_str)
        img_np = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        # print(img.shape)
        await detect_face_and_move(img)
        cv2.imshow('Frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
    

start_server = websockets.serve(echo, "0.0.0.0", os.environ.get('PORT') or 8080)

print("WebSockets ai server starting", flush=True)
asyncio.get_event_loop().run_until_complete(start_server)

print("WebSockets ai server running", flush=True)
asyncio.get_event_loop().run_forever()
