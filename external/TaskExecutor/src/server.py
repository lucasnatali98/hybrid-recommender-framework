#!/usr/bin/env python

# WS server example

import asyncio

import websockets


async def hello(websocket):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    asyncio.get_event_loop().close()
