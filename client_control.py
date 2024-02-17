#!/usr/bin/env python

import asyncio
import websockets
import os

async def echo(websocket, path):
    async for message in websocket:
        print (message, flush=True)
        await websocket.send(input("CMD: "))

start_server = websockets.serve(echo, "0.0.0.0", os.environ.get('PORT') or 8080)

print("WebSockets echo server starting", flush=True)
asyncio.get_event_loop().run_until_complete(start_server)

print("WebSockets echo server running", flush=True)
asyncio.get_event_loop().run_forever()
