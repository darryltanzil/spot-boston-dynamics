#!/usr/bin/env python

import asyncio
import websockets
import os
import cv2
import base64
import numpy as np
import time

async def echo(websocket, path):
    hello = await websocket.recv()
    while True:
        await websocket.send("[CAM]")
        # Get image back from client as base64 encoded jpeg, and display it using cv2
        base64_str = await websocket.recv()
        print(base64_str)
        if base64_str == "[ERROR]":
            print("Error receiving frame")
            continue
        img_bytes = base64.b64decode(base64_str)
        img_np = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        # print(img.shape)
        cv2.imshow('Frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
    

start_server = websockets.serve(echo, "0.0.0.0", os.environ.get('PORT') or 8080)

print("WebSockets ai server starting", flush=True)
asyncio.get_event_loop().run_until_complete(start_server)

print("WebSockets ai server running", flush=True)
asyncio.get_event_loop().run_forever()
