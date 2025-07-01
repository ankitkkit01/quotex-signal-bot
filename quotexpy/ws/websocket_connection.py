
import asyncio
import websockets

class WebSocketClient:
    def __init__(self, url):
        self.url = url

    async def connect(self):
        async with websockets.connect(self.url) as ws:
            await self.listen(ws)

    async def listen(self, ws):
        async for message in ws:
            print("Received:", message)
