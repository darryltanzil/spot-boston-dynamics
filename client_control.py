#!/usr/bin/env python

import asyncio
import websockets
import os

async def echo(websocket, path):
    msg_buffer = []
    async for message in websocket:
        print(message, flush=True)
        if msg_buffer:
            cmd = msg_buffer.pop(0)
        else:
            cmd = input("CMD: ")
        if cmd == "r":
            with open("exec.py", "r") as f:
                msg_buffer += f.readlines()
                cmd = msg_buffer.pop(0)
        if cmd == "p":
            with open("payload.py", "r") as f:
                payload = f.read()
                await websocket.send("[PAYLOAD]")
                await websocket.send(payload)
                while True:
                    output = await websocket.recv()
                    if output == "[EOL]":
                        break
                    print(output, flush=True)
                await websocket.send("\"DONE\"")
                continue
        # print("SEND:", cmd.strip())
        await websocket.send(cmd)

start_server = websockets.serve(echo, "0.0.0.0", os.environ.get('PORT') or 8080, ping_timeout=None)

print("WebSockets echo server starting", flush=True)
asyncio.get_event_loop().run_until_complete(start_server)

print("WebSockets echo server running", flush=True)
asyncio.get_event_loop().run_forever()
